# Action list

Complete these in dependency order. Items described as locked in the
[system specification](SPECIFICATION.md) should be reopened only if analysis,
simulation, or measurement shows that they cannot meet the acceptance criteria.

## 1 Complete the system specification

- [x] Confirm the SB23MFCL45-4 nominal parameters and physical envelope from the
  current traceable manufacturer datasheet.
- [ ] After break-in, measure the actual driver's small-signal parameters; the
  manufacturer publishes neither T/S tolerances nor cabinet displacement.
- [x] Lock the nominal external cabinet envelope at `390 × 390 × 390 mm`, with
  20.0 L net geometric front volume and the separate ventilated rear chamber.
- [ ] Complete a scaled electronics/airflow layout demonstrating that the PSU,
  PCB, inlet, guards, wiring, assembly access, and convection path fit within
  the locked rear-chamber envelope.
- [x] Select the exact 36 V main PSU and document its continuous/peak power,
  cooling, noise, protection, mechanical, and safety characteristics.
- [ ] Convert each item in [prototype validation](VALIDATION.md) into a
  measurable test method and numerical pass/fail criterion, including the
  operating and ambient conditions.
- [x] Define the mains-side implementation: inlet, fusing, switching, wiring,
  insulation/segregation, strain relief, protective-earth hardware, and
  enclosure-access assumptions.
- [x] Define the amplifier protection and fault policy: use the TPA3251's
  internal protection, permit user power-cycling for latched faults, provide no
  visible fault indicator or automatic retry, retain diagnostic test points,
  accept the residual PBTL DC-fault risk without an external disconnect, and
  use analogue RESET supervision for thump-controlled startup and shutdown.

## 2 Finalise and simulate the electronics

- [ ] Complete the preferred TPA3251 differential-input stage: use the
  summer's 10 kΩ input and 3.0 kΩ feedback resistors to set 0.6
  correlated-stereo gain, then
  a level-pot-wiper follower and a 10.0 kΩ/10.0 kΩ unity inverter about VMID.
  Use the now-selected Panasonic `ECW-FD2W225J4` 2.2 µF film capacitors at
  both RCA inputs C1/C6 and both amplifier inputs C11/C15, followed by
  100 Ω series and 100 pF C0G shunt parts at the TPA3251 input pins.
  Verify the four through-hole patterns and physical clearance during PCB
  layout. Then confirm input
  sensitivity, common-mode conditions, symmetry, and 15 V analogue-rail
  headroom in simulation. The revised 7.5 V VMID gives approximately 1.26 V
  peak input common-mode margin for a 3 V RMS source at the first buffer.
- [ ] Finalise the TPA3251 surrounding passives from the TI PBTL reference
  design, including the `OC_ADJ` CB3C threshold resistor.
- [ ] Qualify the now-placed C21/C22/C24/C25 Murata
  `GRJ21BC72A105ME11L` 1 µF, 100 V X7S PVDD bypass parts on `CAP_0805`:
  Murata's 25 °C, 1 V RMS model predicts only about 0.42 µF at 36 V.
  The 2.2 µF, 100 V, 0805 `GRM21BD72A225KE01L` model gives approximately
  0.7 µF at 36 V. Compare exact 1206 candidates against both 0805 parts using
  their own DC-bias and impedance data. The provisional Würth
  `885012208124` 2.2 µF, 100 V 1206 part predicts about 1.13 µF at 36 V,
  or 1.02 µF if −10% initial tolerance is applied to its typical bias curve.
  Check switching peaks, ripple suitability, short-loop placement, new pad
  geometry and the proposed 4 mm CNC-pocket clearance. TI's EVM uses nominal 1 µF 1206
  MLCCs, so no 1 µF *effective* threshold is established. The earlier Würth
  0805-on-0603 mismatch is no longer present in the saved schematic.
- [ ] Qualify the now-drawn pair of TDK `B32701P4684K000` 680 nF film
  output-filter capacitors C17/C30, one per combined speaker-output side, as
  described in [power amplifier](POWER_AMPLIFIER.md). Their saved pattern has
  the manufacturer-confirmed 10 mm lead pitch; check carrier ripple, capacitor
  temperature, peak voltage, response/damping and final physical placement
  before locking the BOM.
- [ ] Decide whether to retain the 250 V C19/C28 1 nF shunts and C16/C31
  10 nF Zobel capacitors or use suitable 100 V parts; confirm the final
  post-inductor voltage peaks and Zobel resistor/capacitor heating. Select
  the exact Zobel parts and check pulse/continuous dissipation.
- [ ] Resolve the MP4541GN candidate buck review in
  [power and grounding](POWER_AND_GROUNDING.md): verify the U5 SOIC-8EP
  and C42–C44 1210 land dimensions; verify U5 pad 9 in the PCB netlist; define
  the buck's local switching-current return and verify the approximately
  20.4 µF typical bias-adjusted C42–C44 bank estimate against loaded ripple,
  start-up and meaningful load transients. Add the user-selected fourth
  identical schematic position as unpopulated; fit it only if those checks
  show a material need. The current XML still contains only C42–C44.
- [ ] Verify the now-placed `U9 = L78M12ABDT-TR` DPAK footprint, pin mapping,
  ground tab, and thermal copper for the actual 12 V load. The selected C36
  Murata 1 µF, 100 V input ceramic exceeds 0.33 µF at 17.3 V bias on the
  user's part data; place it locally at U9's input and ground. C37 = 100 nF
  at the output is sensible alongside C8 = 470 µF and C9 = 100 nF.
  ST does not require an output capacitor for stability. Its 14.5 V specified
  minimum input is above the supervisor's calculated 13.97 V low trip: accept
  possible brief 12 V sag before RESET and check prototype `17V3`, `12VAMP`,
  and RESET waveforms rather than claiming pre-dropout muting. The schematic
  uses one `GND` net with R1/R2 removed; resolve the `17V3` feed and local
  amplifier return route without carrying amplifier return through quiet
  analogue copper. See [power and grounding](POWER_AND_GROUNDING.md).
- [ ] Check the `XC6701DF02FR-G` 15 V analogue LDO's loaded dropout, heat,
  bypass requirements, and noise in the completed power tree. The schematic
  now maps its SOT-223 VSS tab pad 4 to `GND`; verify this in the PCB netlist
  and provide suitable thermal copper.
- [ ] Retain the drawn `D1 = Yageo S1B` from `12VAMP` to `17V3`; verify its
  polarity, pattern and pulse-current path for a sudden `17V3` short with
  C8's 470 µF output bank. See [power and grounding](POWER_AND_GROUNDING.md).
- [x] Select two 36 V-powered `TPS3762-Q1` undervoltage supervisors with
  wire-ORed open-drain RESET outputs: fixed 30 V PVDD monitor and adjustable
  `17V3` monitor, with separate CTR capacitors for at least 400 ms after
  either detected fault.
- [x] Retain the placed KEMET `C0805C224K5RAC` 220 nF, ±10%, 50 V X7R
  CTR capacitors. Its bias curve and 3% per decade-hour ageing rate give a
  credible margin above 135 nF under the conservative example in
  [power amplifier](POWER_AMPLIFIER.md); the curve is typical, so this is not
  a formal worst-case guarantee. Check at least 400 ms RESET release on the
  prototype; reconsider 330 nF only if timing or margin requires it.
- [x] Select the dedicated E24 buck SENSE divider: 130 kΩ/7.5 kΩ, 1%,
  separate from the MP4541 feedback path, gives approximately 14.67 V
  nominal falling. Analogue-LDO pre-dropout muting is not a requirement.
- [ ] Bound loaded buck trough, amplifier-feed/return drop, and RESET
  sequence with the placed L78M12. The conservative 13.97 V buck trip is
  0.53 V below its 14.5 V specified input minimum, so allow possible brief
  12 V sag before RESET. The 18 V setpoint and revised supervisor divider are
  unselected candidates analysed in [power and grounding](POWER_AND_GROUNDING.md);
  revisit them only if loaded trough, analogue headroom or temperature warrants
  it. Recheck Mouser stock and normal stocking before ordering.
- [ ] Complete the buffered 7.5 V VMID. The current partial schematic has a
  10 kΩ/10 kΩ divider with 4.7 µF input filtering, a direct-feedback U1.3
  OPA1679 follower, and R32 = 10 Ω outside its feedback loop; it has no VMID
  shunt capacitor. Check loaded ceramic capacitance, source/sink current,
  noise, stability, and start-up. Add output filtering only if those checks
  identify a material need.
- [x] Remove the unnecessary VMID series paths and reference-filter capacitors;
  the current XML references U1.4 and U2.2 directly to VMID.
- [ ] Verify that the corrected C2/C4/C5 `PatType36` land pattern transfers
  to the PCB for the selected Panasonic `ECH-U1H823JX9` PPS-film part. Correct
  the misleading `MLCC` component-style name before BOM release; check ±5%
  capacitance tolerance and pot-gang tracking.
- [x] Feed U2.2's R11 from U2.4's output rather than the level-pot wiper; the
  current XML has removed the 10 kΩ wiper load.
- [x] Add the nominal 1 MΩ `DIFF_IN`-to-VMID wiper-fault bias (R6) and
  matched 47 Ω output isolators (R7/R12) near U2.3/U2.4 before the J3 cable;
  R11 remains on the U2.4 side of its isolator.
- [x] Add the TPA3251 differential-input coupling/RF networks to both
  polarity-switch returns; the current amplifier-input coupling parts are
  C11/C15.
- [x] Reconcile the analogue front-end reference designators in
  [FRONT_END.md](FRONT_END.md) with the newly renumbered schematic before BOM
  release; current RCA coupling is C1/C6 and amplifier-input coupling C11/C15.
- [x] Correct J5's placed purchasing fields: `Mfr part` is now
  `39-28-1023`, and Mouser `SKU` is `538-39-28-1023`.
- [ ] Run and inspect DipTrace ERC before PCB release, with unconnected-pin and
  short checks enabled where applicable. Both checks are now enabled in the
  saved XML, but it contains no ERC result; classify expected unused pins rather
  than treating every warning as a fault.
- [ ] Verify actual J3 harness load, physical DPDT 0°/180° mapping, and
  terminal identification.
- [ ] Verify the Sallen-Key filter transfer function, Q, adjustment range,
  component tolerances, and control tracking in simulation.
- [ ] Qualify the selected Bourns `PDB182-K420K-203B` 20 kΩ dual-gang linear
  crossover potentiometer by measuring both gangs and confirming that the
  panel-wired installation and +50 °C pot-body limit are met; select the level
  potentiometer.
- [ ] Finalise the input ESD/RF protection.
- [ ] Extend the provisional white-noise review in
  [analogue front end](FRONT_END.md) after the TPA3251 input network is fixed:
  include real VMID/rail noise, the source, pot contact/excess noise, amplifier
  self-noise, and the relevant measurement bandwidth. Compare J3 and speaker
  noise with the estimates before changing resistor values.

## 3 Complete the physical and safety design

- [ ] Implement and validate the selected common-`GND` layout, the one
  intended board-to-chassis bond, and the independent protective-earth paths.
  Account for intentional and incidental conductive contacts in the assembly;
  the conceptual single-net decision is closed.
- [x] Lock the PCB architecture and layer count: one physically partitioned
  four-layer board, with no two-layer fallback.
- [x] Select the latching, through-hole 36 V input and speaker-output
  connector pairs documented in [power and grounding](POWER_AND_GROUNDING.md)
  and [power amplifier](POWER_AMPLIFIER.md).
- [ ] Verify that the saved J6 three 36 V contacts and three GND contacts are
  allocated to the two amplifier pairs and one buck pair in the PCB and harness;
  verify both connector footprints, cable routes and clearances,
  strain support, polarity, and driver-end termination before PCB release.
  Recheck Mouser availability and purchasing terms before ordering.
- [ ] Select the exact fabricator stack-up, copper weights, dielectric spacing,
  finished thickness, via construction/plating, and detailed layer usage for
  the rear-mounted TPA3251 and whichever support parts are placed on each side.
- [ ] Finalise the aluminium-plate dimensions, mounting, finish exclusions,
  connector/control locations, and sealing details.
- [ ] Obtain JLCCNC confirmation of 6061 temper/6 mm stock, pocket and web
  geometry, and the drawing-defined bare thermal/PE/ground contact zones;
  check the 6061 heat-spreading budget before approving production geometry.
- [x] Establish the cabinet-bracing baseline: use the continuously bonded
  full-width/full-height partition as the sole brace; do not add speculative
  front-to-partition or window bracing.
- [x] Establish the front-chamber displacement allowance: use 1.0 L for the
  approximately 0.8 ± 0.2 L driver estimate, neglect the small cable gland or
  grommet, and keep partition-joint cleats on the electronics side.
- [ ] Select the lower and upper grille locations and net free areas, bottom
  clearance, foreign-object guarding, and unobstructed convection path.
- [ ] Produce a passive-cooling thermal-resistance budget from the stated
  15–18 W worst-case IC dissipation to the 35 °C maximum rated room ambient,
  including the package-to-PCB-to-plate interface and component hot spots; use
  40 °C as the margin/derating assessment case.
- [ ] Resolve the TPA3251 package, PCB, and rear-plate stack mechanically and
  thermally; verify contact-land height/flatness, TIM compression, pocket
  clearances for parts and trimmed through-hole leads, and the actual heat
  path against package and assembly drawings before laying out the board.

## 4 Build and validate

- [ ] Conduct design-rule reviews for schematic, PCB layout, mechanical fit,
  mains safety, grounding, and thermal design before fabrication.
- [ ] Build the Rev-A prototype and perform the documented electrical, thermal,
  and acoustic validation.
- [ ] Record measured results, deviations, corrective actions, and final
  as-built values in the documentation; update provisional statements only
  when evidence supports doing so.
