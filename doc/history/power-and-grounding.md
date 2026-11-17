# Power and grounding history

> **Lifecycle: HISTORY.** Superseded design; do not use as current build instructions. The [current power and grounding authority](../POWER_AND_GROUNDING.md) owns the rev0 design.

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


## 6 Earlier buck setpoint comparison

**2026-10-13 setpoint review — 18 V remains a candidate, not a schematic
change.** Changing only R28 from 11 kΩ to 10.6 kΩ with R24 = 180 kΩ would
give `1 V × (1 + 180/10.6) ≈ 17.98 V` nominal. With the shared
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
and 2.5% hysteresis assumptions used in [Power amplifier](../POWER_AMPLIFIER.md).
At the 17.38 V calculated lowest healthy buck output, that leaves only
0.77 V before loaded ripple and feed/return offsets; its lowest falling
trip is just 0.20 V above the L78M12A's specified input minimum. It therefore
does not establish guaranteed pre-dropout RESET assertion. Retain the drawn
17.36 V feedback and 130 kΩ/7.5 kΩ supervisor divider for now. Reconsider
18 V after the loaded buck trough, analogue load/headroom, and U9 temperature
are known; do not change either divider to claim a protection guarantee from
nominal values alone.


## 7 Earlier U9 layout checkpoints

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
[current routed-board review](../PCB_LAYOUT.md) identifies a roughly 544 mm² Top
GND-pour outline joined to U9's tab, further local GND fills on Inner 1,
Inner 2 and Bottom, and 19 GND vias within 10 mm of the tab centre. The
24 October statement that the planned four-layer structure was absent remains
a dated description of that earlier file. The present geometry now implements
the intended spreader, subject to connectivity/DRC and a temperature check at
the actual continuous load. The dissipation model below remains provisional.

