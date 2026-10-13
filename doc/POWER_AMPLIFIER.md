# Power amplifier

> **State — current amplifier authority; reviewed 2026-10-13.** Owns the
> TPA3251 stage and RESET topology. Two 36 V-powered TPS3762-Q1 supervisors
> monitoring PVDD and `17V3` are selected. The dedicated 130 kΩ/7.5 kΩ,
> 1% E24 buck SENSE divider is selected. The now-placed L78M12 12 V regulator
> may sag briefly before the lowest calculated RESET trip; loaded buck-trough,
> return-offset and start/stop checks remain open.
> The two-position Mini-Fit Jr speaker-output pair is selected; placement and
> finished harness routing remain open.

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

The current partial schematic's MP4541GN feedback divider (`R24 = 180 kΩ`,
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

### 1.3 Speaker-output connection

Selected board-to-driver pair (2026-10-12): Molex Mini-Fit Jr `39-28-1023`
two-position, vertical through-hole, tin-plated PCB header and `215326-1023`
two-position female-to-pigtail assembly. The assembly has two factory-terminated
16 AWG (approximately 1.31 mm²), **600 mm** conductors; its housing and
contacts are supplied as part of the assembly, so no separate pins or crimp
tool are required. Connect the two positions to the filtered PBTL speaker
outputs, not to chassis or `GND`. The selected parts have a positive latch and
are distinct in position count from the six-position 36 V input connector.

At the approximately 150 W into 4 Ω output target, speaker current is
`sqrt(150 W / 4 Ω) = 6.12 A RMS`. Molex's two-position, 16 AWG brass-contact
guideline is 9 A per contact, subject to PCB copper, ambient temperature, and
the completed cable termination. Confirm the 600 mm route, pin numbering,
header footprint and clearance, strain support, polarity, and the driver-end
termination during layout and assembly. Recheck Mouser UK availability,
normal-stock status, MOQ, and price before ordering.

Manufacturer sources: [Mini-Fit Jr product specification](https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/productspecificationpdf/555/5556/PS-5556-001-001.pdf),
[header](https://www.molex.com/en-us/products/part-detail/39281023), and
[600 mm pigtail series](https://www.molex.com/en-us/products/series-chart/215326).

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

> **State:** Provisional capacitor selection, reviewed 2026-10-12. Owns the
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

**Drawn provisional prototype choice:** two TDK `B32701P4684K000`
metallised-polypropylene through-hole capacitors, C17 from `SPK+` to GND and
C30 from `SPK-` to GND. Each is 680 nF ±10%, 450 V DC, with a 13 × 6 × 12 mm
maximum body and 10 mm lead pitch (0.6 mm leads). The alternative TDK
`B32702P4684K000` has the same capacitance and voltage, a 18 × 5 × 10.5 mm
body and 15 mm pitch (0.8 mm leads). The smaller-pitch part occupies about
78 mm² of body plan area versus 90 mm² for the 15 mm version, but is 1.5 mm
taller; verify actual plate clearance. Both have a clear manufacturer drawing,
unlike the conflicting distributor pitch for the earlier Panasonic candidate.
The two-capacitor arrangement follows the data-sheet PBTL figure and avoids
the MLCC bank's uncertain DC-bias capacitance. Place each close to its
inductor join with a compact ground return. The 2026-10-11 six-MLCC proposal
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
filter response on the prototype. At the final PCB stage, confirm lead pitch,
orientation, clearance and mechanically secure mounting. The nominal 450 V
rating alone is not the approval criterion.

Sources: [TDK B3270*P data sheet](https://www.tdk-electronics.tdk.com/inf/20/20/ds/mkp_b32701p_b32703p.pdf),
[TDK B32701P4684K000 product page](https://product.tdk.com/en/search/capacitor/film/snubbering_pfc/info?part_no=B32701P4684K000),
[TDK B32702P4684K000 product page](https://product.tdk.com/en/search/capacitor/film/snubbering_pfc/info?part_no=B32702P4684K000),
[Panasonic ECWFD technical data](https://industrial.panasonic.com/cdbs/www-data/pdf/RDI0000/ABD0000COS113.pdf),
[TI TPA3251 data sheet](https://www.ti.com/lit/ds/symlink/tpa3251.pdf), and
[TI LC filter design guidance](https://www.ti.com/lit/an/slaa701a/slaa701a.pdf).

## 4 Zobel/output damping network

**2026-10-12 output-small-capacitor rating review (no part change yet).** In
the current schematic C19/C28 are 1 nF directly from the two post-inductor
speaker-output nodes to GND. C16/C31 are 10 nF in series with R20/R21
(3.3 Ω) from those same nodes to GND. Each capacitor therefore sees its
own output-to-ground voltage, not the full differential speaker voltage.
In an ideal symmetrical 36 V PBTL stage delivering 144 W into 4 Ω, the
differential 24 V RMS output corresponds to about 12 V RMS per side around
an 18 V midpoint: roughly 1–35 V per node. Add switching ripple and any
LC/output-wiring overshoot to that estimate; the actual peak is unverified.
Thus the drawn 250 V ratings are not required by the nominal waveform.
100 V ceramic parts are a reasonable provisional rating with substantial
nominal margin, subject to the final voltage waveform, dielectric/impedance,
and capacitor and resistor temperature. A 50 V 10 nF X7R/3.3 Ω pair is used
in TI's output-network guidance, but choosing 100 V here leaves more room
for post-filter ringing. The TPA3251's 50 V output-pin absolute maximum
does not itself bound overshoot at the post-inductor nodes. Retain the 250 V
parts if they are convenient and their electrical performance and footprints
are suitable; lowering the rating is a cost/availability choice, not an
electrical requirement. The 1 nF parts are small high-frequency shunts:
at 600 kHz their ideal reactance is about 265 Ω versus 0.39 Ω for the
680 nF film shunts. The 10 nF/3.3 Ω branch starts to become resistive near
4.8 MHz, making its high-frequency damping and heating more important than
the nominal voltage rating alone.
[TPA3251 data sheet](https://www.ti.com/lit/ds/symlink/tpa3251.pdf);
[TI output-network guidance](https://e2e.ti.com/support/audio-group/audio/f/audio-forum/492175/question-about-tpa3251d2-diodes-at-output).

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

**2026-10-12 PVDD bypass review (placed choice unqualified).** The saved
schematic now places Murata `GRJ21BC72A105ME11L` 1 µF, 100 V X7S capacitors
C21/C22/C24/C25 on `CAP_0805` patterns. The earlier Würth 0805 part on a
0603 pattern was a real mismatch in a preceding schematic state; that specific
problem is superseded, not an open error in this snapshot. The nearby 470 µF
capacitors supply lower-frequency energy and do not replace short-loop PVDD
bypass. TI calls for a 1 µF ceramic at each PVDD node, close to the IC. The
placed part's nominal 1 µF and 100 V rating do not establish its effective
capacitance or impedance under 36 V bias and switching peaks. At 600 kHz,
ideal 1 µF and 0.5 µF capacitors have approximately 0.27 Ω and 0.53 Ω
reactance respectively; above self-resonance, package and layout inductance
matter increasingly. Check exact-part biased capacitance, impedance over the
switching harmonics, voltage peaks, short-loop placement and rear-plate
clearance before qualifying the placed choice. The RSP-200-36 output is
adjustable to 39.6 V and its overvoltage trip range reaches 48.6 V; the
TPA3251 PVDD pin itself has a 50 V absolute maximum including peaks, so the
capacitor's higher rating does not relax the rail-voltage limit.
[TPA3251 data sheet](https://www.ti.com/lit/ds/symlink/tpa3251.pdf);
[RSP-200 data sheet](https://www.meanwell.com/Upload/PDF/RSP-200/RSP-200-spec.pdf);
[Murata MLCC part list](https://www.murata.com/-/media/webrenewal/tool/library/common-pdf/dynamic-model/component-list-d-mlcc-2504.ashx?cvid=20250523010405000000&la=en).

**2026-10-13 DC-bias evidence and selection (open).** Murata's supplied
simulation for the placed part reports −58.3% capacitance change at 36 V DC,
25 °C and 1 V RMS AC: approximately 0.42 µF per nominal 1 µF part. This is a
modelled operating-point result, not a guaranteed minimum or impedance curve.
The TPA3251 data sheet recommends a 1 µF ceramic close to each PVDD node; its
[EVM BOM](https://www.ti.com/lit/ug/slau751/slau751.pdf) actually fits nominal
1 µF, 50 V X7R 1206 MLCCs (`GRM31MR71H105KA88L`). Thus the reference
implementation strongly indicates that TI's 1 µF is a nominal component value,
not an explicit requirement for 1 µF *after* DC bias. It does not demonstrate
that this different 0805 part at 0.42 µF has the same margin. At 600 kHz the
ideal capacitive reactance for 0.42 µF is about 0.63 Ω, versus 0.27 Ω for
1 µF; real impedance also includes ESR, ESL and the PCB loop.

Consider replacing all four with an exact, layout-compatible 2.2 µF part to
recover margin. A hypothetical 2.2 µF part with the same 58.3% loss would
provide about 0.92 µF at 36 V, but the new part's bias curve must be checked
individually. Extra local capacitance itself has no identified adverse effect
on the TPA3251; the selection gate is adequate effective capacitance and
low impedance near switching frequencies, voltage/ripple suitability, and a
short PVDD-to-ground loop within the rear-plate clearance. Do not change the
placed MPN or footprint on nominal capacitance alone.

**2026-10-13 0805 comparison (selection still open).** Murata's supplied
simulation for 2.2 µF, 100 V, 0805 X7T `GRM21BD72A225KE01L` reports a
−69.6% change at 36 V DC, 25 °C and 1 V RMS AC, and displays 0.707 µF.
Multiplying nominal 2.2 µF by the displayed percentage gives 0.669 µF;
use roughly 0.7 µF for this comparison and check the simulator's reference
value before relying on a more precise figure. Either value is a material
improvement over the placed part's approximately 0.42 µF, but remains below
1 µF in this model. The TI EVM's nominal 1 µF PVDD parts use 1206 packages.
Investigate a 1206 replacement as the next practical option, comparing exact
parts' biased capacitance and impedance at 36 V and checking the larger land
pattern, package height, short bypass loop and rear-plate clearance. Larger
package alone does not guarantee a particular effective capacitance; 1210 is
an option only if a suitable 1206 cannot meet these constraints. Retain
adequate voltage margin for PVDD peaks rather than treating a 50 V rating as
automatically interchangeable with the placed 100 V rating.

**2026-10-13 1206 candidate (not yet placed).** Würth Elektronik
`885012208124` is a 2.2 µF ±10%, 100 V X7R 1206 MLCC, not a nominal 1 µF
part. Its supplied DC-bias plot indicates approximately −48.5% at 36.2 V:
`2.2 µF × 0.515 = 1.13 µF` typical, or approximately `1.02 µF` if −10%
initial tolerance is applied to the same bias ratio. The plotted bias ratio
is not a guaranteed worst-case specification; temperature dependence (X7R
±15% over its rated range) and ageing can reduce the operating value further.
No 1 µF *effective* minimum is established by TI, so the approximately 1 µF
estimate is a useful margin comparison, not an acceptance threshold. The
manufacturer's package dimensions are 3.2 × 1.6 mm with maximum height
1.9 mm. At the proposed, still-unverified 4 mm PCB-back-to-finished-pocket
clearance, this leaves about 2.1 mm before solder height and assembly
tolerances. The CNC pocket makes vertical space a secondary concern; retain
the short supply/return loop and the continuous TPA3251 thermal land.
Qualify the candidate's switching-frequency impedance/ripple behaviour and
the final pad geometry before changing C21/C22/C24/C25 in DipTrace.
[Würth part data sheet](https://www.we-online.com/components/products/datasheet/885012208124.pdf).

### 5.3 Bulk electrolytics

- SMD aluminium electrolytic
- 63 V preferred for 36 V PVDD
- low ESR
- suitable ripple-current rating
- nominal 470 µF reference positions
