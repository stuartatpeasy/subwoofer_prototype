# Analogue front end

> **State — current design basis; coupling and filter parts checked 2026-10-13,
> controls identified and polarity switch selected 2026-10-31.** Owns the analogue
> signal path and its part choices; power rails and ground partitioning belong
> to [power and grounding](POWER_AND_GROUNDING.md). Read when changing the
> schematic front end. Current conclusions: retain R32 outside the VMID buffer
> feedback loop; the selected Panasonic PPS-film capacitors have the intended
> land pattern, the REAN RCA sockets and E-Switch polarity toggle are selected,
> and the J2 wiper-bias and J3 receiving networks are drawn.
> Next gate: verify external pot/switch wiring and panel-cable stability, then
> validate the assembled filter and noise. The XML is partial, and assembled
> performance has not been measured. Current signal-path reference labels were
> reconciled with the 2026-10-12 saved schematic; explicitly dated former
> labels remain only as historical context.

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

The current partial schematic uses U1.3, an OPA1679 unity-gain buffer, to generate
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
GND (quiet analogue region)
```

The two 10 kΩ legs present a 5 kΩ Thevenin resistance to the divider
capacitor. At its nominal 4.7 µF, the pole is 6.77 Hz, the time constant is
23.5 ms, and 1% settling takes approximately 108 ms. Actual ceramic
capacitance under 7.5 V bias remains to be checked. U1.3 has direct
output-to-inverting-input feedback. The separate `R32 = 10 Ω` lies between
that sensed output and VMID; there is no shunt capacitor directly on VMID.
The former 10 kΩ feedback resistor has been removed, consistent with the
[OPA1679's unity-gain stability](https://www.ti.com/lit/ds/symlink/opa1679.pdf).
Assess VMID noise, load current, and stability with the complete front end
before adding output filtering.

Keep R32 outside U1.3's feedback loop as the present baseline. Sensing VMID
after R32 would correct its small load-dependent voltage drop at low frequency,
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

The partial schematic has `C54` and `C55`, each 100 nF from `15VA` to
`GND`, for U1 and U2 respectively, and a separate nominal `C48 = 1 µF`
at the U6 15 V LDO output. With C54/C55 placed very close to the respective
op-amp supply pins and returned to the local analogue ground, this meets
TI's usual single-supply OPA1679 bypass recommendation: a 0.1 µF ceramic is
adequate in most cases. An additional 1 µF at either op amp is optional if the
15 V distribution becomes long or noisy, not required by the present partial
circuit. Torex recommends a 0.1–1 µF local output capacitor for load-step
response, although XC6701's internal compensation does not require one for
stability; check C48's effective capacitance under 15 V bias and place it near
U6. A remote op-amp capacitor does not replace U6's local capacitor. Sources:
[TI OPA1679 data sheet](https://www.ti.com/lit/ds/symlink/opa1679.pdf),
Sections 8.3–8.4, and [Torex XC6701 data sheet](https://product.torexsemi.com/system/files/series/xc6701.pdf),
Notes on Use.

### 1.4 VMID reference branches in the partial schematic

The 2026-10-06 canonical export confirms that the two former 1 µF local
reference-filter capacitors C18 and C23 have been removed. Previously,
R12/C18 and R13/C23 made separate nominal 3.39 Hz reference filters while
the level-pot bottom and other stages used unfiltered VMID. At J2's minimum
setting, its wiper equals VMID and U2.2's ideal differential output is
`2 × (VMID - Vref)`. A 0.5 mV VMID disturbance well above the former filter
pole would therefore have produced approximately 1 mV differential, not
0.5 mV. Removing the two shunt capacitors removes this mismatch mechanism.

The current XML has no separate series VMID reference-filter resistors. U2.2 and
U1.4 now take their non-inverting references directly from the common VMID
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
Panasonic ECW-FD2W225J4 2.2 µF film coupling capacitor
 |
47 kΩ to VMID
 |
OPA167x unity buffer
```

In the current partial schematic, U1.1 and U1.2 have direct output-to-inverting-
input feedback. The 47 kΩ resistors give their non-inverting inputs a DC path
to VMID. Adding 47 kΩ to each feedback path merely to balance typical
[OPA1679 input bias currents](https://www.ti.com/lit/ds/symlink/opa1679.pdf)
is not selected: 10 pA through 47 kΩ produces
only 0.47 µV of DC shift, while an added resistor contributes noise and can
interact with input capacitance. Revisit this only if measured DC offset
identifies a material need.

Those resistors are `R1` and `R9`. Their primary jobs are to set the
approximately 47 kΩ connected-source input load and provide the AC-coupled
inputs with a DC bias path. With the nominal 2.2 µF input capacitors, the
simple high-pass corner is 1.54 Hz. They are not the main control on
left/right isolation: a low-impedance VMID buffer and deliberate shared-return
layout matter more. The resistor's open-input Johnson voltage-noise density
is about 28 nV/√Hz at room temperature; with a connected low-impedance source,
that resistor is shunted by the source through the coupling capacitor and its
actual input-node noise contribution is smaller. Changing 47 kΩ solely to
reduce an assumed noise or crosstalk figure is not selected.

The current schematic selects Panasonic `ECW-FD2W225J4` (2.2 µF, ±5%,
450 V, metallised polypropylene, radial lead, 7.5 mm pitch) for both RCA
coupling positions C1/C6 and both TPA3251 input positions C11/C15. This
supersedes the earlier Würth `885012208124` X7R selection. Film removes the
Class 2 ceramic voltage-coefficient uncertainty; an audible or measured
distortion improvement in this circuit has not yet been established. Verify
the four through-hole patterns and rear-plate clearance during PCB layout.
[Panasonic part data](https://industrial.panasonic.com/ww/products/pt/film-cap-electroequip/models/ECWFD2W225J4).

**First-prototype RCA protection decision, 26 October 2026.** Retain the
saved coupling, input bias and RF network without adding a dedicated RCA
input ESD suppressor before bare-board fabrication. The capacitor blocks
steady external DC and the series/RF parts limit high-frequency coupling,
but these functions do not establish a quantified ESD immunity level.
Revisit protection if prototype handling or susceptibility observations
show a material problem.

The previously considered Rubycon `16MF225KA23216` and Kyocera AVX
`CB162D0225JBC` film alternatives remain unselected; their different land
patterns would need checking before substitution.

**2026-10-11 film reassessment (historical; substitution made 2026-10-13).** The
schematic labels the RCA coupling capacitors C1/C6 and the amplifier-input
coupling capacitors C11/C15; earlier references C25/C42 and C64/C65 in this
discussion predate the schematic renumbering (reference check 2026-10-12).
These were the four X7R
capacitors carrying bass-band signal. At nominal
2.2 µF, the magnitude of their reactance at 20 Hz is 3.62 kΩ. With a
low-impedance 3 V RMS RCA source, approximately 0.23 V RMS appears across
each RCA coupling capacitor (47 kΩ return plus 1 kΩ input series resistor).
For a 1.8 V RMS driver leg, approximately 0.27 V RMS appears across each
amplifier-input capacitor (nominal 24 kΩ input). These are illustrative
worst-clean-level calculations, not measured distortion; the actual voltage
increases if DC bias reduces the effective X7R capacitance. Film removes this
voltage-dependent-capacitance uncertainty, but no audible or measured
improvement has been established in this circuit. A 2.2 µF film part is a
reasonable pre-layout substitution if its footprint and rear-plate clearance
are acceptable. Polypropylene is not required solely for low distortion:
TI's AC-coupling comparison found no significant performance difference among
the film dielectrics it tested. Keep both amplifier-input legs the same value
and type, and verify the chosen part's voltage rating at the actual DC bias.
[TI capacitor distortion study](https://www.ti.com/lit/an/slyt796a/slyt796a.pdf).

**2026-10-11 input-value check (historical alternatives; C1/C6 remain 2.2 µF).**
Using the 47 kΩ bias resistor alone, 1.0 µF gives a 3.39 Hz pole and
0.123 dB capacitor-related loss at 20 Hz relative to the input's midband
gain; with a −10% film capacitor and −1% bias resistor, that loss is
0.154 dB. The separate 1 kΩ/47 kΩ midband divider loses about 0.18 dB
irrespective of capacitance. This is small, but a corner below 20 Hz does not
mean zero loss at 20 Hz. Defining a strict input-stage budget of 0.10 dB
at 20 Hz gives a maximum pole of 3.05 Hz. With the same tolerances, the
nominal capacitance must be at least 1.25 µF; 1.5 µF ±10% film gives
0.069 dB worst-case loss. At a looser 0.20 dB input-stage budget, 1.0 µF
±10% is sufficient. The existing 2.2 µF amplifier-input coupling adds
approximately 0.10 dB nominally at 20 Hz on each signal path, independent
of this choice. Do not count both RCA coupling capacitors as cascaded poles:
each source traverses only its own input capacitor before summing. The
1 kΩ RCA series resistor slightly lowers the input pole; the calculations
above omit it conservatively. The 2026-10-13 film selection retains 2.2 µF.

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

Assess the assembled low-frequency response as part of normal prototype
validation. The selected Panasonic film part has a distinct through-hole
pattern; verify its 7.5 mm pitch and physical clearance on the PCB.

Requirements:

- source must see a benign, well-defined load
- no dependence on source-specific output impedance
- input protection should not add significant capacitance/distortion

### 2.1 Selected RCA panel sockets, 31 October 2026

The selected pair is REAN `NYS367-9` (white, left; Mouser `568-NYS367-9`)
and `NYS367-2` (red, right; Mouser `568-NYS367-2`), one of each. These are
female panel-mount RCA jacks with gold-plated contacts and solder terminations.
They suit the 2 V RMS nominal / 3 V RMS clean-input target and the nominal
47 kΩ input load. The manufacturer's present product page specifies at most
10 mΩ contact resistance: even if all of that appeared in series with a
47 kΩ input, its fractional voltage loss would be below `0.01/47000`, or
0.000022%. Gold contacts are appropriate for a low-current audio input. This
is an electrical suitability assessment, not an assembled noise or contact
test. [REAN product and variant data](https://www.rean-connectors.com/en/product/nys367-1),
[Mouser red listing](https://www.mouser.co.uk/en/ProductDetail/REAN/NYS367-2?qs=R5cXQUTKuHXVYwwK%252BeCprA%3D%3D),
[Mouser white listing](https://www.mouser.co.uk/ProductDetail/REAN/NYS367-9?qs=R5cXQUTKuHUWHl83AlgzLg%3D%3D).

**Mechanical condition:** the manufacturer's NYS367 sheet specifies a
maximum 3 mm panel thickness. The current 1.6 mm insulating FR-4 control
panel meets that nominal limit; the earlier unrelieved 12 mm plywood wall
did not. The panel support, supplied insulating washers, nut engagement and
wiring clearance remain to be checked
on purchased parts before cutting. This is an implementation check, not a
remaining part-selection gate. The [mechanical authority](MECHANICAL.md#3-rear-panel-structure)
owns the land; [power and grounding](POWER_AND_GROUNDING.md#8-rca-inputs)
owns isolation from the aluminium plate and PE.
[SketchUp layout models](3d_models/Rear-signal-parts.md) record the drawing
dimensions and inferred features for both sockets.
[Manufacturer-branded NYS367 technical sheet](https://static.rapidonline.com/pdf/12-8301_v1.pdf),
[REAN variant drawing](https://www.rean-connectors.com/media/15033/download/NYS367-9.pdf?v=1).

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

The current U1.4 stage uses `R3/R13 = 10 kΩ` inputs and `R8 = 3 kΩ`
feedback; its non-inverting input connects directly to VMID, with no
shunt filter capacitor. There is no feedback capacitor. One could add
approximately 1 nF C0G/NP0 in parallel with R8 for a 53 kHz pole if pre-filter
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
- selected `rev0` part: Bourns `PDB182-K420K-203B` 20 kΩ dual-gang linear pot;
  the user confirmed retention of its PC-pin terminals on 31 October 2026
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

The current canonical XML identifies `C2`, `C4`, and `C5` as Panasonic
`ECH-U1H823JX9` and maps them through `CompType83` to `PatType36`. Its pads
are 1.3 × 3.0 mm on 4.3 mm centres, giving a 5.6 × 3.0 mm land envelope;
this matches Panasonic's recommended E2 land dimensions for the 4.8 × 3.3 mm
body. The saved PCB has the corresponding 1.3 × 3.0 mm lands on 4.3 mm centres;
its internal pattern number differs but the geometry matches. The saved
component-style name now identifies PPS film rather than MLCC.
[Panasonic ECHU(X) data sheet](https://industrial.panasonic.com/content/data/CP/PDF/Film/film_echux_e.pdf).

**2026-10-13 dielectric check.** These three placed parts are already PPS
film chips, not MLCCs. Replacing them with through-hole polypropylene offers
no established distortion benefit here. Preserve the selected PPS parts and
the compact filter layout. The 26 October saved library/CAD update closed
the misleading-name task; this dated dielectric conclusion remains unchanged.

J1 exposes three electrical nodes for the two external pot gangs: pin 3 is
the first arm after R4, pin 2 is the junction of the gangs and C4/C5,
and pin 1 leads through R5 to U2.1's non-inverting input. The external
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

The current part has PC pins and mounts by its threaded bushing in the 1.6 mm
FR-4 control panel, with a supported harness to the main board. Keep the
wiring short and clear of Class-D switching nodes. The manufacturer's +50 °C
maximum applies at the pot body, which still needs a finished-chamber check.

For a temperature-induced fractional change `x` in both pot gangs' resistance
at a fixed shaft position, with the PCB resistors and capacitors unchanged,
the equal-arm cutoff changes by the exact factor
`(13.7 kΩ + Rp)/(13.7 kΩ + Rp(1 + x))`, where `Rp` is that position's nominal
pot resistance. For small `x`, `Δf/f ≈ -[Rp/(13.7 kΩ + Rp)]x`.
The factor is 0.593 at the 40.7 Hz end (`Rp = 20 kΩ`) and falls to zero at
the 100.2 Hz end (`Rp = 0`). For illustration only, a 1% track-resistance
change would move the 40.7 Hz end by approximately 0.24 Hz. The
[Bourns PDB18 data sheet](https://www.bourns.com/docs/product-datasheets/pdb18.pdf)
specifies no track temperature coefficient or thermal gang-tracking limit.
This is a sensitivity calculation, not a predicted drift or guaranteed bound. The
actual pot-body temperature, PCB component temperatures, and assembled response
remain to be checked. The 50 °C body limit leaves 15 K above the 35 °C rated
room ambient, or 10 K above the 40 °C thermal-margin case.

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

### 4.1 Solder-lug alternatives and resistance scaling, 31 October 2026

The user accepted the present 20 kΩ `PDB182-K420K-203B` PC-pin terminals
on 31 October 2026. The following comparison records why changing resistance
would also affect the filter; a resistance change is possible **only with two gangs that vary
together approximately linearly**. The current `rev0` schematic, PCB and
fabrication archive retain 13.7 kΩ arms and three 82 nF capacitors; the
alternatives below are not a selected circuit revision.

For matched gangs, write each arm as `R = R_FIXED + R_POT`. With
`C_FEEDBACK = 2 C_SHUNT`, the unity-gain Sallen-Key equations above reduce to
`f0 = 1/(2π R sqrt(C_FEEDBACK C_SHUNT))` and `Q = 0.707`.
Increasing either arm resistance lowers the frequency. Changing the pot
resistance alone therefore changes the *low* endpoint while the high endpoint
stays set by `R_FIXED`. To retain a 100:40 = 2.5:1 span,
`(R_FIXED + R_POT_MAX)/R_FIXED ≈ 2.5`, so
`R_FIXED ≈ R_POT_MAX/1.5`. Keeping the high endpoint near 100 Hz then requires
capacitors to scale inversely with that fixed resistance, while preserving
their 2:1 ratio to retain Butterworth Q.

| Hypothetical matched linear dual pot | Current 13.7 kΩ / 82 nF / 164 nF gives | Approximate retune for 40–100 Hz | Retuned nominal endpoints |
| --- | --- | --- | --- |
| 10 kΩ | 57.9–100.2 Hz | 6.8 kΩ in each fixed arm; 164 nF shunt, 328 nF feedback | 40.8–100.9 Hz |
| 20 kΩ current | 40.7–100.2 Hz | 13.7 kΩ; 82 nF shunt, 164 nF feedback | unchanged |
| 50 kΩ | 21.5–100.2 Hz | 34.0 kΩ in each fixed arm; 33 nF shunt, 66 nF feedback | 40.6–100.3 Hz |

The 10 kΩ retune could use `2 × 82 nF` in the shunt and `4 × 82 nF` in
feedback, versus the present three footprints total. The 50 kΩ retune needs
smaller capacitors; Panasonic lists 33 nF 50 V PPS in a different package from
the placed 82 nF part. Neither retune is a drop-in component swap on the
released board. Matching the gangs remains important: the general equation
above shows that unequal arms reduce Q below 0.707 as well as moving f0.
[Panasonic ECHU(X) catalogue](https://industrial.panasonic.com/cdbs/www-data/pdf/RDI0000/ABD0000C173.pdf).

A genuine matched-linear 50 kΩ pot could instead be shunted across each
variable gang with about 33.3 kΩ: `50 kΩ || 33.3 kΩ ≈ 20 kΩ` at its maximum.
This nominally preserves the present endpoints and capacitors, but compresses
the frequency scale: halfway through rotation the filter would be about 49 Hz,
versus about 58 Hz for the current 20 kΩ linear control. It needs two matched
external resistors and still requires gang and wiring checks. This is an
exploratory harness option, not a replacement decision.

The two Mouser numbers raised by the user,
[10 kΩ `652-PDB182-GTRB2-103`](https://www.mouser.co.uk/en/ProductDetail/Bourns/PDB182-GTRB2-103MN)
and [50 kΩ `652-PDB182-GTRB2-503`](https://www.mouser.jp/en/ProductDetail/Bourns/PDB182-GTRB2-503MN),
resolve to manufacturer variants ending **`MN`**. Bourns calls the GTRB2 a
blend/balance guitar control with a centre detent: its M gang changes over the
first half of rotation and then stays constant, while its N gang stays constant
over the first half and changes over the second. They are **not matched linear
dual gangs**, despite the catalogue's generic `Linear` attribute. In the
present wiper-to-end rheostat wiring, one filter arm moves in each half-turn;
the response would rise towards the centre and fall again, with Q varying.
For illustration with unchanged 13.7 kΩ/82 nF/164 nF parts, the 50 kΩ MN
option gives approximately `f0 = 46.5 Hz, Q = 0.54` at either end and
`f0 = 100.2 Hz, Q = 0.707` at centre. Do not substitute either GTRB2 part for
the current control. [Bourns GTRB datasheet](https://www.bourns.com/docs/product-datasheets/pdb182-gtrb.pdf),
[Bourns blend/balance application note](https://www.bourns.com/docs/technical-documents/technical-library/sensors-controls/application-notes/Bourns_PDB182_Blend-Balance_Guitar_Pots_AppNote.pdf).

## 5 Level control

- mono
- post-LPF
- selected part: Bourns `PDB181-E420K-103A2`, 10 kΩ single-gang audio
  taper, rear-facing solder lugs; the 1.6 mm FR-4 panel provides a thin land
- connected between LPF output and VMID
- wiper feeds differential-driver stage

In the current schematic J2 pin 1 is the U2.1 filter output, pin 3 is VMID,
and pin 2 is the pot wiper. The wiper feeds only U2.4's high-impedance
non-inverting input; R11 takes its signal from U2.4's output. The
previous 10 kΩ load on the pot wiper has therefore been removed. The user
identified `PDB181-E420K-103A2` on 31 October 2026. Its Bourns PDB18 drawing
gives a 17 mm body, M7 × 0.75 bushing with only 6.5 mm exposed length,
20 mm shaft projection and rear-facing solder lugs. The [3D layout
models](../../Hub/3d_models/electronics/PDB18-family/README.md) record the nominal envelope. The
J2-to-terminal mapping, clockwise level direction and assembled pot-body
temperature still require checking. The bushing needs a thinner mounting
section; the current 1.6 mm FR-4 panel supplies it. [Mechanical design](MECHANICAL.md)
owns that arrangement.

If the off-board wiper or its lead opens, `R6 = 1 MΩ` from `DIFF_IN` to
VMID biases the driver input towards minimum output. With an intact nominal
10 kΩ pot, full level still connects the wiper directly to `FILT_OUT`, so its
ideal fraction remains 1. At the electrical midpoint, the lower 5 kΩ half
is shunted by 1 MΩ: `(5 kΩ || 1 MΩ) / (5 kΩ + (5 kΩ || 1 MΩ)) ≈ 0.4988`
instead of 0.5. This robustness addition is present in the XML.

At a fixed wiper position, a uniform temperature-driven change of the entire
track resistance cancels from an ideal unloaded voltage-divider ratio. With
the present 1 MΩ bias resistor, loading is small: at the electrical midpoint
of a nominal 10 kΩ track, a 1% uniform track-resistance change alters the
output fraction by approximately 0.0000124, or 0.0025% of the half-level
output. This is an illustrative circuit sensitivity, not a bound on the
selected pot's temperature-dependent taper or contact behaviour.

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

Current J3 pin 1 carries U2.4's non-inverted driver output through R7, and
pin 2 carries U2.3's inverted driver output through R12. Pin 3 returns through
C11/R16 to `INPUT_A`, and pin 4 through C15/R17 to `INPUT_B`; C14/C18 provide
the local shunts. The external switch and harness must still provide and verify
the intended 0°/180° mapping.

### 6.1 Dailywell polarity-switch candidate, 31 October 2026

Mouser `118-1MD1T2B3M1QES` is Dailywell `1MD1T2B3M1QES`, a maintained
two-position DPDT panel toggle with six solder lugs. The manufacturer's 1M
series drawing identifies `1MD1` as ON–ON, `T2` as the short actuator, `B3`
as a 7.10 mm threaded 1/4-40 UNS bushing, `M1` as solder lugs and `Q` as
silver-plated contacts/terminals. The 1M series is rated −40 to +85 °C.
This was the first **functional candidate, not a selected switch**; the
gold-contact E-Switch in §6.2 has since been selected.
[Dailywell 1M series datasheet](https://datasheet.lcsc.com/lcsc/2304140030_Dailywell-1M31T1B1M1QES-5_C545198.pdf),
[Mouser listing](https://www.mouser.co.uk/ProductDetail/Dailywell/1MD1T2B3M1QES).

The published contact table gives common terminals 2 and 5. One position
closes 2–3 and 5–6; the other closes 2–1 and 5–4. A proposed four-wire
cross-over harness connects J3 pin 3 (`INPUT_A` return) to 2, pin 4
(`INPUT_B` return) to 5, J3 pin 1 (`VPLUS`) to both 3 and 4, and J3 pin 2
(`VMINUS`) to both 1 and 6. The first switch position then passes the legs
straight; the second swaps them. These are schematic terminal numbers, not
an established front-panel lever direction: check continuity and label the
actual part after mounting.

The switch is before the two 2.2 µF input coupling capacitors, so its contacts
sit at approximately 7.5 V common-mode potential but carry essentially no
steady DC current.
At a representative 1.2 V RMS signal per leg and nominal 24 kΩ amplifier
input, the audio current is only about `1.2/24000 ≈ 50 µA RMS`. The specified
initial 10 mΩ contact resistance would have negligible signal loss; the
question is whether silver contacts remain consistently conductive at such
low current after storage and use. Dailywell specifies `Q` for power contacts
and recommends gold for precision, low-level circuits because it resists
oxidation. No minimum reliable load or low-current contact-life guarantee was
found for this silver variant. A gold-contact ON–ON DPDT with solder lugs is
preferable for a repeatable build; this candidate could be tried in a
prototype if the contact behaviour is checked in the assembled signal path.
[Dailywell contact-material guidance](https://www.dailywell.com.tw/en/faq/Dailywell-FAQ-02.html).

The 7.10 mm bushing cannot clamp the full 12 mm rear plywood. A local recess
must leave enough exposed thread for the supplied nut and lockwasher, with
wood strength and rear lug/harness clearance checked before drilling. The
[mechanical authority](MECHANICAL.md#3-rear-panel-structure) owns that fit.

### 6.2 Selected E-Switch gold-contact switch, 31 October 2026

Mouser `612-100-F1112` resolves to E-Switch `100DP1T1B1M1REH`. The
manufacturer's 100-series code and drawing specify maintained `DP1` DPDT
ON–ON action, `T1` standard actuator, `B1` 8.89 mm threaded 1/4-40 UNS
bushing, `M1` solder lugs, `R` gold contacts, `E` epoxy terminal seal, and
`H` mounting hardware. The gold-contact rating is **0.4 VA maximum at
20 V maximum** (AC or DC); the operating temperature range is −40 to +85 °C.
This is the **selected polarity switch**. FR-4 panel fit and a continuity check
on the purchased part remain implementation checks, not selection gates.
[E-Switch 100-series datasheet](https://www.e-switch.com/wp-content/uploads/2024/05/100-1.pdf),
[Mouser listing](https://www.mouser.com/ProductDetail/E-Switch/100DP1T1B1M1REH).

The `DP1` terminal map is the same as the Dailywell switch above: commons
2 and 5; one position closes 2–3/5–6 and the other 2–1/5–4. The four-wire
J3 cross-over harness and two local jumpers described in §6.1 therefore
apply without a circuit or PCB change. The switch still sits at about 7.5 V
common-mode potential with no steady DC contact current. At the illustrative
1.2 V RMS per-leg signal and 24 kΩ load, about 50 µA RMS is **60 µVA** of
signal power per leg, far below the 0.4 VA contact limit; the highest
illustrative instantaneous leg potential is roughly `7.5 + 1.2√2 ≈ 9.2 V`,
below 20 V. Gold contacts are better suited to this dry signal circuit than
the previous silver-contact candidate, though neither part's listing proves
the finished harness or contact behaviour.

The 8.89 mm bushing is longer than the Dailywell candidate's 7.10 mm, and
the current 1.6 mm FR-4 panel provides a thin mounting land. Check the actual supplied
hardware, thread engagement, keyway, lever access and rear solder-lug
clearance before cutting. [Mechanical design](MECHANICAL.md#3-rear-panel-structure)
owns the mounting arrangement. The [SketchUp switch model](3d_models/Rear-signal-parts.md)
is a layout reference for that work.

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
  Panasonic `ECW-FD2W225J4` 2.2 µF coupling capacitors and RF-isolation networks
  to TPA3251 `INPUT_A` and `INPUT_B`.

The current partial schematic feeds U2.2's inverter through R11 from U2.4's
buffered output and uses U2.3 as a final follower for the inverted leg. This
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
driver output -> polarity switch -> ECW-FD2W225J4 -> 100 Ω -> TPA3251 input
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
100 Ω, ±1% resistors; the existing 0603 footprints for R16/R17 are suitable.
Use generic 100 pF, ±5%, C0G/NP0
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
TPA3251 pins lie beyond that cable and do not isolate U2.3/U2.4 from its
capacitance. TI notes that a unity-gain OPA167x may lose phase margin with
heavier capacitive loading and gives 50 Ω as an example series isolator.
Fit matched approximately 47–51 Ω resistors close to the U2.3 and U2.4
outputs, outside their feedback loops, before the J3 cable. Keep R11 connected
on the U2.4 side of its isolator. With an assumed 24 kΩ amplifier-input load,
each 50 Ω isolator causes only about 0.018 dB passband loss; the actual
harness capacitance and transient stability still need checking.
[TI OPA1679 data sheet, Section 8.1.1](https://www.ti.com/lit/ds/symlink/opa1679.pdf).

R7 and R12 are the matched 47 Ω output isolators. J3 carries the two outgoing
driver legs and their two returns from the off-board switch. C11/C15 are the
matched 2.2 µF series coupling capacitors on the amplifier side of J3;
R16/R17 and C14/C18 form the two 100 Ω/100 pF receiving networks at the
TPA3251 pins. The capacitors block the approximately 7.5 V driver DC level
and let the amplifier establish its own input bias. The 47 Ω isolators serve
a different purpose and do not replace the receiving networks. R16/R17 need
no 0805 or thin-film requirement: their signal current and
dissipation are negligible, and 0603 permits compact, symmetric placement at
the amplifier inputs.

TODO:

- check the four selected film capacitor footprints and clearance during PCB
  layout, then assess the assembled low-frequency response;
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
contributions at U2.1's output are approximately 15.9 and 25.1 nV/√Hz;
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
