# Power and grounding

> **State:** Current authority for mains entry, protective earth, DC
> distribution, and grounding. The RSP-200-36, inlet, fuse, M4 protective-earth
> topology, and unfiltered-inlet decision remain locked. The auxiliary supply
> selection is final for the first prototype: the canonical schematic uses an
> MP4541GN 36 V-to-approximately-17.36 V buck feeding an
> `XC6701DF02FR-G` 15 V analogue LDO and an `L78M12ABDT-TR` 12 V amplifier
> regulator. The 25 October PCB snapshot
> carries the intended DPAK pad nets and a four-layer local GND spreader;
> its land dimensions, loaded thermal result, and physical return paths still
> need checking as described in Section 1 and the
> [current PCB review](PCB_LAYOUT.md). The canonical schematic
> now uses one `GND` net with no R1/R2 links. Analogue, buck, and amplifier
> return-current regions are now joined across U3 in the later 25 October
> routed PCB. The six-position Mini-Fit Jr 36 V board-entry pair is selected;
> its PSU wiring topology, harness implementation, and footprint fit remain
> open checks.
> Do not redesign the selected auxiliary supply unless measurements of a built
> prototype justify a change. This selection is not a claim that the rails,
> thermal behaviour, or final fabrication outputs have been qualified. The two-
> supervisor RESET topology senses 36 V and `17V3` with a selected dedicated
> divider; its headroom claim depends on the loaded buck trough and 12 V LDO
> input in [Power amplifier](POWER_AMPLIFIER.md).
> Earlier STH0548S15/LM2937 selections and their calculations below are
> superseded context, not current implementation instructions. Last reviewed:
> 2026-10-26.

## 1 Power architecture

```text
230 V AC
  |
36 V SMPS
  |
  +--> TPA3251 PVDD
  |
  +--> MP4541GN ~17.36 V buck (selected for first prototype)
         |
         +--> L78M12ABDT-TR 12 V regulator (selected)
         |      |
         |      +--> TPA3251 VDD/GVDD (loaded rail unverified)
         |
         +--> XC6701DF02FR-G 15 V analogue LDO (selected)
                |
                +--> analogue front end
                |
                +--> buffered VMID ≈ 7.5 V
```

Requirements:

- keep the amplifier and analogue supply loads in their appropriate physical
  regions, with locally controlled return paths
- check the selected parts' physical footprints, local return paths, and final
  fabrication outputs before ordering; measure loaded rail levels, ripple,
  heat, and RESET sequencing on the built prototype, including the lowest
  `17V3` trough against the buck supervisor's release threshold

**26 October 2026 selection decision.** The MP4541GN and its present
feedback/output-capacitor implementation, U6 15 V analogue branch, and U9
12 V amplifier branch are final for this prototype. Earlier candidate and
alternative-setpoint calculations below are retained as dated analysis; they
do not authorise a pre-build redesign. The fourth buck-output capacitor
position discussed below is an option only if prototype measurements show a
material need. Correctness checks for the selected PCB footprints, pin nets,
local copper and manufacturing files still apply; loaded voltage and thermal
performance must be measured after assembly.

### 1.1 MP4541GN candidate schematic review (2026-10-06; references refreshed 2026-10-12)

The canonical partial schematic uses `R24 = 180 kΩ` and `R28 = 11 kΩ` at FB,
giving a nominal `1 V × (1 + 180/11) ≈ 17.36 V` output. `R26 = 47 kΩ` sets
approximately 674 kHz in the manufacturer's nominal frequency equation.
With 36 V input and `L5 = 47 µH`, ideal nominal inductor ripple is about
0.28 A peak-to-peak. The Bourns `SRN8040-470M` has 1.4 A rated RMS current,
1.5 A saturation current, and 0.19 Ω maximum DCR; the current rating is
plausible for the auxiliary load, subject to its completed load budget.

**2026-10-13 setpoint review — 18 V remains a candidate, not a schematic
change.** Changing only R28 from 11 kΩ to 10.6 kΩ with R24 = 180 kΩ would
give `1 V × (1 + 180/10.6) ≈ 17.98 V` nominal. With the MP4541's
0.985 V minimum feedback reference and opposed 1% divider tolerances, the
calculated lowest static output would rise from about 16.78 V to 17.38 V,
before loaded ripple, transient sag, feed drop or return offset. The maximum
static output would be about 18.60 V, within the L78M12A's 27 V specified
input range and the XC6701's 28 V operating range. At the provisional
120 mA amplifier load, U9's pass loss plus typical 6 mA ground-current loss
would rise from about 0.75 W to 0.83 W: approximately 0.08 W more, or 8 °C
more rise on ST's 100 °C/W reference thermal arrangement. The 15 V LDO's
pass loss would rise by 0.013 W at 20 mA or 0.064 W at 100 mA.

Raising the buck setpoint alone does not change the existing supervisor's
13.97 V lowest calculated falling threshold, which remains below the L78M12A's
14.5 V specified input minimum. It would increase the calculated static
healthy-rail margin above the highest RESET release threshold from about
1.00 V to 1.60 V. A separate **unselected** 150 kΩ/8.2 kΩ, 1% supervisor
divider would instead move the nominal falling trip to 15.43 V, with
approximately 14.70–16.21 V falling corners and 16.61 V maximum rising
release under the same 2% resistor, ±0.9% threshold, ±200 nA sense-current
and 2.5% hysteresis assumptions used in [Power amplifier](POWER_AMPLIFIER.md).
At the 17.38 V calculated lowest healthy buck output, that leaves only
0.77 V before loaded ripple and feed/return offsets; its lowest falling
trip is just 0.20 V above the L78M12A's specified input minimum. It therefore
does not establish guaranteed pre-dropout RESET assertion. Retain the drawn
17.36 V feedback and 130 kΩ/7.5 kΩ supervisor divider for now. Reconsider
18 V after the loaded buck trough, analogue load/headroom, and U9 temperature
are known; do not change either divider to claim a protection guarantee from
nominal values alone.

The revised canonical XML shows a nine-pad SOIC-8EP pattern for `U5` and
1210 patterns for `C42`–`C44`. U5 has symbol pad 9 assigned to `GND`.
Verify the actual land dimensions against the chosen parts and the resulting
PCB netlist before layout.

The current XML assigns `C38`–`C40` (36 V input capacitors), `C42`–`C44`
(buck output capacitors), `C46` (U5 VCC decoupling), `R26` (FREQ), `R23/R27` (EN
divider), `R24/R28` (FB divider), and U5 GND pin 7 and exposed pad 9 to `GND`.
The 15 V LDO U6 and its local bypass capacitors also return to `GND`.
Connect R28 to a quiet local GND sense point near the output-capacitor return, not
through the high-current switching return. Keep the VIN/input-capacitor and
SW/inductor/output-capacitor current loops compact; a new net name alone does
not control their physical paths. Lay out the buck-to-analogue return region so
the buck's pulsed current does not flow through quiet analogue copper.
The TPA3251's PVDD and 12 V VDD/GVDD returns use one local amplifier ground.
The 12 V branch takes its input from the buck's `17V3` net and returns it to
the local amplifier-side `GND` region. The canonical schematic now uses a
single `GND` net; unpopulated R1/R2 placeholders have been removed. Keep the
amplifier return out of quiet analogue copper. Final 12 V
supply placement and return routing remain open.

The three output capacitors total 30 µF by nameplate value. A user-supplied
Samsung simulator plot for the placed `CL32A106KBJNNNE` reports a typical
−31.92% capacitance change at 17.592 V, 25 °C, 1 kHz and 1 V RMS. Applying
that factor to all three gives approximately 20.4 µF at that condition, before
initial tolerance, temperature and ageing. This is simulation data, not a
guaranteed minimum or a measurement of the assembled bank. With the nominal
0.28 A peak-to-peak inductor ripple and 674 kHz switching estimate above,
`ΔV ≈ ΔI/(8 f C)` gives about 2.5 mV capacitive ripple at 20.4 µF, versus
1.7 mV at an ideal 30 µF; ESR and pulse-skip behaviour are excluded. A fourth
identical part would give about 27.2 µF at the same bias and reduce this
idealised ripple to 1.9 mV. On 2026-10-13 the user chose to add a fourth
identical schematic position as an unpopulated option; this saved XML snapshot
still has only C42–C44. Populate the fourth only if loaded ripple, start-up or
meaningful load transients show a material need. The output net remains named
`17V3`. The 12 V LDO is sourced from this rail; at the previous 120 mA
amplifier-rail allocation its pass loss is approximately
`(17.36 V - 12 V) × 0.12 A ≈ 0.64 W`, before ground-current loss. The MP4541
may enter pulse-skip operation at light load, so assess rail ripple and
analogue noise at the actual idle and operating loads. These are design
checks, not claims of measured faults.

Manufacturer sources: [MP4541GN data sheet](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP4541GN/document_id/9688/),
[MPS exposed-pad guidance](https://forum.monolithicpower.com/t/mp4541-exposed-pad-connection/2823/3),
[SRN8040 data sheet](https://www.bourns.com/docs/product-datasheets/srn8040.pdf),
and [Samsung capacitor identity](https://product.samsungsem.com/mlcc/CL32A106KBJNNN.do).

### 1.2 12 V and 15 V linear-regulator branches (reviewed 2026-10-13)

The saved schematic now places `U9 = L78M12ABDT-TR`: VIN/pin 1 is on
`17V3`, GND/pin 2 and DPAK tab pad 4 are on `GND`, and VOUT/pin 3 is on
`12VAMP`. The 24 October saved PCB carries these pad nets, but verify the land
pattern dimensions and completed thermal copper before layout release. The
former `U4 = NCP1117ST12T3G` and its SOT-223
output-tab mapping, 20 V input limit, and output-capacitor ESR requirement are
superseded by this substitution.

The `XC6701DF02FR-G` 15 V output may be as high as 15.30 V. Torex's
25 °C voltage chart specifies maximum dropout of 0.17 V at 20 mA and
0.85 V at 100 mA for this output version. At the illustrative 16.78 V
minimum buck level, remaining margin is about 1.31 V at 20 mA or
0.63 V at 100 mA, before rail ripple and return-path drops. Establish the
actual analogue load and use its loaded headroom and thermal conditions;
the 20 mA case is promising, while 100 mA leaves little room.
Torex defines the published dropout point at a 2% output fall, so these
25 °C figures do not establish the onset of loss of regulation. The selected
buck supervisor threshold in [Power amplifier](POWER_AMPLIFIER.md) permits
analogue-rail droop during a buck fault; it does not guarantee RESET before
this 15 V LDO leaves regulation.

The saved U6 `XC6701DF02FR-G` symbol now maps VIN/pad 3 to `17V3`, VSS/pad 2
and tab pad 4 to `GND`, and VOUT/pad 1 to `15VA`. Torex identifies the SOT-223
tab as VSS. Verify the transferred PCB netlist and provide suitable thermal
copper before layout release; this closes the earlier missing schematic tab
mapping.

The saved XML now shows `C36 = Murata GRJ21BC72A105ME11L`, a nominal 1 µF,
100 V X7S ceramic from U9's `17V3` input to `GND`, and `C37 = 100 nF` from
its `12VAMP` output to `GND`. The user reports that C36 retains more than
0.33 µF at 17.3 V DC bias; this closes the input-bypass *value* concern on
that supplied part data, while short local placement remains a PCB check.
ST recommends at least 0.33 µF low-impedance input bypass near the regulator
when output capacitance is large. At the output, C37 is paralleled with
`C8 = 470 µF` electrolytic and `C9 = 100 nF`; ST's example uses 0.1 µF
output bypass. ST states that
the L78M does not need an output capacitor for stability, so the former NCP1117
output-bank ESR-floor issue is closed by the regulator change.

The saved C8 is Panasonic FK `EEV-FK1J471M` (catalogue
`EEVFK1J471M`), 470 µF/63 V, in a 16.0 mm
diameter × 16.5 mm body. For this 12 V rail, Panasonic FK
`EEEFK1E471GP` is a **preferred size-reduction candidate**, not yet a
selected substitution: 470 µF/25 V, 10.0 × 10.2 mm body, 0.85 A RMS rated
ripple at 100 kHz and 105 °C, and 5,000 h specified endurance. The present
63 V part is rated 1.41 A RMS at 100 kHz and 105 °C. The 25 V rating leaves
12.5 V above the regulator's 12.5 V high specified output; it also exceeds
the nominal 17V3 input if a regulator fault passed that rail through. A
16 V/470 µF FK part exists in an 8.0 × 10.5 mm body, but leaves only 3.5 V
above the specified 12.5 V output and is below the nominal 17V3 input, so
25 V is the more comfortable candidate. Check the candidate's exact pad
pattern, polarity, local placement and capacitor ripple-current demand before
changing C8 in DipTrace. [Panasonic 25 V part](https://industrial.panasonic.com/ww/products/pt/aluminum-cap-smd/models/EEEFK1E471GP);
[Panasonic 16 V comparison](https://industrial.panasonic.com/ww/products/pt/aluminum-cap-smd/models/EEEFK1C471V);
[Panasonic current 63 V part](https://industrial.panasonic.com/ww/products/pt/aluminum-cap-smd/models/EEVFK1J471M).

ST specifies 11.5–12.5 V at 5–350 mA and 14.5–27 V input across its AB operating
temperature range; this fits the TPA3251's 10.8–13.2 V VDD/GVDD operating
range under those stated conditions. Its 35 V absolute input limit offers
more transient headroom than the former NCP1117's 20 V limit, but is not a
continuous operating target. Place C36 close to U9's input and ground pins.
At 17.36 V input and the
provisional 120 mA load, `(17.36 − 12) V × 0.12 A ≈ 0.64 W` heats the pass
element, while ST's
typical 6 mA ground current adds about 0.10 W of regulator dissipation. Its
100 °C/W DPAK junction-to-ambient figure would imply roughly 75 °C rise on
the reference arrangement; actual PCB copper, enclosure ambient and measured
load must be checked before approving the placed part.

**24 October 2026 U9 PCB thermal checkpoint (provisional).** The saved
`diptrace/main_board.dipxml` (SHA-256
`45FE65236B2B1EA68EB9F5CC34BEE44550DD954FE301C733DB515B7A8B11C152`,
`DipTrace-PCB` 5.3.5.1, mm) places U9 on Top at (27.2, 85.5) mm. Its placed
footprint has physical pads 1=`17V3`, 3=`12VAMP`, and tab 4=`GND`; the omitted
lead 2 is the DPAK ground/tab connection, not an output-tab mapping. The Top
`GND` pour ID 34 reaches the tab and has a 499 mm² outline area before pad,
hole and clearance cut-outs. Its useful thermal area is therefore smaller
than 499 mm². The nearest saved `GND` vias are about 5.5–7.8 mm from the tab
centre; there are none immediately beside it. The present Inner 2 `GND` pour ends
around x=22.2 mm, to the left of the tab, while Inner 1 and Bottom have no
local `GND` pour under U9. The planned four-layer heat-spreading structure is
not yet implemented. Adjacent `17V3` and `12VAMP` copper is electrically
separate and should not be counted as a directly joined tab heat spreader.
The screenshots agree with this saved geometry; neither
is an assembled thermal result or current DipTrace connectivity/DRC pass.

**25 October 2026 superseding geometry checkpoint.** The
[current routed-board review](PCB_LAYOUT.md) identifies a roughly 544 mm² Top
GND-pour outline joined to U9's tab, further local GND fills on Inner 1,
Inner 2 and Bottom, and 19 GND vias within 10 mm of the tab centre. The
24 October statement that the planned four-layer structure was absent remains
a dated description of that earlier file. The present geometry now implements
the intended spreader, subject to connectivity/DRC and a temperature check at
the actual continuous load. The dissipation model below remains provisional.

For a linear regulator, input power is `VIN × (IOUT + IQ)` and delivered
output power is `VOUT × IOUT`, so
`PD = (VIN − VOUT) × IOUT + VIN × IQ`. With the provisional 120 mA load,
17.36 V input, 12 V output, and ST's *typical* 6 mA ground current, this is
`(5.36 V × 0.120 A) + (17.36 V × 0.006 A) = 0.747 W`. At the unselected 18 V
buck setting it would be 0.828 W. At 17.36 V, 200 mA would dissipate about
1.18 W. These are operating-point estimates, not maximum device losses: the
12 V load, input voltage under load, ground current and local air temperature
are unmeasured. ST specifies 125 °C maximum operating junction temperature
for the AB grade, 8 K/W DPAK junction-to-case and 100 K/W junction-to-ambient
in its thermal table; the latter is not a prediction for this PCB. With
illustrative 50 °C local air,
0.747 W at 100 K/W would put the junction near 125 °C; 70 K/W would put it
near 102 °C. At 1.18 W, even 70 K/W would put it near 133 °C. This makes
the actual continuous 12 V current as important as the copper outline.

ST's [DPAK copper-area illustration](https://www.st.com/resource/en/application_note/an1703-guidelines-for-using-sts-mosfet-smd-packages-stmicroelectronics.pdf)
shows roughly 62 K/W at a 45 mm² recommended pad and about 50 K/W at
600 mm² on its 70 µm copper test board. It uses a MOSFET and different board
conditions, so these figures are **scale guidance**, not U9's thermal
resistance. The existing approximately 5 cm² Top outline is already in the
right area range for a 120 mA first layout; do not assert that it is inadequate
from appearance alone. Preserve a broad, directly joined tab-to-Top-GND
connection. Add connected `GND` spreading copper on the other layers where it
does not cut the buck's 36 V or 17V3 distribution, amplifier return, or quiet
analogue paths. Begin with roughly 8–12 well-spaced through-vias immediately
around the tab and its copper extension (the present style is 0.45 mm land /
0.20 mm hole); inspect the filled clearances and add more only where useful.
Keep ordinary open vias out of the soldered tab pad to avoid solder wicking,
unless a filled/capped via-in-pad process is deliberately selected. A target
of roughly 5–10 cm² of *well-connected local spreader*, counting overlapping
layers as coupled paths rather than independent free-air surfaces, is a
layout starting point, not a guaranteed minimum. Measure U9 tab/copper and
local air temperature at the actual continuous 12 V load during prototype
thermal testing; if the load approaches 200 mA or temperature margin is poor,
revisit the regulator or heat path before relying on extra distant copper.
As a first interpretation of a tab/case measurement, add approximately
`8 K/W × PD` (about 6 K at 0.747 W) to estimate junction temperature; the
case-temperature measurement point and contact must be credible for this
estimate.

The selected buck supervisor's `17V3` falling threshold is 14.67 V nominal
and about 13.97 V at the calculated low corner. The L78M12A is specified
to regulate down to 14.5 V input at 5–350 mA; its 2 V dropout is *typical*
at 25 °C and the 350 mA table condition, not a guaranteed maximum at this
board's load and temperature. Thus the lowest supervisor trip can fall
0.53 V below the regulator's specified input range, and a brief 12 V rail
sag before RESET assertion cannot be excluded. At 13.97 V input, the 12 V
rail would have to fall by more than 1.2 V, equivalent to an input/output
difference greater than 3.17 V, to cross the TPA3251's 10.8 V recommended
minimum. This is unlikely at the provisional 120 mA load but is not a
guarantee from ST's data. A short dip may affect audio or invoke the
TPA3251's internal undervoltage protection; it is not, by itself, an
expected damage mechanism. During a rapid input collapse, the VOUT-to-VIN
diode can discharge the large output bank into `17V3`, so C8 must not be
counted as guaranteed hold-up. RESET-before-any-12 V-sag is no longer a design
claim; check the actual
`17V3`, `12VAMP` and RESET waveforms and the audible start/stop behaviour
on the prototype.

The saved `D1 = Yageo S1B` has its anode on `12VAMP` and cathode on `17V3`.
C8 alone stores `½ × 470 µF × (12 V)² ≈ 34 mJ`. If the 17 V input is suddenly
shorted or collapses faster than the 12 V output, D1 offers that charge an
external path around U9. The L78M data sheet does not call for this diode or
specify reverse-current tolerance; ST's related L78 data sheet explicitly
recommends an output-to-input diode for high-capacitance loads under an input
short. Retain D1 as proportionate protection, and verify its polarity, pattern,
and pulse path in the PCB. D1 also prevents counting C8 as assured 12 V
hold-up during an input fault.

U6's saved `15VA` output capacitors C48/C54/C55 total 1.2 µF nominal,
storing `½ × 1.2 µF × (15 V)² ≈ 0.135 mJ` at that capacitance.
Torex's XC6701D absolute maximum limits VOUT to VIN + 0.3 V; it does not
specify reverse-current tolerance or request an external diode. The `17V3`
rail has a much larger local capacitor bank than `15VA`, and the 15 V load
also drains the small output bank, making output-above-input during ordinary
shutdown unlikely. There is no compelling reason to add a second diode now.
A standard silicon rectifier would not guarantee the +0.3 V limit
on a sudden input short. Reassess a low-forward-voltage external bypass if
15VA gains substantial stored capacitance or an independently powered load
that can hold it up while `17V3` falls.

Manufacturer sources: [onsemi NCP1117 data sheet](https://www.onsemi.com/download/data-sheet/pdf/ncp1117-d.pdf),
[Torex XC6701 data sheet](https://product.torexsemi.com/system/files/series/xc6701.pdf),
[ST L78M data sheet](https://www.st.com/resource/en/datasheet/l78m.pdf),
[ST L78 data sheet](https://www.st.com/resource/en/datasheet/CD00000444.pdf),
and [TI TPA3251 data sheet](https://www.ti.com/lit/ds/symlink/tpa3251.pdf).

### 1.3 Locked 36 V supply: Mean Well RSP-200-36

Use the Mean Well `RSP-200-36`. Manufacturer data current at the review date:

| Characteristic | RSP-200-36 value | Design consequence |
| --- | ---: | --- |
| rated output | 36 V, 5.56 A, 200.16 W | continuous system input-power ceiling |
| output adjustment | 32.4–39.6 V | set to 36 V; adjustment is not design margin |
| voltage tolerance | ±1.0% | includes setup, line, and load regulation |
| line / load regulation | ±0.2% / ±0.5% | verify the as-built 36 V rail under load |
| ripple and noise | 220 mV peak-to-peak maximum | manufacturer method uses 20 MHz bandwidth, 300 mm twisted pair, and 0.1 µF + 47 µF termination |
| input | 88–264 V AC, 47–63 Hz | universal input; no voltage selector |
| AC current | 1.3 A typical at 230 V AC | basis for the 2 A time-lag appliance fuse |
| inrush | 40 A typical at 230 V AC | requires a time-lag fuse and cold-start testing |
| power factor | greater than 0.95 typical at 230 V AC/full load | active PFC is internal |
| efficiency | 90% typical | about 22 W supply loss at 200 W output |
| leakage current | less than 1 mA at 240 V AC | component value; final equipment still requires verification |
| setup / rise time | 1500 ms / 50 ms at 230 V AC/full load | amplifier mute/enable design must tolerate this |
| hold-up time | 8 ms typical at full load | do not assume ride-through beyond this |

The 200.16 W rating is adequate for the 140–150 W amplifier target. As a
conservative illustration, 150 W audio output at 90% amplifier efficiency
requires

```text
150 W / 0.90 = 167 W DC
```

before auxiliary loads, leaving approximately 33 W within the PSU's continuous
rating. This is a sizing check, not a measured amplifier-efficiency result.

Protection behaviour:

- overload at 105–135% of rated output power: hiccup mode, automatic recovery
  after the fault is removed;
- overvoltage at 41.4–48.6 V: output shutdown, requiring input power cycling to
  recover; and
- overtemperature: output shutdown with automatic recovery after cooling.

Do not treat the overload range as a guaranteed peak-power rating.

Cooling and environment:

- fanless free-air convection;
- specified working range: -30 to +70 °C, subject to the manufacturer's
  derating curve;
- full rated load is available to 45 °C in the documented horizontal
  orientation, followed by linear derating to approximately 50% at 70 °C;
- do not obstruct the perforations; the final enclosed installation must prove
  its own internal ambient and PSU temperature; and
- above 2000 m altitude, reduce maximum ambient by 3.5 °C per 1000 m.

Mechanical and terminal data:

- 215 × 115 × 30 mm, manufacturer tolerance ±1 mm, mass 0.72 kg;
- four M4 bottom mounting holes, maximum screw penetration 3 mm;
- four M4 side mounting holes, maximum screw penetration 5 mm;
- terminal assignment: 1 `AC/L`, 2 `AC/N`, 3 `FG`, 4–6 `-V`, 7–9 `+V`;
- M3.5 terminal screws, tightened to the Mean Well installation-manual value
  of 8–10 kgf·cm (approximately 0.78–0.98 N·m); and
- exact placement and convection clearance remain part of the mechanical
  layout, using the manufacturer's drawing rather than re-created dimensions.

Published approvals and EMC claims:

- UL 62368-1 and TÜV BS EN/EN 62368-1;
- DEKRA EN 61558-1 and EN/IEC 61558-2-16 for the 36 V model;
- EAC TP TC 004, CCC GB 4943.1, BSMI CNS 15598-1, AS/NZS 60950.1, and the
  applicable BIS approval listed by Mean Well;
- emissions to BS EN/EN 55032 Class B and BS EN/EN 61000-3-2/-3; and
- immunity to BS EN/EN 61000-4-2, -3, -4, -5, -6, -8, and -11 and EN 55035
  light-industrial level.

These are component approvals/claims, not certification of the completed
subwoofer. Mean Well's EMC result used a particular metal test plate and the
manufacturer explicitly requires the final equipment to be re-confirmed.

Primary sources:

- [Mean Well RSP-200 series specification](https://www.meanwell.com/Upload/PDF/RSP-200/RSP-200-spec.pdf)
- [Mean Well enclosed-supply installation manual](https://www.meanwell.com/Upload/PDF/Enclosed_Type_EN.pdf)
- [Mean Well RSP-200 approvals and declarations](https://www.meanwell.com/webaPP/Product/search.aspx?pdf=UlNQLTIwMCwzMjAtVUstZGVjLnBkZg%3D%3D&prod=RSP-200)

### 1.4 Mains inlet, switching, and appliance fuse

Locked inlet assembly:

- Schurter `DD11.0111.1111`, Mouser `693-DD11.0111.1111`;
- IEC C14 Class-I inlet, 10 A at 250 V AC;
- front screw mounting, suitable for panels up to 8 mm thick and therefore for
  the 6 mm aluminium plate;
- non-illuminated two-pole line switch;
- one-pole 5 × 20 mm fuseholder in line only;
- 4.8 × 0.8 mm quick-connect terminals;
- V-Lock provision and rear insulation cover; and
- use the supplier drawing/CAD as the cut-out authority. The present drawing
  gives a 47.1 × 28.1 mm nominal opening, 56 mm mounting-hole centres, and
  3.4 mm mounting holes.

Required separate fuse drawer:

- Schurter `4301.1407`, Mouser `693-4301.1407`;
- extra-safe, one-pole drawer for a 5 × 20 mm fuse.

Initial locked appliance fuse:

- Schurter SPT `0001.2507`;
- `T2AH250V`: 2 A, 250 V AC, time-lag, ceramic, 5 × 20 mm;
- 1.5 kA AC breaking capacity and typical melting I²t of 9.2 A²s; and
- verify repeated cold starts at the highest expected internal ambient. If it
  nuisance-opens, do not increase the rating until the measured startup event,
  fuse time-current curve, and wiring protection have been reviewed.

Mean Well includes an internal line fuse, but it is a component-protection
device. The accessible inlet fuse is retained to protect the appliance mains
wiring and to provide serviceable, installation-specific coordination.

Wire the inlet as follows:

```text
C14 L --> T2A fuse --> switch pole 1 --> RSP terminal 1 AC/L
C14 N -------------> switch pole 2 --> RSP terminal 2 AC/N
C14 PE --> short PE lead --> dedicated M4 plate stud
                                  |
                                  +--> aluminium plate
                                  |
                                  +--> separate PE lead --> RSP terminal 3 FG
```

The switch must open line and neutral. Protective earth is never switched or
fused.

No additional mains-input filter is fitted for Rev A. The RSP-200 already has
an internal EMI filter and PFC and carries a component-level Class-B emissions
claim. A second filter would add size, cost and earth-leakage capacitance
without guaranteeing system compliance. Reopen this decision only if final
equipment conducted/radiated-emissions or audible-noise testing shows a need.

Primary component sources:

- [Schurter DD11 data](https://www.schurter.com/en/datasheet/typ_dd11.pdf)
- [Mouser DD11.0111.1111 listing](https://www.mouser.co.uk/en/ProductDetail/Schurter/DD11.0111.1111)
- [Schurter fuse-drawer data](https://www.schurter.com/en/datasheet/typ_fusedrawer_2.pdf)
- [Schurter SPT fuse data](https://www.schurter.com/en/datasheet/typ_spt_5x20.pdf)

### 1.5 Internal mains wiring and access assumptions

- Use harmonised stranded copper appliance wire, 0.75 mm² minimum, rated
  300/500 V or better and for the expected internal temperature: brown line,
  blue neutral, green/yellow protective earth.
- Use correctly tooled, fully insulated 4.8 × 0.8 mm receptacles at the inlet.
  One conductor per receptacle; do not stack receptacles or improvise a
  two-wire crimp on the PE blade.
- Use crimped ferrules or terminals compatible with the RSP terminal block.
  No loose strands may enter a screw terminal.
- Keep the mains loom short, supported near each termination, protected from
  sharp plate edges, and physically segregated from DC, loudspeaker, and
  signal wiring. Cross other wiring only where unavoidable.
- Fit the inlet's rear cover and a Mean Well `TBC-09` cover to the RSP-200
  terminal strip. These guards must prevent finger, tool, loose-wire, and
  displaced-component contact with mains terminals.
- Removing the rear plate is a service operation: disconnect the IEC lead
  first. No mains terminals are user-accessible in normal use.
- Provide enough PE slack that protective earth is the last conductor stressed
  if the rear assembly is displaced.

## 2 Grounding and earthing

### 2.1 Objectives

- Maintain Class-I protective earthing.
- Keep Class-D switching currents out of analogue return paths.
- Avoid unintended chassis/signal-ground loops.
- Use deliberate branch returns rather than arbitrary shared wiring.
- Use solid local ground planes on each PCB; do not implement literal long-wire star grounding at high frequencies.

---

## 3 Protective earth and chassis

The exposed aluminium rear panel is protective-earthed.

```text
IEC PE
  |
short dedicated PE conductor
  |
M4 protective-earth stud --> aluminium rear plate
  |
separate dedicated PE conductor
  |
Mean Well terminal 3 FG / chassis
```

Requirements:

- Use a dedicated M4 machine screw through the 6 mm plate, with its threaded
  end inboard. M3 is electrically adequate but is not the selected mechanical
  baseline.
- The stud must be mechanically independent of PCB, PSU, and plate mounting.
- On the bare inner plate face use a serrated/internal-tooth washer and first
  nut to clamp the stud permanently. Fit the two PE ring terminals above that
  fixed joint, followed by a flat washer and an all-metal prevailing-torque
  locknut. Servicing a conductor must not loosen the stud-to-plate bond.
- Remove paint/coating at PE contact point.
- Clean/abrade the contact area immediately before assembly; after tightening,
  protect around but never between the conductive interfaces against
  corrosion.
- Use M4 ring terminals crimped with their specified tooling to 0.75 mm²
  green/yellow conductors.
- Mark the stud with the protective-earth symbol.
- Do not rely on heatsink contact, PCB screws, RCA connectors, or PSU mounting screws as the sole protective-earth path.

---

## 4 36 V distribution

The existing wiring proposal uses the Mean Well PSU output as the primary DC
branching point.

**Later 25 October PCB review:** The proposal below records the previous
dedicated-branch wiring plan, not the present saved copper. The current PCB
joins all three J6 `36V` pads into a broad Inner 1 feed and all three J6
`GND` pads into common GND; no ratline is visible. The six selected conductors
can therefore form three closely paired parallel feed/return paths between
the common PSU rails and J6, with the buck branch taken locally from the board
entry. This removes the former mismatch in which a buck-labelled return could
carry amplifier current without a matching positive conductor. Actual harness
pairing, PSU terminations, connector/copper capacity and temperature derating
still need verification. Parallel cables need not share current equally.
The [current PCB review](PCB_LAYOUT.md#3-engineering-interpretation) gives the
electrical interpretation. Preserve the contiguous U3 GND plane.

```text
Mean Well +V (three common terminals)
  |-- two proposed conductors --> TPA3251 amplifier-domain power entry
  +-- one proposed conductor  --> 36 V -> 17V3 buck converter

Mean Well -V (three common terminals)
  |-- two proposed conductors --> TPA3251 power-ground region
  +-- one proposed conductor  --> buck-converter input return
```

Requirements:

- Keep the buck's fast input-current loop local to its capacitors and avoid
  significant shared feed/return impedance between that loop and U3's PVDD
  capacitors. The board now joins the return regions; do not assume the PSU
  terminals are their only connection. Keep each fitted outgoing feed close
  to its corresponding return and review parallel cable paths.
- Use suitably heavy conductors for the amplifier branch.
- TPA3251 PCB must use a compact, low-impedance ground plane rather than star traces.

Selected 36 V board-entry pair (2026-10-12): Molex Mini-Fit Jr
`39-28-1063` six-position, vertical through-hole, tin-plated PCB header and
`215326-1063` six-position female-to-pigtail assembly. The latter has six
factory-terminated 16 AWG (approximately 1.31 mm²), 600 mm conductors and
requires no user crimping or separately purchased contacts. The original
assignment was two feed/return pairs to the amplifier and one to the buck;
the current PCB instead joins all three pairs at J6 and takes the buck branch
locally. The three PSU `+V` screws are common, as are the three `-V` screws. Molex's
Mini-Fit Jr [product specification](https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/productspecificationpdf/555/5556/PS-5556-001-001.pdf)
gives a **7 A per-contact guideline** for a six-position assembly with 16 AWG
brass contacts (correcting the earlier 8 A figure), subject to board copper
and ambient temperature derating. This exceeds the PSU's 5.56 A rated output
under the specification's reference conditions, but a one-pair alternative
would need a board-entry and enclosure-temperature check. The three-pair
arrangement must not rely on equal sharing. Confirm the exact pin numbering,
PCB footprint,
connector clearance, cable reach, strain support, and polarity marking during
layout. Recheck Mouser UK price, stock, normal-stock status, and MOQ for both
parts before ordering; the six-position pigtail's UK listing was not confirmed
at selection.

The earlier four-contact SMT Micro-Fit+ candidate (`218216-0400` with
`226263-1043`) is superseded by this through-hole, six-conductor selection.

Manufacturer sources: [Mini-Fit Jr product specification](https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/productspecificationpdf/555/5556/PS-5556-001-001.pdf),
[header](https://www.molex.com/en-us/products/part-detail/39281063), and
[pigtail series](https://www.molex.com/en-us/products/series-chart/215326).

---

## 5 Superseded auxiliary-rail design and grounding

Sections 5.1 and 5.2 retain the earlier 15 V converter and two 12 V
post-regulator analysis for provenance. They do not define the current power
tree, bill of materials, or grounding junctions. The current design uses one
electrical GND net with physically controlled return regions; its detailed
branch routing awaits the PCB layout.

The 15 V buck output is the branching/reference point for the two 12 V rails.

```text
15 V buck
  |
  +--> 12V_AMP LDO
  |      |
  |      +--> TPA3251 VDD/GVDD
  |
  +--> 12V_ANA LDO
         |
         +--> analogue front end
```

Returns:

```text
buck output return
  |
  +--> 12V_AMP_GND
  |
  +--> 12V_ANA_GND
```

Requirements:

- `12V_AMP_GND` and `12V_ANA_GND` are separate nets/branches.
- Their intentional common point is the STH0548S15 output-return/reference
  region.
- Each electrical domain uses a solid local ground plane, whether the domains
  are implemented on separate PCBs or on one partitioned PCB.
- Do not route TPA3251 gate-drive or switching-current returns through analogue-ground wiring.

### 5.1 Previous 15 V converter: XP Power STH0548S15

Use the XP Power `STH0548S15` non-isolated switching-regulator module:

- nominal system input: 36 V from its separate RSP-200-36 branch;
- module input range: use the manufacturer's conservative published
  `21–72 V DC` range for this design;
- regulated output: 15 V;
- component rating: 400 mA and 6 W;
- project maximum total 15 V rail load: 250 mA and 3.75 W;
- SMD-10 package, approximately `19.5 × 11.8 × 5.0 mm`;
- no galvanic isolation; and
- remote on/off left open for normal enabled operation unless the final
  schematic identifies a specific need to control it.

The 250 mA project limit preserves current and thermal margin for component
tolerance and the TPA3251's typical-only VDD/GVDD current figures. It is the
combined input-current budget for the `12V_AMP` LDO, `12V_ANA` LDO, RESET
supervisor, VMID, and every other auxiliary load derived from 15 V. Do not use
the module's unused 150 mA component capability to add functions without
reopening this budget.

Implementation requirements from the
[STH05 data sheet](https://www.xppower.com/portals/0/pdfs/SF_STH05.pdf):

- fit a performance-critical generic 22 µF, 63 V minimum, ±20%, 105 °C SMD
  aluminium-electrolytic input capacitor at the converter pins; its 17.6 µF
  tolerance minimum exceeds the manufacturer's 10 µF requirement; 63 V is the
  preferred rating, while a 100 V substitute is acceptable if it meets the
  same footprint, ripple, lifetime, and damping requirements;
- measure a sample's ESR near the filter's 10–20 kHz resonance region and at
  100 kHz, then use those values in the final damping assessment; this is not
  the LM2937 output-capacitor stability test and no pass/fail ESR range is yet
  asserted;
- parallel it with the exact KEMET `C1206C104K1RAC7867` 100 nF, 100 V,
  ±10%, X7R, 1206 ceramic capacitor;
- keep total effective output capacitance within the specified 100 µF maximum;
- populate the manufacturer's external C-L-C EMI-filter arrangement in Rev A
  rather than treating the module-level Class-B claim as a completed-system
  result;
- use the exact Bourns `SRR7045-560M` 56 µH, ±20% shielded power inductor;
- keep the input filter, converter, and local capacitors close together with
  short current loops;
- do not route PCB tracks beneath the module; and
- place the module in the power region, away from the RCA inputs, VMID,
  crossover filter, and other high-impedance analogue nodes.

Use pin 9 as the 36 V branch input return and pin 7 as the output-side 15 V
reference/branching region. Because the converter is non-isolated, these are
electrically common inside the module; do not create an additional external
return path that bypasses the intended input/output current routing.

Implement the manufacturer's differential-mode input filter as two parallel
2.2 µF, 100 V, 1206 MLCCs from the incoming 36 V branch to its return, followed
by the series 56 µH inductor, followed by a second pair of parallel 2.2 µF,
100 V, 1206 MLCCs at the converter side. The two 4.4 µF banks are on opposite
sides of the inductor and therefore do not form one parallel 8.8 µF bank. With
an ideally stiff source, 56 µH and the converter-side 4.4 µF give a nominal
10.1 kHz pole; the inductor's ±20% tolerance moves that calculation to
approximately 9.26–11.3 kHz. The local 22 µF aluminium electrolytic materially
lowers the actual converter-side resonance, so final damping must be assessed
using the selected capacitors' effective capacitance and ESR, the inductor DCR,
and the source impedance.

The `SRR7045-560M` has 0.18 Ω maximum DCR, 1.30 A typical RMS-current rating,
0.80 A typical saturation current, and 9 MHz typical self-resonant frequency.
These provide ample margin over both the 250 mA project output-load limit and
the module's published 311 mA full-load input current at minimum input voltage.
Treat it as a specialised exact part.

Provisionally use four Würth Elektronik `885012208124` capacitors for the two
EMI-filter shunt banks. This is a performance-critical exact Rev-A selection:
2.2 µF, 100 V, ±10%, X7R, 1206. Würth's typical DC-bias curve indicates that
approximately 45% of nominal capacitance remains near 40 V, giving about
0.99 µF per capacitor and 1.98 µF per parallel pair. Using that estimate with
56 µH moves the stiff-source pole estimate from the nominal 10.1 kHz to about
15.1 kHz. This typical curve is a design estimate, not a guaranteed minimum.

The Samsung `CL31B225KCHSNNE` was considered as an alternative. Its modelling
tool indicates approximately 51.2% of nominal capacitance remains at 36.24 V,
or about 1.13 µF per capacitor. Even if that model-to-model difference is
real, it changes the calculated pole by only about 7% and ideal attenuation
well above resonance by about 1.1 dB. That is not material enough to justify
further catalogue optimisation before Rev-A measurement. Reopen the capacitor
choice only if the assembled filter shows unacceptable ripple or ringing.

Capacitor sources:

- [Würth Elektronik 885012208124 data sheet](https://www.we-online.com/components/products/datasheet/885012208124.pdf)
- [Samsung CL31B225KCHSNN component data](https://weblib.samsungsem.com/mlcc/mlcc-ec-data-sheet.do?partNumber=CL31B225KCHSNN)

The data sheet gives approximately 540 kHz switching at 20% load and about
50 kHz at 10% load. Check conducted ripple, magnetic/electric coupling, and
mixing with the TPA3251's then-assumed 450 kHz switching during prototype
validation. The current amplifier setting is nominal 600 kHz; this paragraph
records the superseded converter option. The
two 12 V post-regulators remain required; the converter does not directly feed
the analogue or amplifier housekeeping circuits.

### 5.2 Previous 12 V post-regulators and branch networks

Use one Texas Instruments `LM2937ESX-12/NOPB` on each branch. This is the
fixed-12 V, 500 mA DDPAK/TO-263 version; do not substitute the lower-current
SOT-223 `LM2937IMPX-12/NOPB`. The common part was selected because its typical
ripple-rejection plot remains useful through the STH0548S15's documented
50–540 kHz operating region, it has adequate voltage/current/thermal margin,
and it avoids a second regulator type. The graph is typical data measured on a
5 V version under different conditions, not a guaranteed 12 V minimum. The
12 V version's specified 10 Hz–100 kHz output noise is 360 µV RMS typical at a
5 mA load, so prototype rail and audio-output noise measurements remain the
acceptance evidence.

A mixed regulator scheme could reduce intrinsic `12V_ANA` noise, but it would
add another BOM line and layout pattern without solving a demonstrated problem.
The OPA167x stages have strong supply rejection, the analogue branch receives
additional RC attenuation, and the audio path is low-bandwidth. Rev A therefore
uses two LM2937s. Reopen the mixed-regulator option only if the assembled board
shows regulator-related noise or STH0548S15/TPA3251 mixing products that the
defined filtering and layout cannot reduce adequately.

Implement the 15 V output and two regulator inputs as follows:

```text
STH0548S15 pin 5
  |
  +-- 10 µF, 25 V SMD aluminium electrolytic
  |     || KEMET C1206C104K1RAC7867 100 nF to pin 7
  |
  +-- 0 Ω link (12V_AMP; reserve 3.3 Ω option)
  |     +-- KEMET EEV226M035S9DAA 22 µF aluminium electrolytic
  |           || KEMET C1206C104K1RAC7867 100 nF
  |     +-- LM2937ESX-12/NOPB
  |
  +-- 10 Ω, 1206, >=0.25 W (12V_ANA)
        +-- KEMET EEV226M035S9DAA 22 µF aluminium electrolytic
              || KEMET C1206C104K1RAC7867 100 nF
        +-- LM2937ESX-12/NOPB
```

Fit the amplifier link as 0 Ω for Rev A. A 3.3 Ω population option is retained
for measured-noise troubleshooting, but must not be fitted until RESET timing,
minimum 15 V rail voltage, and loaded LDO headroom have been rechecked. Fit the
10 Ω analogue resistor. With the nominal 22 µF downstream capacitance and
ignoring ESR initially, its one-pole corner is

```text
fc = 1 / (2 pi R C) = 1 / (2 pi x 10 ohm x 22 µF) = 723 Hz
```

The selected capacitor's listed 1 Ω impedance at 100 kHz and 20 °C limits the
high-frequency attenuation of the real 10 Ω RC network. Approximating that
impedance as ESR gives a pole near 658 Hz, a zero near 7.23 kHz, and a
high-frequency shelf of `1 / (10 + 1)`, or approximately -20.8 dB, before the
LDO's own rejection. This is still useful: applying the shelf conservatively
to the converter's specified 75 mV peak-to-peak ripple gives about 6.8 mV
peak-to-peak at the LDO input. These are model estimates because impedance
varies with frequency and temperature; assembled ripple measurement remains
the acceptance evidence.

At the 35 mA analogue branch budget the resistor drops 0.35 V and dissipates
12 mW. The nominal capacitance directly associated with the converter output
is 54.3 µF: 10 µF common, two 22 µF branch capacitors, and three 100 nF
capacitors. This remains below the module's 100 µF maximum; even the stated
positive component tolerances total only about 65.1 µF. Verify the final BOM
and every additional 15 V capacitor against that limit.

The power-tree capacitor selections use the project-wide generic/specialised
distinction:

| Function | Classification | Required selection |
| --- | --- | --- |
| STH0548S15 input bulk | performance-critical generic because its ESR contributes to filter damping | 22 µF, 63 V minimum and preferred, ±20%, 105 °C SMD aluminium electrolytic; 6.3 mm diameter × approximately 8 mm high can/land pattern; at least 100 mA ripple-current rating; measure ESR near 10–20 kHz and at 100 kHz and use it in the damping assessment; a 100 V substitute is acceptable if all requirements are met |
| STH0548S15 EMI-filter shunt banks | performance-critical; provisional exact Rev-A part | four Würth Elektronik `885012208124`, 2.2 µF, 100 V, ±10%, X7R, 1206 MLCCs, used as two parallel pairs; use approximately 0.99 µF each at 40 V for preliminary analysis and verify the assembled filter |
| 36 V-side high-frequency bypass | exact part for BOM consolidation | KEMET `C1206C104K1RAC7867`: 100 nF, 100 V, ±10%, X7R, 1206 |
| STH0548S15 output bulk | generic | 10 µF, 25 V minimum, ±20%, 105 °C SMD aluminium electrolytic; 5 mm diameter × approximately 5.8 mm high can/land pattern |
| STH0548S15 output and LM2937-input high-frequency bypasses | exact part for BOM consolidation | KEMET `C1206C104K1RAC7867`: 100 nF, 100 V, ±10%, X7R, 1206; one at the converter output and one directly at each LM2937 input |
| each LM2937 input reservoir | performance-critical exact part | KEMET `EEV226M035S9DAA`: 22 µF, 35 V, ±20%, 105 °C SMD aluminium electrolytic, 5 mm diameter × 5.65 mm maximum height, listed 1 Ω impedance at 100 kHz and 20 °C, 160 mA ripple-current rating at 100 kHz, and 2,000-hour life at 105 °C |
| each LM2937 output capacitor | performance-critical exact part | KEMET `EEV226M035S9DAA`; the same electrical and mechanical data apply; capacitance must remain at least 10 µF and measured ESR must remain between 0.01 Ω and 3 Ω over the project's operating-temperature range |
| 12 V load decoupling | generic | 100 nF, 50 V, ±10%, X7R, 0603 unless a load data sheet requires otherwise |

Use the same exact KEMET `EEV226M035S9DAA` at both LM2937 inputs and outputs.
Its listed 1 Ω impedance at 100 kHz and 20 °C is comfortably within the
LM2937's required 0.01–3 Ω output-capacitor ESR range; a lower ESR is not an
intrinsic improvement because the regulator also imposes a lower stability
limit. Before assembly approval, measure a representative sample's ESR at
100 kHz. Manufacturer data or further measurements must also establish that
capacitance remains at least 10 µF and ESR remains in range over the project's
actual operating-temperature range. Preserve capacitor polarity. Reopen the
selection only if those checks fail or Rev-A ripple/noise is unacceptable.

Use KEMET `C1206C104K1RAC7867` for all four 100 nF high-frequency bypass
positions in the auxiliary filter chain: the STH0548S15 input, its output, and
the two LM2937 inputs. Its 100 V rating and 1206 package are deliberately
overspecified on the 15 V nodes to consolidate the BOM. Yageo/KEMET's current
specification identifies `C1206C104K1RACTU`, with
`C1206C104K1RAC7800` as a packaging alias; treat those suffixes as the same
electrical component only after confirming the supplied termination and
packaging are compatible. This consolidation does not apply automatically to
distributed 12 V load decouplers, which remain generic 100 nF parts placed in
the package most appropriate to each load.

All generic capacitor substitutions are acceptable only when every property
in the table is met. Do not substitute the four exact KEMET capacitors without
repeating their capacitance, ESR, temperature, ripple, lifetime, mechanical,
and regulator-stability review. Confirm regulator stability on the assembled
PCB because distributed ceramic load bypasses appear in parallel with the
stability capacitor at high frequency.

The current allocation is:

| 15 V-derived load | Design allocation | Basis |
| --- | ---: | --- |
| TPA3251 VDD plus two PBTL gate-supply bridges | 120 mA | 90 mA published typical operating current plus 30 mA engineering allowance; TI gives no maximum |
| eight OPA167x channels, including VMID allowance and signal current | 35 mA | 22.4 mA maximum quiescent current plus 12.6 mA allowance |
| two LM2937 ground currents | 40 mA | 20 mA data-sheet maximum per regulator, conservatively applied outside its stated 500 mA test condition |
| TPS3842 and divider/pull-up overhead | <1 mA | supervisor itself is microampere-scale; allowance covers the passive network |
| **allocated total** | **196 mA maximum** | **54 mA remains inside the 250 mA project limit** |

The TPA3251 figures are typical-only, so 120 mA is a controlled design
allocation, not a guaranteed device maximum. Measure both branch currents on
the first assembled board and reopen the budget if either allocation is
exceeded.

The LM2937 data sheet guarantees dropout only at 50 mA and 500 mA, not around
the expected amplifier-branch current. Characterise one `LM2937ESX-12/NOPB`
sample at 25 °C and 50, 75, 100, 125, 150, 175, and 200 mA. At each current,
establish the regulated output at 15.0 V input, reduce input voltage slowly,
and record `VIN - VOUT` when `VOUT` has fallen 100 mV from that regulated
baseline. Treat this as sample characterisation rather than a guaranteed
production limit, and use the result when finalising the TPS3842 threshold.

For a deliberately pessimistic thermal check at 15.6 V, 40 °C ambient, full
allocated load, and the LM2937's 20 mA maximum ground current, the amplifier
regulator dissipates approximately

```text
PD = (15.6 V - 12 V) x 0.120 A + 15.6 V x 0.020 A = 0.744 W
```

Using TI's 41.8 °C/W JEDEC junction-to-ambient figure gives about 31 °C rise,
or 71 °C junction. The analogue regulator, after the 10 Ω drop, dissipates
approximately 0.42 W and reaches about 58 °C by the same deliberately
pessimistic method. Both are comfortably below the 125 °C operating limit,
but each DDPAK tab still needs a generous local copper heat-spreader; final PCB
thermal verification supersedes the JEDEC estimate.

Primary source:

- [Texas Instruments LM2937 data sheet](https://www.ti.com/lit/ds/symlink/lm2937.pdf)
- [KEMET EEV226M035S9DAA specification](https://search.kemet.com/download/specsheet/EEV226M035S9DAA)
- [KEMET C1206C104K1RACTU specification](https://search.kemet.com/component-documentation/download/specsheet/C1206C104K1RACTU)

---

## 6 Amplifier ground and rear plate

The aluminium rear plate acts as:

- exposed conductive chassis
- TPA3251 heatsink
- protective-earth bonded metalwork

The TPA3251 heatsink/PowerPAD arrangement requires the amplifier ground to be intentionally referenced to the rear plate.

```text
TPA3251-side GND copper
  |
controlled low-impedance bond
  |
aluminium rear plate
  |
PE
```

Requirements:

- Use one intentional amplifier-ground-to-chassis bond.
- Locate this bond close to the TPA3251/heatsink region.
- Avoid additional unintended low-impedance GND-to-chassis connections elsewhere.
- Treat the Mean Well `-V` rail as earth-referenced once the completed amplifier/chassis bonding is installed.

---

## 7 Analogue ground

The analogue domain uses a quiet region of the common `GND` copper:

```text
analogue-side GND copper
  |
analogue-domain ground plane
  |
input buffers / summer / LPF / level / differential driver
```

Requirements:

- Keep analogue ground currents local to the analogue domain.
- Do not intentionally route Class-D or PSU switching currents through this plane.
- Connect this region to the wider board return without bringing buck or
  amplifier switching current through it; settle the exact geometry in layout.
- Any future analogue-ground-to-chassis network must be deliberate and added only if prototype EMC/hum testing justifies it.

---

## 8 RCA inputs

Use chassis-isolated RCA connectors.

Requirements:

- RCA shells must not make direct electrical contact with the aluminium rear plate.
- Use insulated RCA sockets/bushes.
- Signal ground returns to the analogue domain only.
- Do not use the RCA mounting hardware as a chassis-ground connection.

Reason:

- Prevent a second signal-ground-to-PE connection through the rear panel.
- Avoid forming a loop between RCA shell/chassis and amplifier-ground/chassis bonds.

---

## 9 Grounding topology summary

The canonical partial schematic now uses one electrical `GND` net, with the
unpopulated R1/R2 links removed. This closes the conceptual split-net versus
single-net decision. The board layout must control analogue, buck, and
amplifier return paths by placement and copper geometry. The six Mean Well
output terminals are three connections to each common +V and -V rail, not
isolated outputs. The earlier dedicated amplifier and buck 36 V wire-branch
plan is superseded in the current saved PCB by a common J6 entry and local
buck branch; the selected six conductors remain available as three paired
paths. Their returns also share the PCB `GND` net. Do not claim a single
physical ground junction or use the
TPA3251's internal ground connections as a PCB return conductor. Keep the
12 V amplifier return out of quiet analogue copper. The 25 October saved board
assigns J6 pins 1–3 to the common `36V` field and pins 4–6 to common `GND`.
The [current PCB review](PCB_LAYOUT.md#2-findings) finds both U3 GND and the
36 V board entry joined locally, with no visible ratline. The former ground
seam and asymmetric positive/return connection are resolved in saved copper;
the physical PSU harness pairing and termination remain to be verified.

### 9.1 Remaining grounding implementation gates

- Verify the now-joined six-position J6 pads against the actual mating
  harness and Mean Well terminations. Use three closely paired feed/return
  cable paths with the buck branch local to the common board entry. A single
  pair would require further contact, copper and enclosure-temperature
  checks. Parallel conductors' current division is not guaranteed by terminal
  assignment alone.
- Trace the actual `17V3` supply and return loops, U3 local GND connection,
  analogue reference, and any parallel return path to the PSU. Select the
  ordered four-layer stack-up and copper weights from those routes. The
  current 1 oz outer / 0.5 oz inner starting point is provisional, not a
  finished-board current or thermal qualification.
- Define the one intentional board-GND-to-rear-plate bond near the TPA3251 and
  account for possible additional contacts through the thermal interface,
  mounting hardware, connectors, and PSU. Verify the independent PE conductors
  and finished bonds during assembly as specified in Sections 3 and 6 and in
  [Prototype validation](VALIDATION.md).

---

## 10 PCB grounding rules

### 10.1 TPA3251 amplifier domain

- Use a solid, low-impedance ground plane.
- Keep PVDD decoupling loops extremely short.
- Keep bootstrap and switching-current loops compact.
- Minimise switching-node copper area.
- Keep output-filter current returns local.
- Do not use long star traces for high-frequency returns.
- Follow TI reference-layout guidance closely.

### 10.2 Analogue domain

- Use a continuous analogue-ground plane.
- Keep VMID distribution distinct from ground.
- Keep high-impedance nodes away from Class-D switching nodes and PSU magnetics.
- Connect the quiet analogue return region to the wider board return outside
  the buck's pulsed current paths.

### 10.3 Combined-PCB grounding and placement

Rev A uses one four-layer PCB with physically partitioned analogue and
Class-D domains. The schematic uses a common `GND` net; it does not require
uniform ground copper across the entire board.

Partition rules:

- Keep broad, low-impedance local return copper for the amplifier and a quiet
  analogue return region. Contain the buck's pulsed input and output loops near
  its capacitors and switch. Define any inter-region ground connections from
  complete supply-and-return loops, not from a literal single-point rule.
- Keep a placement and routing corridor between the analogue circuitry and
  switching nodes. Route the balanced audio pair together across it. Determine
  other crossings from the finished placement and supply/return loops; do not
  leave a signal or power trace crossing a reference-plane gap.
- Bring the three paired 36 V feeds and returns from the common Mean Well
  rails to J6; branch to the buck locally. The buck-fed 12 V amplifier branch
  also connects to board GND. Review parallel cable paths and local return
  geometry rather than assuming the PSU is the sole meeting point.
- Put the TPA3251 input side at the corridor edge. Put its switching nodes,
  PVDD commutation loops, output inductors, and speaker connection on the far
  side, away from the analogue domain.
- Route the two audio conductors together, symmetrically, and without stubs.
  Terminate them into the TPA3251-side input network immediately after the
  crossing.
- AC-couple both conductors symmetrically at the TPA3251 side so the amplifier
  establishes its own input bias/common-mode voltage. Confirm the final input
  network when the differential-driver values are selected.
- Populate the symmetric 100 Ω/100 pF input networks specified in
  [Front end](FRONT_END.md). Reserve matched optional footprints for any
  additional RF/common-mode mitigation justified by prototype measurements;
  leave those additional positions unpopulated by default.
- Keep mounting hardware in the analogue domain electrically isolated from the
  protective-earthed aluminium plate. The single intended amplifier-ground to
  chassis bond remains near the TPA3251/heatsink region.

The corridor is a placement and field-control tool, not galvanic isolation.
Good Class-D loop layout and a continuous return reference beneath any
crossing are more important than a nominal corridor width.

### 10.4 Layer-count decision

Two layers are technically feasible: TI's TPA3251 evaluation module implements
the amplifier and local differential-input op amps on a 2-layer, 2-oz-copper
PCB. It would require disciplined use of broad copper pours, an unbroken local
amplifier-ground plane, and close adherence to the TI reference placement.
This feasibility basis is the official
[TPA3251EVM product page](https://www.ti.com/tool/TPA3251EVM),
[EVM user guide](https://www.ti.com/lit/pdf/SLAU751), and the
[TPA3251 layout guidance](https://www.ti.com/lit/ds/symlink/tpa3251.pdf).
This is supporting precedent only; a two-layer board is not a project fallback.

Four layers are locked for this project's combined Rev-A board because they
provide materially better implementation margin:

- a substantially less interrupted local ground plane for each domain;
- easier, lower-inductance access from decoupling and signal returns to their
  local planes;
- less competition between high-current routing and return continuity;
- better containment of fields and more routing freedom at the boundary; and
- a less fragile route to a quiet analogue section on the same substrate.

This choice reduces EMC, noise, and layout-rework risk. It does not imply that
a competent 2-layer implementation would necessarily sound worse or measure
worse in-band.

Current layer intent for the first-prototype bare board:

- front outer layer: analogue components and amplifier parts best placed away
  from the plate, with broad high-current copper where appropriate;
- rear outer layer: the TPA3251, selected close decoupling/bootstrap and other
  support parts that fit the machined reliefs, with direct short pin connections;
- inner layers: keep a solid `GND` reference adjacent to the rear-mounted
  TPA3251 and a quiet `GND` region for front-side analogue circuitry; reserve
  the remaining area for supply distribution without severing critical
  return paths; and
- begin with approximately 35 µm (1 oz) outer and 15.2 µm (0.5 oz) inner
  copper for the published JLCPCB stack. The
  [19 October power-stage review](POWER_AMPLIFIER.md#117-power-stage-copper-review-19-october-2026)
  provisionally supports this for the 150 W / 4 Ω design point. Upgrade
  selected layers only if final route width, length, RMS current, voltage
  drop, heating, or fabrication constraints justify the extra cost. The user
  selected JLCPCB standard four-layer, 1.6 mm construction on 26 October;
  confirm its options in the actual order before release.

The latest 25 October saved board restores broad GND to Inner 2, next to the
rear-mounted U3, and broad 36 V to Inner 1. Bottom GND remains local at U3.
This resolves the preceding revision's adjacent-ground concern in saved
geometry. The reciprocal trade-off is on the Top analogue side: some
buffered/filter and `VMID` traces overlie Inner 1 `15VA` rather than GND,
with their GND reference on Inner 2. The raw input traces by J4 remain over
local Inner 1 GND. See [PR-006 and PR-007](PCB_LAYOUT.md#2-findings); retain
the present layer order unless a targeted route or prototype noise check
gives a reason to change the local analogue reference.

The saved DipTrace PCB stack now uses 1 oz outer / 0.5 oz inner copper and
0.2104/1.065/0.2104 mm dielectric spacing, matching JLCPCB's published
1.6 mm `JLC04161H-7628` / no-impedance-requirement example at the nominal
design level. This supersedes the earlier saved default with 1 oz on all
four layers. The 25 October saved entries are 34.8 µm outer and 15.2 µm
inner copper, so the inner entry now matches the published selected example.
The via-barrel resistance table in the
[power-amplifier review](POWER_AMPLIFIER.md#112-via-barrel-resistance-estimate-17-october-2026)
uses JLCPCB's published finished-layer figures; the user selected JLCPCB
standard four-layer, 1.6 mm construction for the first bare-board order.
Confirm the actual order options before release. If 1 oz inner planes are later
needed for current distribution, select them deliberately and update the
DipTrace stack and resistance estimate. The current saved via land is 0.45 mm,
and the [via-field review](POWER_AMPLIFIER.md#113-via-field-current-and-plane-review-17-october-2026)
identifies the `SPK+` and `36V` fields as the principal places to inspect
plane clearance against useful via count.
[JLCPCB layer stack](https://jlcpcb.com/impedance).

**Bottom GND extension:** On 18 October the saved Inner 2 (layer 3) `GND`
pour spanned most of the 54 × 61 mm amplifier area, while Bottom (layer 4)
`GND` pours were local patches. In the 19 October saved layout a broad Bottom
GND pour now fills much of that area, below the local 36 V and switching-node
pours in priority. In that revision it joined nearby ground pads and the then
Inner 2 GND plane through existing or deliberate, well-spaced GND vias. The
immediately preceding revision carried broad 36 V on Inner 2; the current
revision restores Inner 2 GND. Check its actual Bottom-to-Inner 2 stitching.
Do not copy the plane outline as a goal in itself: a
slotted or weakly connected outer fill offers little parallel conductance, and
extra through-vias can perforate the 36 V plane. Keep the Bottom U3 PVDD and
GND ceramic paths, switching-node/output copper and quiet input return
geometry intact; avoid making a narrow Bottom GND bridge that offers amplifier
switching or filter-capacitor return current a route through the analogue
region. Remove isolated islands, then inspect filled copper, DRC and net
connectivity. The fill is present in saved geometry but remains subject to
finished connectivity and return-path checks.

At 20 °C, copper sheet resistance `rho/t` is about 1.15 mΩ/square for a
15 µm inner layer and 0.49 mΩ/square for a 35 µm outer layer. If both layers
offered the *same continuous path* and were adequately stitched, their
parallel sheet resistance would be about 0.34 mΩ/square. Actual extra Bottom
copper will be slotted and current will enter/leave through discrete pads and
vias, so this is an optimistic illustration, not a predicted board resistance.
The TPA3251's principal heat route is to the rear aluminium plate; Bottom
copper may spread local component heat but is not a substitute for that path.

The former requirement that every TPA3251 support part crosses the PCB is
superseded. Put the high-frequency local decoupling on the IC side where the
pin geometry and milled clearance permit. Where a loop must cross layers,
keep its outward and return transitions adjacent and use appropriate local
via groups. Apply the return-path and placement rules on both populated sides.

---

## 11 Locked grounding decisions

Treat the following as fixed unless prototype evidence requires revision:

- Rear aluminium plate is permanently protective-earthed.
- Mean Well FG/chassis is connected to PE.
- IEC inlet PE connects by one short conductor to the dedicated M4 plate stud;
  a separate conductor runs from that stud to RSP terminal 3 `FG`.
- The selected six-conductor harness provides three 36 V feed/return pairs
  from the common Mean Well rails to J6; the current PCB joins them at entry
  and branches to the buck locally. Verify physical pairing and termination.
- Use one electrical `GND` net in the main-board schematic; control
  analogue, buck, and amplifier return currents through placement and copper.
- TPA3251 uses a solid local power-ground plane.
- Analogue circuitry uses a quiet local region of the common GND copper.
- TPA3251 amplifier ground is intentionally bonded to the aluminium rear plate at one controlled point.
- RCA sockets are electrically isolated from the aluminium panel.
- No additional chassis/signal-ground bonds are permitted unless explicitly added after prototype testing.
- Protective-earth continuity must not depend on PCB mounting or signal connectors.
- Rev A uses one four-layer PCB with physically partitioned analogue and
  amplifier domains. There is no two-layer fallback; four layers are a project
  robustness requirement, not a TPA3251 functional requirement.
