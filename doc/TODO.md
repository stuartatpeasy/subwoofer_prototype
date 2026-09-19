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

- [ ] Finalise the TPA3251 differential-input stage, including exact gain,
  input sensitivity, common-mode conditions, and 12 V rail headroom.
- [ ] Finalise the TPA3251 surrounding passives from the TI PBTL reference
  design, including the `OC_ADJ` CB3C threshold resistor.
- [ ] Select the exact output-filter MLCC bank using capacitance-under-bias,
  tolerance, ripple-current/loss, voltage, and package data.
- [ ] Select the exact Zobel parts and check pulse/continuous dissipation.
- [x] Select the XP Power `STH0548S15` non-isolated 15 V converter and limit
  the combined project load on its output to 250 mA.
- [ ] Finalise the populated STH0548S15 external EMI network. The exact Bourns
  `SRR7045-560M` 56 µH inductor, local input capacitor, direct output capacitor,
  and two post-regulator input networks are defined. Provisionally use four
  Würth Elektronik `885012208124` 2.2 µF, 100 V, X7R, 1206 capacitors, using
  approximately 0.99 µF effective capacitance each at 40 V for preliminary
  analysis. Select a generic 22 µF, 63 V-minimum aluminium electrolytic and
  measure its ESR near 10–20 kHz and at 100 kHz. Resolve damping using the
  measured values, verify ripple/ringing on Rev A, and keep the complete final
  15 V capacitance within 100 µF.
- [x] Select `LM2937ESX-12/NOPB` for `12V_AMP`, with a 0 Ω default input link
  and a reserved 3.3 Ω measured-noise option.
- [x] Select a second `LM2937ESX-12/NOPB` for `12V_ANA`, with a fitted 10 Ω
  input RC prefilter.
- [x] Define the power-tree capacitor requirements: use substitution-safe
  generic specifications where the required properties adequately define the
  part, and exact parts where parasitics or bias behaviour matter.
- [x] Select KEMET `EEV226M035S9DAA` 22 µF, 35 V SMD aluminium electrolytics
  for both LM2937 input reservoirs and both regulator output capacitors.
- [x] Select KEMET `C1206C104K1RAC7867` 100 nF, 100 V, X7R, 1206 MLCCs for
  the STH0548S15 input/output and both LM2937 input bypass positions.
- [ ] Measure an `EEV226M035S9DAA` sample at 100 kHz and confirm ESR is
  0.01–3 Ω; confirm from manufacturer data or further measurement that
  capacitance and ESR remain compliant over the project temperature range.
- [ ] Characterise an `LM2937ESX-12/NOPB` sample's dropout at 25 °C and 50,
  75, 100, 125, 150, 175, and 200 mA, then use the measured curve when
  finalising the TPS3842 threshold.
- [x] Select the Texas Instruments `TPS3842A011DRLR` analogue RESET supervisor;
  accept its exposed-lead, 0.50 mm-pitch SOT-5X3 package and confirm Mouser
  single-unit availability before ordering.
- [ ] Finalise the TPS3842 SENSE divider, `CTR` delay capacitor, RESET pull-up
  network, and any SENSE filtering. The former 13.44 V divider seed is rejected;
  validate the current approximately 13.9 V seed against measured loaded
  LM2937 dropout and minimum 15 V rail voltage before locking it.
- [ ] Design the buffered 6 V VMID and check its source/sink current, noise,
  start-up, stability, and decoupling.
- [ ] Verify the Sallen-Key filter transfer function, Q, adjustment range,
  component tolerances, and control tracking in simulation.
- [ ] Select the crossover and level potentiometers.
- [ ] Finalise the input ESD/RF protection.

## 3 Complete the physical and safety design

- [ ] Review and validate the documented grounding, chassis, and
  protective-earth strategy, including every intentional and incidental
  conductive path in the assembled unit.
- [x] Lock the PCB architecture and layer count: one electrically partitioned
  four-layer board, with no two-layer fallback.
- [ ] Select the exact fabricator stack-up, copper weights, dielectric spacing,
  finished thickness, via construction/plating, and detailed layer usage for
  the rear-mounted TPA3251 and front-side support components.
- [ ] Finalise the aluminium-plate dimensions, mounting, finish exclusions,
  connector/control locations, and sealing details.
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
  thermally; verify clearances and the actual heat path against package and
  assembly drawings before laying out the board.

## 4 Build and validate

- [ ] Conduct design-rule reviews for schematic, PCB layout, mechanical fit,
  mains safety, grounding, and thermal design before fabrication.
- [ ] Build the Rev-A prototype and perform the documented electrical, thermal,
  and acoustic validation.
- [ ] Record measured results, deviations, corrective actions, and final
  as-built values in the documentation; update provisional statements only
  when evidence supports doing so.
