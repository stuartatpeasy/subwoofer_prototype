"""Build the SketchUp amplifier assembly from the STEP, DipTrace XML and Gerbers."""

import math
from collections import defaultdict
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile

import MeshPart
import Part
from PySide import QtCore, QtGui


RED = (0.62, 0.055, 0.085, 1)
FACE_ART = {"Top_Silk": "TopSilk.gbr", "Bottom_Silk": "BottomSilk.gbr"}
BOUNDS = ("XMin", "YMin", "ZMin", "XMax", "YMax", "ZMax")
BOARD_DEFLECTION = 0.01
COMPONENT_DEFLECTION = 0.06
ENVELOPE_LIMIT = 0.06


def xy(point):
    return QtCore.QPointF(*point)


def render_legend(gerber, output, width, height):
    """Render the metric, dark-only Gerber commands in the rev0 legend layers."""
    pixels_per_mm = 20
    image = QtGui.QImage(round(width * pixels_per_mm), round(height * pixels_per_mm),
                         QtGui.QImage.Format.Format_RGB32)
    red = QtGui.QColor.fromRgbF(*RED)
    image.fill(red)
    painter = QtGui.QPainter(image)
    white = QtGui.QColor(250, 250, 248)
    painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
    painter.translate(0, image.height())
    painter.scale(pixels_per_mm, -pixels_per_mm)
    apertures = {}
    point = (0, 0)
    region = None
    aperture = None
    mode = "01"
    assert "%FSLAX35Y35*%" in gerber and "%MOMM*%" in gerber
    try:
        for command in re.sub(r"[%\s]", "", gerber).split("*"):
            if not command or command.startswith("G04") or command in {
                "MOMM", "FSLAX35Y35", "LPD", "G71", "G90", "G75", "M02"
            }:
                continue
            definition = re.fullmatch(r"ADD(\d+)C,([\d.]+)", command)
            if definition:
                apertures[int(definition[1])] = float(definition[2])
                continue
            if command in ("G36", "G37"):
                if command == "G36":
                    region = QtGui.QPainterPath()
                else:
                    region.closeSubpath()
                    painter.fillPath(region, white)
                    region = None
                continue
            if command[:3] in ("G01", "G02", "G03"):
                mode, command = command[1:3], command[3:]
                if not command:
                    continue
            match = re.fullmatch(r"(?:X(-?\d+))?(?:Y(-?\d+))?(?:I(-?\d+))?(?:J(-?\d+))?D(\d+)", command)
            if not match:
                raise ValueError(f"Unsupported legend command: {command}")
            x, y, i, j, op = match.groups()
            op = int(op)
            if op >= 10:
                aperture = apertures[op]
                continue

            # The fabrication outline's lower-left is (10, 10) mm.
            end = tuple(int(coord) / 100000 - 10 if coord is not None else prior
                        for coord, prior in zip((x, y), point))
            if op == 2:
                if region is not None:
                    region.moveTo(xy(end))
            elif op == 3:
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.setBrush(white)
                painter.drawEllipse(xy(end), aperture / 2, aperture / 2)
            elif op == 1:
                points = [end]
                if mode != "01":
                    dx, dy = (int(offset or 0) / 100000 for offset in (i, j))
                    cx, cy = point[0] + dx, point[1] + dy
                    start = math.atan2(-dy, -dx)
                    finish = math.atan2(end[1] - cy, end[0] - cx)
                    direction = 1 if mode == "03" else -1
                    sweep = direction * ((direction * (finish - start)) % math.tau)
                    steps = max(1, math.ceil(abs(sweep) * 12))
                    radius = math.hypot(dx, dy)
                    points = [(cx + radius * math.cos(start + sweep * k / steps),
                               cy + radius * math.sin(start + sweep * k / steps))
                              for k in range(1, steps)] + [end]
                if region is not None:
                    for vertex in points:
                        region.lineTo(xy(vertex))
                else:
                    pen = QtGui.QPen(white)
                    pen.setWidthF(aperture)
                    pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
                    pen.setJoinStyle(QtCore.Qt.PenJoinStyle.RoundJoin)
                    painter.setPen(pen)
                    painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
                    painter.drawPolyline(QtGui.QPolygonF([xy(v) for v in [point, *points]]))
            else:
                raise ValueError(f"Unsupported operation D{op}")
            point = end
    finally:
        painter.end()
    if not image.save(str(output)):
        raise OSError(f"Could not save {output}")


def bounds_match(a, b, tolerance):
    return max(abs(getattr(a, name) - getattr(b, name)) for name in BOUNDS) <= tolerance


def tessellate(shape, on_board, *, refine=False):
    return MeshPart.meshFromShape(
        Shape=shape.copy(),
        LinearDeflection=BOARD_DEFLECTION if on_board or refine else COMPONENT_DEFLECTION,
        AngularDeflection=0.22 if on_board or refine else 0.72,
        Relative=False,
    )


def simplify(shape, original, bounds):
    if original.CountFacets < 40:
        return original
    candidate = original.copy()
    candidate.decimate(0.025, 0.78)
    if not bounds_match(candidate.BoundBox, bounds, ENVELOPE_LIMIT):
        return original
    if shape.ShapeType == "Solid" and not candidate.isSolid():
        return original
    return candidate


def add_geometry(mesh, tessellation, materials, group, board_z=None):
    positions, faces = tessellation.Topology
    indices = [mesh.vertex((p.x, p.y, p.z)) for p in positions]
    for a, b, c in faces:
        material = materials
        if board_z is not None:
            z = [positions[index].z for index in (a, b, c)]
            if max(abs(level) for level in z) < 1e-6:
                material = "Top_Silk"
            elif max(abs(level - board_z) for level in z) < 1e-6:
                material = "Bottom_Silk"
        mesh.face(indices[a], indices[b], indices[c], material, f"{group}-{material}")


def attach_textures(path, width, height):
    uri = "http://www.collada.org/2005/11/COLLADASchema"
    q = lambda name: f"{{{uri}}}{name}"
    tree = ET.parse(path)
    root = tree.getroot()
    images = ET.Element(q("library_images"))
    root.insert(1, images)
    mesh = root.find(f".//{q('mesh')}")
    positions = mesh.find(f"{q('source')}[@id='position_source']/{q('float_array')}")
    xyz = list(map(float, positions.text.split()))
    uv = [(xyz[i] / width, xyz[i+1] / height) for i in range(0, len(xyz), 3)]
    # Only board triangles reference the UVs, using the same indices as positions.
    source = ET.Element(q("source"), id="board_uv")
    mesh.insert(2, source)
    data = ET.SubElement(source, q("float_array"), id="board_uv_array", count=str(2*len(uv)))
    data.text = " ".join(f"{u:.7g} {v:.7g}" for u, v in uv)
    common = ET.SubElement(source, q("technique_common"))
    accessor = ET.SubElement(common, q("accessor"), source="#board_uv_array",
                             count=str(len(uv)), stride="2")
    for name in ("S", "T"):
        ET.SubElement(accessor, q("param"), name=name, type="float")

    for material in FACE_ART:
        image_id = material + "_image"
        image = ET.SubElement(images, q("image"), id=image_id)
        ET.SubElement(image, q("init_from")).text = f"main_board_textures/{material}.png"
        profile = root.find(f".//{q('effect')}[@id='{material}_effect']/{q('profile_COMMON')}")
        surface = ET.Element(q("newparam"), sid="board_surface")
        ET.SubElement(ET.SubElement(surface, q("surface"), type="2D"), q("init_from")).text = image_id
        sampler = ET.Element(q("newparam"), sid="board_sampler")
        ET.SubElement(ET.SubElement(sampler, q("sampler2D")), q("source")).text = "board_surface"
        profile.insert(0, surface)
        profile.insert(1, sampler)
        diffuse = profile.find(f".//{q('diffuse')}")
        diffuse.remove(diffuse.find(q("color")))
        ET.SubElement(diffuse, q("texture"), texture="board_sampler", texcoord="UVSET0")
        symbol = material + "_symbol"
        triangles = mesh.find(f"{q('triangles')}[@material='{symbol}']")
        triangles.insert(1, ET.Element(q("input"), semantic="TEXCOORD", offset="1",
                                       source="#board_uv", set="0"))
        indices = triangles.find(q("p"))
        indices.text = " ".join(f"{index} {index}" for index in indices.text.split())
        binding = root.find(f".//{q('instance_material')}[@symbol='{symbol}']")
        ET.SubElement(binding, q("bind_vertex_input"), semantic="UVSET0",
                      input_semantic="TEXCOORD", input_set="0")
    ET.indent(tree, space="  ")
    tree.write(path, xml_declaration=True, encoding="utf-8")


def separate_opposing_normals(mesh):
    """Use flat normals where a STEP part has coincident opposed faces."""
    from model_mesh import add, length, triangle_normal

    sums = defaultdict(lambda: (0, 0, 0))
    for face, group in zip(mesh.faces, mesh.groups):
        normal = triangle_normal(*(mesh.vertices[i] for i in face))
        for i in face:
            sums[i, group] = add(sums[i, group], normal)
    opposed = {group for (_, group), normal in sums.items() if length(normal) < 1e-12}
    for index, group in enumerate(mesh.groups):
        if group in opposed:
            mesh.groups[index] = f"flat-{index}"


def build(project):
    sys.path.insert(0, str(project.parent / "Hub/tools/3d_models"))
    from collada_export import write_dae
    from model_mesh import Mesh

    source = project / "diptrace"
    output = project / "3d_models"
    assembly = Part.read(str(source / "main_board.step"))
    parts = assembly.childShapes()
    board = max(assembly.Solids, key=lambda solid: solid.Volume)
    design = ET.parse(source / "main_board.dipxml").getroot()
    outline = design.findall("Board/BoardOutline/Points/Point")
    dims = board.BoundBox
    assert design.attrib["Units"] == "mm"
    assert {(float(p.get("X")), float(p.get("Y"))) for p in outline} == {
        (0, 0), (dims.XLength, 0), (0, dims.YLength), (dims.XLength, dims.YLength)
    }
    diameters = {p.get("PatternStyle"): float(p.find("Holes/Hole").get("HoleDiam"))
                 for p in design.findall("Library/Library/Patterns/Pattern")
                 if p.find("Holes/Hole") is not None}
    expected = sorted((float(p.get("X")), float(p.get("Y")), diameters[p.get("PatternStyle")])
                      for p in design.findall("Board/Components/Component[@Type='MtHole']"))
    top = max(board.Faces, key=lambda face: face.CenterOfMass.z)
    holes = [w.Edges[0].Curve for w in top.Wires if len(w.Edges) == 1]
    assert sorted((round(c.Center.x, 5), round(c.Center.y, 5), round(2*c.Radius, 5))
                  for c in holes) == expected

    mesh = Mesh()
    bare = tessellate(board, True)
    assert bare.isSolid()
    add_geometry(mesh, bare, "Red_solder_mask", "board", dims.ZMin)
    before = bare.CountFacets
    bound_checks = []
    for index, part in enumerate(parts):
        if part.isSame(board):
            continue
        for item, shape in enumerate(part.childShapes() if part.ShapeType == "Compound" else [part]):
            bounds = shape.optimalBoundingBox(False, False)
            original = tessellate(shape, False)
            if not bounds_match(original.BoundBox, bounds, ENVELOPE_LIMIT):
                original = tessellate(shape, False, refine=True)
            lighter = simplify(shape, original, bounds)
            before += original.CountFacets
            if not bounds_match(lighter.BoundBox, bounds, ENVELOPE_LIMIT):
                raise ValueError(f"Component {index}/{item} exceeds the envelope tolerance")
            bound_checks.append(True)
            # Small elements read as pins and contacts. Package surfaces are charcoal.
            colour = "Metal" if sorted((bounds.XLength, bounds.YLength, bounds.ZLength))[1] < 1 else "Package"
            add_geometry(mesh, lighter, colour, f"part-{index}-{item}")

    palette = {"Red_solder_mask": RED, "Top_Silk": RED, "Bottom_Silk": RED,
               "Package": (0.16, 0.17, 0.18, 1), "Metal": (0.62, 0.64, 0.67, 1)}
    materials = {name: {"diffuse": rgba, "specular": (0.1, 0.1, 0.1, 1), "shininess": 8}
                 for name, rgba in palette.items()}
    textures = output / "main_board_textures"
    textures.mkdir(exist_ok=True)
    with ZipFile(source / "main_board_gerber.zip") as fabrication:
        profile = fabrication.read("BoardOutline.gbr").decode()
        assert "X1000000Y1000000D2*" in profile
        assert f"X{round((dims.XLength + 10)*100000)}D1*" in profile
        assert f"Y{round((dims.YLength + 10)*100000)}D1*" in profile
        for material, file in FACE_ART.items():
            render_legend(fabrication.read(file).decode(), textures / f"{material}.png",
                          dims.XLength, dims.YLength)
    dae = output / "main_board.dae"
    separate_opposing_normals(mesh)
    stats = write_dae(mesh, dae, materials, "Subwoofer amplifier PCB")
    attach_textures(dae, dims.XLength, dims.YLength)
    archive = output / "main_board_sketchup.zip"
    with ZipFile(archive, "w", ZIP_DEFLATED) as bundle:
        for file in [dae, *(textures / f"{name}.png" for name in FACE_ART)]:
            bundle.write(file, file.relative_to(output))
    print(stats, "before simplification", before, "envelopes within limit",
          f"{sum(bound_checks)}/{len(bound_checks)}", "assembly bounds", assembly.BoundBox)


if __name__ == "__main__":
    build(Path(__file__).resolve().parents[2])
