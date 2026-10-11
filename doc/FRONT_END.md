# Analogue front end

> **State — current design basis; reviewed 2026-10-11.** Owns the analogue
> signal path and its part choices; power rails and ground partitioning belong
> to [power and grounding](POWER_AND_GROUNDING.md). Read when changing the
> schematic front end. Current conclusions: retain R5 outside the VMID buffer
> feedback loop; the selected Panasonic PPS-film capacitors have the intended
> land pattern, and the J2 wiper-bias and J3 receiving networks are drawn.
> Next gate: verify external pot/switch wiring and panel-cable stability, then
> validate the assembled filter and noise. The XML
> is partial, and assembled performance has not been measured.

## 1 Overview

Use OPA167x family.

Preferred parts:

- `OPA1678` dual
- `OPA1679` quad

### 1.1 Signal chain

```text
RCA L/R
  |
RF protection + DC blocking
  |
L/R unity buffers
  |
active L+R averaging summer
  |
variable 2nd-order Butterworth LPF
  |
level control
  |
0° / 180° polarity selection
  |
single-ended to differential driver
  |
TPA3251
```

### 1.2 Buffered VMID

The current partial schematic uses U5.3, an OPA1679 unity-gain buffer, to generate
the nominal 7.5 V analogue midpoint from `15VA`:

```text
15VA
  |
10 kΩ
  |
  +-- OPA1679 voltage follower -- 10 Ω --> VMID
  |
10 kΩ || 4.7 µF ceramic
  |
AGND
```

The two 10 kΩ legs present a 5 kΩ Thevenin resistance to the divider
capacitor. At its nominal 4.7 µF, the pole is 6.77 Hz, the time constant is
23.5 ms, and 1% settling takes approximately 108 ms. Actual ceramic
capacitance under 7.5 V bias remains to be checked. U5.3 has direct
output-to-inverting-input feedback. The separate `R5 = 10 Ω` lies between
that sensed output and VMID; there is no shunt capacitor directly on VMID.
The former 10 kΩ feedback resistor has been removed, consistent with the
[OPA1679's unity-gain stability](https://www.ti.com/lit/ds/symlink/opa1679.pdf).
Assess VMID noise, load current, and stability with the complete front end
before adding output filtering.

Keep R5 outside U5.3's feedback loop as the present baseline. Sensing VMID
after R5 would correct its small load-dependent voltage drop at low frequency,
but would put the VMID load and its capacitance in the feedback path. TI
recommends a series output resistor to isolate heavier capacitive loads on
the OPA167x; compensated dual feedback would be a separate design if lower
VMID source impedance became necessary. At 100 µA through 10 Ω, the present
drop is only 1 mV. No material benefit to moving the feedback takeoff has
been established. [TI OPA1679 data sheet](https://www.ti.com/lit/ds/symlink/opa1679.pdf),
[TI capacitive-load compensation guidance](https://www.ti.com/document-viewer/lit/html/SSZT999/GUID-7ACEA978-4202-4BB8-8E9A-DE4DEC6654C4).
Revisit RESET timing against the complete start-up waveform and loudspeaker
transient after the revised approximately 17.36 V/15 V/12 V power tree is
defined.

### 1.3 OPA1679 supply decoupling

The partial schematic has `C1` and `C2`, each 100 nF from `15VA` to
`AGND`, for U5 and U6 respectively, and a separate nominal `C16 = 1 µF`
at the U3 15 V LDO output. With C1/C2 placed very close to the respective
op-amp supply pins and returned to the local analogue ground, this meets
TI's usual single-supply OPA1679 bypass recommendation: a 0.1 µF ceramic is
adequate in most cases. An additional 1 µF at either op amp is optional if the
15 V distribution becomes long or noisy, not required by the present partial
circuit. Torex recommends a 0.1–1 µF local output capacitor for load-step
response, although XC6701's internal compensation does not require one for
stability; check C16's effective capacitance under 15 V bias and place it near
U3. A remote op-amp capacitor does not replace U3's local capacitor. Sources:
[TI OPA1679 data sheet](https://www.ti.com/lit/ds/symlink/opa1679.pdf),
Sections 8.3–8.4, and [Torex XC6701 data sheet](https://product.torexsemi.com/system/files/series/xc6701.pdf),
Notes on Use.

### 1.4 VMID reference branches in the partial schematic

The 2026-10-06 canonical export confirms that the two former 1 µF local
reference-filter capacitors C18 and C23 have been removed. Previously,
R12/C18 and R13/C23 made separate nominal 3.39 Hz reference filters while
the level-pot bottom and other stages used unfiltered VMID. At J2's minimum
setting, its wiper equals VMID and U6.2's ideal differential output is
`2 × (VMID - Vref)`. A 0.5 mV VMID disturbance well above the former filter
pole would therefore have produced approximately 1 mV differential, not
0.5 mV. Removing the two shunt capacitors removes this mismatch mechanism.

The current XML has no separate series VMID reference-filter resistors. U6.2 and
U5.4 now take their non-inverting references directly from the common VMID
net. The previous reference-filter mismatch and its two unnecessary 47 kΩ
series-noise sources are therefore absent.

## 2 Inputs

Per channel:

- RCA input
- target input impedance: nominal 47 kΩ
- nominal source level: approximately 2 V RMS
- clean handling target: approximately 3 V RMS

The OPA167x input common-mode range reaches only to `(V+) - 2 V`.
With the current 0–15 V supply and 7.5 V VMID, the input-buffer upper limit
is 13 V. A 3 V RMS sine wave centred on VMID reaches 11.74 V before the small
loss in the 1 kΩ/47 kΩ input network. Thus the revised rail provides about
1.26 V peak input common-mode margin at this target. Full-chain output swing
and clipping still need confirmation.

During a buck-voltage fault the 15 V analogue LDO may leave regulation before
the buck supervisor asserts RESET. If the analogue supply falls to 12 V and
VMID follows to 6 V, the same 3 V RMS input reaches about 10.24 V while the
OPA167x upper common-mode limit is 10 V. The full 3 V RMS clean-input target
therefore ceases to be guaranteed below approximately 12.5 V analogue supply
(`Vrail/2 - 2 V = 3 V × √2`). At smaller normal input levels this particular
limit recedes, but the front end's behaviour in LDO dropout is unverified.
The buck monitor's current divider and remaining 12 V LDO headroom are given
in [power amplifier](POWER_AMPLIFIER.md).

Initial network:

```text
RCA
 |
1 kΩ series
 |
330–470 pF RF shunt
 |
Würth 885012208124 2.2 µF X7R coupling capacitor
 |
47 kΩ to VMID
 |
OPA167x unity buffer
```

In the current partial schematic, U5.1 and U5.2 have direct output-to-inverting-
input feedback. The 47 kΩ resistors give their non-inverting inputs a DC path
to VMID. Adding 47 kΩ to each feedback path merely to balance typical
[OPA1679 input bias currents](https://www.ti.com/lit/ds/symlink/opa1679.pdf)
is not selected: 10 pA through 47 kΩ produces
only 0.47 µV of DC shift, while an added resistor contributes noise and can
interact with input capacitance. Revisit this only if measured DC offset
identifies a material need.

Those resistors are `R12` and `R23`. Their primary jobs are to set the
approximately 47 kΩ connected-source input load and provide the AC-coupled
inputs with a DC bias path. With the nominal 2.2 µF input capacitors, the
simple high-pass corner is 1.54 Hz. They are not the main control on
left/right isolation: a low-impedance VMID buffer and deliberate shared-return
layout matter more. The resistor's open-input Johnson voltage-noise density
is about 28 nV/√Hz at room temperature; with a connected low-impedance source,
that resistor is shunted by the source through the coupling capacitor and its
actual input-node noise contribution is smaller. Changing 47 kΩ solely to
reduce an assumed noise or crosstalk figure is not selected.

Select Würth Elektronik `885012208124` (2.2 µF, ±10%, 100 V, X7R, 1206)
for both RCA-input coupling positions and both TPA3251 differential-input
coupling positions described in Section 7. This is the confirmed Rev-A
assembly choice, not a claim that its in-circuit distortion and capacitance
have already been measured. Review the assembled 20–100 Hz distortion and
effective low-frequency response after construction; reopen the choice only
if those results show a material problem. Its 100 V rating and the relatively
small signal voltage across each coupling capacitor make it a reasonable
Class 2 ceramic candidate, but neither fact establishes a distortion result.
The former 15 V converter plan also provisionally used this part in its EMI
filter; that supply-filter use is superseded by the revised power tree.

Retain Rubycon `16MF225KA23216` and Kyocera AVX `CB162D0225JBC` as film
references or fallback parts if the assembled signal path reveals a problem.
Their different land patterns must be checked before any substitution.

A Nichicon UWP 2.2 µF bipolar aluminium electrolytic remains an unselected
alternative. Of its two relevant ratings, prefer the
`UWP1V2R2MCL1GB` 35 V, 4 mm-diameter part over the
`UWP1H2R2MCL1GB` 50 V, 5 mm-diameter part: both are ±20%, 5.4 mm high,
rated for 1,000 hours at 85 °C, and have the same maximum 0.15 dissipation
factor and 10 µA leakage specification, so the larger voltage rating provides
no useful circuit benefit. Bipolar construction removes the start-up polarity
constraint of an ordinary polarised electrolytic, and 2.2 µF preserves the
nominal frequency response and settling times already calculated. Before
approval, compare 20–100 Hz distortion with a film reference and measure
leakage-induced DC shifts at both the 47 kΩ input nodes and the two nominal
24 kΩ TPA3251 inputs. Pair the two amplifier-input parts by measured
capacitance and leakage.

Panasonic `EEE-1VA2R2NR` is a technically lower-leakage bipolar SMD
alternative: its maximum leakage is 6 µA rather than 10 µA, although its
maximum dissipation factor is higher at 0.24. A 2026-09-23 Mouser UK check
with `In Stock`, `Normally Stocked`, and `Active` all selected retained the
part and showed 20,607 in stock, a minimum order of one, and a one-off price
of £0.353. Do not select it as the new-design default, however: Panasonic's
own current product page marks it `NRFND`. Treat it only as a stocked
contingency unless Panasonic restores a new-design lifecycle status or an
active successor with the same electrical advantage becomes available.

Confirm the selected Würth capacitor's effective capacitance at the actual DC
biases and assess the assembled 20–100 Hz distortion at representative and
maximum clean signal levels. If there is a material excess, compare against a
film reference to isolate the capacitor contribution before changing the
selection. Provide the Würth land pattern from its manufacturer's recommendation;
do not assume the film, bipolar-electrolytic, and MLCC terminations are
interchangeable.

Requirements:

- source must see a benign, well-defined load
- no dependence on source-specific output impedance
- input protection should not add significant capacitance/distortion

## 3 Stereo-to-mono summer

Topology:

- active inverting averaging summer
- non-inverting input referenced to VMID

Initial values:

- `R_L = 10 kΩ`
- `R_R = 10 kΩ`
- `R_F = 3.0 kΩ`

Transfer:

```text
Vmono = -0.3 × (VL + VR)
      = -0.6 × ((VL + VR) / 2)
```

The stage therefore forms the mono average and applies the fixed 0.6 scaling
needed by the complete gain structure. For equal correlated left and right
signals, `VL = VR = VS`, its output is `-0.6 × VS`. This avoids making the
maximum system gain depend on the level potentiometer's total-resistance
tolerance. Use generic 0.1%, 0805 thin-film resistors with temperature
coefficient no worse than ±25 ppm/°C for all three summing resistors.

The current U5.4 stage uses `R16/R27 = 10 kΩ` inputs and `R22 = 3 kΩ`
feedback; its non-inverting input connects directly to VMID, with no
shunt filter capacitor. There is no feedback capacitor. One could add
approximately 1 nF C0G/NP0 in parallel with R22 for a 53 kHz pole if pre-filter
ultrasonic pickup or overload appears. The following 40–100 Hz Sallen-Key
already supplies the required bass-band roll-off, so this capacitor is not
needed for the intended filter response. A signal-path feedback capacitor
must use a low-distortion dielectric; [TI warns against X7R in this role](https://www.ti.com/lit/ds/symlink/opa1679.pdf).

## 4 Variable low-pass filter

Locked topology:

- 2nd-order Sallen-Key
- Butterworth
- `Q ≈ 0.707`
- 12 dB/octave
- continuously variable
- Bourns `PDB182-K420K-203B` 20 kΩ dual-gang linear pot, provisionally
  accepted subject to the mechanical and thermal conditions below
- target range approximately 40–100 Hz
- unity-gain filter stage

Initial values:

- use three Panasonic `ECH-U1H823JX9` 82 nF, ±5%, 50 V, PPS-film
  capacitors; their corrected land pattern still needs PCB-export verification
- `C_SHUNT = 82 nF` from the op-amp non-inverting-input node to VMID
- `C_FEEDBACK = 164 nF` from the two-resistor junction to the op-amp output,
  using the other `2 × 82 nF` capacitors in parallel
- each R arm = one generic 13.7 kΩ, ±1%, 0805 thin-film resistor with
  temperature coefficient no worse than ±50 ppm/°C, plus one 20 kΩ pot gang

The user selected the Panasonic PPS-film part on 2026-10-06, superseding the
earlier Murata `GRM3195C1H823GA05D` 82 nF, ±2%, 50 V, C0G, 1206 selection.
Both PPS film and C0G are suitable low-distortion, stable dielectrics for this
filter; an audible or measurable advantage of this film part over the C0G
alternative has not been established. The film part has a wider nominal
tolerance, so check the crossover-frequency and Q bounds for ±5% capacitance
and actual gang tracking. X7R's capacitance-versus-bias and voltage-dependent
behaviour is not a sound basis for ranking film above C0G.
With equal R arms, `Q = 0.5 × sqrt(C_FEEDBACK/C_SHUNT)`; capacitor tolerance
alone permits approximately 0.672–0.744 when the three film parts vary
independently by ±5%. If all three shift together, Q stays nominal while
cutoff frequency changes by approximately −4.8% to +5.3%. These are bounds,
not a prediction of actual assembled parts or pot-gang tracking.

The current canonical XML identifies `C30`, `C37`, and `C41` as Panasonic
`ECH-U1H823JX9` and maps them through `CompType49` to `PatType21`. Its pads
are 1.3 × 3.0 mm on 4.3 mm centres, giving a 5.6 × 3.0 mm land envelope;
this matches Panasonic's recommended E2 land dimensions for the 4.8 × 3.3 mm
body. Verify this mapping in the eventual PCB export. The component-style
name still contains `MLCC` although the manufacturer identity specifies PPS
film; correct that misleading name before final BOM release.
[Panasonic ECHU(X) data sheet](https://industrial.panasonic.com/content/data/CP/PDF/Film/film_echux_e.pdf).

J1 exposes three electrical nodes for the two external pot gangs: pin 3 is
the first arm after R18, pin 2 is the junction of the gangs and C37/C41,
and pin 1 leads through R19 to U6.1's non-inverting input. The external
wiper/end straps described below must be made in the harness or at the pot.

Wire each pot gang for **clockwise-increasing cutoff frequency**: strap terminal 1
to the wiper, terminal 2, and use terminal 3 as the other rheostat connection;
repeat with terminals 1', 2', and 3' for the second gang. This gives maximum
track resistance at the fully counter-clockwise position and minimum resistance
at the fully clockwise position. If the wiper loses contact, the terminal-1-to-3
track remains in circuit at full resistance rather than opening the filter arm.
Confirm the resistance direction with an ohmmeter on the physical part before
wiring the panel harness, because interpreting a rear-view terminal drawing as a
front view would mirror the connections.

For control position \(\theta\), defined as the fraction of clockwise travel from
the fully counter-clockwise stop, the nominal resistance is

\[
R_1 = R_2 = 13.7\,\mathrm{k\Omega} + 20\,\mathrm{k\Omega}(1-\theta).
\]

This gives approximately 40.7 Hz fully counter-clockwise, 50.8 Hz at one-third
clockwise travel, 67.4 Hz at two-thirds clockwise travel, and 100.2 Hz fully
clockwise. Equivalently, 67.4 Hz corresponds to one-third of the pot's full
resistance remaining above its minimum-resistance end, not to one-third clockwise
travel from the counter-clockwise stop.

The part has PC pins and should be supported by its threaded panel bushing and
wired to the main board in the present arrangement. The relaxed through-hole
rule also permits direct PCB mounting if the finished panel/board geometry
supports the body without stressing the pins. Keep the wiring short if used
and away from Class-D switching nodes. The manufacturer's +50 °C
maximum operating temperature applies at the pot body and must be confirmed by
the thermal/mechanical layout.

For unity gain, the nominal relationships are:

```text
f0 = 1 / (2 pi sqrt(R1 R2 C_FEEDBACK C_SHUNT))
Q  = sqrt(R1 R2 C_FEEDBACK / C_SHUNT) / (R1 + R2)
```

When `R1 = R2` and `C_FEEDBACK = 2 C_SHUNT`, `Q = sqrt(2) / 2 = 0.707`.

The exact total resistances required for nominal 100 Hz and 40 Hz endpoints
are 13.724 kΩ and 34.310 kΩ respectively, an ideal variable span of
20.586 kΩ. The standard 13.7 kΩ fixed value and nominal 20 kΩ pot therefore
give approximately 100.2–40.7 Hz without a trim or selected resistor. Do not add
calibration hardware for the small nominal endpoint difference; measure the
assembled range and mark the panel scale accordingly.

Expected range:

- minimum R: approximately 100 Hz
- maximum R: approximately 41 Hz

TODO:

- verify exact transfer function/Q/frequency range in simulation
- measure both pot gangs end-to-end and through their travel because the
  data sheet specifies ±20% total resistance but no gang-tracking tolerance
- confirm the pot-body temperature remains at or below +50 °C

## 5 Level control

- mono
- post-LPF
- initial value: 10 kΩ logarithmic pot
- connected between LPF output and VMID
- wiper feeds differential-driver stage

In the current schematic J2 pin 1 is the U6.1 filter output, pin 3 is VMID,
and pin 2 is the pot wiper. The wiper feeds only U6.4's high-impedance
non-inverting input; R26 takes its signal from U6.4's output. The
previous 10 kΩ load on the pot wiper has therefore been removed. The exact
level-pot part and panel-terminal mapping remain to be selected and checked.

If the off-board wiper or its lead opens, `R20 = 1 MΩ` from `DIFF_IN` to
VMID biases the driver input towards minimum output. At full level its loading
of a nominal 10 kΩ pot changes the ideal maximum fraction from 1 to
`1 MΩ / (1 MΩ + 10 kΩ) = 0.990`, or −0.086 dB. This robustness
addition is present in the XML.

## 6 Polarity control

Provide user-selectable:

- 0°
- 180°

Preferred implementation:

- differential driver generates `+V` and `−V`
- DPDT switch swaps differential lines
- no unnecessary dedicated inverter stage

Polarity accounting: with the switch in its 0° position, connect the positive
differential-driver leg to `INPUT_A` and the negative leg to `INPUT_B`. The
stereo averaging summer in Section 3 has a gain of `−0.6` for equal correlated
left and right inputs. The differential driver preserves that sign in
`VDIFF = INPUT_A − INPUT_B`, and TI specifies the TPA3251 voltage gain as
inverting with a magnitude of 20 dB (nominally 10 V/V). The two inversions
therefore cancel: the 0° position gives the speaker voltage the same electrical
polarity as an in-phase RCA input. The 180° position swaps the two driver legs,
reverses `VDIFF`, and consequently reverses the speaker voltage. Here 0° and
180° refer to the end-to-end RCA-to-speaker electrical polarity; acoustic
polarity still depends on the loudspeaker's wiring and driver convention.

This is the intended switch mapping. Confirm the physical DPDT contact wiring
and speaker-terminal convention during schematic review and prototype
validation; the switch action itself does not establish which panel label is
connected to which contact.

Current J3 pin 1 carries U6.4's non-inverted driver output through R21, and
pin 2 carries U6.3's inverted driver output through R24. Pin 3 returns through
C64/R35 to `INPUT_A`, and pin 4 through C65/R36 to `INPUT_B`; C62/C63 provide
the local shunts. The external switch and harness must still provide and verify
the intended 0°/180° mapping.

## 7 Differential driver

Requirements:

- drive TPA3251 differentially
- target total differential voltage gain approximately 1.2
- approximate per-leg gain: ±0.6
- allow approximately 2 V RMS source to drive amplifier close to full power with level control at maximum

Preferred initial implementation:

- connect the level-pot wiper to an OPA167x unity-gain follower; its output is
  the positive driver leg;
- use the second OPA167x section as a unity-gain inverter about VMID, driven
  from the follower output;
- use generic 10.0 kΩ, 0.1%, 0805 thin-film resistors with temperature
  coefficient no worse than ±25 ppm/°C for both the inverter input and
  feedback resistors; and
- route the two outputs through the polarity switch, then through matched
  Würth `885012208124` 2.2 µF coupling capacitors and RF-isolation networks
  to TPA3251 `INPUT_A` and `INPUT_B`.

The current partial schematic feeds U6.2's inverter through R26 from U6.4's
buffered output and uses U6.3 as a final follower for the inverted leg. This
leaves both J3 drive legs buffered and removes the old level-pot loading.

If the level-pot wiper signal is `VMID + u`, the two outputs are

```text
VPLUS  = VMID + u
VMINUS = VMID - u
VDIFF  = VPLUS - VMINUS = 2u
```

Together with the summer's 0.6 gain for equal correlated stereo inputs, the
maximum end-to-end differential gain is nominally `2 × 0.6 = 1.2`. The level
pot controls `u` without its ±20% end-to-end resistance tolerance entering the
fixed gain calculation.

Ten-kilohm inverter resistors are preferred over 20 kΩ or 22 kΩ. With the
TPA3251's nominal 24 kΩ input resistance, the follower sees approximately
`10 kΩ || 24 kΩ = 7.06 kΩ` at signal frequencies, which is an easy load for
the OPA167x. At a 1.2 V RMS per-leg signal it supplies only about 170 µA RMS in
total to the inverter input and TPA3251 input. Increasing the inverter
resistors saves only tens of microamps while increasing their thermal-noise
contribution.

The TPA3251 has nominal 20 dB voltage gain. A 2 V RMS correlated stereo source
therefore produces approximately 2.4 V RMS differential at the TPA3251 input,
24 V RMS at the amplifier output, and 144 W into 4 Ω, before real-device
clipping and losses are included.

Use this matched network on each TPA3251 input leg:

```text
driver output -> polarity switch -> 885012208124 -> 100 Ω -> TPA3251 input
                                                        |
                                                      100 pF
                                                        |
                                               local TPA3251 ground
```

The nominal coupling pole set by 2.2 µF and the TPA3251's 24 kΩ input
resistance is 3.01 Hz. Its attenuation is approximately 0.10 dB at 20 Hz,
its time constant is 52.8 ms, and nominal 1% settling takes approximately
243 ms. These are acceptable in exchange for BOM consolidation and useful
margin before the provisional approximately 500 ms RESET release.

The 100 Ω series resistors and 100 pF shunt capacitors follow TI's
[TPA3251 EVM](https://www.ti.com/lit/ug/slau751/slau751.pdf) input treatment.
Their simple RC corner is approximately 15.9 MHz, so they
provide RF isolation without affecting the audio-band response. Use generic
100 Ω, ±1%, 0805 thin-film resistors and generic 100 pF, ±5%, C0G/NP0
capacitors rated for at least 25 V. Keep both legs geometrically symmetric,
place the 100 Ω resistors and 100 pF capacitors at the TPA3251 input pins, and
return the capacitors locally on the amplifier side rather than to VMID.
The 100 Ω resistor and nominal 24 kΩ input resistance also form a 0.9959
passband divider, adding approximately 0.036 dB loss. Including this and the
coupling pole, the receiving network alone loses approximately 0.13 dB at
20 Hz. The 47 Ω driver-output isolator adds approximately 0.017 dB, making
the complete nominal path loss approximately 0.15 dB at 20 Hz. Include that
small factor in the final gain simulation rather than increasing the nominal
front-end gain to compensate for it.

J3 drives an off-board polarity switch. The 100 Ω resistors at the
TPA3251 pins lie beyond that cable and do not isolate U6.3/U6.4 from its
capacitance. TI notes that a unity-gain OPA167x may lose phase margin with
heavier capacitive loading and gives 50 Ω as an example series isolator.
Fit matched approximately 47–51 Ω resistors close to the U6.3 and U6.4
outputs, outside their feedback loops, before the J3 cable. Keep R26 connected
on the U6.4 side of its isolator. With an assumed 24 kΩ amplifier-input load,
each 50 Ω isolator causes only about 0.018 dB passband loss; the actual
harness capacitance and transient stability still need checking.
[TI OPA1679 data sheet, Section 8.1.1](https://www.ti.com/lit/ds/symlink/opa1679.pdf).

R21 and R24 are the matched 47 Ω output isolators. J3 carries the two outgoing
driver legs and their two returns from the off-board switch. C64/C65 are the
matched 2.2 µF series coupling capacitors on the amplifier side of J3;
R35/R36 and C62/C63 form the two 100 Ω/100 pF receiving networks at the
TPA3251 pins. The capacitors block the approximately 7.5 V driver DC level
and let the amplifier establish its own input bias. The 47 Ω isolators serve
a different purpose and do not replace the receiving networks. The exact
R35/R36 0603 construction should be reconciled with the 0805 thin-film
preference above before the BOM is frozen.

TODO:

- assess the assembled 20–100 Hz distortion and effective low-frequency
  response with the selected Würth `885012208124` in all four coupling
  positions; compare with a film reference and revisit the choice if the
  capacitor contribution proves material;
- confirm 15 V analogue-rail headroom and differential symmetry in simulation;
- verify gain, clipping level, polarity switching, and quiescent differential
  DC during prototype validation.

## 8 Provisional front-end noise review

The following are calculated **white-noise estimates**, not measurements or a
whole-system noise verdict. Assumptions: 300 K, a connected low-impedance RCA
source, nominal component values, quiet VMID, OPA1679's typical 4.5 nV/√Hz
voltage-noise density at 1 kHz extended into the bass band, cutoff pot at its
nominal electrical midpoint (`R1 = R2 = 23.7 kΩ`, `f0 = 57.9 Hz`), and level
at maximum. The estimates exclude op-amp 1/f and pot excess/contact noise,
rail ripple, shared-return interference, the source's noise, and the now-drawn
TPA3251 input network. [TI OPA1679 data sheet](https://www.ti.com/lit/ds/symlink/opa1679.pdf).

For an ordinary resistor, `eR = sqrt(4 k T R)` V/√Hz. A 23.7 kΩ complete
filter arm therefore contributes about 19.8 nV/√Hz before the frequency-
dependent Sallen-Key transfer. At 50 Hz, the two independent arm-noise
contributions at U6.1's output are approximately 15.9 and 25.1 nV/√Hz;
their root-sum-square is 29.7 nV/√Hz. The differential driver doubles that
shared signal, making about 59 nV/√Hz at J3 from the filter arms alone.
Including the summer, filter op amp, and driver gives approximately
69 nV/√Hz differential at J3 at 50 Hz and 0.56 µV RMS integrated over
20–100 Hz. At minimum level, the driver itself remains and gives about
0.20 µV RMS over the same band.

The driver's 10 kΩ input and feedback resistors each contribute about
12.9 nV/√Hz; with its three op-amp sections, the estimated post-filter
differential floor is about 23 nV/√Hz. Because this noise is generated after
the low-pass stage, its flat-white extrapolation alone integrates to roughly
3.2 µV RMS over 20 Hz–20 kHz. This wide-band figure is not the predicted
loudspeaker noise: the TPA3251, input network, output filter, source, and
acoustic response are not yet included.

The 47 kΩ input-bias resistors are shunted by a connected low-impedance source
through the coupling capacitors over the bass band, so lowering them is not
the first useful noise change. Reducing the filter-arm resistance would require
larger capacitors and a different dual-gang pot for a small absolute gain.
Retain the present values provisionally; once the power stage is assembled,
separate broadband random noise from 50/100 Hz hum, buck switching products,
and amplifier self-noise in measurement before changing the front-end parts.
