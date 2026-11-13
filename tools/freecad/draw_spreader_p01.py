"""Generate the P01 prototype drawing with ReportLab 4.4.9."""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / 'output/pdf/Thermal spreader plate - P01.pdf'
W, H = landscape(A3)
c = canvas.Canvas(str(PDF), pagesize=(W, H))
c.setTitle('Thermal spreader plate - P01')
INK = colors.HexColor('#162433')
BLUE = colors.HexColor('#164e76')
MASK = colors.HexColor('#d5e9f4')
LIGHT = colors.HexColor('#eef2f4')


def text(x, y, value, size=10, bold=False, colour=INK):
    c.setFillColor(colour)
    c.setFont('Helvetica-Bold' if bold else 'Helvetica', size)
    c.drawString(x, y, value)


def paragraph(x, y, value, width=330):
    for line in simpleSplit(value, 'Helvetica', 10, width):
        text(x, y, line)
        y -= 14
    return y - 6


def view(x0, y0, rear=False):
    scale = 2.42

    def x(v):
        return x0 + scale * (152-v if rear else v)

    def y(v):
        return y0 + scale*v

    def rect(x1, y1, x2, y2, radius=0, fill=colors.white):
        c.setStrokeColor(INK)
        c.setFillColor(fill)
        c.roundRect(min(x(x1), x(x2)), y(y1), scale*(x2-x1),
                    scale*(y2-y1), scale*radius, stroke=1, fill=1)

    def circle(cx, cy, radius, fill=colors.white):
        c.setStrokeColor(INK)
        c.setFillColor(fill)
        c.circle(x(cx), y(cy), scale*radius, stroke=1, fill=1)

    def label(cx, cy, value, dx=7, dy=4):
        text(x(cx)+dx, y(cy)+dy, value, 9, True, BLUE)

    c.setLineWidth(0.8)
    rect(0, 0, 152, 137, 6.35)
    if rear:
        rect(29, 16.5, 123, 120.5, 2, LIGHT)
        circle(19, 45.5, 10, MASK)
        label(19,45.5,'A',-16,19)
        rect(72.715,80.515,77.715,89.515,1,MASK)
        label(75.215,85.015,'B',9,0)
        for cx,cy in ((75,72.5),(75,97.5)):
            circle(cx,cy,3,MASK)
            circle(cx,cy,1.025)
            label(cx,cy,'T3 / D')
    else:
        for cx in (11.1,80.1):
            rect(cx,10,cx+60.96,126.84,0,MASK)
            label(cx+30,115,'C',-3)
        for cy in (72.5,97.5):
            circle(75,cy,1.025)
    for cx in (14,69,83,138):
        for cy in (22.5,68.5,114):
            circle(cx,cy,1.25)
            if not rear:
                label(cx,cy,'T1',5,3)
    for cx in (36,116):
        for cy in (23.5,113.5):
            if rear:
                circle(cx,cy,4)
            circle(cx,cy,1.25)
            if rear:
                label(cx,cy,'T2',12,0)
    for cx in (7,145):
        for cy in (7,130):
            circle(cx,cy,2.5 if rear else 4.25)
    circle(19,45.5,2.5 if rear else 4.25)
    if not rear:
        label(19,45.5,'PE',12)
    c.setStrokeColor(BLUE)
    c.line(x(0),y(0)-12,x(0)+(-22 if rear else 22),y(0)-12)
    text(x(0)+(-44 if rear else 25),y(0)-15,'+X',8,True,BLUE)
    text(x(0)-3,y(0)-29,'X0 / Y0',8,True,BLUE)


text(36,H-49,'THERMAL SPREADER PLATE',24,True)
text(38,H-70,'P01  /  PROTOTYPE MACHINING DRAWING  /  13 NOVEMBER 2026',10,True,BLUE)
text(38,H-91,'6061-T6 aluminium  |  152 x 137 x 8 overall  |  R6.35 plan corners  |  All dimensions in mm',12)
text(W-282,H-52,'STEP  Thermal spreader plate - P01.step',11,True)
text(W-282,H-72,'1 sheet  /  A3  /  Views not to scale',10)

text(40,715,'FRONT  /  HEATSINK FACE',12,True,BLUE)
text(439,715,'REAR  /  PCB FACE',12,True,BLUE)
view(40,363)
view(439,363,rear=True)

text(839,715,'FINISH AND FUNCTIONAL SURFACES',12,True,BLUE)
y=691
for note in (
    'Matt black anodise outside the marked zones. Cosmetic finish on exposed surfaces. Confirm selective finish before machining.',
    'A  Rear PE contact. Bare, unblasted Ø20 circle centred on the PE bore at (19, 45.5). This boundary is a finish mask.',
    'B  Rear IC thermal land. Keep the entire 5 x 9, R1 top face bare, flat and unblasted. Land centre (75.215, 85.015). Protect the face from tool and rack marks.',
    'C  Front heatsink seats. Keep both marked rectangles bare and unblasted, including plate-side heatsink bond areas. Lower-left corners (11.1, 10) and (80.1, 10). Each is 60.96 x 116.84. Confirm masking edge visibility.',
    'D  Rear inner seat tops. Keep both Ø6 faces bare and unblasted for shims and provision for the amplifier bond.',
    'Keep rack marks off contact faces and exposed cosmetic areas. Threads must accept the specified screws after finishing.',
    'If selective anodising is unavailable, quote an as-machined alternative for approval.',
):
    y=paragraph(839,y,note,310)

c.setStrokeColor(BLUE)
c.line(38,319,W-38,319)
text(38,300,'HOLE SCHEDULE  /  COORDINATES FROM FRONT VIEW DATUM',12,True,BLUE)
text(38,281,'X increases right and Y up in the front view. The rear view is mirrored.',9)
y=259
for callout, detail in (
    ('T1   12 x M3 x 0.5 THRU', 'Tap from front, Ø2.50 pilots. X = 14, 69, 83, 138 at each Y = 22.5, 68.5, 114.'),
    ('T2   4 x M3 x 0.5 THRU', 'Tap from rear, Ø2.50 pilots. X = 36, 116 at each Y = 23.5, 113.5.'),
    ('T3   2 x M2.5 x 0.45 THRU', 'Tap from rear, Ø2.05 pilots. X = 75 at Y = 72.5, 97.5.'),
    ('Plate fixings   4 x Ø5 THRU', 'X = 7, 145 at each Y = 7, 130. Front countersink Ø8.5 x 90°.'),
    ('PE post   1 x Ø5 THRU', 'X = 19, Y = 45.5. Front countersink Ø8.5 x 90°. Fit M4 head flush or below.'),
):
    text(38,y,callout,10,True)
    text(229,y,detail,9)
    y-=27
text(38,111,'Thread callouts apply only to T1, T2 and T3. Plate fixings and PE are plain clearance holes.',9,True)
text(38,92,'STEP carries tap-drill diameters. Deburr without reducing the functional seating areas.',9)

text(718,300,'PROTOTYPE HEIGHTS  /  FROM PCB POCKET FLOOR',12,True,BLUE)
y=276
for label,value in (
    ('Corner support tops','4.00 mm'),
    ('IC land top','2.75 mm'),
    ('Two IC-adjacent seat tops','2.75 mm'),
    ('Metal web under pocket','4.00 mm'),
):
    text(718,y,label,10)
    text(977,y,value,10,True)
    y-=21
y=paragraph(718,y-4,'Machine the prototype at the shown heights. Shims are installed by the customer. Keep all contact surfaces as machined after finish.',405)
y=paragraph(718,y,'Report achievable tolerances on the IC land and the corner seat plane. Apply finished dimensions. Follow the STEP for other geometry.',405)

c.setStrokeColor(BLUE)
c.line(38,53,W-38,53)
text(38,33,'P01  |  Prototype for PCB fit and thermal contact assessment',10,True)
text(W-175,33,'DRAWING 1 / 1',10,True)
c.save()
