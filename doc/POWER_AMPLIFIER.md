# Power amplifier

> **State — current amplifier authority; reviewed 2026-11-08.** Owns the
> TPA3251 stage and RESET topology. Two 36 V-powered TPS3762-Q1 supervisors
> monitoring PVDD and `17V3` are selected. The dedicated 130 kΩ/7.5 kΩ,
> 1% E24 buck SENSE divider is selected. The now-placed L78M12 12 V regulator
> may sag briefly before the lowest calculated RESET trip; loaded buck-trough,
> return-offset and start/stop checks remain open. Würth `885012208124` PVDD
> bypass capacitors are selected. Their 36 V biased performance remains a
> model-based estimate. The current saved U3 output and supply copper has a
> promising scoped layout review: C20/C26 now feed broad 36 V and GND planes,
> while their solder-mask and mechanical clearances and prototype switching
> behaviour remain open. The 18 October Bottom-layer same-priority
> copper-pour warning cleared after the output pours were reprioritised;
> the 19 October power-stage copper review provisionally supports standard
> 35 µm outer / 15.2 µm inner copper for the 150 W into 4 Ω design point;
> the user reports that final-board DRC and net-connectivity checks pass;
> the reports were not independently inspected.
> D4 is now a green `ACTIVE` indicator driven by U11's N-channel directly
> from `AMP_nRESET`: lit when RESET is released and dark when it is asserted.
> The former false RESET-indication issue SR-001 is closed in the saved design;
> assembled brightness and polarity remain checks.
> The two-position Mini-Fit Jr speaker-output PCB header and short mating
> pigtail are selected; the 2.5 mm² driver-cable route, splice and service
> lengths remain to be fitted in the cabinet.

## 1 TPA3251 output stage

Configuration:

- PBTL
- use TI post-filter-parallel topology
- follow TI layout guidance closely

Critical layout requirements:

- very short PVDD decoupling loops
- compact bootstrap loops
- minimise switching-node area
- short high-current paths
- correct return-current routing
- keep analogue and switching grounds controlled
- on the combined PCB, face the TPA3251 input pins toward the analogue/power
  placement corridor and keep switching nodes and output inductors on the
  opposite side
- use the four-layer partition and layer intent defined in
  [Power and grounding](POWER_AND_GROUNDING.md); TI's 2-layer EVM establishes
  device feasibility, but two layers are not a project fallback

### 1.1 Rear-mounted IC and local support components

The TPA3251 faces the machined rear plate. Reliefs around its thermal land now
permit selected support components on the same PCB side as the IC. Prefer that
placement for PVDD ceramic decoupling and bootstrap capacitors when it gives
the shortest complete supply/return or BST/OUT loop. TI's PBTL layout guidance
places close ceramic bypass parts by the IC pins and calls for direct, broad
PVDD/ground connections without a via in the main current path. The rev0 layout is in fabrication; confirm actual component and plate
clearances during the physical dry fit.

Layout requirements:

- keep each local PVDD-to-GND decoupling loop compact and use broad same-side
  copper where practical; use local paired/parallel vias only where a layer
  transition is actually required;
- keep each complete BST-to-capacitor-to-OUT loop extremely small;
- keep AVDD, DVDD, GVDD, VBG, VDD, C_START, and other local bypass loops short;
- preserve symmetry through the via transitions for the differential input;
  and
- determine any high-current via drill, plating, count, and geometry from both
  current capacity and high-frequency inductance; do not size from DC ampacity
  alone.

The released PCB implements the selected component placements; verify physical
clearance during assembly.

#### 1.1.1 Partial PCB layout review, 17 October 2026

The earlier snapshots and evolving geometry are historical. The current PCB
release and remaining prototype checks are owned by [PCB layout](PCB_LAYOUT.md).

#### 1.1.2 Via barrel resistance estimate, 17 October 2026

An illustrative 0.20 mm drill, 18 µm copper-plating estimate gives about
2.36 mΩ per full-length via at 20 °C, excluding pad entry, spreading and
uneven current sharing. It is not a measured via rating.

#### 1.1.3 Via-field current and plane review, 17 October 2026

The analysis found that local return continuity and copper leading into the
fields matter alongside barrel resistance. See the current PCB layout for
final saved geometry and prototype checks.

#### 1.1.4 Local PVDD ceramic copper-parasitic estimate, 17 October 2026

The estimated local copper loops supported the selected ceramic placement;
they did not establish switching-edge overshoot or installed impedance.
Measure the PVDD waveform on the prototype using a suitably small probe loop.

#### 1.1.5 Four-layer output and supply review, 17 October 2026

The saved layout connects the bulk capacitors to the rail and return planes,
while the close ceramics supply the shortest switching-current loops. Final
release evidence and physical verification are in [PCB layout](PCB_LAYOUT.md).

#### 1.1.6 Bottom copper-pour priority warning, 18 October 2026

The user reported the warning cleared after reprioritising the output pours;
this is not itself a DRC result. The current release record owns the checks.

#### 1.1.7 Power-stage copper review, 19 October 2026

The scoped estimate provisionally supported 35 µm outer and 15.2 µm inner
copper at the 150 W / 4 Ω design point; it was not a thermal measurement.
Check actual switching and temperatures during prototype validation.

The detailed intermediate snapshots, calculations and superseded actions are
in the [historical amplifier record](history/power-amplifier.md#1-interim-layout-reviews).

### 1.2 Protection, fault response, and RESET control

Use the TPA3251's internal undervoltage, overcurrent, short-circuit, and thermal
protection. Supply undervoltage may recover automatically. A persistent
overload or overtemperature shutdown may remain latched until the user switches
the complete subwoofer off and on. Do not add an automatic fault-retry circuit.
The partial schematic draws `R18 = 22 kΩ` from `OC_ADJ` to GND, matching the
[TI PBTL reference circuit](https://www.ti.com/lit/ds/symlink/tpa3251.pdf).
TI's protection table assigns 22 kΩ to cycle-by-cycle current control (CB3C)
and lists a 16.3 A OC threshold; its electrical-characteristics table separately
lists 14 A nominal peak current for a 1 Ω test load at 22 kΩ. These are
different published descriptions, not a guaranteed 16.3 A trip point in this
board. The IC senses individual half-bridge FET current. At 150 W into a
nominal 4 Ω resistive load, the speaker current is
`sqrt(2 × 150 W / 4 Ω) = 8.66 A peak`; ideal sharing gives about 4.33 A peak
through each of the two parallel output paths on either bridge side. Real
speaker impedance, filter ripple, sharing error, and faults change those
currents. The 22 kΩ value therefore follows TI's starting example but is not
yet proven to protect this driver's voice coil or the output inductors. The
[Vishay inductor data sheet](https://www.vishay.com/docs/34337/ihlp5050fd-5a.pdf)
lists 7.8 A typical DC current for an approximately 20% inductance drop in the
10 µH part. That criterion is not a destructive limit, but it is below even
TI's 12.3 A table threshold at 30 kΩ; IC overcurrent protection cannot be
treated as an inductor saturation guard. CB3C
can limit individual overcurrent cycles and later latch off after persistent
overload; it is not a continuous output-power limiter. Retain R18 provisionally
while checking the chosen inductor's current limits and the 22–30 kΩ CB3C
options against the finished output stage. The
[TPA3251EVM guide](https://www.ti.com/lit/ug/slau751/slau751.pdf) lists
24, 27, and 30 kΩ as progressively lower nominal CB3C thresholds.

The former test-point-only indicator plan is superseded: the current saved
schematic and PCB have board-level diagnostic LEDs D2 (red, `FAULT`), D3
(orange, `CLIP_OTW`) and D4 (green, `ACTIVE`). No front-panel indicator is
required. The current board also has Top-side TP9/TP10/TP11 on
`AMP_nRESET`/`AMP_nFAULT`/`AMP_nCLIP_OTW`, with local rail and ground pads;
see the [current PCB review](PCB_LAYOUT.md#1-reviewed-design-state-and-scope).
The LEDs do not themselves qualify short-pulse diagnostics.
Each active-low FAULT and CLIP_OTW output drives the gate of a P-channel half of an onsemi
`NTJD4105CT2G` complementary pair (U4/U10). Its source is on `AMP_DVDD`; its
drain drives the paired N-channel gate and a 130 kΩ pull-down to GND. When the
status pin falls, the P-channel turns on, raising the N-channel gate and
sinking LED current from `12VAMP` through a 1.5 kΩ resistor. Saved net and
symbol numbering matches onsemi's S1/G1/D1 = 1/2/6 and S2/G2/D2 = 4/5/3;
the selected six-pad pattern has 0.65 mm pitch. The chosen Kingbright LED
symbols put anode on pad 1 and cathode on pad 2; confirm the actual package
polarity mark and land geometry before assembly. The earlier 18 October PCB
did not yet contain those indicators; the current saved PCB does.

**26 October ACTIVE revision:** D4 is Kingbright green
`APHCM2012CGCK-F01`. R40 connects `12VAMP` to its anode (pad 1); its cathode
(pad 2) connects to U11's N-channel drain (pad 6). U11's N-channel source
(pad 1) is at GND and gate (pad 2) is directly on `AMP_nRESET`. The unused
P-channel's source, gate and drain (pads 4, 5 and 3) are all at GND. R39 has
been removed. These nets and physical pad numbers agree in the saved
schematic and PCB, and Top silkscreen reads `ACTIVE`. RESET released turns on
the sink and lights D4; RESET asserted leaves it dark. `ACTIVE` reports RESET
release, not proof of fault-free operation or amplifier output. Confirm the
actual LED polarity mark, land dimensions and visible brightness on assembly.

The earlier 1 kΩ/100 mW selection exceeded its continuous rating at a
plausible high regulated rail, so the user selected 1.5 kΩ in R36/R37/R40. The
placed part is TE `CRGCQ0603F1K5`, 0603, 1%, 100 mW; its manufacturer and
Mouser part fields match the published identity. At a nominal 12 V rail and
illustrative 2 V LED drop, each branch draws `(12 − 2) / 1.5 kΩ ≈ 6.67 mA`
and the resistor dissipates `(12 − 2)^2 / 1.5 kΩ ≈ 66.7 mW`. The L78M12A's
specified regulated upper output is 12.5 V over its stated load/input range.
With an illustrative 1.8 V LED drop and a 1%-low 1.485 kΩ resistor, the
current is about 7.2 mA and dissipation is
`(12.5 − 1.8)^2 / 1.485 kΩ ≈ 77.2 mW`. This is a useful design corner, not a
formal absolute maximum: the Kingbright sheets specify typical LED forward
voltages at 20 mA, with no guaranteed minimum at this roughly 7 mA current.
Lower forward voltage or rail overshoot increases the resistor's power. TE
rates the resistor at 100 mW through 70 °C ambient and requires derating
above that temperature. The selection is reasonable if the local resistor
ambient stays within the un-derated range; check the eventual hot local
temperature if an indicator may remain continuously lit during a fault. The Kingbright
parts' intensity specifications are given at 20 mA, so actual board-level
visibility at 6–7 mA remains to be checked. The 26 October saved schematic
and PCB agree on the corrected R2/R10 `Mfr part` `CRGCQ0603F1K0` and Mouser
SKU `279-CRGCQ0603F1K0`. They also agree on Yageo `Mfr part`
`RC0603FR-0710KL` and Mouser SKU `603-RC0603FR-0710KL` for all five 10 kΩ
parts R19/R27/R30/R33/R34. The former purchasing-identity mismatches are
closed; these metadata edits did not change their electrical values.
The MOSFET ratings have ample voltage and current margin in the drawn circuit:
N-channel `VDS` is at most approximately the 12 V rail versus 20 V rating;
P-channel `VDS` and both `VGS` values remain within the roughly 3.3 V DVDD
domain versus the P-channel's 8 V limits. Both channels' guaranteed
`RDS(on)` points at 2.5 V gate drive are adequate for these small currents.

Each of the D2/D3 asserted branches adds up to
`3.6 V / 130 kΩ ≈ 0.028 mA` of external DVDD draw at nominal resistance.
With both status outputs low, their pull-down load is about 0.055 mA; the
two built-in pull-ups can each draw up to `3.6 V / 20 kΩ = 0.180 mA`, giving
approximately 0.415 mA total DVDD-sourced status-circuit current. The new
U11/D4 ACTIVE branch has no external static DVDD connection; the user's
earlier risk acceptance of the additional RESET-branch DVDD load is no longer
needed for this circuit. D4's approximately 6–7 mA LED current is sourced
from `12VAMP` and adds roughly 35 mW to U9's pass loss at the nominal
17.36 V input, subject to the actual LED voltage and load.
The selected 130 kΩ value supersedes both the original 47 kΩ and the examined
180 kΩ candidate. At the specified 25 °C P-channel off-leakage test value of
1 µA, it would develop 0.13 V versus 0.18 V for 180 kΩ. The built-in
20–32 kΩ pull-up range changes the two asserted-pin currents at 3.6 V by
0.135 mA; this is larger than the additional 0.055 mA through both 130 kΩ
pull-downs. That comparison describes current scale, but does not qualify
external loading of the DVDD reference node.
When the P-channel is off, its specified 1 µA maximum drain leakage at 25 °C
and −6.4 V test bias corresponds to 0.13 V across 130 kΩ, if applied as a
conservative estimate at the actual approximately −3.3 V bias. The N-channel
threshold is at least 0.6 V at 25 °C under its specified 250 µA test, but that
threshold is not a guaranteed zero-current boundary. The P-channel leakage
limit is not given over operating temperature, so false illumination at the
hot corner is not formally excluded by these data. The N-channel's specified
46 pF maximum input capacitance at its 20 V test point gives an illustrative
`130 kΩ × 46 pF ≈ 6 µs` discharge constant; actual capacitance and PCB
coupling can differ. For diagnostic LEDs the selected value appears reasonable,
subject to checking that D2/D3 remain dark in the inactive state on the
assembled board, including when warm.
TI nevertheless says DVDD/AVDD are not external supplies, and gives no
guaranteed external-load allowance. Treat this small draw as an explicit
design deviation pending measurement of DVDD under asserted conditions, not
as a data-sheet-qualified feature. Do not confuse the approximately 7 mA LED
current, which comes from `12VAMP`, with the DVDD load. Also, TI forces
`FAULT` high while RESET is low; D2 therefore cannot show a supervisor-held
reset or every protection event. D3 combines clipping and overtemperature
warning, and brief assertions may be too short for the eye without a latch.

**SR-001 — Medium, closed in saved schematic and PCB on 26 October:** The
original P-channel RESET LED could light while RESET was released. The saved
ACTIVE revision uses the N-channel connection described above, so a high
`AMP_nRESET` lights D4 and a low one extinguishes it. R31/R34 remain
30 kΩ/10 kΩ. At the 11.5 V rail, opposing 1% divider tolerances and a
conservative 100 µA sinking RESET-pin leakage give approximately 2.086 V at
the released node, above the TPA3251's 1.9 V high threshold. LED brightness
at that extreme is not guaranteed by the transistor's 2.5 V on-resistance
specification; check it on the prototype. Confirm LED polarity and function during prototype assembly and bring-up.

The superseded indicator analysis and rejected alternatives are preserved in
the [historical amplifier record](history/power-amplifier.md#4-previous-reset-indicator).
[TPA3251 data sheet](https://www.ti.com/lit/ds/symlink/tpa3251.pdf);
[NTJD4105C data sheet](https://www.onsemi.com/pdf/datasheet/ntjd4105c-d.pdf);
[red LED](https://www.kingbrightusa.com/images/catalog/spec/aphcm2012surck-f01.pdf);
[orange LED](https://www.kingbrightusa.com/images/catalog/spec/aphcm2012seck-f01.pdf);
[green LED](https://www.kingbrightusa.com/images/catalog/spec/aphcm2012cgck-f01.pdf);
[TE CRGCQ resistor](https://www.te.com/en/product-2-2176339-5.html);
[ST L78M regulator](https://www.st.com/resource/en/datasheet/l78m.pdf).

The selected analogue RESET topology uses two 36 V-powered Texas Instruments
`TPS3762-Q1` undervoltage supervisors. The fixed-30 V
`TPS3762EUVF4DDFRQ1` senses the local TPA3251 PVDD branch directly. The
adjustable-0.8 V `TPS3762EUV02DDFRQ1` senses the approximately 17.36 V buck
output through a divider, preferably at the amplifier-side `17V3` feed to
the 12 V LDO so no additional signal need cross the PCB partition. Each
active-low open-drain RESET output connects to the same TPA3251 `RESET` node:
either fault holds it low, and release requires both rails to recover. Both
parts use the 0.65 mm-pitch SOT-23-thin-8 package. No separate 3.3 V supply,
logic gate, 12 V supervisor, MCU, or automatic fault retry is selected.

Fit at least 0.1 µF of effective local VDD bypass capacitance at each device.
Tie each BIST_EN pin low; leave BIST and fixed-delay CTS pins unconnected.
Fit a separate timing capacitor from each CTR pin to its local ground. C0G is
not required by this circuit: TI limits CTR to 5.5 V in operation, so a 50 V
X7R is electrically suitable if its **minimum effective capacitance** after
initial tolerance, temperature, DC bias and ageing remains at least
`0.400 s / 2.96 MΩ = 135 nF`. A nominal 220 nF, ±10% X7R loses at most 10%
initially and 15% over the X7R temperature range, leaving `220 nF × 0.90 ×
0.85 = 168 nF` before bias and ageing. The placed KEMET base part
`C0805C224K5RAC` has the same nominal 220 nF, ±10%, 50 V X7R specification
as the cited `C0805C224K5RACTU` packaging variant. The latter part's data
show a small typical DC-bias change at the CTR pin's
at-most-5.5 V operating voltage and specify 3% ageing loss per decade-hour,
with capacitance tolerance referred to 1,000 hours after the last heating
above the ceramic's Curie point. Ten years after that event is about 1.94
decades beyond the reference, or approximately 5.8% further ageing loss. For
illustration, allowing 5% bias loss as well as the full 15% X7R temperature
change and the initial 10% tolerance gives `220 nF × 0.90 × 0.85 × 0.95 ×
0.942 ≈ 151 nF`, corresponding to approximately 446 ms at TI's minimum
2.96 MΩ timing resistance. The bias plot is typical, not a guaranteed
part-by-part bound, so this is a credible design margin rather than a formal
400 ms guarantee. Retain the placed 220 nF parts and check RESET release
timing on the prototype; consider 330 nF only if that check fails or more
margin becomes necessary. At nominal values, 330 nF would lengthen the
delay to about 1.22 s instead of 0.81 s. A single, provisional 30 kΩ/10 kΩ,
1%-resistor divider from the existing 12 V amplifier rail supplies the shared
RESET pull-up, subject to confirmation of the finished 12 V rail limits and
ground offsets. The 12 V rail supplies a logic level, not a precision sense
threshold. Do not load the TPA3251 DVDD reference as an external supply.

The selected dedicated buck SENSE divider is **130 kΩ** from `17V3` to
SENSE and **7.5 kΩ** from SENSE to the supervisor's local ground. Both are E24,
1% resistors with TCR no worse than 100 ppm/°C. The purpose is to detect a
falling buck rail and assert RESET while the 12 V amplifier supply is still
usable, while allowing some droop of the 15 V analogue rail during a buck
fault. With the now-placed L78M12, a brief 12 V sag before RESET assertion
remains possible at the lowest threshold. The
15 V rail is not itself monitored. With a nominal 0.8 V falling SENSE threshold,

```text
VBUCK,fall = 0.8 V × (1 + 130 kΩ / 7.5 kΩ) = 14.667 V nominal.
```

Using TI's ±0.9% threshold accuracy, ±200 nA as a conservative SENSE-current
bound, independent resistor initial tolerances and worst-opposed 100 ppm/°C
drift over 100 °C from 25 °C, the rail trip is calculated from
`VBUCK,fall = VITN × (1 + Rtop/Rbottom) + ISENSE × Rtop` (positive ISENSE into
the pin). Each resistor's combined worst-case initial and temperature change
is 1% + 100 °C × 100 ppm/°C = 2%. Opposed resistor extremes give a calculated
falling threshold of about **13.97–15.40 V**. With maximum 2.5% hysteresis,
the highest rising release is about **15.78 V**. The calculated lowest healthy
buck output is 16.78 V, so the rising threshold leaves about **1.00 V** for
buck ripple, transients, and sense/return offsets. ST specifies the placed
L78M12A's 12 V output over 5–350 mA with VIN from **14.5 to 27 V**. The lowest
calculated falling threshold is therefore **0.53 V below** its specified
minimum input. Brief 12 V sag before RESET assertion cannot be excluded, even
without buck ripple or feed drop. The 2 V dropout figure is typical at 25 °C,
not a guaranteed limit at this board's load and temperature. The
analogue 15 V LDO may already be out of regulation when RESET asserts; no
pre-dropout mute is claimed for that branch. At a fully specified 3 V RMS
input, the OPA167x first-buffer common-mode margin disappears if its supply
falls below approximately 12.5 V; smaller programme signals need less
headroom (see [analogue front end](FRONT_END.md)). Implement the chosen
divider at the amplifier-side `17V3` feed; confirm loaded buck trough,
amplifier-feed and return drops, and start/stop behaviour. RESET-before-any-
12 V-sag is not a design claim.

The current partial schematic's U5 buck feedback divider (`R24 = 180 kΩ`,
`R28 = 11 kΩ`) is not a substitute for this separate SENSE divider. Its FB
node is regulated near 1.0 V; the TPS3762's 0.8 V falling threshold would
represent only `0.8 V × (1 + 180/11) = 13.89 V` nominal at the buck output.
With the same conservative ±0.9% TPS threshold, ±200 nA SENSE current, 1%
resistor initial tolerance and opposed 100 ppm/°C drift over 100 °C used
above, its calculated minimum trip falls to about 13.22 V, below the
L78M12's 14.5 V specified input minimum even before ripple or feed losses.
If the extra SENSE current were 200 nA, the static shift in the buck's regulated
output would be about `200 nA × 180 kΩ = 36 mV`: small, but not zero. The
added SENSE input and long branch would also expose the buck's
feedback node to coupling and capacitance; MPS calls for the feedback
resistors beside FB and away from SW. Sensing the `17V3` feed near the
amplifier LDO also covers a drop in that feed which the buck-local FB node
cannot see. Retain the separate divider.

The intended verification is RESET low for at least 400 ms after PVDD
application or either detected fault, prompt assertion on each monitored
rail's decay, and acceptable post-filter loudspeaker transients on normal
start-up, shutdown, and rapid off/on. The two monitors do not independently
detect failure of either downstream LDO while both monitored rails stay
healthy; the TPA3251 retains its internal supply protection.

Primary sources: [TI TPS3762-Q1 data sheet](https://www.ti.com/lit/ds/symlink/tps3762-q1.pdf),
[KEMET C0805C224K5RACTU specification](https://search.kemet.com/download/specsheet/C0805C224K5RACTU),
[KEMET X7R series test methods](https://content.kemet.com/datasheets/KEM_C1002_X7R_SMD.pdf),
[TI TPA3251 data sheet](https://www.ti.com/lit/ds/symlink/tpa3251.pdf), and
[Torex XC6701 data sheet](https://product.torexsemi.com/system/files/series/xc6701.pdf),
and [ST L78M data sheet](https://www.st.com/resource/en/datasheet/l78m.pdf).

#### 1.2.1 Superseded supervisor analyses (decision record)

Earlier supervisor candidates and their calculations are documented in the
[historical amplifier record](history/power-amplifier.md#2-superseded-supervisor-analyses).
They do not specify the selected RESET circuit.

#### 1.2.2 Accepted PBTL DC-fault policy

The [TPA3251 data sheet](https://www.ti.com/lit/ds/symlink/tpa3251.pdf)
states that its DC-speaker protection is disabled in PBTL mode. Rev A will not
add an external differential-DC detector, speaker relay, series output MOSFETs,
or switched-PVDD protection. This deliberately accepts the residual risk that
a rare amplifier-output failure could damage the internally connected driver.
The decision is proportionate to the fixed internal speaker wiring: there are
no user-accessible speaker terminals, and the cable and sealed feed-through
must remain insulated, supported, and protected from abrasion and earthed
metalwork. `RESET` control is thump suppression and functional shutdown; it is
not claimed as independent protection against a physically shorted output
transistor.

### 1.3 Speaker-output connection

The saved J5 PCB header remains Molex Mini-Fit Jr `39-28-1023`, two-position,
vertical through-hole and tin-plated. The mating board-end assembly is now
`215326-1021`: a two-position, tin-plated female pigtail with two
factory-terminated **150 mm, 16 AWG (approximately 1.31 mm²)** leads. It
replaces the previously selected `215326-1023`. The previous part's 600 mm leads are unlikely
to reach both planned service positions as a complete harness and would leave
an unnecessarily long 16 AWG section when joined to the heavier cable.
The assembly includes housing and contacts; no Mini-Fit crimp tooling is needed.
The selected parts have a positive latch and are distinct in position count
from the six-position 36 V input connector. Connect the two positions to the
filtered PBTL speaker outputs, not to chassis or `GND`.

Join the short pigtail to the user's round-jacketed, two-conductor **2.5 mm²**
speaker cable within the ventilated electronics chamber. Use separately
insulated, mechanically supported splices, kept clear of mains wiring,
heatsinks and the PCB; do not let the splice or connector carry a pull on the
cable. Pass the intact outer jacket through the sealed partition and terminate
the driver end after installation. Leave independent service slack on **both**
sides of the fixed feed-through: enough to remove and support the driver and
to draw out the rear panel with J5 still connected. Approximately 1 m total
is a planning estimate, not a cut length; dry-fit both service positions before
cutting the cable or sealing the penetration.

On 15 November 2026 the user measured both received SB23MFCL45-4 tabs at
approximately 6.3 mm wide and 0.7–0.8 mm thick. This suggests the 6.3 × 0.8 mm
(.250 × .032 inch) receptacle family; the [driver data sheet](https://sbacoustics.com/wp-content/uploads/2024/02/8in-SB23MFCL45-4.pdf)
does not specify the tabs. A candidate, not yet physically fitted or selected,
is [TE 9-160313-2](https://www.te.com/en/product-9-160313-2.html): 6.35 ×
0.81 mm tab, 1–2.5 mm² conductor, partially insulated, with a maximum
4.32 mm insulation diameter. Confirm cable insulation diameter, crimp tooling,
tab engagement and retention on the actual driver before committing the harness.
[Farnell UK](https://uk.farnell.com/amp-te-connectivity/9-160313-2/crimp-terminal-female-blue/dp/587254)
listed stock in multiples of ten on 15 November; recheck before ordering.

At the approximately 150 W into 4 Ω output target, speaker current is
`sqrt(150 W / 4 Ω) = 6.12 A RMS`. Molex's two-position, 16 AWG brass-contact
guideline is 9 A per contact, subject to PCB copper, ambient temperature, and
the completed cable termination. The Mini-Fit Jr female contact's specified
maximum conductor is 16 AWG; do not force the 2.5 mm² conductor into it.
For scale, taking copper resistivity as approximately
`0.01724 Ω mm²/m` at 20 °C, a 1 m two-conductor 16 AWG run has an estimated
`2 × 0.01724 × 1/1.31 = 0.0263 Ω` loop resistance and dissipates about
`6.12² × 0.0263 = 0.99 W` at the 150 W design point. A 1 m run comprising
150 mm of 16 AWG and 850 mm of 2.5 mm² gives approximately `0.0157 Ω` and
`0.59 W`, before contact and splice resistance. The change is modest
electrically, but retains the user's preferred heavier jacketed cable through
the cabinet. Confirm J5 pin numbering, polarity, routing, strain support,
splices and the driver-end termination during assembly. Recheck Mouser UK
availability, normal-stock status, MOQ and price before ordering.

If a hand-built Mini-Fit end is later preferred, the corresponding loose
two-position receptacle housing is Molex `39-01-2020` (5557 series), with two
tin-plated 16 AWG female contacts `39-00-0078` (bag packaging). These retain
the 16 AWG termination limit and require suitable crimp tooling; they do not
accept the 2.5 mm² cable directly.

Manufacturer sources: [Mini-Fit Jr product specification](https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/productspecificationpdf/555/5556/PS-5556-001-001.pdf),
[header](https://www.molex.com/en-us/products/part-detail/39281023),
[150 mm pigtail](https://www.molex.com/en-us/products/part-detail/2153261021),
[loose housing](https://www.molex.com/en-us/products/part-detail/39012020), and
[16 AWG loose contact](https://www.molex.com/en-us/products/part-detail/39000078).

## 2 Output inductors

Locked part:

- Vishay-Dale `IHLP5050FDER100M5A`
- 10 µH
- four required

Reasons:

- low DCR
- provisional current margin; saturation under actual carrier and load
  conditions is not yet qualified
- acceptable bias behaviour
- published L/Q vs frequency
- provisionally suitable for the specified nominal 600 kHz operation; confirm
  loss and temperature in the assembled amplifier

Prototype validation required:

- idle temperature
- sustained-load temperature
- contribution to idle PVDD current

## 3 Output capacitors

> **State:** First-prototype capacitor selection, reviewed 2026-10-26. Owns the
> output-filter capacitor choice. The 10 µH inductors are locked in Section 2.
> The canonical schematic now draws two TDK `B32701P4684K000` film capacitors,
> one on each combined speaker-output side. Next gate: check response/damping,
> carrier ripple and capacitor temperature in the prototype. The TDK series has
> a published 600 kHz current allowance.

The [TPA3251 data sheet's differential PBTL example](https://www.ti.com/lit/ds/symlink/tpa3251.pdf)
draws four 10 µH inductors but only **two** 680 nF post-filter shunts: one
on each combined speaker-output side. Its accompanying design-requirements
table describes the filter as 10 µH + 1 µF, so the figure and table should
be treated as example values rather than an exact capacitor mandate. The
[TPA3251 EVM](https://www.ti.com/lit/ug/slau751/slau751.pdf) instead has four
680 nF positions and 7 µH inductors; that different LC implementation was the
source of the previous four-position assumption.

In the current XML, L1 and L3 join at `SPK+`, while L2 and L4 join at `SPK-`.
C17 and C30 each provide one 680 nF shunt to GND. Each same-side pair of
10 µH inductors is ideally 5 µH in parallel, giving the simple LC scale
`f0 = 1/(2π√(5 µH × 680 nF)) ≈ 86 kHz`. This is not a measured loaded
response; speaker impedance, filter loss, layout, and the Zobel network alter
damping. The earlier 12 × 220 nF MLCC arrangement, with six shunts per side,
was superseded by the two film parts; its idealised scale was about 62 kHz.

**Capacitance trade-off (idealised):** for differential operation into a
purely resistive 4 Ω speaker, symmetry lets each combined output side be
modelled with 5 µH series inductance, its shunt capacitor, and 2 Ω to a
virtual ground. The low-pass denominator is
`1 + sL/R + s²LC`, so `f0 = 1/(2π√(LC))` and `Q = R√(C/L)`.

| Capacitance per side | Implementation example | Ideal f0 | Ideal Q | Additional ideal attenuation at 600 kHz versus 680 nF |
| --- | --- | ---: | ---: | ---: |
| 680 nF | one 680 nF | 86 kHz | 0.74 | reference |
| 1.0 µF | one 1.0 µF | 71 kHz | 0.89 | about 3 dB |
| 1.36 µF | two 680 nF in parallel | 61 kHz | 1.04 | about 6 dB |
| 2.04 µF | three 680 nF in parallel | 50 kHz | 1.28 | about 9.5 dB |

The 680 nF value gives Q close to the 0.707 Butterworth value in this simple
4 Ω model. Larger capacitance reduces carrier voltage ripple, but raises Q
and can increase response peaking around the lowered LC frequency. The real
speaker is not a 4 Ω resistor at tens of kilohertz, and the Zobel and loss
change the result; this table is a sensitivity calculation, not a predicted
measured response. At 100 Hz and 150 W into 4 Ω, each side carries only about
5 mA RMS of audio-frequency current in a 680 nF shunt (about 10 mA for
1.36 µF), so extra capacitance offers little benefit within the intended
subwoofer passband. At the carrier, inductor ripple is set mainly by rail
voltage, inductance and switching period; extra capacitance chiefly lowers
the shunt voltage ripple. Paralleling identical parts shares that ripple
current, but the selected single TDK part already has substantial published
current allowance. Retain one 680 nF per side as the prototype baseline;
increase capacitance only if measured residual carrier or response warrants
the accompanying damping and layout review. TI's PBTL figure uses 680 nF,
while its accompanying table gives 1 µF as another example.

**Selected first-prototype choice:** two TDK `B32701P4684K000`
metallised-polypropylene through-hole capacitors, C17 from `SPK+` to GND and
C30 from `SPK-` to GND. Each is 680 nF ±10%, 450 V DC, with a 13 × 6 × 12 mm
maximum body and 10 mm lead pitch (0.6 mm leads). The alternative TDK
`B32702P4684K000` has the same capacitance and voltage, a 18 × 5 × 10.5 mm
body and 15 mm pitch (0.8 mm leads). The smaller-pitch part occupies about
78 mm² of body plan area versus 90 mm² for the 15 mm version, but is 1.5 mm
taller; verify actual plate clearance. Both have a clear manufacturer drawing,
unlike the conflicting distributor pitch for the earlier Panasonic candidate.
The two-capacitor arrangement follows the data-sheet PBTL figure and avoids
the MLCC bank's uncertain DC-bias capacitance. The saved layout places each near its inductor join; assess the actual
return and switching behaviour on the prototype. The 2026-10-11 six-MLCC proposal
and subsequent Panasonic film proposal are superseded as preferred candidates;
they remain alternatives if the TDK part fails prototype checks.

At idle, each output shunt sits near half of the 36 V rail; audio and
switching ripple add to this. The 450 V DC rating has ample nominal margin,
subject to measured overshoot. For a first-order carrier
current estimate, each 10 µH inductor sees about 18 V for half a 600 kHz
period: `ΔI ≈ 18 V / (2 × 600 kHz × 10 µH) = 1.5 A` peak-to-peak. If the
two same-side PBTL currents add, the single shunt sees about 3 A peak-to-peak,
or `3/(2√3) ≈ 0.87 A RMS` for a triangular ripple at idle. This is an
idealised estimate, not a measured worst case over modulation and load.

TDK's 680 nF permissible-current curves extend to 1 MHz, unlike Panasonic's
published ECWFD plot, which stops around 250 kHz and omits the exact
15 mm-pitch 680 nF variant. Reading TDK's **sinusoidal** curves at 600 kHz
gives approximately 3 A RMS for `B32701P4684K000` and 2.5 A RMS for
`B32702P4684K000` at ambient temperature at most 85 °C and no more than
15 °C self-heating. The 10 mm part thus has both the smaller plan area and
the higher published current allowance. These curves are stronger selection
evidence than either part's isolated-pulse dV/dt limit (60 V/µs and
25 V/µs respectively), but a PWM waveform has harmonics and its actual
current changes with modulation and load. Verify the waveform, capacitor case
temperature at representative maximum output, residual carrier and loaded
filter response on the prototype. On the received board confirm lead pitch,
orientation, clearance and mechanically secure mounting. The nominal 450 V
rating alone is not the approval criterion.

Sources: [TDK B3270*P data sheet](https://www.tdk-electronics.tdk.com/inf/20/20/ds/mkp_b32701p_b32703p.pdf),
[TDK B32701P4684K000 product page](https://product.tdk.com/en/search/capacitor/film/snubbering_pfc/info?part_no=B32701P4684K000),
[TDK B32702P4684K000 product page](https://product.tdk.com/en/search/capacitor/film/snubbering_pfc/info?part_no=B32702P4684K000),
[Panasonic ECWFD technical data](https://industrial.panasonic.com/cdbs/www-data/pdf/RDI0000/ABD0000COS113.pdf),
[TI TPA3251 data sheet](https://www.ti.com/lit/ds/symlink/tpa3251.pdf), and
[TI LC filter design guidance](https://www.ti.com/lit/an/slaa701a/slaa701a.pdf).

## 4 Zobel/output damping network

**2026-10-12 output-small-capacitor rating review (historical analysis;
selection updated 2026-10-26).** C19/C28 are 1 nF directly from the two post-inductor
speaker-output nodes to GND. C16/C31 are 10 nF in series with R20/R21
(3.3 Ω) from those same nodes to GND. Each capacitor therefore sees its
own output-to-ground voltage, not the full differential speaker voltage.
In an ideal symmetrical 36 V PBTL stage delivering 144 W into 4 Ω, the
differential 24 V RMS output corresponds to about 12 V RMS per side around
an 18 V midpoint: roughly 1–35 V per node. Add switching ripple and any
LC/output-wiring overshoot to that estimate; the actual peak is unverified.
Thus the formerly drawn 250 V ratings were not required by the nominal waveform.
100 V ceramic parts provide substantial
nominal margin, subject to the final voltage waveform, dielectric/impedance,
and capacitor and resistor temperature. A 50 V 10 nF X7R/3.3 Ω pair is used
in TI's output-network guidance, but choosing 100 V here leaves more room
for post-filter ringing. The TPA3251's 50 V output-pin absolute maximum
does not itself bound overshoot at the post-inductor nodes. The earlier option
to retain 250 V parts was superseded by the saved 100 V selection. The 1 nF
parts are small high-frequency shunts:
at 600 kHz their ideal reactance is about 265 Ω versus 0.39 Ω for the
680 nF film shunts. The 10 nF/3.3 Ω branch starts to become resistive near
4.8 MHz, making its high-frequency damping and heating more important than
the nominal voltage rating alone.
[TPA3251 data sheet](https://www.ti.com/lit/ds/symlink/tpa3251.pdf);
[TI output-network guidance](https://e2e.ti.com/support/audio-group/audio/f/audio-forum/492175/question-about-tpa3251d2-diodes-at-output).

**First-prototype saved selection, 26 October 2026:** C19/C28 use Würth
`885012207116` 1 nF, 100 V; C16/C31 use Würth `885012207122` 10 nF,
100 V. R20/R21 use Yageo `RC2512FK-7W3R3L` 3.3 Ω, 2 W, 2512.
The 17 November catalogue check corrected the former 2.2 W description:
[Yageo’s high-power series datasheet](https://www.mouser.com/datasheet/2/447/PYu-RC-HP_51_RoHS_L-1-532175.pdf)
rates the 2512 part at 2 W at 70 °C, with derating above that temperature.
Mouser’s listing has a conflicting 1 W description but a 2 W attribute.
The user accepts the 2 W selection for intermittent peak output; actual
heating remains a prototype measurement. The saved schematic and PCB now
show the correct 2 W rating.
The nominal voltage argument supports trying these values; it does not
establish the actual overshoot, high-frequency damping or heat dissipation.

Prototype validation:

- temperature at idle
- temperature under sustained high output

## 5 General amplifier-board passives

### 5.1 Resistors

Default:

- SMD preferred; allow through-hole with justified layout and plate clearance
- 1%
- choose the package and power rating for the actual voltage, dissipation,
  assembly method, and placement; 0603 is suitable for the low-level input
  resistors R16/R17

Exceptions:

- precision signal networks
- Zobel/power resistors

### 5.2 Ceramics

Use voltage rating appropriate to node.

Guideline:

- 12 V rails: 16–25 V X7R
- bootstrap: 50–100 V
- PVDD bypass: 50–63 V minimum; 100 V is acceptable when the chosen part
  retains sufficient capacitance and low impedance under 36 V bias
- output filter: provisional 680 nF TDK metallised-polypropylene film
  shunt per combined speaker side; see Section 3 for qualification
- use C0G/NP0 for small precision/HF values where appropriate

Do not blindly use 100 V parts everywhere.

**Selected choice, confirmed by the user 2026-10-17; operating margin still to
verify.** Both saved DipTrace XML files place Würth `885012208124` 2.2 µF,
100 V X7R 1206 at C21/C22/C24/C25. The substitution was made to target at
least 1 µF per part at 36 V DC bias, which the prior placed Murata 0805 model
did not achieve. The supplied typical bias plot implies approximately
`2.2 µF × 0.515 = 1.13 µF` at 36.2 V and 25 °C. Applying the specified
−10% initial tolerance to that *typical* ratio gives about 1.02 µF, but this
is not a guaranteed minimum: the data sheet specifies nominal capacitance at
its 1 kHz test condition, not a minimum at 36 V DC bias. For illustration,
also applying the X7R −15% temperature extreme to 1.02 µF yields about
0.87 µF before ageing. That is a conservative margin illustration, not a
measured capacitance at an operating temperature. Keep the Würth MPN selected;
verify its exact-part biased impedance/ripple at the switching harmonics,
assembled pocket clearance, and finished capacitor-to-U3 supply/ground loops.
The earlier Murata comparisons are historical and do not describe the saved design.

Earlier capacitor candidates and their bias calculations are retained in the
[historical amplifier record](history/power-amplifier.md#3-superseded-pvdd-bypass-candidates).

### 5.3 Bulk electrolytics

- SMD aluminium electrolytic
- 63 V preferred for 36 V PVDD
- low ESR
- suitable ripple-current rating
- nominal 470 µF reference positions

**17 October 2026 comparison — retain the selected 63 V parts at C20/C26.**
The saved schematic and PCB place Panasonic FK `EEV-FK1J471M` (catalogue
`EEVFK1J471M`), 470 µF/63 V, at both positions. Panasonic lists its body as
16.0 mm diameter × 16.5 mm
length, with 1.41 A RMS rated ripple at 100 kHz and 105 °C. The direct FK
470 µF/50 V alternative `EEVFK1H471M` has the *same* 16.0 × 16.5 mm body;
it therefore solves no placement problem. Its 100 kHz ripple rating is
1.61 A RMS, but that is not a reason by itself to lose voltage margin. The
36 V PSU can be adjusted to 39.6 V, and its overvoltage-shutdown threshold
extends to 48.6 V; 63 V gives useful room for rail peaks while adding no
body size within this direct comparison. These PSU limits are not permission
to operate the TPA3251 near its 50 V PVDD absolute maximum. A genuinely
smaller 36 V bulk part would require a separate exact-part comparison of
capacitance, ripple heating, lifetime, footprint and actual rail peaks.

The bulk terminals need a broad, paired supply/return connection into the
amplifier rail. They need not sit adjacent to the C21/C22/C24/C25 ceramic
pads, whose local U3 loop handles the fast switching current. C20 and C26 connect to the supply and return planes in the released PCB;
physical performance remains a prototype check.
[Panasonic 63 V part](https://industrial.panasonic.com/ww/products/pt/aluminum-cap-smd/models/EEVFK1J471M),
[Panasonic 50 V part](https://industrial.panasonic.com/ww/products/pt/aluminum-cap-smd/models/EEVFK1H471M),
[RSP-200 specification](https://www.meanwell.com/Upload/PDF/RSP-200/RSP-200-spec.pdf).
