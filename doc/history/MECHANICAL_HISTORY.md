# Mechanical design history

> **Lifecycle: HISTORY.** Superseded early plate and rear-control proposals. Current geometry, assembly checks and fabrication status are in [mechanical design](../MECHANICAL.md). These records are not machining instructions.

## 1 Earlier spreader geometry and proposed stack

**Historical base geometry, 11 November 2026:** the first model recorded the DAE's 152 × 137 × 6 mm blank with R6.35 mm plan
corners. In plate-local coordinates, viewed from the heatsink/front face, the
lower-left outline corner is (0, 0) mm. Ten Ø3.5 mm through holes for the
heatsinks are centred at (14, 22.5), (14, 68.5), (14, 114), (69, 22.5),
(69, 114), (83, 22.5), (83, 114), (138, 22.5), (138, 68.5), and
(138, 114) mm. Four plate fixing holes are centred at (7, 7), (145, 7),
(7, 130), and (145, 130) mm; each is Ø5 mm through with an Ø8.5 mm,
1.75 mm deep, nominal 90° countersink on the front face. Local +Z runs from
the PCB/rear face to the heatsink/front face; DAE (X, Y, Z) maps approximately to
local (X − 127.013, Z − 153, Y − 478) mm. The slight world-X fraction comes
from the SketchUp transform, not a machining dimension.

The [base generator](../../tools/freecad/build_thermal_spreader_plate.py)
rebuilds that historical geometry in FreeCAD 1.1.4. Run
`runpy.run_path(path)` in the FreeCAD GUI Python console, where `path`
is the generator's absolute path. Its retained constants and sketch
definitions generate a native model and STEP in
`tmp/thermal-spreader-base-rebuild/`. The expected result is a single
valid 152 × 137 × 6 mm solid of 123569.154 mm³.

**Proposed rear-face arrangement, 11 November 2026:** the user intends the
PCB centred on the plate, with four corner supports and the two holes beside
the TPA3251 used for its thermal contact. The heatsink-side face is the front;
the opposite face is the rear. The user permits tapped through holes provided
the installed screws do not project through the front. This is a preliminary
layout proposal, not approved machining geometry.

The PCB STEP used for the preliminary fit study had a 90 × 100 mm
board, four Ø3 mm corner holes and two Ø2.5 mm IC-adjacent holes. Its modelled
IC thermal face projects 1.25 mm from the rear PCB surface; four 1206 bodies
project about 1.915 mm. Modelled through pins are longer, but the user plans
to trim them to at most 2 mm beyond the rear PCB surface. These are CAD
dimensions and a trimming assumption, not as-built measurements. Centred
orientations screened put PCB fixing centres at least approximately 17.6 mm
from existing heatsink-hole centres; select the final orientation only after
checking pockets, tooling, hardware and electrical isolation.
The [14 November PCB STEP](../../diptrace/main_board.step) includes the enlarged
Ø3.40 and Ø2.90 mm mounting holes. The centres match the saved PCB and
the P01 seats. For cabinet placement, see the
[amplifier assembly DAE](../3d_models/README.md#4-amplifier-pcb-assembly).

A candidate is approximately 4 mm from the PCB rear surface to local pocket
floors. With the nominal 1.25 mm IC projection and its land at the original
plate surface, that implies about 2.75 mm pocket depth and 3.25 mm remaining
web in 6 mm stock; the nominal clearance above trimmed 2 mm pins is then
2 mm. Limit the pocket footprint to the component and pin fields while
retaining the IC land, support pads and continuous heat paths. Verify actual
component, solder, pin, tool-radius and tolerance envelopes before machining.
PCB supports at the IC land height would need to stand approximately 1.25 mm
above the original plate face: separate supports or additional stock can
provide this; a boss of that height cannot be cut out of the existing flat
6 mm blank without lowering the land. Keep analogue-domain mounting isolation
as specified in §2 and the grounding authority.

Equal rigid support heights alone do not establish controlled IC contact
pressure. Resolve the contact stack from actual package projection, PCB and
support dimensions and a thin TIM film; assess a compliant, limited-load
clamping arrangement at the two IC-adjacent holes without imposing excessive
PCB or solder-joint bending. Fix screw size, engagement and length after the
hardware stack and thread depths are selected. The Ø3 and Ø2.5 mm board holes
do not themselves establish clearance for nominal M3 and M2.5 screws.


## 2 Earlier plywood control recess and component mounting

### 3.2 Superseded 8 November plywood control recess

The following assessment records why the earlier shared thin-plywood land
was replaced; its relief dimensions are not current machining instructions.

The 8 November DAE relieves one continuous X = 34–107 mm, Z = 62–181 mm
region from the inside by 8 mm, leaving a **4 mm outer plywood skin** for
the IEC inlet, two potentiometers, polarity switch and RCA sockets. This
73 × 119 mm thin land is interrupted by their cut-outs and sits only about
5 mm from the spreader rebate at X ≈ 112 mm. For scale, a free 4 mm skin
has `(4/12)^3 = 1/27` the bending stiffness of the full 12 mm sheet in
the same span; surrounding wood helps but does not make repeated plug and
switch loads harmless. This is a material mechanical concern before cutting.
Prefer separate local reliefs matched to each part's required clamping
thickness, retaining full-depth wood between them, or design a supported
subpanel. Recheck the inlet cover, mains/signal separation, PE scheme,
washer support and fixings on the actual assembly; the DAE does not show
the cable bends or guards. The modelled IEC and nearest RCA envelopes are
only about 12 mm apart laterally over a shared height range, so the
unmodelled inlet cover and wiring route matter here. The selected
NYS367 RCA sockets allow at most 3 mm effective panel thickness, so this
4 mm land still needs at least 1 mm further local relief at each RCA before
any finish or washer stack. Preserve support between the individual controls.

The [Hub PDB18 models](../../../Hub/3d_models/electronics/PDB18-family/README.md) and
[DD11 inlet model](../../../Hub/3d_models/electronics/DD11.0111.1111/README.md) support layout in SketchUp.
Their panel guides are references, not cutting instructions. Each selected
PDB18 potentiometer has only 6.5 mm of exposed M7 bushing, so the full 12 mm
ply cannot sit under its washer and nut. Design a local recess or thin control
land, then check actual nut engagement, anti-rotation feature, knob reach and
remaining plywood strength. Same Sky `SAK-007` (Mouser `179-SAK-007`) was
checked on 1 November 2026 and is not a direct-fit knob for either selected
PDB18: its [D-shaped 6 × 4.5 mm socket and 9.6 mm depth](https://jp.sameskydevices.com/product/resource/knobs-compatibility-guide.pdf)
are specified for a D shaft, while the selected `K420K` shafts have 18-tooth
knurls. The [Bourns drawing](https://www.bourns.com/docs/product-datasheets/pdb18.pdf)
gives a 20 mm shaft projection from the pot's seating face; even a 3 mm
finished mounting land would leave about 17 mm outside the panel. With a
9.6 mm-deep socket fully seated on the shaft, the knob base would stand about
7.4 mm off that panel. Select a knob for the 6 mm, 18-tooth spline and check
its socket depth against the final panel, washer and nut stack.

Mouser-listed shaft-profile candidates checked on 2 November 2026 are
[Davies Molding `1106WA`](https://www.mouser.co.uk/en/ProductDetail/Davies-Molding/1106WA?qs=sGAEpiMZZMt59L%252B180nu3T6TRtZ1rFBWDLLs7PLd1bgcYNFjF0fNCw%3D%3D)
(18.5 mm diameter, 18 mm high, black with white pointer),
[Eagle Plastic Devices `450-AE185`](https://www.mouser.co.uk/en/ProductDetail/Eagle-Plastic-Devices/450-AE185?qs=sGAEpiMZZMt59L%252B180nu3QVMcO3xhYHCvPKHdInvapI%3D)
(19 mm diameter, 18 mm high, grey with black line), and
[`450-AE141`](https://www.mouser.co.uk/en/ProductDetail/Eagle-Plastic-Devices/450-AE141?qs=OEmOpuBgIMzKdJe6iTJ5jg%3D%3D)
(14 mm diameter, 17 mm high, black with black line). Davies specifies a
6 mm, 18-tooth moulded spline for `1106WA`; Eagle's [T18 definition](https://www.mouser.com/catalog/catalogusd/646/2041.pdf)
is likewise a 6 mm, 18-tooth shaft. Their published overall heights do not
establish usable bore depths. With about 17 mm of shaft above a proposed 3 mm
land, none is yet a verified direct fit. Trial-fit a sample on the actual
potentiometer and final panel/nut stack before fixing knob height or trimming
a shaft. Mouser stock and prices are transient and need rechecking at purchase.

The Schurter DD11 screw-mounted inlet permits at
most **8 mm panel thickness**. Its location therefore needs an effective ply
thickness no greater than 8 mm, requiring at least 4 mm local relief in the
12 mm wall before any veneer or finish in the clamped stack; check the
purchased inlet, rear cover, screw fixing and
remaining wood web before machining. Keep the inlet rear cover and mains loom
clear of signal controls and the plate's thermal/PE fixtures.

The selected
[E-Switch polarity switch](../FRONT_END.md#62-selected-e-switch-gold-contact-switch-31-october-2026)
has an 8.89 mm threaded bushing, so its nut and washer need a locally relieved
land in the 12 mm plywood. Check actual hardware engagement, lever access,
anti-rotation keyway, remaining wood and rear solder-lug clearance. The switch
mounting cut-out is not yet locked.

The selected [REAN NYS367 RCA sockets](../FRONT_END.md#21-selected-rca-panel-sockets-31-october-2026)
also need a relieved land: their published maximum effective panel thickness
is 3 mm, implying at least 9 mm rear-side relief in 12 mm plywood before
finish or washer effects. Check whether the resulting wood web and the
15.5 mm mounting-washer footprint will support repeated plug insertion and
removal; use a suitably supported thin insulating insert if that is more
robust. Confirm the purchased washers, nut engagement and rear solder/wire
clearance before cutting. Keep every conductive socket part clear of the
aluminium plate and its fixings, as specified in
[power and grounding](../POWER_AND_GROUNDING.md#8-rca-inputs). The exact socket
cut-out is not yet locked. The [rear signal-part layout models](../3d_models/Rear-signal-parts.md)
show the component envelopes but do not define the pocket machining.

The acoustic partition, rather than this outer rear wall, now contains the
driver pressure. The rear structure must still carry the electronics safely,
retain the plate, preserve cabinet stiffness, and provide the bottom-panel
inlet, upper-rear-panel outlet, and service access without exposing live parts.

## 3 Early CNC quote-tool experiment

The intended fabrication route is now a custom CNC-machined plate. An
illustrative `300 × 200 × 5 mm` FreeCAD solid with representative holes and a
recess was accepted by JLCCNC's quote tool on 2026-10-07; the user reported an
approximate US$20 quote for that test article. This establishes that a native
solid STEP export can pass the upload/quote stage. It is not a quote for the
project plate or evidence that the final material, features, thermal path,
PCB clearance, or machining details are resolved. The experimental generator
and outputs were local to an ignored `tmp/` directory; they are not a retained
reconstruction route. The P01 fabrication package is independent of this
exploratory quote probe.


## 4 Earlier volume calculations

The earlier 2.585 L figure was obtained by directly summing signed
triangle volumes from the prior DAE. Some SketchUp surfaces had
inconsistent winding, making that method unreliable. The current
1.259 L result comes from reorienting each closed brace mesh consistently
before integrating its enclosed volume; all six meshes had paired edges
and no orientation conflicts in that check.

The previous driver-displacement estimate of about 0.8 ± 0.2 L came from
the manufacturer's section drawing, not a displaced-volume measurement.
The roughly 130 mm diameter motor has an approximately 0.66 L cylindrical
envelope at an inferred 50 mm length, before subtracting its vent and
reliefs. The open basket adds less solid volume than its outside shape
suggests. The user reasonably suspects that 1.0 L may be low; keep it as
a provisional calculation input, not an upper bound. The visual 3D driver
model is not a solid-displacement model. Count only driver solids extending
into the sealed chamber, relative to the inner baffle plane.


## 5 Earlier component clearance screen

The previous version's 106 nominal rear-component and IC-lead bounding boxes
showed no solid overlap after limiting pin projection to 2 mm. The revised
sink bores and recessed screw tips stay outside that component clearance
envelope. This is a nominal interference
screen, not a tolerance, solder, fastener or physical-assembly check.
1050A-H14 was the
earlier flat-plate choice; its higher thermal conductivity does not resolve the
PCB-side placement problem by itself. Verify the received part, panel stiffness and passive-cooling performance
during prototype assembly and validation.

