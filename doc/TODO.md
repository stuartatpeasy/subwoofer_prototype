# Action list

Complete these in dependency order. Items described as locked in the
[system specification](SPECIFICATION.md) should be reopened only if analysis,
simulation, or measurement shows that they cannot meet the acceptance criteria.

## 1 Complete the system specification

- [ ] Confirm the driver parameters from traceable manufacturer data and, when
  hardware is available, measure the actual unit's small-signal parameters.
- [ ] Reconcile the stated 24–25 L gross internal volume with the approximately
  26.0 L rectangular internal volume implied by the external dimensions and
  18 mm wall thickness; then finalise bracing, driver, PCB, PSU, and plate
  displacement to demonstrate approximately 20 L net acoustic volume.
- [ ] Select the exact 36 V main PSU and document its continuous/peak power,
  cooling, noise, protection, mechanical, and safety characteristics.
- [ ] Convert each item in [prototype validation](VALIDATION.md) into a
  measurable test method and numerical pass/fail criterion, including the
  operating and ambient conditions.
- [ ] Define the mains-side implementation: inlet, fusing, switching, wiring,
  insulation/segregation, strain relief, protective-earth hardware, and
  enclosure-access assumptions.
- [ ] Define the required amplifier protection, fault indication, enable/mute,
  and power-up/power-down behaviour.

## 2 Finalise and simulate the electronics

- [ ] Finalise the TPA3251 differential-input stage, including exact gain,
  input sensitivity, common-mode conditions, and 12 V rail headroom.
- [ ] Finalise the TPA3251 surrounding passives from the TI PBTL reference
  design.
- [ ] Select the exact output-filter MLCC bank using capacitance-under-bias,
  tolerance, ripple-current/loss, voltage, and package data.
- [ ] Select the exact Zobel parts and check pulse/continuous dissipation.
- [ ] Select the 15 V buck converter.
- [ ] Select the `12V_AMP` LDO.
- [ ] Select the `12V_ANA` low-noise LDO.
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
- [ ] Define the PCB stack-up and layer usage.
- [ ] Finalise the aluminium-plate dimensions, mounting, finish exclusions,
  connector/control locations, and sealing details.
- [ ] Finalise cabinet bracing and all internal displacement calculations.
- [ ] Produce a passive-cooling thermal-resistance budget from the stated
  15–18 W worst-case IC dissipation to a specified maximum ambient temperature,
  including the package-to-PCB-to-plate interface and component hot spots.
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
