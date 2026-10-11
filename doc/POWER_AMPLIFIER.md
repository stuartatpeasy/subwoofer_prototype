# Power amplifier

> **State — current amplifier authority; reviewed 2026-10-11.** Owns the
> TPA3251 stage and RESET topology. Two 36 V-powered TPS3762-Q1 supervisors
> monitoring PVDD and `17V3` are selected. The dedicated 130 kΩ/7.5 kΩ,
> 1% E24 buck SENSE divider is selected; its 12 V LDO headroom claim still
> requires a loaded buck-trough and return-offset check.

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
PVDD/ground connections without a via in the main current path. The exact
placement still depends on the pin map, component heights and plate reliefs.

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

The former mandatory opposite-side capacitor/via arrangement is superseded.
Use the layout review to choose which remaining components belong on each side.

### 1.2 Protection, fault response, and RESET control

Use the TPA3251's internal undervoltage, overcurrent, short-circuit, and thermal
protection. Supply undervoltage may recover automatically. A persistent
overload or overtemperature shutdown may remain latched until the user switches
the complete subwoofer off and on. Do not add an automatic fault-retry circuit.
The partial schematic draws `R13 = 22 kΩ` at `OC_ADJ`; its CB3C threshold
and associated surrounding passives still require final review with the PBTL
implementation.

No normally visible fault LED is required. Provide accessible SMD diagnostic
test points for `FAULT` and `CLIP_OTW`; TP1 and TP2 are now drawn. These signals
are for prototype and service diagnosis rather than normal user indication.
The TPA3251 supplies internal pull-ups to DVDD on both outputs, so separate
pull-up resistors are not required for high-impedance voltage measurements.

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
0.85 = 168 nF` before bias and ageing. Those latter effects together may
reduce the remaining value by no more than 19.7% if the 400 ms minimum is
to be guaranteed. A 220 nF, 50 V X7R is therefore acceptable when its
manufacturer data support that bound at up to 5.5 V on CTR; it is not an
unqualified generic substitution. A 330 nF, ±10%, 50 V X7R offers more
capacitance margin, at the cost of a longer nominal release delay (about
1.22 s rather than 0.81 s). The capacitor value remains provisional until
the chosen X7R construction is checked. A single, provisional 30 kΩ/10 kΩ,
1%-resistor divider from the existing 12 V amplifier rail supplies the shared
RESET pull-up, subject to confirmation of the finished 12 V rail limits and
ground offsets. The 12 V rail supplies a logic level, not a precision sense
threshold. Do not load the TPA3251 DVDD reference as an external supply.

The selected dedicated buck SENSE divider is **130 kΩ** from `17V3` to
SENSE and **7.5 kΩ** from SENSE to the supervisor's local ground. Both are E24,
1% resistors with TCR no worse than 100 ppm/°C. The purpose is to assert RESET
before the NCP1117 12 V amplifier LDO loses its specified input headroom,
while allowing some droop of the 15 V analogue rail during a buck fault. The
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
buck ripple, transients, and sense/return offsets. Onsemi specifies the fixed
12 V NCP1117 output over 0–800 mA with VIN from **13.5 to 20 V**; its output
range over those conditions is 11.76–12.24 V. The lowest calculated falling
threshold is therefore **0.47 V above** its specified minimum input. That is
the entire allowance for instantaneous buck trough below the sensed rail,
trace/return drop, and other unmodelled effects. A divider cannot guarantee
full 12 V regulation unless those effects are bounded below 0.47 V. The
analogue 15 V LDO may already be out of regulation when RESET asserts; no
pre-dropout mute is claimed for that branch. At a fully specified 3 V RMS
input, the OPA167x first-buffer common-mode margin disappears if its supply
falls below approximately 12.5 V; smaller programme signals need less
headroom (see [analogue front end](FRONT_END.md)). Implement the chosen
divider at the amplifier-side `17V3` feed; confirm loaded buck trough,
amplifier-feed and return drops, and start/stop behaviour before claiming
guaranteed 12 V LDO regulation until RESET assertion.

The current partial schematic's MP4541GN feedback divider (`R6 = 180 kΩ`,
`R10 = 11 kΩ`) is not a substitute for this separate SENSE divider. Its FB
node is regulated near 1.0 V; the TPS3762's 0.8 V falling threshold would
represent only `0.8 V × (1 + 180/11) = 13.89 V` nominal at the buck output.
With the same conservative ±0.9% TPS threshold, ±200 nA SENSE current, 1%
resistor initial tolerance and opposed 100 ppm/°C drift over 100 °C used
above, its calculated minimum trip falls to about 13.22 V, below the
NCP1117's 13.5 V specified input minimum even before ripple or feed losses.
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
[TI TPA3251 data sheet](https://www.ti.com/lit/ds/symlink/tpa3251.pdf), and
[Torex XC6701 data sheet](https://product.torexsemi.com/system/files/series/xc6701.pdf),
and [onsemi NCP1117 data sheet](https://www.onsemi.com/download/data-sheet/pdf/ncp1117-d.pdf).

#### 1.2.1 Superseded supervisor analyses (decision record)

The following earlier candidates and calculations are retained for provenance
only. They do not specify the current RESET circuit.

The Nisshinbo `R3160N310A-TR-FE` was evaluated as an alternative to the
TPS3842. Its SOT-23-6 package has 0.95 mm lead pitch
and it can directly sense the 36 V PVDD branch: its falling threshold is 31.0 V
nominal (30.535–31.465 V across −40 to 105 °C), with approximately 32.33 V
nominal rising release from its 4.3% typical hysteresis. Pin 5 (`TAB`) must be
connected to ground as well as pin 6. Its active-low open-drain `DOUT` requires
a pull-up to a suitable low-voltage logic source: the detector output has a
7 V absolute maximum, while the TPA3251 `RESET` input has a 4.2 V absolute
maximum. A 3.3 V pull-up through about 4.7–10 kΩ is a starting point, subject
to confirming the actual logic-rail source and power sequence. A resistor
divider from the 12 V amplifier rail is another possible logic-level source,
but must be checked against both voltage extremes and the TPA3251 RESET
input's leakage. Do not pull either pin directly up to 12 V or 15 V.

The R3160 also requires a capacitor at `CD`. Its specified 10 nF release delay
is 9–27 ms at 25 °C, and the manufacturer's *typical* timing equation is
`t = 1.8 × 10⁶ s/F × CD`. Extrapolating the 10 nF minimum would require at
least 444 nF of **effective** capacitance for 400 ms; the published timing
plot only covers 100 pF–47 nF and does not guarantee that extrapolation or the
full-temperature delay. A local supply bypass is prudent on the switching
36 V branch and is specifically recommended by Nisshinbo if a series input
resistor is used, so a capacitor-count saving is not established. Monitoring
36 V alone cannot assert RESET for a failed or collapsed 17V3 buck or either
downstream LDO while 36 V remains healthy. This was a reason to select the
second TPS3762-Q1. Neither selected monitor independently detects both
downstream LDO faults. [Nisshinbo R3160N data
sheet](https://www.nisshinbo-microdevices.co.jp/en/pdf/datasheet/r3160-ea.pdf)
and [TPA3251 data sheet](https://www.ti.com/lit/ds/symlink/tpa3251.pdf).

The following calculation records the superseded 15 V-buck/two-LM2937
baseline; neither divider seed applies to the revised supply tree. The earlier
182 kΩ over 10.0 kΩ seed was rejected. Its nominal 13.44 V falling
threshold can leave only 0.84 V across a worst-high 12.6 V LM2937 output, even
before PCB distribution loss, while the regulator guarantees dropout only at
50 mA (250 mV maximum) and 500 mA (1 V maximum), not at the 120 mA project
allocation. A lower-resistance 47.0 kΩ over 2.49 kΩ, both 0.1%, was the later
calculation seed:

```text
0.700 V x (1 + 47.0 kΩ / 2.49 kΩ) = 13.91 V nominal
```

This was not a locked divider. Worst-case TPS3842 threshold,
hysteresis and SENSE-current tolerances leave only a small window between
asserting RESET before a pessimistic 1 V LM2937 dropout and reliably releasing
RESET at the STH0548S15's pessimistic minimum output. The 0 Ω default amplifier
prefilter link preserves that window; fitting its reserved 3.3 Ω option would
require this calculation and the startup/down sequence to be repeated.

Primary sources:

- [Texas Instruments TPS3842 data sheet](https://www.ti.com/lit/ds/symlink/tps3842.pdf)
- [Mouser TPS3842A011DRLR listing](https://www.mouser.co.uk/ProductDetail/Texas-Instruments/TPS3842A011DRLR)

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

## 2 Output inductors

Locked part:

- Vishay-Dale `IHLP5050FDER100M5A`
- 10 µH
- four required

Reasons:

- low DCR
- ample current margin
- acceptable bias behaviour
- published L/Q vs frequency
- provisionally suitable for the specified nominal 600 kHz operation; confirm
  loss and temperature in the assembled amplifier

Prototype validation required:

- idle temperature
- sustained-load temperature
- contribution to idle PVDD current

## 3 Output capacitors

> **State:** Provisional capacitor selection, reviewed 2026-10-07. Owns the
> output-filter capacitor choice. The 10 µH inductors are locked in Section 2.
> Next gate: compare effective capacitance and PWM-frequency heating for the
> exact bank at the actual post-filter waveform before PCB implementation.

TI's TPA3251 EVM has four 680 nF film shunt positions with 7 µH inductors.
This project's four 10 µH inductors remain locked, so 680 nF is a reference
target rather than an exact copy of the EVM filter. With an ideal 10 µH and
680 nF, `1/(2π√(LC)) ≈ 61 kHz`; 660 nF gives approximately 62 kHz.
These are unloaded LC frequencies, not a complete prediction of the driven
speaker response. The 100 V X7R bank previously shown here is superseded by
the higher-voltage candidate below: TI's LC-filter guidance calls for a
ceramic rating above 150 V and recommends 250 V for capacitance stability.

**Preferred provisional implementation:** three 220 nF ±10%, 250 V X7R,
soft-termination 1210 MLCCs in parallel at each of the four filter positions
(660 nF nominal per position, 12 parts total). TDK
`C3225X7R2E224K200AE` is a candidate, not yet a locked BOM part. It is
currently listed as in production. A single 680 nF, 250 V X7R 2220 such as
TDK `CGA9N3X7R2E684K230KA` is a simpler comparison candidate; banking does
not itself cure X7R voltage dependence or distortion. The bank divides ripple
current and dissipation among three smaller bodies and permits compact,
symmetric placement, at the cost of more joints and board area. Keep all
three on the same post-inductor node with short, similarly sized connections
to the correct return. Select the side from the completed electrical layout
and machined-plate clearance, rather than the former front-side-only rule.

Each shunt capacitor sees a DC level around half of 36 V at idle, plus audio
and switching ripple; the relevant rating check is its peak terminal voltage,
including overshoot. Do not equate `3 × 220 nF` nameplate with 660 nF in
operation: obtain the manufacturer's exact DC-bias, frequency, and ripple
temperature-rise data, then check the total effective capacitance over the
actual voltage and temperature range. X7R's ±15% temperature classification
does not cover DC-bias loss. Avoid Y5V/Z5U. Check ceramic flex/crack risk in
the final layout and compare loaded response and capacitor temperature during
prototype validation.

Film remains an alternative if a part fits and its **AC current and
voltage at the PWM frequency**, pulse-rise rating, and temperature are
verified. TI favours film for stable capacitance and audio performance; the
EVM's 680 nF, 250 V through-hole film part can now be considered, but is not
automatically approved for this board's waveform, placement, or clearance.
A nominal-value part is not approved merely from its DC voltage rating.

Sources: [TI TPA3251 EVM](https://www.ti.com/lit/ug/slau751/slau751.pdf),
[TI LC filter design guidance](https://www.ti.com/lit/an/slaa701a/slaa701a.pdf),
[TDK 220 nF candidate](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C3225X7R2E224K200AE),
and [TDK 680 nF comparison](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=CGA9N3X7R2E684K230KA).

## 4 Zobel/output damping network

Reference resistor:

- 3.3 Ω

Requirements:

- non-inductive
- SMD preferred; allow through-hole with justified layout and plate clearance
- approximately 1–2 W class
- 1206/2010/2512 depending selected series

Prototype validation:

- temperature at idle
- temperature under sustained high output

## 5 General amplifier-board passives

### 5.1 Resistors

Default:

- SMD preferred; allow through-hole with justified layout and plate clearance
- 1%
- 0805 preferred
- approximately 125 mW minimum

Exceptions:

- precision signal networks
- Zobel/power resistors

### 5.2 Ceramics

Use voltage rating appropriate to node.

Guideline:

- 12 V rails: 16–25 V X7R
- bootstrap: 50–100 V
- PVDD bypass: 50–63 V minimum
- output filter: provisional 250 V X7R bank; see Section 3
- use C0G/NP0 for small precision/HF values where appropriate

Do not blindly use 100 V parts everywhere.

### 5.3 Bulk electrolytics

- SMD aluminium electrolytic
- 63 V preferred for 36 V PVDD
- low ESR
- suitable ripple-current rating
- nominal 470 µF reference positions
