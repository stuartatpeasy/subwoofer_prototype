# Mechanical design

> **State — current mechanical authority; reviewed 2026-11-17.** Owns cabinet,
> rear-plate and PCB/plate fit; electrical bonds are owned by
> [power and grounding](POWER_AND_GROUNDING.md), and heat-load acceptance by
> [thermal design](THERMAL.md). Read for plate or PCB packaging changes.
> Current direction: 12 mm plywood rear panel, separate FR-4 controls and
> the P01 nominal 8 mm CNC-relieved plate. The user reports that the rev0
> board and P01 plate are in fabrication and that design clearances are
> adequate for prototyping. Next gate: check the received parts' actual
> contact stack, fastener fit, clearances, electrical isolation and PE
> bonds; assess cooling in prototype validation. The model is not a physical
> fit or temperature measurement. The cabinet, control-panel support,
> guards, harness and loaded carpet and wall clearance remain open.

## 1 Two-chamber cabinet architecture

The [SketchUp enclosure model](../3d_models/Subwoofer%20cabinet.dae) provides
the layout basis. The locked
**bare structural** outer envelope is
300 × 470 × 320 mm (width × front-to-rear depth × height), confirmed by
the current DAE. The user retained the extra 10 mm at the rear for the
electronics compartment; the partition and acoustic chamber retain their
previous dimensions. For the coordinates in this section, use the structural
cabinet's front-left-bottom corner as the local origin. The current DAE's
world coordinates are offset from it by X = 14 mm, Y = 14 mm and Z = 100 mm.
Later veneer, edge protection, or other decorative trim may increase the finished outer
dimensions without breaching that decision. The model is not a final cutting
drawing: joint details, tolerances, actual PCB and plate contacts, some
fasteners, and finished trim remain open. The model includes candidate braces, two bottom
vent/PSU-mount panels, two upper vent inserts, a separate FR-4 control panel,
and a smaller spreader with two external sinks. Both vent fields are reviewed
in §1.3; their finished guards, fixings and thermal performance remain open.

The driver fires downwards from a recessed opening in the laminated bottom
baffle. It is 36 mm over the sealed acoustic chamber but locally only 18 mm
in the rear electronics floor. The present model uses 18 mm plywood for
the other panels and inclined partition, with **12 mm rear plywood**.
The partition spans the internal width
and height, separates the sealed acoustic chamber from the ventilated
electronics chamber, and must be continuously bonded and sealed at its
perimeter. Only the protected, airtight driver-cable feed-through passes
between chambers. Wadding stays clear of the cone, suspension, motor vents,
and terminals and is not counted as recovered geometric volume.
The rear wall lies outside the sealed acoustic chamber, so its thickness
does not change the volume calculations in §1.1 or the 20.0 L net target.
The exposed sinks project about 35.6 mm beyond the structural rear face,
giving **505.6 mm** from the structural front before front trim and room-wall
clearance. The ash corner legs and bumpers extend the width to about 328 mm;
the whole model spans about 520 mm front-to-rear including the projecting
sinks, and 440 mm from floor to top of ash. These finished dimensions do not
change the 300 × 470 × 320 mm bare structural decision.

### 1.1 Volume and bracing

For later DAE revisions, the project-owned [inspection declarations](../3d_models/dae-inspect.json)
work with the shared [read-only DAE inspector](../../Hub/tools/3d_models/README.md#read-only-dae-inspection).
From the project root, run
`python ..\Hub\tools\3d_models\dae_inspect.py report "3d_models\Subwoofer cabinet.dae" --config "3d_models\dae-inspect.json"`.
The configuration was updated for the 11 November rear control opening and
the 10 mm higher world-Z placement, then its four vent-part names were
corrected on 13 November to match the current DAE assembly export. It
identifies the three rear-panel
features by unique expected bounds, so their direct geometry indices may
change without breaking the inspection. It also declares one PDB181 level
control and one PDB182 crossover control beneath the rear control assembly.
The 16 November DAE passes this identity check with one of each; the
check establishes names and counts only, not wiring or physical fit.
The configuration declares the trapezoidal acoustic-space dimensions and
the provisional 1.0 L driver allowance; those inputs are not inferred from
the mesh. It also identifies the vent openings and rear-panel features.
Check its expected feature bounds and update the declarations when the
SketchUp geometry changes. The report is a geometry screen, not a physical
volume, airflow or fastener qualification.

In the current model the acoustic chamber is 264 mm wide and 266 mm high.
The partition's acoustic-side face lies at Y = 258 mm at the bottom and
Y = 420.626 mm at the top, measured from the DAE; the inner front wall is at
Y = 18 mm. The clear depth therefore grows linearly from 240 mm at the
bottom to 402.626 mm at the top. Its gross volume is:

```text
Vgross = 264 × 266 × (240 + 402.626) / 2 = 22.564 L
Vnet   = Vgross − effective driver displacement − bracing and other solids
```

The target remains **20.0 L net geometric air volume**. The excess 2.564 L
is provision for solid intrusions. The six closed brace meshes in the
11 November DAE sum to approximately **1.259 L** of solid volume
after correcting inconsistent exported triangle orientations. This is a
geometric sum, subject to any overlapping solids or later joinery changes.
The 10 mm reduction in sealed-chamber depth removes **0.702 L** from the
preceding 23.266 L gross estimate. The model leaves approximately
**21.305 L before driver displacement**.
Using the provisional 1.0 L driver allowance gives approximately
**20.305 L net**. Exactly 20.0 L would require about 1.305 L effective
driver displacement if nothing else occupies the acoustic chamber. At
1.35–1.85 L driver displacement, net would be approximately
19.955–19.455 L. These are planning figures, not an actual-driver
displacement measurement. Reconcile all solids before cutting; do not
add wood solely to force the estimate to exactly 20.0 L.
The new rear perimeter brace is entirely in the electronics chamber and
does not reduce this acoustic estimate. The model's single approximately
12 mm driver-cable hole through the partition is intended to be sealed
during assembly; protect and restrain the cable at the plywood edge, then
check the completed seal for leaks.

The [Speaker prototype damping material](../../Speaker%20prototype/doc/CABINET_DESIGN.md#9-internal-damping-and-stuffing)
is open, air-permeable 4 oz polyester/Dacron upholstery wadding. For this
subwoofer, an **unlined starting state is reasonable**: at the intended
40–100 Hz passband, the approximately 403 mm longest clear chamber depth
puts a simple half-wave cavity mode near `343/(2 × 0.403) ≈ 425 Hz`, well
above the passband. A single securely retained, uncompressed layer on the
upper and side walls is an optional precaution if later access is awkward;
do not blanket the driver-side floor or add loose fill by default. Keep any
material clear of the cone, suspension, basket and motor vents, terminals,
and cable feed-through, and out of the electronics airflow path. The fibre
solid occupies a little physical air space, while sufficient distributed
fibre can soften the acoustic air spring through heat exchange and add
loss. The effect of a thin wall layer here is unmeasured and likely small:
retain the **20.0 L geometric target without a wadding credit**. If tuning
this detail, compare low-level installed impedance under otherwise matched
conditions before and after adding the chosen lining.

The 1.259 L brace volume uses consistently oriented closed meshes. The
1.0 L driver allowance is provisional, not an upper bound; the visual model
is not a displacement measurement. Count only driver solids inside the sealed
chamber relative to the inner baffle plane. [Earlier volume methods and
limitations](history/MECHANICAL_HISTORY.md#4-earlier-volume-calculations)
are retained for provenance.

The revised window and rib network retains the same load paths while
reducing member depth: it ties the side panels at about 160 mm height,
crosses the cabinet at about 160 mm front-to-rear position, stiffens the
front wall and inclined partition, and divides the long top panel with
longitudinal and transverse ribs. The modelled brace contacts reach the
panels they are meant to support; the top longitudinal rib stops short
of the partition but is bonded to the top panel and transverse rib.
The front-to-rear mid-height brace stops short of the partition; a
separate inclined brace supports the partition. With close-fitting, correctly
clamped Titebond II bonds on the stated contact surfaces, the topology
is a plausible and likely adequate brace layout for the present
18 mm panels. This is an engineering screen, not a measured resonance
or joint-strength qualification. The driver mesh shows no obvious brace
intersection, but actual driver, fastener and assembly clearances still
need checking. Place joint cleats on the electronics side where practical
so their volume does not consume the acoustic allowance.

Halving the depth of a free rib makes its own bending second moment
`I = b d³/12` one-eighth as large for bending in that direction. It does
not make the unchanged 18 mm cabinet panels one-eighth as stiff, and a
fully bonded panel and rib act as a deeper composite section. As a
conservative scale check, published ±12 mm linear-coil travel displaces
about 0.252 L of the 20 L air volume. An adiabatic small-change estimate
then gives about 1.8 kPa peak pressure. Treating an 18 mm plywood panel
as a simply supported beam strip across a 270 mm bay, with provisional
`E = 6 GPa`, gives
`δ = 5 p L⁴ / (384 E (t³/12)) ≈ 0.04 mm` static deflection under that
pressure for a unit-width strip.
The actual braced panels have support on more than two edges, but
material variation, joint details and dynamic modes are not captured
by this illustrative calculation. A finished-box tap/listening check
is a proportionate way to catch an unexpected buzz or ringing.

### 1.2 Downward driver and carpeted-floor clearance

The driver recess is intentional. It adds protection and floor clearance
without a material diffraction effect across the intended 40–100 Hz
low-pass range. The model's outer recess is 236 mm in diameter around the
nominal 234.25 mm flange, giving only 0.875 mm radial assembly clearance
before fabrication and finish tolerances. The inner relief leaves about
10 mm of wood between its front/rear edges and the adjacent wall/partition
inner faces. Verify the actual flange, fasteners, wood land, and joint before
cutting. The static mesh places the outermost surround point approximately
2.4 mm inside the cabinet's bottom plane. It has no moving-surface envelope;
the published 24 mm peak-to-peak *linear coil travel* is not a mechanical
stop or a motion specification for every surround point. Set any grille
clearance from the actual driver and intended drive level.

**Current driver mounting, 16 November 2026:** the DAE places eight
M4 × 20 mm pan-head machine screws on the 219 mm pitch circle, with eight
M4 × 10 mm non-flanged Type E timber inserts in the baffle. This supersedes
the 8 November 4 × 25 mm wood-screw proposal. The modelled screws and inserts
are coaxial. In world coordinates their inserts occupy Z = 120–130 mm and
the screw tips reach Z = 131 mm; the chamber-side baffle face is Z = 136 mm.
Thus the model has approximately 10 mm axial insert overlap and 5 mm between
the screw tips and chamber-side face. These are nominal envelopes, not a
thread-engagement or drilling-depth guarantee. The insert opening faces the
driver side, so the downward driver load is carried through the insert's
external thread into the plywood. The eight fixings share roughly 49 N of
static gravity load, about 6 N each if evenly loaded; dynamic loads, uneven
preload and plywood strength are not established by that arithmetic.

The modelled pan head is 8.0 mm diameter; the driver record gives a nominal
7.9 mm head recess and 4.3 mm through hole. The head may therefore catch on
the recess edge instead of bearing flat; tolerances and the actual recess shape
matter. Trial the received driver and selected screw, ensuring the head bears
fully without damaging the cast frame. If it does not, select a compatible
head while retaining the M4 insert arrangement; recheck length from its
actual bearing plane. Do not assume that the older countersunk screw fits.
Trial the selected insert and its supplier-specified pilot in laminated plywood,
checking edge breakout, square installation, full screw engagement without
bottoming, and the remaining blind-hole depth. Locate holes from the actual
driver and seal any accidental breakthrough. The physical fasteners, gasket,
installation strength and airtightness remain unverified.

Let `h` be the **loaded** vertical gap from the cabinet's outer bottom
surface to the top of the nearby carpet pile, measured with the completed
cabinet on its four legs. Air leaving the 236 mm opening passes through
an approximate cylindrical throat of area `A = π × 236 mm × h`. Equating
this to the opening area `π × (236 mm)² / 4` gives `h = 59 mm`. Thus
approximately **60 mm loaded clearance** is a useful lower geometric
reference: the under-cabinet radial throat is then no smaller than the
recess mouth. It is not a measured acoustic threshold. Aim provisionally
for **70–90 mm loaded clearance** on carpet, leaving margin for pile,
leg settlement, unevenness, and a possible grille. If `L` is the leg
projection and `δ` is the height by which the surrounding pile rises
above each loaded foot's bearing level, then `h = L − δ`. For illustration,
the 11 November ash legs put the plywood baffle bottom **100 mm** above a hard
floor, so its loaded carpet clearance is `100 − δ` mm. The lower ash edge
bumpers extend 10 mm below the baffle and leave **90 − δ mm** at the
perimeter. Thus 10 mm of pile rise above the loaded feet gives 90 mm under
the baffle and 80 mm at the trim; 20 mm gives 80 and 70 mm respectively.
The 59 mm throat comparison applies at the 236 mm driver opening; farther
out, the available perimeter grows, so a 60 mm trim-edge gap does not by
itself imply an undersized outlet. Check the completed cabinet on the
intended carpet; lengthen the legs or use firm bearing pads if the measured
gap, level or inlet access is unsatisfactory.

Each of the four modelled ash legs has a roughly 32 × 32 mm foot and wraps
the plywood corner in an 18 × 18 mm notch through the cabinet's 320 mm
height. The plywood corner can bear on the leg's lower shoulder, while the
two long mating faces provide a substantial glued joint if milled accurately,
bonded and clamped as assumed. The ash edge bumpers are likewise assumed
glued. None crosses the driver opening or bottom inlet. Check the actual
joinery fit and avoid resting the full cabinet on loose, compressible pile
at only one or two feet.

As a separate orientation check, gravity on the nominal 59 g moving mass
is approximately 0.58 N. The published 0.59 mm/N compliance gives a
nominal **free-air** offset of `0.58 × 0.59 ≈ 0.34 mm`. The moving-mass
figure includes air loading, so this is not a precise weight measurement.
If a 20.0 L chamber holds a static pressure difference, its isothermal
air stiffness is approximately `P0 × Sd² / V ≈ 2.23 N/mm`, using
atmospheric pressure `P0 ≈ 101 kPa` and effective area `Sd = 0.021 m²`.
Adding the suspension's `1/Cms ≈ 1.69 N/mm` gives about **0.15 mm**
static offset.
At audio frequencies the sealed air spring is stiffer still. Slow pressure
equalisation through minute leakage can remove its *DC* support, so the
long-term offset may approach the free-air estimate while the chamber
remains sealed for bass frequencies. This time-scale distinction is
described in [Klippel's loudspeaker analysis](https://www.klippel.de/fileadmin/klippel/Files/Know_How/Literature/Papers/Maximizing%20Efficiency%20in%20Active%20Loudspeaker%20Systems.pdf).
Conversely, an unusually pressure-tight cabinet can show a static cone
shift as room temperature or barometric pressure changes. A very slow
equalisation path is distinct from an unacceptable audio-band leak; no
special vent or test is called for without an observed offset.

Gravity is a constant force that shifts the equilibrium; it does not by
itself create different incremental inboard and outboard forces in a
linear suspension/box model. The actual driver has position-dependent
suspension stiffness and motor force, so an offset can add some
asymmetry at large excursion. The manufacturer does not supply those
curves, and neither offset estimate is a measured installed result.
The nominal 0.34 mm free-air figure is only about 3% of the published
±12 mm geometric linear-coil travel. No separate sag qualification is
indicated unless assembled testing reveals rubbing or unexpectedly
asymmetric distortion.

### 1.3 Electronics chamber, ventilation, and packaging

The locked passive-flow direction is bottom electronics-chamber inlet,
past the PSU and amplifier, to an upper rear outlet. The current inlet
geometry is accepted as the design basis. The 11 November DAE has two upper
inserts on the outside of one rear-plywood opening; their fixings,
protection and assembled airflow remain unqualified.

The lower inlet comprises two 128 × 145 × 5 mm perforated panels with
their undersides at Z = 18 mm and tops at Z = 23 mm, seated in the
rear-floor recess. Each sits over a 110 × 129 mm aperture through the
outer 18 mm plywood layer. The current panels have 245 and 252 nominal 6 mm
through-holes. Allowing for holes partly masked by the plywood aperture
edges gives approximately **135 cm² combined geometric inlet area** in the
11 November DAE: about 103 cm² below the PSU's projected footprint and
33 cm² outside it. The 18 mm-deep plywood apertures are much larger in area than the
perforations and are not the nominal inlet throat. All areas are from
the DAE, before guards, carpet lint, tolerances, or measured airflow.

Four 15 mm bosses now raise the 215 × 115 × 30 mm PSU bottom to
Z = 38 mm, leaving a **15 mm gap above the inlet-panel tops**.
Their centres match the manufacturer's 150 × 50 mm underside M4
pattern. The 660 mm PSU case perimeter times this gap gives about
**99 cm² nominal lateral turning area**, close to the 103 cm² of
modelled inlet area beneath the PSU. This removes the obvious
under-case area mismatch of the earlier 10 mm gap; it does not prove
flow because bosses, the actual PSU case, nearby walls, wiring and guards
affect the turns. The PSU remains at X = 52–267 mm and Y = 307–422 mm,
with 34/15 mm nominal left/right wall clearance and 26 mm behind it.
Its selected TBC-09 terminal guard, leads and cable bends are not modelled.
The [Mean Well mechanical specification](https://www.meanwell.com/Upload/PDF/RSP-200/RSP-200-spec.pdf)
limits underside M4 screw penetration to 3 mm; finalise the screw stack,
vent-panel material and attachment, support, and protective-earth continuity.
The four modelled M4 × 20 pan screws extend from the vent-panel underside
at world Z = 118 mm to Z = 141 mm, nominally 3 mm into the PSU base
at Z = 138 mm. This consumes the entire stated penetration limit; actual
length, panel thickness, seating and tolerances must keep penetration within
3 mm, using a suitable shorter screw or spacing if necessary.

The upper 18 mm baffle lamination is cleared over X = 18–282 mm,
Y = 293–442 mm, leaving the rear electronics floor locally 18 mm thick.
This removal is behind the sealed pressure chamber: the driver and its
acoustic floor remain in the laminated 36 mm region, and the inclined
partition meets a full-thickness baffle land. The two lower apertures
leave an approximately 24 mm central wood rail, 28 mm outer-side
rails and 28 mm rear margin; the aperture front edge is about 24 mm
behind the partition's rear foot. The vent panels overlap their apertures
by roughly 8–10 mm, but their material, fixings and any contribution
to stiffness are not established. The side, rear and partition joints
retain full-thickness baffle material. This makes a significant acoustic
baffle-stiffness penalty unlikely, despite the local 18 mm thickness.
As a scale check, a simply supported 24 × 18 mm plywood rail spanning
129 mm with a provisional 6 GPa modulus deflects only about 0.005 mm
under the PSU's entire nominal 0.72 kg weight applied at its centre;
the actual load is shared. This is a static screen, not a vent-panel
fastener or vibration qualification. Place the rear legs on solid
full-thickness corners, clear of the apertures.

Keep the inlet above the intended carpet with the loaded leg clearance
in §1.2. Retain the IEC mains-inlet rear cover and PSU terminal guard, and protect
mains parts from direct probing or foreign objects through the 6 mm
lower holes. A retained screen would reduce net free area and must be
considered with the modelled outlet. The modelled PCB, and the still-unresolved thermal-contact
land, mounts, wiring and control harnesses may affect the chamber path.
Preserve solid rear-plate land for the PCB, thermal contact and PE stud;
validate the finished enclosure thermally using
[Thermal design](THERMAL.md).

The 30 October layout's solid 182 × 232 mm plate left too little space for
a useful outlet. The current model has two
123 × 94 × 8 mm inserts spanning local X = 27–273 mm and Z = 199–293 mm on the
**outside** of the 12 mm rear plywood. They project about 3 mm beyond the
rear wood face. A single 232 × 80 mm plywood through-opening
spans X = 34–266 mm and Z = 206–286 mm, leaving nominal 15 mm side and top
rails. Each insert has 176 nominal 6 mm airflow holes. Counting only the
airflow holes exposed through the plywood
gives about **99.5 cm² projected geometric outlet area**; the 3.5 mm
mounting holes are excluded. Each insert overlaps the opening by about 7 mm;
all 352 airflow holes remain exposed. The four modelled 3 × 15 mm screws
now lie 2 mm outward in both directions from the plywood opening's corners.
Their nominal thread engagement is still only about 7 mm, but the screw
shanks no longer break into the aperture: a 3 mm nominal screw has about
`sqrt(2² + 2²) − 1.5 ≈ 1.3 mm` minimum wood to the nearest opening
corner. For this light insert the layout is a reasonable starting point;
use properly sized pilot holes and a trial in an offcut before finalising
the plywood/insert screw joint. The eight lower-vent screws have similarly
close aperture corners and also carry the PSU through the vent mounts, so
check that joint in the same trial.

The partition narrows the electronics-side passage. From its rear face
to the plywood opening's inner face at Y = 458 mm, the depth falls from
about 75 mm
at the opening's lower edge (Z = 206 mm) to about 26 mm at its upper edge
(Z = 286 mm). Air can leave through the lower rows before reaching the
shallow top; the geometric area is plausible but does not prove buoyancy
flow. The deeper 8 mm insert is intended to be stiffer, but its resistance
to pushing and rattling remains to be checked in the finished assembly.
Any added insect screen reduces both the outlet free area and, if actual
insect exclusion is wanted, the lower inlet area. Account for those screens,
wiring and the intended rear-wall clearance in the assembled thermal check.

The 152 × 137 × 8 mm spreader spans world X ≈ 127.013–279.013 mm,
Y = 476–484 mm and Z = 153–290 mm in the current DAE.
Its rebate is separated from the new outlet through-opening by about
15 mm of plywood in height. The two external sink envelopes occupy
X ≈ 138.1–199.1 and 207.1–268.0 mm, Z ≈ 163.0–279.8 mm, and
project to Y ≈ 519.6 mm.
Their fin channels are vertical, with a nominal 8 mm horizontal gap and
about 10 mm plate margin at the sides and ends. The sinks' outside plumes
will rise below the outlet; assess both paths with the cabinet at its
intended distance from a room wall. The [two-sink thermal screen](THERMAL.md)
supports this layout as a candidate, not an approved temperature result.
The sink tips extend about **22 mm behind the rear faces of the ash legs**.
The legs therefore cannot act as rear-wall stops for the sinks; maintain
clearance behind the sink fins and upper outlet at the intended placement,
and validate temperatures with that wall gap. The outlet insert is recessed
about 11 mm ahead of the rear ash faces, but this does not establish airflow
against a wall.

The 12 mm-deep rear perimeter brace bears against the cabinet sides,
top and bottom and supports the removable rear wall around its edge. Twelve
M4 × 10 threaded inserts and matching rear-panel screws are modelled. Their
outermost centres now sit 8 mm from the brace outer and inner edges; with a nominal
8.5 mm [insert outside diameter](https://www.theinsertcompany.com/type_e_threaded_insert_for_wood.php),
the remaining brace-edge ligament is about **3.75 mm**. The modelled
8.5 mm rear-panel countersinks now leave about **2.75 mm** to the panel
edge at the closest positions. These are meaningful improvements and appear
workable for the serviceable wall with correctly sized pilots and inserts.
The brace is glued to the surrounding cabinet as assumed; confirm one
representative insert/plywood joint in an offcut before committing the pattern.
The rear brace does not directly back the central FR-4 control-panel opening
described in §3. The driver, rear wall, spreader, vents, IEC inlet, control
panel and two sinks show candidate fasteners; four PSU mounting screws are
also modelled. The independent PE post is modelled. The amplifier PCB and its mounting fasteners are now modelled; the plate
pocket is not represented in the cabinet DAE, and physical component clearances
still require checking. The ash legs and
bumpers are present as glued wooden geometry, without mechanical fasteners.

## 2 PCB and mechanical constraints

The Rev-A implementation is one partitioned four-layer PCB carrying
both the amplifier and analogue front end. It sits parallel to the rear
aluminium plate while preserving physically controlled circuit regions as defined in
[Power and grounding](POWER_AND_GROUNDING.md).

The former approximately 1.2 mm uniform PCB-to-flat-plate gap, sole rear-side
TPA3251, front-side-only support parts, and SMD-only board are superseded. Use a
CNC-relieved inner plate face: a local, flat, bare thermal land contacts the
TPA3251 top PowerPAD through a thin TIM, while surrounding recessed fields
clear selected same-side SMD parts, through-hole terminations, copper, and
assembly tolerances. The land and substantial surrounding plate remain one
continuous thermal spreader; do not create a narrow thermal neck merely to
gain component clearance.

The intended local pocket clearance from the rear PCB surface to the finished
plate is approximately 4 mm, subject to the actual PCB/plate stack-up and
machined drawing. This makes a 1206 PVDD ceramic of at most 1.9 mm body
height plausible on the plate-facing side, with approximately 2.1 mm nominal
remaining for its solder stand-off, tolerances and electrical clearance. Keep
the pocket local to the parts and do not sacrifice the TPA3251 thermal land.

The TPA3251 must not become a mechanical spacer. Set PCB supports and the land
height from the actual package height, PCB thickness/bow, TIM compression, and
machining tolerances. The clamping arrangement must keep a reliable thermal
contact without loading the soldered leads. For each relieved zone, check the
maximum assembled component or trimmed-lead projection plus electrical
clearance and tolerance against the finished pocket depth. Define the pocket
floor/web thickness and flatness after the actual layout and thermal budget;
the remaining web must support heat spreading. Keep all other unintended
metal-to-net contacts clear, including
under board bow and loose or mis-trimmed leads. Insulate only where a verified
clearance and thermal design calls for it. Keep analogue-domain mounting
points isolated from the plate and do not bridge the PCB-domain partition with
mounting hardware.

The 17 October saved PCB geometry places the C26 470 µF capacitor's 17 mm
footprint/courtyard only 0.2 mm inside the board edge. C20 and C26 each have
about 0.3 mm nominal courtyard clearance to a 6 mm-diameter TPA3251
mounting-hole envelope. Panasonic lists a 16.0 mm nominal body diameter for
`EEVFK1J471M`, implying about 0.7 mm nominal lower board-edge clearance and
about 1 mm body-to-hole-envelope clearance. This is a placement observation,
not a measured collision. Verify the body tolerance, fastener/washer swept
area and assembly access in that earlier board state. The later saved PCB and
the user's selected hardware supersede its fastener concern: the 5 mm maximum
washer diameter fits the 6 mm keep-out, giving 0.5 mm nominal radial margin.
This closes [PR-003](PCB_LAYOUT.md#2-findings); retain the selected fastener
geometry. The separate C26 body-to-board-edge observation remains subject to
the actual component tolerance and final fabrication preview. The
[17 October amplifier layout review](POWER_AMPLIFIER.md#115-four-layer-output-and-supply-review-17-october-2026)
records the earlier saved-XML coordinates.

### 2.1 Aluminium heatsink plate

The P01 nominal 152 × 137 × 8 mm spreader and the rev0 PCB are in
fabrication (user report, 17 November 2026). Two external 557-140AB
sinks are the current cooling arrangement. The user considers the design
clearance adequate for prototyping; fit remains to be checked on receipt. The DAE omits the component pocket; actual PCB-to-metal clearance depends
on the received parts and mounted stack. With vertical 116.84 mm fin channels, the two nominal sink
footprints occupy 121.92 × 116.84 mm; with the modelled 8 mm gap between
them, the pair occupies about 130 × 116.84 mm. This leaves about 11 mm at
each plate side and end before fasteners, gasket and tolerances. The
90 × 100 mm PCB outline also fits nominally. Its supports and recessed field
are explored in the study below. The 13 November DAE shows four plate
bolts, twelve heatsink screws and the dedicated PE point. Retain the continuous IC thermal land and perimeter fixing/seal when
finishing the upper outlet. [Hub heatsink layout model](../../Hub/3d_models/thermal/557-140AB/README.md) records its
nominal envelope; [thermal design](THERMAL.md)
owns the cooling screen.

The 13 November [system order review](REV0_ORDER_REVIEW.md#2-findings-and-consequences)
found that the DAE's plate-fixing washers stop around world Y = 470 mm,
about 2 mm inboard of the rear plywood bearing face at Y = 472 mm. The
depicted stack therefore does not clamp the 4 mm residual plywood land.
Set the actual washer/nut stack to bear on sound ply, and trial that land,
insert and countersink before using the DAE as an assembly drawing. This
is a rear-panel hardware correction, not evidence of a P01 plate-hole error.

The preliminary 6 mm plate and early PCB stack proposal were superseded by
the 8 mm P01 design below. Their geometry is retained in
[mechanical history](history/MECHANICAL_HISTORY.md#1-earlier-spreader-geometry-and-proposed-stack).

The [working FreeCAD plate](../3d_models/Thermal%20spreader%20plate.FCStd)
records the nominal 8 mm geometry. The cabinet DAE uses the same thickness
and a rebate floor at world Y = 476 mm.

Using the base plate's local XY datum, the board maps as X = 31 + PCB X and
Y = 118.5 − PCB Y. A rounded clearance field spans X = 29–123 and
Y = 16.5–120.5 mm with R2 mm outer corners. It is 4 mm deep from the
rear seat plane, leaving 4 mm of metal to the front face. Four Ø8 mm
corner seats remain at (36, 23.5), (116, 23.5), (36, 113.5), and
(116, 113.5) mm. The 5 × 9 mm rounded IC land is centred at (75.215,
85.015) mm, 1.25 mm below those seats; two Ø6 mm adjustable-support
lands at (75, 72.5) and (75, 97.5) mm have the same nominal height as
the IC land. They need approximately 1.25 mm of selected shims to reach
the nominal board plane, before resolving the real contact stack. The land
size is a trial provision for TI's exposed pad, not a proven contact fit.
Its nominal clearance to the modelled lead rows is limited; assess actual
package, solder, placement and machining tolerances on the received parts.

The P01 prototype models four Ø2.50 mm pilots for M3 × 0.5 corner
threads and two Ø2.05 mm pilots for M2.5 × 0.45 IC-adjacent threads.
The drawing specifies through threads from the PCB face. The matching drill clearances
in the saved PCB are Ø3.40 and Ø2.90 mm respectively.
[JLCCNC ordering guidance](https://jlccnc.com/help/article/cnc-machining-ordering-guidelines).

**Heatsink fasteners:** the P01 drawing specifies twelve M3 × 0.5
through threads for six short screws per sink. Six inner positions pass
through the 4 mm pocket web; the six outer positions pass through 8 mm.
Check all slots and washer seats on the actual extrusions and plate.

The user measured a 3.2 mm flange and confirmed M3 × 8 mm screws for all
twelve positions. Use fully threaded M3 × 0.5 screws, 8 mm under the head,
and a nominal 0.5 mm steel flat washer. Nominal entry is 8 − 3.2 − 0.5 =
4.3 mm, giving 0.3 mm projection into the pocket at the six inner holes.
The [M3 × 8 mm pan screw](../../Hub/3d_models/fasteners/M3x8_PZ1_Pan_Head_Machine_Screw_Black/README.md)
and [M3 Form A washer](../../Hub/3d_models/fasteners/M3_Form_A_Flat_Washer_Black_A2/README.md)
models illustrate this nominal stack; neither model fixes the supplier or
surface finish for the final assembly.
The user accepts up to 0.7 mm projection, leaving 3.3 mm to the nominal
PCB rear surface. The user reports those locations are free of rear
components and may add PCB mechanical keepouts in future revisions.
Include the screw tip envelope, solder and copper clearance in that check.
Check actual stack dimensions, usable engagement and tip projection
during dry assembly before installing the PCB. Check washer support and
driver access at the open slots
and tighten evenly. A split spring washer flattens under preload. If extra
retention is required, consider low-strength removable threadlocker on clean
threads and keep the dedicated sink bonding path independent.
[NASA Fastener Design Manual](https://ntrs.nasa.gov/api/citations/19900009424/downloads/19900009424.pdf)
and [Henkel LOCTITE 222](https://datasheets.tdx.henkel.com/LOCTITE-222-en_GL.pdf).

**IC clamp proposal, 12 November 2026:** use the two existing recessed
support seats and select separate shim stacks from the assembled board.
Measured from the pocket floor, the four corner supports are 4.00 mm high
and the two inner seats and thermal land are each 2.75 mm high. The
nominal inner shim thickness is therefore 4.00 − 2.75 = 1.25 mm. With
the PCB seated on its corners, select each inner shim to fill the local
space under the PCB. Set the IC gap independently: it is the local PCB
height minus the thermal land height minus the installed pad projection.
For a 1.25 mm projection and 4.00 mm PCB height, the current land gives
zero nominal gap. A 2.70 mm land would give 0.05 mm if those inputs were
confirmed. Raising the inner shims alone would instead bow the PCB against
the four fixed corner supports. Establish the actual pad projection and
board plane before finalising the land height. A coordinated change to
all support heights can also increase the gap if needed. Start with a
small positive gap consistent with the nominal 0.05 mm grease bondline used in
the [thermal screen](THERMAL.md#16-current-8-mm-plate-and-intermittent-output-12-november-2026).
Verify a thin grease witness across the exposed pad under light, even
tightening and confirm the board seats on both shim stacks without visible
bow or rocking. If the package contacts before the supports seat, correct
the land-to-board gap before tightening. A fixed 0.10–0.20 mm interference
against the CAD package height
would make the preload depend on PCB and lead stiffness and the actual
package and solder stack. Spring hardware would need a defined working
deflection and would still transfer a reaction through the soldered package
in this layout. TI's evaluation module uses a separate screw-mounted
heatsink with a machined pedestal and supplies no package force target for
this plate. For a PCB revision using M2.5 IC screws, the recommended
clearance is Ø2.90 mm finished NPTH at the two existing centres. It gives
0.20 mm nominal radial play per screw. Ø2.70 mm gives 0.10 mm before hole
size and position tolerances and is a close-fit option only with a checked
tolerance stack. The [12 November PCB](PCB_LAYOUT.md#1-reviewed-design-state-and-scope) has
Ø2.90 mm NPTH. The spreader has M2.5 tap drills at those seats. Check all layers and preserve the 5 mm hardware
envelope and controlled amplifier-ground contact when assembling the received
board. Start all six screws loosely and locate the board by the
PowerPAD-to-land alignment before tightening. Use a separate assembly
guide if the thermal land needs tighter registration.
[JLCPCB NPTH guide](https://jlcpcb.com/blog/npth-design-guide).

The same PCB revision has Ø3.40 mm finished NPTH at the four existing
corner centres for M3 screws. This gives 0.20 mm nominal radial
clearance, matching the proposed M2.5 IC hardware. Check the combined
PCB and plate position tolerances and all-layer copper clearances. Where
an insulating sleeve passes through the board, size the hole to the sleeve
outside diameter and required clearance. The P01 study uses four M3 × 0.5 through callouts and Ø2.50 mm
tap-drill geometry at those centres.
[TI EVM guide](https://www.ti.com/lit/ug/slau751/slau751.pdf).

**Protective earth post and fastener review, 13 November 2026.** The DAE
has twelve M3 × 8 mm screws with tips 4.32 mm into the plate. The six inner
tips therefore project about 0.32 mm into the FreeCAD pocket. The simplified
DAE bores are Ø3.5 mm. The FreeCAD plate retains Ø2.50 mm pilots for M3 × 0.5.
The DAE shows twelve washers, one at each screw. Dry-check seating, tool access
and tip projection on the actual assembly.
The DAE screws are about 0.12 mm higher than the FreeCAD tap-drill rows.
Keep the existing drill rows and confirm alignment on the actual sinks.

The M4 post is centred at plate-local (19, 45.5) mm. The DAE defines a
Ø5 mm through bore with a Ø8.5 mm, 90° countersink from the heatsink face.
The machining study now includes that cut. The post centre is 12 mm from
the PCB outline and 10 mm from the pocket edge. The rear Ø20 mm finish
mask is tangent to the pocket edge and reaches to about 1 mm inside the
plywood opening. It is a finish callout. Verify the actual ring terminals,
cable bends and spanner access. Seat the actual head flush or slightly below
the heatsink face and secure the post before fitting the sink. The 16 November DAE depicts the inner full nut, serrated washer and outer
Nyloc on the post. The two nuts touch and the ring terminals are not modelled:
move the outer nut along the post to accommodate both actual terminals. The
modelled outer nut's outer face is about 7.8 mm from the screw tip before
that movement; this is an envelope, not a verified usable thread allowance.
Dry-fit both terminals and confirm full nylon engagement and accessible
thread before treating the assembly as complete.
The [grounding authority](POWER_AND_GROUNDING.md#3-protective-earth-and-chassis)
owns the hardware and bond. The heatsinks need their own verified bonds.
Check the received plate for the specified Ø20 mm anodising exclusion.

During dry assembly, verify PCB mounting isolation, actual finish and real
board and part tolerances.

The [working plate generator](../tools/freecad/build_thermal_spreader_study.py)
captures the current 8 mm geometry. To rebuild it in FreeCAD 1.1.4, run
`runpy.run_path(path, run_name="__main__")` in the GUI Python console,
where `path` is the generator's absolute path. It writes
`3d_models/Thermal spreader plate.FCStd` if that filename is free.
The final `Study` object is a valid single solid with 152 × 137 × 8 mm
bounds. The P01 STEP was re-imported as one valid solid of 126817.184 mm³
and checked for the six revised PCB tap drills. The 126886.059 mm³
pre-P01 model used smaller PCB tap drills.

**P01 prototype order package.** Use the matching
[STEP](../output/pdf/Thermal%20spreader%20plate%20-%20P01.step) and
[PDF drawing](../output/pdf/Thermal%20spreader%20plate%20-%20P01.pdf) for
the P01 fabrication package. The user reports that this plate and the PCB are in fabrication.
Trial the actual contact stack before deciding whether a revised plate is needed. Both
IC screw seats and the thermal land remain 2.75 mm above the pocket floor.
The nominal inner shim is 1.25 mm. Use actual support gaps and pad height
to select shims and to derive the next land height. If the IC contacts
before the supported board seats, use a matched set of corner spacers
for the trial and remeasure the two inner gaps before tightening.

Suggested fully threaded, non-countersunk PCB screws are M3 × 8 mm at
the four corners and M2.5 × 8 mm at the two IC seats. Length is measured
under the head. With a 1.6 mm PCB and 0.5 mm top washer, a corner screw
enters 5.9 mm into the 8 mm plate. With the same board and washer and
a 1.25 mm inner shim, the IC screw enters 4.65 mm into the 6.75 mm seat.
Both leave 2.1 mm to the heatsink face nominally. Check real screw length,
engagement, insulation thickness and the 5 mm hardware envelope at the
IC, then dry-check for tip projection. Fit the trial shims before tightening
the two inner screws.

The drawing proposes 6061-T6, matt black anodising outside four defined
finish zones, bare and unblasted PE and IC lands, both heatsink mating
footprints and both inner seat tops. Bare seat tops preserve options for
the shim and intentional amplifier bond trial. They do not decide the
electrical bonding point or replace the separate heatsink bond on each
extrusion. Inspect the received finish boundaries and finished land and seat dimensions;
the physical parts have not yet been verified.

The [drawing generator](../tools/freecad/draw_spreader_p01.py) uses
ReportLab 4.4.9. Run it with the bundled Python from the project root to
recreate the PDF at its linked path. Inspect the front and mirrored rear
views against the STEP before reusing the script for another revision.

Create a STEP only when needed. In FreeCAD select only `Study`, clear
**Export invisible objects**, and use millimetres and AP214. Alternatively
use `App.ActiveDocument.getObject("Study").Shape.exportStep(path)` with
the working plate active and an explicit output path. Reopen the result
and verify one solid of the expected dimensions and volume. A previous
whole-document STEP contained four solids because it included the hidden
machining stages.

Earlier plate geometry and its historical reconstruction notes are recorded in
[mechanical history](history/MECHANICAL_HISTORY.md).

The user reports that design clearance is adequate for the rev0 prototype.
Verify the received part, panel stiffness, actual component and screw-tip
clearances and passive-cooling performance during assembly and validation.

**Revised mounting decision, 11 November 2026:** no user control or external
connector mounts in the aluminium heat-spreader plate. The potentiometers,
polarity switch, IEC inlet and other external connectors mount on an insulating
FR-4 panel fastened to the 12 mm structural rear plywood. The plate carries the PCB, provides the continuous
TPA3251 thermal land and remains the dedicated protective-earth bond point.
This removes direct plate-to-pot bushing conduction; local electronics-chamber
air can still warm the controls, so confirm their body temperatures in the
finished thermal test. Both specified Bourns PDB18 parts are rated to +50 °C.
Keep their harnesses short and routed clear of Class-D switching nodes. The
[Hub potentiometer layout models](../../Hub/3d_models/electronics/PDB18-family/README.md) show their
nominal envelopes; the DAE now shows candidate positions, not a locked
control-panel machining drawing.

At roughly 20 °C, published representative conductivities are 222 W/(m·K)
for 1050A-H14, 166 W/(m·K) for 6061-T6, and 130 W/(m·K) for 7075. For an
unchanged plate geometry, a local conduction resistance varies approximately
as `1/(k × remaining thickness)`: 6061 therefore gives about 34% more
conduction resistance than 1050A, while 7075 gives about 71% more. This is a
material/geometry comparison, not a prediction of the assembled IC temperature.
Sources: [JLCCNC CNC materials](https://jlccnc.com/cnc-machining),
[1050A-H14 data](https://ucpcdn.thyssenkrupp.com/_legacy/UCPthyssenkruppBAMXUK/assets.files/material-data-sheets/aluminium/1050-h14.pdf),
[6061-T6 data](https://www.aalco.co.uk/datasheets/Aluminium-Alloy-6061-T6-Extrusions_145.ashx),
and [7075 data](https://ucpcdn.thyssenkrupp.com/_legacy/UCPthyssenkruppBAMXUK/assets.files/material-data-sheets/aluminium/7075.pdf).

Preferred visible finish: bead blasting plus ordinary matt-black anodising.
Do not assume a menu selection provides selective finishing. The fabrication
drawing must identify the visible cosmetic face and explicitly show bare,
unblasted functional zones: the flat TPA3251 thermal land, dedicated M4 PE-stud
contact on the inner face, and controlled amplifier-ground-to-plate contact.
Preserve specified contact flatness and finish; a blasted land may increase
TIM thickness. Show coating boundaries and acceptable anodising rack/contact
marks away from the visible face and functional zones. Mark any other
tolerance-critical bores, threads, mating/gasket faces or recess depths with
their required finished dimensions and coating state. Inspect the received plate for the required bare contacts and finish.
If the functional zones are not suitable, resolve the finish before assembly.
Sources: [JLCCNC finish comparison](https://jlccnc.com/finishes) and
[anodising dimensional guidance](https://jlccnc.com/blog/anodizing-thickness).

Keep an independently mounted M4 protective-earth stud on the plate near the
FR-4-panel-mounted inlet. Its hardware and wiring are defined in
[Power and grounding](POWER_AND_GROUNDING.md); the inlet cut-out belongs to
the rear-wall assembly in §3.

The selected Mean Well `RSP-200-36` envelope is 215 × 115 × 30 mm. Its final
internal position must preserve free-air convection, keep the terminal guard
accessible for assembly, respect the manufacturer's mounting-screw penetration
limits, accommodate the Mean Well `TBC-09` terminal cover, and prevent mains
wiring from sharing the signal/DC loom space.
The [Hub PSU 3D layout model and M4 guide](../../Hub/3d_models/electronics/RSP-200-36/README.md) can be used to
place its nominal case and threaded-hole centres. The separate guard and wiring
still need actual-part clearance checks.

### 2.2 Plate installation

- inset into structural plywood rear panel
- do not replace entire rear wall with aluminium
- closed-cell perimeter gasket
- dense perimeter fastening
- external surface exposed to room air

### 2.3 Thermal interface

Use the [provisionally selected MG Chemicals 8616 grease](THERMAL.md#15-thermal-interfaces-for-the-ic-and-two-sinks-1-november-2026)
at the TPA3251 top PowerPAD-to-spreader land and at both external
`557-140AB`-to-spreader joints. The three contacts need mechanical fixings;
the grease does not bond the parts. Clean the IC pad and bare, flat plate land,
apply a small continuous film, then bring the plate down squarely. Resolve
the real PCB/package/support stack so this joint closes with a thin film
without the IC acting as a spacer or its leads taking clamp load. Keep excess
grease off pins and surrounding parts. Do not use a thick compliant pad at
the IC to compensate for an unmeasured assembly gap.

For each sink, specify a flat, unblasted plate contact region beneath the
black-anodised extrusion, clean both faces, apply a thin continuous grease
film and tighten the sink fasteners evenly. Check the actual extrusions'
mating faces, slot hardware, thread engagement and assembled contact on the
received plate. Because grease and anodising cannot establish a
protective-earth path, provide a local bare-metal bonding contact at a
mounting point for each externally accessible sink, independent of the
greased face, and verify continuity to the earthed plate;
[power and grounding](POWER_AND_GROUNDING.md#3-protective-earth-and-chassis)
owns the PE architecture. A compliant gap pad is a fallback only if the
received surfaces or tolerances make grease contact unworkable, and its
compressed thickness and thermal effect must then be recalculated.

## 3 Rear-panel structure

Use:

```text
12 mm plywood structural rear wall (rear panel only)
+
large inset aluminium amplifier plate (8 mm current design basis)
```

Reasons:

- plywood provides cabinet stiffness/damping
- aluminium handles heat spreading/rejection
- smaller aluminium span reduces resonance risk
- plate carries the PCB and thermal contact; the rear plywood supports the
  insulating FR-4 control panel carrying all controls and external connectors

For an unchanged unsupported span, plywood panel bending stiffness scales
approximately with thickness cubed: `(12/18)^3 ≈ 0.30`. The rear wall is
outside the sealed acoustic chamber, but its remaining rails must still carry
the plate, controls, connectors and upper outlet without excessive flex or
poor fastener engagement. Keep continuous wood around the plate and openings,
then check the actual joint and fastener layout. With the same bare outer
envelope and exterior rear face, the modelled 12 mm wall adds 6 mm nominal
electronics-side depth relative to the superseded 18 mm rear wall.

### 3.1 Current FR-4 control panel (11 November 2026)

The user confirms the new control panel is **insulating FR-4**, not a metal
chassis part. The DAE shows a 65 × 137 × 1.6 mm panel (world X = 48–113 mm,
Z = 153–290 mm) covering a 55 × 110 mm through-opening in the 12 mm rear
plywood (X = 53–108 mm, Z = 167–277 mm). The nominal bearing overlap is
5 mm at each side and 13–14 mm at the ends. Four modelled M3 screw, washer
and nut sets clamp the panel near its corners into full-thickness plywood
outside the opening. The outline and hardware are a plausible mounting
scheme, but FR-4 sheet grade, cut-edge quality, fastener torque and resistance
to repeated plug and switch loads are not yet verified. Trial the assembled
panel and add a local support if the IEC inlet or RCA sockets flex it
noticeably; the large cut-outs and the approximately 7 mm lateral gap between
the modelled inlet and nearest RCA envelopes deserve particular attention.

The 1.6 mm panel is within the selected RCA sockets' 3 mm effective-panel
limit and the DD11 inlet's 8 mm limit. It also leaves ample nominal bushing
length for the PDB18 potentiometers and polarity switch. These dimensional
comparisons do not prove nut engagement, washer seating, keying, panel-hole
profiles, or fit of the actual received parts. The DAE includes candidate
`1106WA` knobs, but their bore depth and final stand-off remain to be checked
on the actual shaft and panel stack. The panel's outer face lies at Y =
485.6 mm, just outside the structural rear face at Y = 484 mm.

The [control panel DipTrace layout](../diptrace/control_panel.dipxml)
copies the DAE's `Control_panel` part as a separate mechanical board.
The current export uses the outside view with +X to the right and +Y
upwards from the lower-left corner of the bounding rectangle. The
[SketchUp layout model](3d_models/README.md#3-rear-fr-4-control-panel)
combines the STEP solid and the Top Silk artwork to depict the specified
black FR-4 and white legend. The 65 × 137 mm outline
retains the DAE's 52 vertices around its R6.35 mm corners. The nominal
thickness is 1.6 mm. Eleven circular openings are non-plated mounting
holes, and the 29 × 48 mm rectangular opening is a Board Cutout polygon.
The two signal layers have no copper features. Specify insulating FR-4
when ordering, and verify the routed opening's internal corner radius
against the physical inlet. The XML geometry was checked against both
the panel face boundaries and the DAE's through-wall meshes. Check the
outline, cutout and drill rendering in DipTrace before exporting for
fabrication.

**Control identities, 16 November 2026:** the DAE now contains one
`PDB181-E420K-103A2` and one dual-gang `PDB182-K420K-203B`; the PDB182 is
in the left-hand position in the model. This resolves the earlier duplicate
identity. Confirm that position is the intended crossover control, and check
its six PC pins, approximately 2 mm greater inboard reach, harness and actual
panel fit. The [Hub PDB182 record](../../Hub/3d_models/electronics/PDB182-K420K-203B/README.md)
owns the part dimensions.

The FR-4 panel gives a nominal 14 mm X gap to the aluminium spreader
(panel X maximum 113 mm; spreader X minimum 127 mm). The RCA model envelope
ends at X = 105.8 mm, about 21 mm from that spreader edge. This supports the
intended RCA-to-chassis isolation **geometrically**; finished metal hardware,
any decorative trim and wiring still need an actual isolation check. No PE
bond to the insulating panel is intended. The inlet PE conductor must instead
reach the independent plate stud, and the inlet rear cover, PSU terminal guard
and mains/signal harness segregation remain unmodelled. The modelled inlet
and nearest RCA envelopes are only about 7 mm apart laterally over a shared
height, so check the real inlet cover and wire bends before approving the
cut-outs. The FR-4 panel and its fasteners are not a mains safety enclosure
by themselves.

### 3.2 Knob and control fit

Select knobs for the PDB18 6 mm, 18-tooth splined shafts. The previously
considered Same Sky SAK-007 is for a D shaft and is not a direct fit.
Davies `1106WA` and Eagle `450-AE185`/`450-AE141` are shaft-profile
candidates, not physically verified selections; trial the actual knob,
potentiometer, FR-4 panel and nut stack before setting knob height or trimming
the shaft. The replaced plywood recess and earlier alternatives are recorded
in [mechanical history](history/MECHANICAL_HISTORY.md#2-earlier-plywood-control-recess-and-component-mounting).
