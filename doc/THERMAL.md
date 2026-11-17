# Thermal design

> **State — current thermal authority; reviewed 2026-11-17.** Owns passive
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
> Next gate: verify the received PCB/plate fit and validate temperatures in the
> assembled enclosure at representative sustained load. PCB and P01 are in fabrication.
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

The earlier bare-plate screen is superseded by the two-sink P01 assessment in §1.6; its assumptions are retained in [thermal history](history/THERMAL_HISTORY.md#11-rear-spreader-screen-31-october-2026).

### 1.2 Bolt-on extrusion shortlist (31 October 2026)

The rev0 layout uses two 557-140AB extrusions; their actual cooling remains to be validated in the assembly. The [earlier shortlist](history/THERMAL_HISTORY.md#12-bolt-on-extrusion-shortlist-31-october-2026) is historical.

### 1.3 Two 557-140AB extrusions (1 November 2026)

For two independent sinks with equal heat sharing in unobstructed air, the provisional sink-only screen uses `rise ≈ 40 K × (P / 28 W)^0.8`, based on the manufacturer's 14 W per sink at a 40 K rise. This is not an assembled cooling result; see §1.6.

### 1.4 Proposed 152 × 137 mm plate with two sinks (1 November 2026)

The [earlier plate-area comparison](history/THERMAL_HISTORY.md#14-proposed-152-137-mm-plate-with-two-sinks-1-november-2026) is superseded by the 8 mm P01 screen in §1.6.

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
between the package top and spreader. The 0.10 mm example adds about 17 K at 10 W: grease must not make up an
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

The [8 mm P01 plate](MECHANICAL.md#21-aluminium-heatsink-plate)
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
the modelled PCB, actual thermal interface, wiring, fixings and guards may
change the path. The upper passage from partition rear face to plywood opening
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
