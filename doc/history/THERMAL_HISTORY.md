# Thermal design history

> **Lifecycle: HISTORY.** Superseded heat-sink and plate comparisons, retained for provenance. Current assumptions, decisions and validation are in [thermal design](../THERMAL.md). These calculations are not current acceptance evidence.

### 1.1 Rear spreader screen (31 October 2026)

Use the then-intended **182 × 172 mm**, nominally 6 mm, black-anodised
spreader for this dated flat-plate screen. On 1 November the user corrected
the current starting outline to **185 × 172 mm** and proposed **152 × 137 mm**
with two external sinks; this earlier flat-plate calculation is retained for
comparison, not as the current outline. The current DAE depicts the
smaller plate and an upper outlet; [mechanical design](../MECHANICAL.md#13-electronics-chamber-ventilation-and-packaging)
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
representative sustained load. [Mechanical design](../MECHANICAL.md#21-aluminium-heatsink-plate)
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

The [557-140AB SketchUp layout model](../../../Hub/3d_models/thermal/557-140AB/README.md) records the
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
[557-140AB layout model](../../../Hub/3d_models/thermal/557-140AB/README.md).

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
[earlier flat-plate screen](../THERMAL.md#11-rear-spreader-screen-31-october-2026).

