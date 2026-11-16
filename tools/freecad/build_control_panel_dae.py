"""Convert the DipTrace control panel STEP and Top Silk XML to a layout DAE.

Run as a macro in FreeCAD, or execute this file in its Python console.
"""

import os
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

import FreeCAD as App
from FreeCAD import Vector
import MeshPart
import Part


BOARD = "Black FR-4"
SILK = "White silkscreen"
SILK_Z = 0.05  # Small visual separation from the STEP surface at Z=0.
MATERIALS = {
    BOARD: {"diffuse": (0.027, 0.027, 0.027, 1), "specular": (0.06, 0.06, 0.06, 1),
            "shininess": 8},
    SILK: {"diffuse": (0.98, 0.98, 0.98, 1), "specular": (0, 0, 0, 1),
           "shininess": 1},
}


def text_faces(item, anchor):
    """Use Arial outlines fitted to the saved DipTrace text block."""
    if (item.get("Angle"), item.get("Inverted"), item.get("FontVector")) != ("0", "N", "N"):
        raise ValueError("Expected upright, unmirrored TrueType lettering")

    lines = item.findall("TextLines/TextLine")
    block_width = float(item.attrib["TextWidth"])
    block_height = float(item.attrib["TextHeight"])
    # DipTrace's logical line box includes leading. Arial's visible capitals
    # occupy roughly 60% of this box, with room beneath for descenders.
    line_box = float(item.attrib["FontSizeFloat"]) * 0.433333
    advance = (block_height - line_box) / (len(lines) - 1) if len(lines) > 1 else 0
    x = anchor.x - block_width * {"Left": 0, "Center": 0.5, "Right": 1}[item.attrib["HorzAlign"]]
    y = anchor.y + block_height * {"Top": 0, "Center": 0.5, "Bottom": 1}[item.attrib["VertAlign"]]
    font_dir = (Path(os.environ["WINDIR"]) / "Fonts").as_posix() + "/"
    rows = [
        [Part.makeFace(wires, "Part::FaceMakerBullseye")
         for wires in Part.makeWireString(line.text, font_dir, "arial.ttf", line_box * 0.63)
         if wires]
        for line in lines
    ]
    bounds = [Part.makeCompound(row).BoundBox for row in rows]
    scale_x = block_width / max(bound.XLength for bound in bounds)
    transform = App.Matrix()
    transform.A11 = scale_x
    for row_number, (row, bound) in enumerate(zip(rows, bounds)):
        align = {"Left": 0, "Center": 0.5, "Right": 1}[item.attrib["TextAlign"]]
        offset_x = x + align * (block_width - bound.XLength * scale_x) - bound.XMin * scale_x
        baseline = y - line_box * 0.79 - row_number * advance
        transform.A14, transform.A24 = offset_x, baseline
        for glyph in row:
            yield from glyph.transformGeometry(transform).Faces


def stroke_face(item, points):
    """Make a constant-width planar stroke with round ends."""
    radius = float(item.attrib["LineWidth"]) / 2
    if item.attrib["Type"] == "Line":
        start, end = points
        offset = (end - start).cross(Vector(0, 0, 1))
        offset.normalize()
        offset *= radius
        body = Part.Face(Part.makePolygon(
            [start + offset, end + offset, end - offset, start - offset, start + offset]
        ))
    else:
        start, middle, end = points
        arc = Part.Arc(start, middle, end).toShape()
        centre = arc.Curve.Center
        arc_radius = (start - centre).Length

        def offset(point, distance):
            return centre + (point - centre) * (1 + distance / arc_radius)

        outside = [offset(point, radius) for point in points]
        inside = [offset(point, -radius) for point in reversed(points)]
        body = Part.Face(Part.Wire([
            Part.Arc(*outside).toShape(), Part.makeLine(outside[-1], inside[0]),
            Part.Arc(*inside).toShape(), Part.makeLine(inside[-1], outside[0]),
        ]))

    caps = [Part.Face(Part.Wire([Part.makeCircle(radius, p)])) for p in (start, end)]
    return body.fuse(caps).removeSplitter()


def add_mesh(mesh, shape, material, group, z_offset=0):
    tessellation = MeshPart.meshFromShape(
        Shape=shape, LinearDeflection=0.02, AngularDeflection=0.28, Relative=False
    )
    vertices, triangles = tessellation.Topology
    indices = [mesh.vertex((p.x, p.y, p.z + z_offset)) for p in vertices]
    for a, b, c in triangles:
        if material == SILK and (vertices[b] - vertices[a]).cross(vertices[c] - vertices[a]).z < 0:
            b, c = c, b
        mesh.face(indices[a], indices[b], indices[c], material, group)


def build(project):
    sys.path.insert(0, str(project.parent / "Hub/tools/3d_models"))
    from collada_export import read_toolkit_dae, write_dae
    from model_mesh import Mesh, mesh_stats

    plate = Part.read(str(project / "3d_models/control_panel.step"))
    board = ET.parse(project / "diptrace/control_panel.dipxml").getroot()
    if board.get("Units") != "mm" or not plate.isValid() or len(plate.Solids) != 1:
        raise ValueError("Expected a valid one-solid STEP and DipTrace XML in millimetres")
    top = max(plate.Faces, key=lambda face: face.CenterOfMass.z)
    if abs(top.BoundBox.ZMin) > 1e-7 or top.normalAt(0, 0).z < 0.999:
        raise ValueError("Expected outward STEP face at Z=0")

    mesh = Mesh()
    add_mesh(mesh, plate, BOARD, BOARD)
    for item in board.findall("Board/Shapes/Shape[@Layer='Top Silk']"):
        points = [Vector(float(p.attrib["X"]), float(p.attrib["Y"]), 0)
                  for p in item.findall("Points/Point")]
        kind = item.attrib["Type"]
        if kind == "Text":
            faces = list(text_faces(item, points[0]))
        elif kind in ("Arc", "Line"):
            faces = stroke_face(item, points).Faces
        else:
            raise ValueError(f"Unsupported silkscreen shape {kind}")
        if not faces:
            raise ValueError(f"No geometry for silkscreen shape {item.attrib['Id']}")
        for face in faces:
            # Clip as DipTrace fabrication artwork would be clipped at cut-outs.
            for clipped in face.common(top).Faces:
                add_mesh(mesh, clipped, SILK, f"silk-{item.attrib['Id']}", SILK_Z)

    output = project / "3d_models/control_panel.dae"
    write_dae(mesh, output, MATERIALS, "Subwoofer control panel")
    reopened, colours, _ = read_toolkit_dae(output)
    print(output, mesh_stats(reopened), colours)


if __name__ == "__main__":
    build(Path(__file__).resolve().parents[2])
