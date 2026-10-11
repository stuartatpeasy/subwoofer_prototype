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
  Use the selected Würth `885012208124` 2.2 µF X7R capacitors at both RCA
  inputs and both amplifier inputs, followed by 100 Ω series and 100 pF C0G
  shunt parts at the TPA3251 input pins. The Würth part is confirmed for
  Rev-A assembly; review distortion and effective capacitance after assembly
  and compare with film if a material excess appears. Then confirm input
  sensitivity, common-mode conditions, symmetry, and 15 V analogue-rail
  headroom in simulation. The revised 7.5 V VMID gives approximately 1.26 V
  peak input common-mode margin for a 3 V RMS source at the first buffer.
- [ ] Finalise the TPA3251 surrounding passives from the TI PBTL reference
  design, including the `OC_ADJ` CB3C threshold resistor.
- [ ] Qualify the provisional three-per-position 220 nF, 250 V X7R
  output-filter bank in [power amplifier](POWER_AMPLIFIER.md) against the
  single 680 nF, 250 V comparison: confirm exact-part effective capacitance,
  PWM ripple heating/loss, peak voltage, and final layout, then lock the BOM.
- [ ] Select the exact Zobel parts and check pulse/continuous dissipation.
- [ ] Resolve the MP4541GN candidate buck review in
  [power and grounding](POWER_AND_GROUNDING.md): verify the revised U2 SOIC-8EP
  and C7–C9 1210 land dimensions; verify U2 pad 9 in the PCB netlist; define
  the buck's local switching-current return and output capacitance under bias
  and load/ripple.
- [ ] Verify the now-correct U1 NCP1117 pin 2/tab 4 `12VAMP` mapping in the PCB
  netlist.
  Check its 20 V input limit against the approximately 17.36 V buck's transient
  peaks; verify C2 effective capacitance and ESR for stability, and size its
  thermal copper for
  the actual 12 V load. Revise the proposed schematic to one `GND` net and
  remove unpopulated R1/R2 placeholders; resolve the `17V3` feed and local
  amplifier return route without carrying amplifier return through quiet
  analogue copper. Check the resulting RESET timing.
- [ ] Check the `XC6701DF02FR-G` 15 V analogue LDO's loaded dropout, heat,
  bypass requirements, and noise in the completed power tree.
- [x] Select two 36 V-powered `TPS3762-Q1` undervoltage supervisors with
  wire-ORed open-drain RESET outputs: fixed 30 V PVDD monitor and adjustable
  `17V3` monitor, with separate CTR capacitors for at least 400 ms after
  either detected fault.
- [ ] Select the CTR capacitors: a nominal 220 nF, ±10%, 50 V X7R is acceptable
  if manufacturer bias/ageing data establish at least 135 nF effective over
  tolerance and temperature; 330 nF X7R provides more margin but extends the
  nominal release delay to about 1.22 s.
- [x] Select the dedicated E24 buck SENSE divider: 130 kΩ/7.5 kΩ, 1%,
  separate from the MP4541 feedback path, gives approximately 14.67 V
  nominal falling. Analogue-LDO pre-dropout muting is not a requirement.
- [ ] Verify that the conservative lowest buck trip retains adequate margin
  above the NCP1117's 13.5 V specified input: the calculated allowance is
  0.47 V. Bound loaded buck trough, amplifier-feed/return drop, and RESET
  sequence. Recheck Mouser stock and normal stocking before ordering.
- [ ] Complete the buffered 7.5 V VMID. The current partial schematic has a
  10 kΩ/10 kΩ divider with 4.7 µF input filtering, a direct-feedback U5.3
  OPA1679 follower, and R5 = 10 Ω outside its feedback loop; it has no VMID
  shunt capacitor. Check loaded ceramic capacitance, source/sink current,
  noise, stability, and start-up. Add output filtering only if those checks
  identify a material need.
- [x] Remove the unnecessary VMID series paths and reference-filter capacitors;
  the current XML references U5.4 and U6.2 directly to VMID.
- [ ] Verify that the corrected C30/C37/C41 `PatType21` land pattern transfers
  to the PCB for the selected Panasonic `ECH-U1H823JX9` PPS-film part. Correct
  the misleading `MLCC` component-style name before BOM release; check ±5%
  capacitance tolerance and pot-gang tracking.
- [x] Feed U6.2's R26 from U6.4's output rather than the level-pot wiper; the
  current XML has removed the 10 kΩ wiper load.
- [x] Add the nominal 1 MΩ `DIFF_IN`-to-VMID wiper-fault bias (R20) and
  matched 47 Ω output isolators (R21/R24) near U6.3/U6.4 before the J3 cable;
  R26 remains on the U6.4 side of its isolator.
- [x] Add the TPA3251 differential-input coupling/RF networks (C64/C65,
  R35/R36, C62/C63) to both J3 returns.
- [ ] Verify actual J3 harness load, physical DPDT 0°/180° mapping, and
  terminal identification. Reconcile R35/R36 0603 parts with the documented
  0805 thin-film preference before BOM release.
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

- [ ] Review and validate the documented grounding, chassis, and
  protective-earth strategy, including every intentional and incidental
  conductive path in the assembled unit.
- [x] Lock the PCB architecture and layer count: one electrically partitioned
  four-layer board, with no two-layer fallback.
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
