r"""Create a review-only 8 mm spreader study inside FreeCAD 1.1.4.

Run using runpy.run_path on this file from the FreeCAD GUI Python console.
All dimensions are mm. See doc/MECHANICAL.md for datum, thread callouts,
unresolved clamping/fastener interfaces, and limits of this study.
"""
from pathlib import Path
import math
import FreeCAD as App
import FreeCADGui as Gui
import Part

ROOT = Path(__file__).resolve().parents[2]
MODEL = ROOT / '3d_models' / 'Thermal spreader plate.FCStd'
SINK = [(x, y) for x in (14, 69, 83, 138) for y in (22.5, 68.5, 114)]
FIX = [(7,7),(145,7),(7,130),(145,130)]
CORNER = [(36,23.5),(116,23.5),(36,113.5),(116,113.5)]
IC_SCREWS = [(75,72.5),(75,97.5)]
PE_POST = (19.0, 45.5)
THREAD_CALLOUTS = '12 x M3 x 0.5 (sink face), 4 x M3 x 0.5 and 2 x M2.5 x 0.45 (PCB face); through, nominal tap drills'

def rounded_rect(x0,y0,x1,y1,r,z,height):
    p = App.Vector
    s = Part.makeBox(x1-x0-2*r, y1-y0, height, p(x0+r,y0,z))
    s = s.fuse(Part.makeBox(x1-x0, y1-y0-2*r, height, p(x0,y0+r,z)))
    for x in (x0+r,x1-r):
        for y in (y0+r,y1-r):
            s = s.fuse(Part.makeCylinder(r,height,p(x,y,z)))
    return s.removeSplitter()

def cylinder(x,y,r,z,height):
    return Part.makeCylinder(r,height,App.Vector(x,y,z))

def earth_post_cut(shape):
    """Copy the cabinet DAE's through bore and front-face countersink."""
    x, y = PE_POST
    bore = cylinder(x, y, 2.5, -2, 8)
    countersink = Part.makeCone(2.5, 4.25, 1.75, App.Vector(x, y, 4.25))
    return shape.cut(bore.fuse(countersink)).removeSplitter()

def pcb_tap_drill_cut(shape):
    for x,y in CORNER:
        shape=shape.cut(cylinder(x,y,1.25,-2,8))
    for x,y in IC_SCREWS:
        shape=shape.cut(cylinder(x,y,1.025,-2,8))
    return shape.removeSplitter()

def stage(doc,name,label,shape,colour):
    shape=shape.removeSplitter()
    if shape.isNull() or not shape.isValid() or len(shape.Solids)!=1:
        raise RuntimeError(f'{name}: expected one valid solid')
    obj=doc.addObject('PartDesign::Feature',name)
    obj.Label=label
    obj.Shape=shape
    obj.ViewObject.ShapeColor=colour
    return obj

def main():
    if MODEL.exists():
        raise FileExistsError(f'Reconstruction would overwrite {MODEL}')
    name='ThermalSpreaderStudy'
    if name in App.listDocuments():
        raise RuntimeError('Close the existing ThermalSpreaderStudy document first')
    d=App.newDocument(name)
    d.Label='Thermal spreader — 8 mm design study'
    blank=rounded_rect(0,0,152,137,6.35,-2,8)
    for x,y in SINK:
        blank=blank.cut(cylinder(x,y,1.25,-2,8))
    for x,y in FIX:
        blank=blank.cut(cylinder(x,y,2.5,-2,8))
        blank=blank.cut(Part.makeCone(2.5,4.25,1.75,App.Vector(x,y,4.25)))
    a=stage(d,'Blank','8 mm blank, plate fixings and sink tap drills',blank,(0.7,0.7,0.72))

    # The pocket extends 2 mm beyond the PCB outline. Raised islands retain
    # the four corner seats, the two adjustable IC screw seats, and IC land.
    tool=rounded_rect(29,16.5,123,120.5,2,-2,4)
    for x,y in CORNER:
        tool=tool.cut(cylinder(x,y,4,-2,4))
    for x,y in IC_SCREWS:
        tool=tool.cut(cylinder(x,y,3,-2,4))
    land=rounded_rect(72.715,80.515,77.715,89.515,1,-2,4)
    tool=tool.cut(land)
    recessed=blank.cut(tool)
    b=stage(d,'Clearance','4 mm deep PCB clearance field',recessed,(0.72,0.72,0.74))
    # Land and IC screw seats sit 1.25 mm below the corner seats. Final
    # IC-adjacent supports/shims and clamp must be set from the real board.
    shallow=rounded_rect(72.715,80.515,77.715,89.515,1,-2,1.25)
    for x,y in IC_SCREWS:
        shallow=shallow.fuse(cylinder(x,y,3,-2,1.25))
    recessed=recessed.cut(shallow)
    c=stage(d,'Land','Nominal IC land and adjustable seats',recessed,(0.74,0.74,0.76))
    # These are tap-drill bores, not modelled helical threads.
    recessed=pcb_tap_drill_cut(recessed)
    final=stage(d,'Study','STUDY: tap-drill holes and PE countersink',earth_post_cut(recessed),(0.76,0.76,0.78))
    final.addProperty('App::PropertyString','ThreadCallouts','Design').ThreadCallouts=THREAD_CALLOUTS
    final.addProperty('App::PropertyString','StatusNote','Design').StatusNote='Review only: clamp, sink slot fit and screw stack, grounding, finish and cabinet fit open'
    final.addProperty('App::PropertyString','EarthPostNote','Design').EarthPostNote='M4 post at (19, 45.5) mm: Ø5 through, Ø8.5 x 90° countersink from heatsink face; mask Ø20 on PCB face'
    for o in (a,b,c): o.Visibility=False
    final.Visibility=True
    d.recompute()
    d.saveAs(str(MODEL))
    Gui.activeDocument().activeView().viewBottom()
    Gui.activeDocument().activeView().fitAll()
    print('valid',final.Shape.isValid(),'solids',len(final.Shape.Solids),'volume',final.Shape.Volume)

if __name__ == '__main__':
    main()
