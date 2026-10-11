# Prototype validation

> **State — current prototype checks; reviewed 2026-10-11.** Owns practical
> build verification. The auxiliary buck and regulators remain candidates;
> the two-supervisor RESET topology and dedicated buck divider are selected;
> 12 V LDO headroom remains to be checked at the loaded buck trough.

## 1 Mains construction and protective earth

Before first energisation:

- inspect line, neutral, and PE routing against the current schematic: the
  fuse is in line only, the switch opens line and neutral, and PE is neither
  switched nor fused;
- inspect every crimp and terminal for correct engagement, insulation, strain
  relief, conductor colour, absence of loose strands, and a firm pull-test;
- confirm the inlet rear cover and PSU terminal guard are fitted and that mains
  wiring cannot contact signal/DC wiring, sharp edges, or ventilation slots;
- confirm bare metal, serrated washer, fixed-stud nut, ring terminals, final
  washer, and all-metal locknut are present in the documented M4 PE stack; and
- with the unit unplugged, verify the inlet truth table: `OFF` opens both line
  and neutral to the PSU, `ON` closes both, and PE remains continuous in both
  positions.

Protective-bond acceptance:

- measure from the C14 PE pin to the farthest accessible point on the aluminium
  plate and separately to the RSP metal case/FG;
- pass at no more than 0.10 Ω after subtracting test-lead resistance, using a
  low-resistance tester supplying at least 200 mA;
- flex the protected wiring and operate the controls during the test; no
  discontinuity is permitted; and
- if a Class-I PAT tester is available, also perform its high-current earth-bond
  and insulation/leakage procedures. Do not improvise a mains hipot test.

First energisation must use a fused, RCD-protected outlet with all guards and
covers installed. Confirm 36 V DC output, correct switch operation, survival of
at least ten fully discharged cold starts at representative cold and warm
conditions, and absence of abnormal sound, smell, or heating. The RCD is
additional protection and does not replace the PE inspection and bond test.

## 2 Electrical

- input impedance vs frequency
- assembled 20–100 Hz analogue-path distortion at representative and maximum
  clean signal levels with the selected Würth `885012208124` coupling
  capacitors; if a material excess appears, compare with a film reference
  and measure effective capacitance at the actual DC biases before changing
  the part choice
- LPF frequency range
- LPF Q
- gain structure
- clipping level into 4 Ω
- output noise
- PWM residual
- MP4541GN candidate `17V3` output regulation, minimum loaded trough, ripple,
  load-step response, and switching spectrum at representative reset, idle,
  and driven auxiliary loads, including
  any interaction products with the TPA3251's nominal 600 kHz switching
- measure the actual 15 V analogue-rail load and XC6701 dropout/headroom at
  that load and the expected warm operating condition; note any analogue-rail
  droop before RESET without treating pre-dropout muting as a requirement
- verify the NCP1117 12 V regulator's effective output capacitance and ESR
  meet its stability requirements at the assembled voltage and temperature;
  check its thermal behaviour at the actual amplifier-rail load
- quiescent differential DC voltage at the post-filter loudspeaker output
- shared TPS3762 RESET timing at cold and warm start: remain low for at least
  400 ms after PVDD application and release only after the amplifier and
  analogue rails have settled
- peak and duration of post-filter loudspeaker-output transients during normal
  power-up, normal power-down, rapid off/on operation, and removal/restoration
  of mains power; define the numerical thump criterion before testing
- prompt RESET assertion as either 36 V PVDD or `17V3` decays; measure the
  buck monitor's falling and rising thresholds against its calculated divider
  limits, and verify at least 400 ms hold after an isolated buck interruption.
  Bound the instantaneous `17V3` trough and amplifier-feed/return drop against
  the calculated 0.47 V allowance above the NCP1117's 13.5 V specified
  input minimum; record both LDO outputs at RESET assertion
- correct diagnostic states at the `FAULT` and `CLIP_OTW` test points for safe,
  non-destructive conditions available during bring-up; do not inject a
  destructive output fault merely to exercise protection
- analogue-output and loudspeaker-output noise with the Class-D stage disabled,
  idle, and driven, to expose coupling across the combined-PCB partition
- check for common-mode/RF pickup on the balanced inter-domain pair before
  populating any optional mitigation footprints
- differential-drive symmetry
- polarity switching
- idle PVDD current
- PVDD and bootstrap switching-node ringing at the IC pins, using a probing
  method with sufficiently small loop area to assess the actual local
  capacitor/routing implementation rather than the probe loop

## 3 Thermal

- TPA3251 temperature
- aluminium plate temperature
- output-inductor temperatures
- Zobel resistor temperature
- auxiliary-regulator temperatures
- local air temperature at the lower intake, PSU intake, and upper exhaust
- unobstructed bottom-to-top flow with the finished grilles, feet/plinth,
  guards, covers, and wiring installed
- the defined continuous thermal test at 35 °C room ambient, within all
  component limits and the RSP-200-36 ambient-temperature/derating limit
- a 40 °C room-ambient assessment that records remaining margin or required
  derating without treating continuous full-power operation as a requirement

## 4 Acoustic

- before assembly, reconcile measured/CAD internal dimensions and every solid
  intrusion to demonstrate `20.0 L` geometric net front-chamber air volume;
  record wadding separately rather than crediting it as geometric volume
- verify the partition perimeter and driver-cable feed-through are airtight;
  investigate any impedance or low-frequency response evidence of a leak
- after driver break-in and final wadding installation, measure the installed
  impedance curve and derive actual system `Qtc` and `Fc`; compare them with
  the nominal predictions `Qtc = 0.574` and `Fc = 45.6 Hz`
- REW frequency response
- integration with mains
- required crossover setting
- driver excursion
- requirement for LF shelf/EQ
