# Thermal design

> **State — current thermal authority; reviewed 2026-11-12.** Owns passive
> cooling assumptions and acceptance limits; [mechanical design](MECHANICAL.md)
> owns the vent geometry. Read for heat or airflow changes. The revised
> inlet geometry and 15 mm under-PSU gap are the current design basis.
> The provisional sustained IC heat screen is 5–10 W, with 15–18 W retained
> as a bounded full-output stress case, not a continuous music requirement.
> Retain the two external 557-140AB sinks as the thermal design candidate.
> The current screen in §1.6 uses the 152 × 137 × 8 mm plate study with a
> 4 mm web. Check the exposed strip between the sinks in the assembled test.
> MG Chemicals 8616 grease is the preferred provisional TIM for the IC land
> and both sink joints; achieved film thickness and contact remain open.
> The 11 November DAE models both externally mounted upper inserts, a 152 × 137 mm spreader
> and two external 557-140AB sinks with candidate fixings; its outlet is about 99.5 cm² geometric
> area before any extra screen. Its finished airflow and cooling are unmeasured.
> Controls and external connectors now mount on an insulating FR-4 panel
> attached to the rear plywood, away from
> direct plate conduction; their assembled temperatures remain to be checked.
> Next gate: detail outlet and sink fixings with the PCB/plate layout, then validate
> temperatures with the finished enclosure at representative sustained load.
> Neither the plate calculation nor modelled vent area is a measured cooling result.
> The current ash legs do not set rear-wall clearance: the external sink tips
> project about 22 mm behind their rear faces. Test at the intended wall gap.

## 1 Cooling requirement

- no fan
- no forced air
- use **5–10 W IC heat as a provisional sustained music-use screening range**;
  its upper end represents deliberately bass-heavy use, not a measured duty cycle
- retain **15–18 W IC heat as a bounded full-output stress case** for temperature
  margin and short-event behaviour; continuous 140–150 W audio output is **not**
  a design or qualification requirement
- maximum rated room ambient: 35 °C
- thermal-design margin case: 40 °C room ambient; this evaluates margin or
  required derating and does not claim continuous full-power operation above
  35 °C

The 18 W figure comes from approximately 150 W audio output at about 89%
amplifier efficiency: `150 W / 0.89 − 150 W ≈ 18.5 W`. It is a
conservative project heat-allocation figure, not a measured IC-only loss; some
system loss occurs in the output filter and supplies. The clean-output target
specifies available level during bounded peaks. It does not prescribe a sine
wave held at that level for many minutes.

For an illustrative 4 Ω resistive load, a 150 W sine has 24.5 V RMS and
34.6 V peak. If filtered programme peaks reach 34.6 V and its **voltage** crest
factor is `C` dB, then `V_rms = 34.6 / 10^(C/20)` and
`P_audio,average = 300 / 10^(C/10)` watts. Thus 12, 10 and 6 dB give about
19, 30 and 75 W average output respectively. These are sensitivity cases,
not measured crest factors for this subwoofer or promises about particular
recordings. AES technical discussion identifies music crest factor as variable
and uses a 12 dB example for loudspeaker testing.
[AES technical committee notes](https://www.aes.org/technical/documentDownloads.cfm?docID=589).
The subwoofer and main loudspeakers reproduce different parts of the spectrum;
a 150 W subwoofer peak does not imply comparable simultaneous power in the mains.

The TPA3251 still loses power while switching at zero audio output. TI's
typical operating currents imply approximately 0.9 W from 36 V and 1.1 W
from 12 V across the active stage and its output network; not all of this
necessarily heats the IC. An intentionally simple screen taking 2 W fixed
loss and the remaining 16 W as proportional to *average* audio output gives
approximately 4, 5 and 10 W IC/system-stage heat for the three cases above.
This is not an efficiency curve or a guaranteed IC-loss bound. Keep the
5–10 W range provisional until actual output and temperature are measured;
compressed bass or sustained test tones can give a larger average.
[TI TPA3251 data sheet](https://www.ti.com/lit/ds/symlink/tpa3251.pdf).

### 1.1 Rear spreader screen (31 October 2026)

Use the then-intended **182 × 172 mm**, nominally 6 mm, black-anodised
spreader for this dated flat-plate screen. On 1 November the user corrected
the current starting outline to **185 × 172 mm** and proposed **152 × 137 mm**
with two external sinks; this earlier flat-plate calculation is retained for
comparison, not as the current outline. The current DAE depicts the
smaller plate and an upper outlet; [mechanical design](MECHANICAL.md#13-electronics-chamber-ventilation-and-packaging)
owns their geometry. With only the outer
face exposed to 35 °C room air, its area is 0.0313 m². A free vertical-plate
natural-convection correlation, representative air properties and surface
emissivity 0.8 give the following *idealised mean outside-face* temperatures:

| Heat through outside face | Estimated face temperature at 35 °C room ambient |
| ---: | ---: |
| 5 W | 51 °C |
| 10 W | 64 °C |
| 18 W | 83 °C |

At the 18 W point the estimate divides into roughly 8 W convection and 10 W
radiation. Anodised-aluminium emissivity near 0.8 is plausible, but finish,
surrounding surface temperatures, wall spacing and obstruction remain unverified.
The inner face and cabinet flow are excluded rather than credited as extra
cooling. [ASHRAE vertical-plate correlations](https://handbook.ashrae.org/Handbooks/F25/SI/f25_ch04/f25_ch04_si.aspx),
[anodised-aluminium emissivity measurement](https://bies.lbl.gov/publications/spectral-emissivity-anodized-aluminum).

The IC junction is hotter than the face mean. A 3 mm-deep pocket in 6 mm stock
leaves a 3 mm local web. For a roughly 30 mm² PowerPAD, illustrative 6061
conductivity of 166 W/(m·K), a small local pocket and a broader 6 mm plate,
a radial conduction screen gives about 0.6–1.0 K/W for spreading. For example,
`R ≈ ln(r2/r1)/(2πkt)` applied from a 3 mm-equivalent pad radius to a
20 mm pocket radius through 3 mm of metal, then to 80 mm through 6 mm,
gives about 0.8 K/W; real rectangular geometry and distributed cooling change
that value. A 0.05 mm
TIM at 3 W/(m·K) over 30 mm² adds `t/(kA) ≈ 0.56 K/W`; TI lists about
0.36 K/W junction-to-top-case resistance. Applying these illustrative paths
puts the junction at roughly **59–61 °C at 5 W**, **80–84 °C at 10 W**, and
**110–118 °C at 18 W**, at 35 °C room ambient. The near-field values are
particularly sensitive to pocket width, contact area, TIM thickness and clamp
pressure; they are not verified limits. [6061 conductivity](https://www.aalco.co.uk/datasheets/Aluminium-Alloy-6061-T6-Extrusions_145.ashx),
[TI package and thermal data](https://www.ti.com/lit/ds/symlink/tpa3251.pdf).

**31 October disposition, superseded as the current direction:** 182 × 172 mm
was a credible starting spreader for the
provisional sustained use range, without an evidence-led reason to enlarge it
for indefinite 18 W operation. Retain the intended plate area until the pocket,
outer-face exposure and finished assembly are defined; do not use this screen
as permission to shrink it. The 18 W case still approaches TI's 125 °C
overtemperature-warning level in the illustrative model and must be checked as
a bounded stress case. Both specified PDB18 potentiometers have a separate
50 °C body limit. They now mount on the rear FR-4 control panel, away from direct plate
conduction; check their body temperatures under the finished chamber's
representative sustained load. [Mechanical design](MECHANICAL.md#21-aluminium-heatsink-plate)
owns their placement.

### 1.2 Bolt-on extrusion shortlist (31 October 2026)

A rear-mounted, vertically channelled extrusion could permit a smaller plate,
provided it sits behind the IC with a flat, clamped TIM joint and has free air
entry below and exit above. As a stand-alone cooling path for the 10 W sustained
screen, retaining approximately the present 80–84 °C illustrative junction
temperature at 35 °C room ambient calls for roughly 3 K/W sink-to-room
resistance at its **actual** operating temperature. The exposed plate can
contribute additional cooling, but that contribution is not credited here.

Wakefield's 547-45AB is **not** a 2.1–2.2 K/W passive sink: the manufacturer's
2.1 K/W rating requires 300 ft/min (about 1.5 m/s) forced airflow, and no
natural-convection rating is given. Wakefield does publish free-air ratings for
the following black-anodised full-brick extrusions. The Mouser quantities and
single-unit prices are a **31 October 2026 UK catalogue snapshot**, not design
properties or a commitment to buy.

| Wakefield part | Footprint; fin projection | Natural-convection rating | Mouser UK snapshot |
| --- | --- | --- | --- |
| [557-140AB](https://www.mouser.co.uk/en/ProductDetail/Wakefield-Thermal/557-140AB) | 116.8 × 61.0 mm; 35.6 mm | 14 W at 40 K sink rise | 212 in stock; minimum 1; £7.29 each |
| [558-75AB](https://www.mouser.co.uk/en/ProductDetail/Wakefield-Thermal/558-75AB) | 61.0 × 116.8 mm; 19.1 mm | 12 W at 40 K sink rise | 194 in stock; minimum 1; £6.64 each |

At the specified 40 K rise, the ratings correspond to 2.86 and 3.33 K/W
respectively (`40/14` and `40/12`). Natural-convection resistance rises as
power and temperature rise fall, so neither number can be used unchanged at
10 W. Using the approximate natural-convection relation
`P ∝ (temperature rise)^1.25`, the 557-140AB's 10 W sink rise would be
`40 × (10/14)^0.8 ≈ 31 K` in unobstructed air. Adding the earlier illustrative
IC/top-TIM and local-spreading allowances plus a provisional 0.2–0.5 K/W
plate-to-sink joint gives roughly 83–90 °C junction at 35 °C room ambient.
This is a sensitivity screen, not a product rating or assembled-cabinet result.
The 557-140AB was the stronger single-sink candidate; the shallower
558-75AB may fit better if the cabinet sits close to a wall. Rotate either
profile so the fin channels run vertically on the finished cabinet. Check the
manufacturer's mounting-hole pattern, actual plate/PCB footprint, contact
flatness and pressure, rear-wall clearance, external protective-earth bond,
and assembled temperatures before reducing the plate. Mouser's API confirms
current stock and single-unit orderability but does not establish **active**
or **normally stocked** status; recheck those and the price before ordering.
[Wakefield full-brick data](https://wakefieldthermal.com/content/data_sheets/2021_data_sheets/Wakefield-Thermal-Extrusion-Profile-Guide.pdf),
[natural-convection guidance](https://www.micforg.co.jp/en/naturalcone.html).

The [557-140AB SketchUp layout model](../../Hub/3d_models/thermal/557-140AB/README.md) records the
manufacturer drawing's footprint, height and six-slot mounting grid for
placement checks. It does not change this provisional thermal disposition.

### 1.3 Two 557-140AB extrusions (1 November 2026)

Preferred provisional side-by-side arrangement, with its plate outline and
mounting still unqualified: assume both sinks receive equal heat from the
TPA3251 through the plate, have
their fin channels vertical, and draw unobstructed room air from below. The
manufacturer rates each sink at 14 W for a 40 K sink-to-air rise. Using the
approximate natural-convection scaling `P ∝ (temperature rise)^1.25`, the two
independent sinks would satisfy
`P_total ≈ 28 W × (sink rise / 40 K)^1.25`, or
`sink rise ≈ 40 K × (P_total / 28 W)^0.8`.

| Total allocated IC heat | Ideal equal share per sink | Calculated sink rise above room air |
| ---: | ---: | ---: |
| 5 W sustained screen | 2.5 W | 10 K |
| 10 W sustained screen | 5 W | 18 K |
| 15 W bounded stress | 7.5 W | 24 K |
| 18 W bounded stress | 9 W | 28 K |

At 35 °C room ambient, the 10 W point implies an approximately 53 °C sink
temperature. Reusing the earlier illustrative 0.36 K/W junction-to-case,
0.6–1.0 K/W local spreading, and an assumed 0.2–0.5 K/W plate-to-sink
joint, with the §1.5 preferred 8616 grease at an illustrative 0.05 mm IC
film (about 0.83 K/W bulk), gives roughly 73–80 °C at the IC junction.
This assumes
that the earlier spreading allowance applies to the actual two-sink layout;
a small central heat source does not automatically divide its heat equally.
The exposed parts of the plate may cool in parallel but are not credited,
while adjacent fin plumes, a nearby wall or obstructed airflow can increase
the sink rise. The 15–18 W rows are steady-equilibrium screens only; bounded
peaks need a duration-aware check. With the 116.84 mm fin-channel lengths
vertical, two nominal 60.96 mm widths occupy 121.92 mm across the plate,
before mounting and spacing allowances. The user's corrected 185 × 172 mm
starting plate and proposed 152 × 137 mm plate both contain that nominal
footprint. Neither this calculation nor the nominal fit approves
a smaller plate without the PCB, mounting, outlet and finished-temperature
review. [Wakefield 557-140AB rating](https://wakefieldthermal.com/wakefield-thermal-heatsink-dc-dc-full-brick-557-140ab/),
[natural-convection scaling](https://www.micforg.co.jp/en/naturalcone.html),
[557-140AB layout model](../../Hub/3d_models/thermal/557-140AB/README.md).

### 1.4 Proposed 152 × 137 mm plate with two sinks (1 November 2026)

The user corrected the pre-reduction plate to **185 × 172 mm** and proposed
**152 × 137 mm**, now depicted in the current DAE, to create more room
for the upper exhaust outlet. The outer
face areas are 0.03182 and 0.020824 m² respectively, a 34.6% reduction. Two
557-140AB base footprints total about 0.01425 m². If they fully cover those
regions, the remaining exposed outer plate falls from about 0.01757 to
0.00658 m², a 62.6% reduction. This affects the plate's parallel convection
and radiation path; it does not change the manufacturer's sink rating.

For an illustrative sensitivity calculation, take the earlier free flat-plate
screen's 5 W at 16 K rise over 0.0313 m² as about 10 W/(m²·K) effective
combined convection and radiation over the *uncovered* plate. Assume that
uncovered metal and both sink bases have one mean temperature, each sink sees
fresh room air, and both share heat equally. Combining the plate and sink
paths then gives
`P_total ≈ 28 W × (rise / 40 K)^1.25 + 10 W/(m²·K) × A_exposed × rise`.

| Total heat | Calculated sink rise with 185 × 172 mm plate | With 152 × 137 mm plate | Sinks alone, no plate credit |
| ---: | ---: | ---: | ---: |
| 5 W sustained screen | 8 K | 9 K | 10 K |
| 10 W sustained screen | 14 K | 16 K | 18 K |
| 18 W steady-equilibrium stress screen | 23 K | 26 K | 28 K |

Thus the *area change alone* raises the illustrative sink temperature by about
2 K at 10 W and 3 K at 18 W. At 35 °C room ambient the proposed plate gives
about 51 °C sink temperature at 10 W and 61 °C at 18 W in this model; the
sink-only free-air reference is about 53 and 63 °C. These are not upper bounds
for a cabinet close to a wall. The effective plate coefficient, near-isothermal
assumption, sink-to-plate contact and equal sharing are unmeasured; inner-face
cooling is excluded. Trimming perimeter metal outside the sink footprints
should leave the central conduction route broadly similar if the web, sink
overlap and clamping remain continuous, but mounting holes or a narrow neck
could raise local spreading resistance.

The 63 °C sink-only figure must not be treated as the maximum externally
accessible metal temperature. Under the earlier illustrative 0.6–1.0 K/W
local-spreading and 0.2–0.5 K/W plate-to-sink joint allowances, a plate patch
near the IC could be about 8–15 K hotter than the sinks at 10 W, or 14–27 K
hotter at an 18 W steady stress point, if that patch is exposed. The actual
surface gradient depends on where the IC thermal land lies relative to the
two sink bases and their central seam. Check the hottest reachable plate and
fins with the final placement and intended wall clearance; preserve the
separate 15–18 W bounded-duration requirement. [Wakefield 557-140AB rating](https://wakefieldthermal.com/wakefield-thermal-heatsink-dc-dc-full-brick-557-140ab/),
[natural-convection scaling](https://www.micforg.co.jp/en/naturalcone.html),
[earlier flat-plate screen](#11-rear-spreader-screen-31-october-2026).

### 1.5 Thermal interfaces for the IC and two sinks (1 November 2026)

**Preferred provisional build material:** one 3 mL syringe of MG Chemicals
`8616-3ML` silicone-free, electrically non-conductive thermal grease for all
three clamped contacts. The [current manufacturer data sheet](https://mgchemicals.com/downloads/tds/tds-8616.pdf)
lists 2.0 W/(m·K), non-bleeding behaviour and a −70 to +165 °C service range.
[RS UK lists the 3 mL syringe](https://uk.rs-online.com/web/p/thermal-grease/1247689),
but price and stock are transient; its older 1.8 W/(m·K) description is not the
value used below. The plain `557-140AB` order code has no integral thermal pad,
per [Wakefield's series guide](https://wakefieldthermal.com/content/data_sheets/2021_data_sheets/Wakefield-Thermal-Extrusion-Profile-Guide.pdf).
The grease is a gap-filling thermal contact material, not an adhesive, spacer,
electrical insulator for safety purposes, or protective-earth connection.

At the TPA3251's approximately 30 mm² top PowerPAD, film thickness matters.
The idealised bulk resistance is `R = t/(kA)`: for 8616 at 0.025, 0.05 and
0.10 mm, the results are about 0.42, 0.83 and 1.67 K/W respectively, before
real contact effects. At 10 W IC heat, the 0.05 mm example adds about 8 K
between the package top and spreader, versus about 6 K for the earlier
0.05 mm, 3 W/(m·K) illustrative assumption in §1.1. It would raise that
screen's junction estimate by about 3 K if every other term stayed fixed.
The 0.10 mm example adds about 17 K at 10 W: grease must not make up an
uncontrolled PCB-to-plate gap. TI's own [TPA3251 thermal model](https://www.ti.com/lit/ds/symlink/tpa3251.pdf)
uses a roughly 0.05 mm compound film at 0.7 W/(m·K); this supports the
thin-film approach but does not validate the assembled pocket. Set the land
height and PCB supports from the real package and board stack, with light,
reliable clamping that does not bend the PCB or load the soldered leads.
Apply a small, continuous, very thin film to the clean bare IC land and remove
excess from adjacent pins and components.

Each sink's nominal 116.84 × 60.96 mm base is much larger. Even a uniform
0.05 mm film at 2 W/(m·K) across one complete footprint has only about
0.004 K/W *bulk* resistance; actual loss is governed by flatness, anodised
surface finish, clamping, contact area and heat spreading. Apply a thin,
continuous film on each clean, flat mating region and bolt the sinks firmly
and evenly. Specify flat, unblasted plate regions beneath the sinks; do not
assume grease can rescue a bowed extrusion or a poor machined surface. Retain
the earlier 0.2–0.5 K/W plate-to-sink allowance as an unverified assembly
screen, not a material data-sheet rating. Since the same heat must still leave
through the sinks, TIM selection mainly changes IC and central-plate
temperatures; it does not materially lower the exposed sink temperature at a
fixed heat load. [Mechanical design](MECHANICAL.md#23-thermal-interface) owns
the assembly details and [validation](VALIDATION.md#3-thermal) owns the
finished-temperature check.

### 1.6 Current 8 mm plate and intermittent output (12 November 2026)

The [8 mm machining study](MECHANICAL.md#21-aluminium-heatsink-plate)
supersedes the assumed plate geometry for this thermal screen. It leaves a
4 mm web through the PCB pocket and 6.75 mm under the IC land. The land is
centred near the 8 mm gap between the sink bases, so the exposed strip over it
can run hotter than either extrusion. The two 557-140AB sinks remain the
candidate. The choice of heatsink fastener affects this model through the
flatness and repeatability of the clamped joints.

A steady finite-volume conduction screen uses 166 W/(m·K) for 6061,
152 × 137 mm outer dimensions, a rectangular pocket at X = 29–123 mm and
Y = 16.5–120.5 mm, and a 5 × 9 mm land centred at (75.215, 85.015) mm
with a uniform 1 W input over a centred 4.2 × 7.143 mm contact area.
The two front footprints start at X = 11.1 and 80.1 mm, Y = 10 mm, and
each measures 60.96 × 116.84 mm. Both sink bases are held at a common
reference temperature. Each footprint has a uniform contact conductance per
unit area of `1/(2 × R × A)`, where `A` is one footprint area and `R`
is the assumed aggregate joint resistance (0.2–0.5 K/W for the pair under
uniform flux). Local flux is
allowed to concentrate. All other boundaries are insulated. The screen
omits small holes, support islands and corner radii and does not solve the
airflow or detailed extrusion temperature.

For reproduction, connect adjacent volume centres with conductance
`k × shared area / centre spacing`. Use 1 mm XY cells and divide each of
the 4, 2.75 and 1.25 mm thickness layers into steps no greater than 1 mm.
On each sink footprint put the half-cell conduction resistance in series
with the contact resistance. Apply heat by source overlap area, solve the
steady heat balance, and add the source half-cell rise to the mean land
cell temperature. At 0.2 K/W assumed joint resistance, halving the XY and
main Z grid spacing changed the corrected land and seam results by less
than 0.03 K/W. The sink footprints carried approximately equal heat with
the common base temperature assumption. The ideal joint gave about
0.8 K/W land-to-sink. With the assumed joint range this becomes about
1.3–1.65 K/W, and the exposed seam hot spot is about 0.75–1.07 K/W above
the bases. An otherwise similar 6 mm plate with a 3 mm pocket web gave
roughly 0.15 K/W more land rise and 0.2 K/W more seam rise at the low
joint-resistance setting. Thus the thicker web saves about 1.5–2 K at 10 W
in this comparison. The actual contact and wall clearance can matter more.

Use the sink-only natural-convection approximation in §1.3, giving no
cooling credit to the plate surfaces. At 35 °C room ambient, add the
calculated plate gradients to the sink-base temperature and add another
1.19 K/W for the junction-to-top-case path plus a nominal 0.05 mm 8616
film. These are model estimates spanning the assumed sink-joint range.

| Heat allocated to IC path | Sink bases | Exposed strip near IC | IC junction |
| ---: | ---: | ---: | ---: |
| 2 W illustrative switching idle | 40 °C | 41–42 °C | 45–46 °C |
| 5 W sustained screen | 45 °C | 49–50 °C | 58–59 °C |
| 10 W sustained bass-heavy screen | 53 °C | 60–63 °C | 77–81 °C |
| 18 W steady stress comparison | 63 °C | 77–82 °C | 108–114 °C |

A 25% reduction in effective sink heat rejection at a given rise would
add about 5 K at 10 W or 7 K at 18 W. This illustrates airflow sensitivity
without assigning a penalty to an unmeasured wall gap. At 40 °C ambient
add another 5 K at unchanged heat and cooling conditions. A 0.10 mm IC
grease film would add about 8 K to the 10 W junction estimate compared
with the 0.05 mm assumption. The assembled junction and touch margins
therefore depend on contact and installation.

The 150 W audio rating is intermittent peak capability. Use the §1
loss and filtered programme examples for sustained heating, with 5 W
as a representative screen and 10 W for sustained bass-heavy use.
The plate study volume is approximately 127 cm³, or 0.34 kg and about
310 J/K at representative aluminium density and specific heat. A one-second
18 W heat event on a 5 W baseline adds 13 J. This represents about
0.04 K if averaged over the whole plate, while local pad and junction
temperatures respond more quickly. The bulk estimate does not establish
the safe duration of a peak. Check repeated peaks through the average load
and retain the bounded output test in [validation](VALIDATION.md#3-thermal).
For the sustained test, measure both sink bases and the exposed seam at the
intended wall gap. Compare the measured sink-to-room and seam-to-sink rises
with the screen before changing the heatsinks.

## 2 Rear electronics chamber

All heat-producing electronics occupy a chamber behind the sealed, inclined
acoustic partition. The locked natural-convection route is from a guarded
field of bottom-panel holes under the electronics chamber, past the PSU,
PCB, inductors, regulators, and inner face of the aluminium plate, to a
guarded outlet field in the upper half of the rear panel. The partition
guides this route but narrows the chamber near the top; place the outlet
below the narrow tip. The inlet and outlet need sufficient **net free area**
and a clear path with covers, wiring, and guards installed. Legs
must preserve the bottom inlet clearance on carpet in normal use; the
provisional gap calculation is in [Mechanical design](MECHANICAL.md#12-downward-driver-and-carpeted-floor-clearance).

Do not size the chamber by litres alone. Its minimum depth is the smallest that
meets component, terminal, wire-bend, guard, segregation, and assembly
clearances and then passes thermal validation. The 11 November DAE has about
135 cm² projected geometric bottom inlet area after its plywood apertures,
a 15 mm nominal under-PSU gap with about 99 cm² lateral turning area, and
about 99.5 cm² projected geometric upper outlet area after its plywood
opening. The outlet is now the smaller vent field. The upper insert's
nominal 6 mm holes are 8 mm deep and sit outside a 12 mm plywood opening;
any additional insect screen reduces the free area further. These are
modelled passages, not a measured flow rate. The supply's own vent openings,
unmodelled PCB, thermal interface, wiring, fixings and guards may change
the path. The upper passage from partition rear face to plywood opening
is about 75 mm at its lower edge and 26 mm at its upper edge;
the [mechanical authority](MECHANICAL.md#13-electronics-chamber-ventilation-and-packaging)
owns the geometry.

For scale, 20 W carried entirely by air with a 10 K rise needs
`Q = 20 W / (1.2 kg/m³ × 1000 J/(kg·K) × 10 K) ≈ 0.00167 m³/s`,
or about 6 m³/h. A 0.19 m warm-air column with a very optimistic 10 K
average temperature excess supplies only about 0.07 Pa of buoyancy
pressure. At 6 m³/h the nominal inlet velocity is about 0.12 m/s and
the outlet velocity about 0.17 m/s. Its ideal dynamic pressure alone is
`ρv²/2 ≈ 0.017 Pa`; entrance, hole, screen and turning losses add to that,
as do inlet losses. About 76% of inlet area lies under the PSU and must
turn through its 99 cm² nominal perimeter gap if that perimeter is
available. This supports the layout as a starting point, but
does not establish a system flow rate. The finished outlet and
heat path require the assembled test; heat can also leave
through the aluminium plate, PSU case, and cabinet surfaces, and PSU
intake air need not equal outlet air temperature.

At 35 °C rated room ambient, compare the measured local PSU intake temperature
and actual sustained PSU load with the RSP-200-36 derating curve. Its 45 °C
**full-load** ambient point gives a 10 K local-air-rise allowance only if the
full 200 W continuous rating is being claimed; continuous full-output audio is
not required. Repeat or extrapolate the thermal assessment at 40 °C room
ambient, recording the smaller margin and any necessary derating. The PSU's
overload protection is not a substitute for this temperature/load check.
