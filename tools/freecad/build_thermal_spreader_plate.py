r"""Build the first CNC solid from Subwoofer cabinet.dae's thermal spreader.

Run inside FreeCAD (GUI Python console or MCP execute_code):
    import runpy
    runpy.run_path(r"C:\Users\swallace\Projects\Subwoofer prototype\tools\freecad\build_thermal_spreader_plate.py")

The local XY plane is the plate outline. Local +Z points towards
the outside of the cabinet: DAE (X, Y, Z) maps to plate (X-127.01308,
Z-153, Y-478) in millimetres. The DAE is the dimensional authority.
"""

from pathlib import Path
from math import sqrt

import FreeCAD as App
import FreeCADGui as Gui
import Import
import Part
import Sketcher


ROOT = Path(__file__).resolve().parents[2] / "tmp" / "thermal-spreader-base-rebuild"
WIDTH = 152.0
HEIGHT = 137.0
THICKNESS = 6.0
CORNER_RADIUS = 6.35
SINK_HOLES = [
    (14.0, 22.5), (14.0, 68.5), (14.0, 114.0),
    (69.0, 22.5), (69.0, 114.0),
    (83.0, 22.5), (83.0, 114.0),
    (138.0, 22.5), (138.0, 68.5), (138.0, 114.0),
]
FIXING_HOLES = [(7.0, 7.0), (145.0, 7.0),
                (7.0, 130.0), (145.0, 130.0)]


def vec(x, y):
    return App.Vector(x, y, 0)


def fixed_sketch(body, name, label, geometry, z=0.0):
    sketch = body.newObject("Sketcher::SketchObject", name)
    sketch.Label = label
    sketch.Placement.Base.z = z
    sketch.addGeometry(geometry, False)
    for index in range(len(geometry)):
        sketch.addConstraint(Sketcher.Constraint("Block", index))
    return sketch


def rounded_outline():
    w, h, r = WIDTH, HEIGHT, CORNER_RADIUS
    q = r / sqrt(2.0)
    return [
        Part.LineSegment(vec(r, 0), vec(w-r, 0)),
        Part.Arc(vec(w-r, 0), vec(w-r+q, r-q), vec(w, r)),
        Part.LineSegment(vec(w, r), vec(w, h-r)),
        Part.Arc(vec(w, h-r), vec(w-r+q, h-r+q), vec(w-r, h)),
        Part.LineSegment(vec(w-r, h), vec(r, h)),
        Part.Arc(vec(r, h), vec(r-q, h-r+q), vec(0, h-r)),
        Part.LineSegment(vec(0, h-r), vec(0, r)),
        Part.Arc(vec(0, r), vec(r-q, r-q), vec(r, 0)),
    ]


def circles(points, radius):
    return [Part.Circle(vec(x, y), App.Vector(0, 0, 1), radius)
            for x, y in points]


def checked(obj, label):
    shape = obj.Shape
    if shape.isNull() or not shape.isValid() or len(shape.Solids) != 1:
        raise RuntimeError(f"{label} did not produce one valid solid: {obj.State}")


def main():
    name = "ThermalSpreaderPlateBase"
    if name in App.listDocuments():
        raise RuntimeError(f"Close the existing {name} document before rebuilding")
    doc = App.newDocument(name)
    doc.Label = "Thermal spreader plate — DAE base geometry"

    body = doc.addObject("PartDesign::Body", "Plate")
    body.Label = "Thermal spreader plate (base only)"
    outline = fixed_sketch(body, "Outline", "152 × 137, R6.35 outline", rounded_outline())
    pad = body.newObject("PartDesign::Pad", "Blank")
    pad.Label = "6 mm blank"
    pad.Profile = outline
    pad.Length = THICKNESS
    doc.recompute()
    checked(pad, "Blank")

    sink_layout = fixed_sketch(
        body, "SinkHoleLayout", "Ten Ø3.5 heatsink holes",
        circles(SINK_HOLES, 1.75), THICKNESS)
    sink_pocket = body.newObject("PartDesign::Pocket", "SinkHoles")
    sink_pocket.Label = "Heatsink through holes Ø3.5"
    sink_pocket.Profile = sink_layout
    sink_pocket.Length = THICKNESS
    doc.recompute()
    checked(sink_pocket, "Heatsink holes")

    fixing_layout = fixed_sketch(
        body, "FixingHoleLayout", "Four plate fixing centres",
        circles(FIXING_HOLES, 2.5), THICKNESS)
    fixing_holes = body.newObject("PartDesign::Hole", "FixingHoles")
    fixing_holes.Label = "Four Ø5 through, Ø8.5 countersunk"
    fixing_holes.Profile = fixing_layout
    fixing_holes.Diameter = 5.0
    fixing_holes.DepthType = "ThroughAll"
    fixing_holes.HoleCutType = "Countersink"
    fixing_holes.HoleCutCustomValues = True
    fixing_holes.HoleCutDiameter = 8.5
    fixing_holes.HoleCutCountersinkAngle = 90.0
    doc.recompute()
    checked(fixing_holes, "Plate fixing holes")

    for obj in (outline, pad, sink_layout, sink_pocket, fixing_layout):
        obj.Visibility = False
    fixing_holes.Visibility = True
    body.Tip = fixing_holes
    doc.recompute()

    bb = body.Shape.BoundBox
    dims = (bb.XLength, bb.YLength, bb.ZLength)
    if any(abs(a-b) > 1e-5 for a, b in zip(dims, (WIDTH, HEIGHT, THICKNESS))):
        raise RuntimeError(f"Unexpected final bounds: {dims}")
    checked(body, "Final plate")

    fcstd = ROOT / "Thermal spreader plate - base.FCStd"
    step = ROOT / "Thermal spreader plate - base.step"
    ROOT.mkdir(parents=True, exist_ok=True)
    doc.saveAs(str(fcstd))
    Import.export([body], str(step))
    Gui.activeDocument().activeView().viewAxonometric()
    Gui.activeDocument().activeView().fitAll()
    print(f"FCStd: {fcstd}")
    print(f"STEP: {step}")
    print(f"Bounds: {dims}; volume: {body.Shape.Volume:.6f} mm^3")


main()
