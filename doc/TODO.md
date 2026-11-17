# Action list

Complete these in dependency order. Items described as locked in the
[system specification](SPECIFICATION.md) should be reopened only if analysis,
simulation, or measurement shows that they cannot meet the acceptance criteria.

The user reports that the rev0 PCB and P01 spreader are in fabrication as of
17 November 2026. Their designs are complete for this prototype, with clearance
verified as adequate for prototyping; physical fit and thermal performance are
not yet verified. Perform the received-part checks and prototype validation
below. Reopen a design only if the actual parts or measurements require it.

## 1 Complete the system specification

- [x] Confirm the SB23MFCL45-4 nominal parameters and physical envelope from the
  current traceable manufacturer datasheet.
- [ ] After break-in, measure the actual driver's small-signal parameters; the
  manufacturer publishes neither T/S tolerances nor cabinet displacement.
- [x] Lock the nominal bare structural envelope at `300 × 470 × 320 mm`,
  downward driver, sloped pressure partition, 20.0 L net geometric acoustic
  target, and bottom-inlet/upper-rear-outlet ventilation direction. Decorative
  exterior ash legs, bumpers and later trim may extend beyond the bare
  envelope. The extra 10 mm depth serves the electronics compartment; the
  acoustic-chamber planning volume is unchanged.
- [ ] Complete a scaled electronics/airflow layout demonstrating that the PSU,
  PCB, bottom inlet, upper rear outlet, guards, wiring, assembly access, and
  convection path fit within the current sloped electronics chamber.
- [x] Select the exact 36 V main PSU and document its continuous/peak power,
  cooling, noise, protection, mechanical, and safety characteristics.
- [ ] Convert each item in [prototype validation](VALIDATION.md) into a
  measurable test method and numerical pass/fail criterion, including the
  operating and ambient conditions.
- [x] Define the mains-side implementation: inlet, fusing, switching, wiring,
  insulation/segregation, strain relief, protective-earth hardware, and
  enclosure-access assumptions.
- [x] Define the amplifier protection and fault policy: use the TPA3251's
  internal protection, permit user power-cycling for latched faults, add
  board-level diagnostic LEDs and plan test access without automatic retry,
  accept the residual PBTL DC-fault risk without an external disconnect, and
  use analogue RESET supervision for thump-controlled startup and shutdown.

## 2 Finalise and simulate the electronics

- [ ] Validate the selected TPA3251 differential-input stage: use the
  summer's 10 kΩ input and 3.0 kΩ feedback resistors to set 0.6
  correlated-stereo gain, then
  a level-pot-wiper follower and a 10.0 kΩ/10.0 kΩ unity inverter about VMID.
  Use the now-selected Panasonic `ECW-FD2W225J4` 2.2 µF film capacitors at
  both RCA inputs C1/C6 and both amplifier inputs C11/C15, followed by
  100 Ω series and 100 pF C0G shunt parts at the TPA3251 input pins.
  Verify the four through-hole patterns and physical fit on the received
  board. Confirm input
  sensitivity, common-mode conditions, symmetry, and 15 V analogue-rail
  headroom in simulation. The revised 7.5 V VMID gives approximately 1.26 V
  peak input common-mode margin for a 3 V RMS source at the first buffer.
- [x] Retain the saved TPA3251 surrounding-passive selection for the first
  bare-board prototype, including R18 = 22 kΩ on `OC_ADJ`. The actual
  overcurrent behaviour remains a built-prototype check; a saved resistor
  value alone does not qualify the protection threshold.
- [ ] Complete the U4/U10/U11 status-LED review in the PCB: confirm Kingbright
  physical polarity marks and pad geometry, onsemi SC-88 pad dimensions,
  routing and LED visibility. The R36/R37/R40 1.5 kΩ TE parts calculate
  to about 77 mW at the 12.5 V rail, 1.8 V LED, 1%-low resistor corner;
  confirm the local hot-ambient margin if an LED could remain on continuously.
  The R2/R10 1 kΩ TE purchasing fields and R19/R27/R30/R33/R34 10 kΩ Yageo
  manufacturer-part fields have been corrected in both saved CAD files.
  Check DVDD under controlled D2/D3 asserted-status conditions
  because each asserted 130 kΩ pull-down draws up to approximately 0.028 mA
  externally from this internal reference. The revised ACTIVE branch uses no
  external static DVDD current. The current schematic and PCB place TP1–TP11, including
  Top-side `AMP_nFAULT`, `AMP_nCLIP_OTW`, and `AMP_nRESET` pads. Verify probe
  access after assembly. The [SR-001
  RESET-indicator off-state concern](POWER_AMPLIFIER.md#12-protection-fault-response-and-reset-control)
  is closed in the saved design by the direct N-channel green ACTIVE circuit;
  confirm actual LED polarity, visibility and RESET truth on the prototype.
- [ ] Verify the operating margin of the selected C21/C22/C24/C25 Würth
  `885012208124` 2.2 µF, 100 V X7R PVDD bypass parts on 1206 patterns.
  The user's target is at least 1 µF each at 36 V DC bias; the supplied
  typical curve suggests 1.13 µF, or about 1.02 µF after −10% initial
  tolerance, but does not guarantee that minimum across temperature and
  ageing. Check switching peaks, exact-part impedance/ripple, the complete
  short-loop placement, pad geometry and proposed 4 mm CNC-pocket clearance.
  Retain the selected MPN unless a material electrical or mechanical issue
  emerges. See [power amplifier](POWER_AMPLIFIER.md#52-ceramics).
- [ ] Validate the selected first-prototype pair of TDK `B32701P4684K000` 680 nF film
  output-filter capacitors C17/C30, one per combined speaker-output side, as
  described in [power amplifier](POWER_AMPLIFIER.md). Their saved pattern has
  the manufacturer-confirmed 10 mm lead pitch; check carrier ripple, capacitor
  temperature, peak voltage, response/damping and final physical placement
  on the built prototype; the first-prototype part selection and 10 mm land
  pitch are settled for bare-board release.
- [x] Select the first-prototype output damping parts: C19/C28 are Würth
  `885012207116` 1 nF, 100 V; C16/C31 are Würth `885012207122` 10 nF,
  100 V; R20/R21 are Yageo `RC2512FK-7W3R3L` 3.3 Ω, 2.2 W. Measure
  post-inductor peaks and Zobel temperature on the built prototype before
  treating the network as qualified for sustained high output.
- [x] Select the first-prototype auxiliary supply in
  [power and grounding](POWER_AND_GROUNDING.md): use the MP4581GN-Z
  approximately 17.36 V buck, C42–C44, XC6701 15 V and L78M12 12 V branches.
  Do not redesign them unless built-prototype measurements justify a change.
  This U5 substitution replaces the originally selected MP4541GN for sourcing.
- [ ] Before populating U5, recheck MP4581GN-Z stock and the actual orderable
  suffix, and confirm its exposed-pad ground connection with MPS or its
  evaluation-board copper. Record the build identity and verify loaded
  buck/RESET behaviour on the prototype.
- [ ] Check the selected U5 SOIC-8EP, C42–C44 1210 and U9 DPAK land dimensions,
  U5 exposed-pad net, and local switching-current return before assembly;
  measure the loaded ripple, start-up and meaningful load transients on the
  prototype. The fourth buck-output capacitor is an unimplemented option,
  to add only if measurements show a material need.
- [ ] Verify the now-placed `U9 = L78M12ABDT-TR` DPAK footprint, pin mapping,
  ground tab, and thermal result for the actual 12 V load. The 25 October saved
  PCB has an approximately 544 mm² Top GND-pour outline, local copper on all
  four layers, and 19 GND vias within 10 mm of the tab centre. Inspect final
  filled connectivity and measure tab/copper and local air at the continuous
  load; see the [current PCB review](PCB_LAYOUT.md). The selected C36
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
  separate from the U5 buck feedback path, gives approximately 14.67 V
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
- [x] Verify that the corrected C2/C4/C5 Panasonic `ECH-U1H823JX9`
  PPS-film land pattern transferred to the PCB. Its 1.3 × 3.0 mm lands on
  4.3 mm centres match the selected E2 geometry; the saved component-style
  name now says `PPS` rather than `MLCC`. Check capacitor tolerance and
  pot-gang tracking during prototype characterisation.
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
- [x] Run DipTrace ERC before bare-PCB release. After the current refill,
  the user reports zero ERC, DRC and connectivity errors; the reports were not
  independently inspected. Repeat affected checks after electrical or layout changes.
- [x] Select the gold-contact E-Switch `100DP1T1B1M1REH` DPDT ON–ON
  [polarity switch](FRONT_END.md#62-selected-e-switch-gold-contact-switch-31-october-2026)
  for the four-wire J3 crossover harness (31 October 2026).
- [ ] Detail the selected switch's mounting land in the 1.6 mm FR-4 control panel and
  confirm nut/washer engagement, lug clearance, contact continuity, and the
  physical 0°/180° lever mapping before panel cutting and labelling.
- [ ] Verify the Sallen-Key filter transfer function, Q, adjustment range,
  component tolerances, and control tracking in simulation.
- [ ] Qualify the selected Bourns `PDB182-K420K-203B` 20 kΩ dual-gang linear
  crossover potentiometer by measuring both gangs and confirming that the
  FR-4-panel installation and +50 °C pot-body limit are met. The specified
  Bourns `PDB181-E420K-103A2` level potentiometer needs its J2 terminal mapping,
  clockwise level direction and the same mounting/temperature checks. Confirm
  nut engagement on the 1.6 mm FR-4 panel for both 6.5 mm bushings.
  Select knobs for their 6 mm, 18-tooth shafts and the final exposed shaft
  length; [SAK-007 does not fit directly, and the Mouser shortlist needs a
  physical depth check](MECHANICAL.md).
- [x] Retain the specified 20 kΩ dual-gang cutoff potentiometer with PC pins;
  the user accepted the terminal style on 31 October 2026. The considered
  10 kΩ/50 kΩ GTRB2 `MN` blend controls are unsuitable; the
  [resistance comparison](FRONT_END.md#41-solder-lug-alternatives-and-resistance-scaling-31-october-2026)
  remains design history, not an open substitution task.
- [x] Retain the saved RCA input coupling and RF network for the first
  bare-board prototype without adding a dedicated input ESD suppressor.
  This is a prototype design choice, not an ESD immunity qualification;
  revisit protection if handling or susceptibility testing reveals a problem.
- [ ] Extend the provisional white-noise review in
  [analogue front end](FRONT_END.md) for the selected TPA3251 input network:
  include real VMID/rail noise, the source, pot contact/excess noise, amplifier
  self-noise, and the relevant measurement bandwidth. Compare J3 and speaker
  noise with the estimates before changing resistor values.

## 3 Complete the physical and safety design

- [ ] Recover or regenerate the source geometry and complete slicer settings
  for any vent printer job to be repeated; the existing ignored G-code is not
  a verified reconstruction route. Preserve it until the source is resolved.
  See the [printer-job retention gap](3d_models/README.md#5-printer-job-retention-gap).

- [ ] Before the wider component order, generate a counted build BOM from the
  placed board references and add the external driver, PSU, inlet/fuse/drawer,
  controls, FR-4 panel, connector mates/pigtails, sinks, TIM, guards,
  fasteners, terminals and cable. Check exact orderable suffixes and current
  availability. The [13 November system order review](REV0_ORDER_REVIEW.md)
  found no consolidated purchasing list in the project. The [fastener BOM](FASTENER_BOM.md)
  now inventories the DAE, and the [off-board electrical BOM](OFFBOARD_ELECTRICAL_BOM.md)
  lists external components and harness candidates; their fit and sourcing
  gates and the combined build BOM remain open.

- [ ] Implement and validate the selected common-`GND` layout, the one
  intended board-to-chassis bond, and the independent protective-earth paths.
  Account for intentional and incidental conductive contacts in the assembly;
  the conceptual single-net decision is closed. The earlier High
  [U3 local ground-seam finding](PCB_LAYOUT.md#2-findings) is resolved in
  saved copper; preserve that connection and verify current connectivity.
  Decide the remaining PSU return-loop question before fixing the harness.
- [x] Lock the PCB architecture and layer count: one physically partitioned
  four-layer board, with no two-layer fallback.
- [x] Select the latching, through-hole 36 V input and speaker-output
  connector pairs documented in [power and grounding](POWER_AND_GROUNDING.md)
  and [power amplifier](POWER_AMPLIFIER.md).
- [ ] Dry-fit the driver-output harness with the driver supported outside its
  opening and the rear panel withdrawn while J5 remains connected. Use the
  selected 150 mm Mini-Fit Jr `215326-1021` pigtail at the unchanged J5 header,
  then a supported, insulated splice to the two-conductor 2.5 mm² jacketed
  cable in the electronics chamber. Set the actual cable length and independent
  service slack on both sides before sealing the partition feed-through; verify
  polarity and the received driver's terminal fit.
- [ ] Verify the joined 36 V and GND entry at J6 with the actual three closely
  paired feed/return cables and common Mean Well terminals. The saved board
  now takes the buck branch locally, resolving the previous asymmetric
  feed/return arrangement; see [PR-005](PCB_LAYOUT.md#2-findings). Parallel
  cables need not share current equally. Check the J6 contact and local copper
  capacity, the corrected Molex 7 A per-contact guideline with enclosure
  derating, both connector footprints, cable routes and clearances, strain
  support, polarity, and driver-end termination before assembly. Recheck
  Mouser availability and purchasing terms before ordering.
- [ ] When the fabricated PCB arrives, inspect the board and its component
  fit. Suppress TP1–TP11 paste if a stencil is ordered; measure U9 temperature
  and relevant switching behaviour during prototype validation. Rerun affected
  design checks if the PCB is revised.
- [ ] Finalise the separate rear FR-4 control panel, its fixings and the
  spreader-to-cabinet mounting and sealing. Verify the fabricated P01 finish,
  contact zones and mechanical fit on receipt.
- [ ] Verify the DD11 inlet on the 1.6 mm FR-4 control panel: confirm the
  mounting cut-out, screw/washer stack, rear cover and wiring clearance on
  the purchased part before cutting. Route its PE lead to the independent
  aluminium-plate stud.
- [x] Select the REAN `NYS367-9` white left and `NYS367-2` red right
  [RCA pair](FRONT_END.md#21-selected-rca-panel-sockets-31-october-2026)
  (31 October 2026).
- [ ] Trial the 1.6 mm FR-4 control panel and four M3 fixings in the rear-ply
  opening. Check stiffness under IEC/RCA plug and switch loads, socket
  washer/nut engagement, actual knob stand-off, and any needed local support.
  Confirm RCA isolation from the plate/PE and the inlet cover and mains/signal
  wiring routes; the modelled inlet and nearest RCA envelopes are about
  7 mm apart laterally. Use the [layout models](3d_models/Rear-signal-parts.md)
  for component placement, not as machining templates.
- [ ] Export and preview the separate `diptrace/control_panel.dipxml` outline,
  cut-out and eleven NPTH holes before ordering the FR-4 panel; the main-board
  Gerber ZIP does not contain its fabrication data.
- [ ] Confirm the modelled PDB182 crossover position, pin and harness
  clearances and actual panel fit; the DAE now contains one PDB181 and one
  PDB182.
- [ ] Trial the driver M4 pan head in the actual flange recess and a Type E
  insert in laminated plywood. Verify blind-hole depth, full engagement without
  bottoming, frame bearing and seal as described in [mechanical design](MECHANICAL.md#12-downward-driver-and-carpeted-floor-clearance).
- [ ] Check the modelled PSU screws against the 3 mm maximum penetration: the
  nominal stack uses all 3 mm, leaving no tolerance margin.
- [x] Replace the 8 November broad, 4 mm-thick plywood control land with
  a separate insulating FR-4 panel over a rear-ply through-opening in the
  11 November DAE. Physical and electrical assembly checks remain above.
- [ ] On receipt, verify the P01 plate material and finished pockets, threads
  and bare thermal/PE/ground contact zones against the fabrication drawing.
- [ ] Finalise the modelled brace network and its joints while retaining sound
  panel support; its roughly 1.259 L solid volume leaves about 21.305 L
  before driver displacement. Reconcile any overlaps and all solid
  intrusions against the 20.0 L net target before cutting.
- [ ] Check the actual driver's effective displacement relative to the inner
  baffle plane. The former 1.0 L calculation input is provisional, not an
  established upper bound; retain the airtight cable feed-through.
- [ ] Finalise the accepted bottom-inlet assembly: select the two vent-panel
  materials and fixings, PSU screw stack, and foreign-object guarding
  without reducing its roughly 135 cm² geometric free area unnecessarily.
  Preserve the nominal 15 mm under-PSU gap. Trial the eight vent screws'
  close aperture-corner lands and the PSU mounting stack in a representative
  offcut; the modelled ash legs clear the apertures.
- [ ] Finalise the modelled upper rear outlet: about 99.5 cm² geometric area
  through two 8 mm inserts with 352 nominal 6 mm airflow holes. Detail its
  fixings in the 15 mm plywood rails; the four screws now sit 2 mm outward
  from the opening corners and need a representative pilot/joint trial.
  Check any insect screen and its
  effect on
  both vents, and the flow route with the PCB, wiring and intended wall gap.
  Validate the final inlet-to-outlet path and heat budget.
- [ ] Detail the DAE's 152 × 137 mm plate with two external 557-140AB sinks
  using the [P01 prototype order package](MECHANICAL.md#21-aluminium-heatsink-plate).
  Verify the twelve tapped heatsink positions against the received slots and
  check the common screw stack at the six inner positions. After receiving the PCB and
  P01, measure the support and contact stack and verify fastener fit,
  component clearance, PCB isolation and PE bond before releasing a revised plate.
- [ ] Trial one rear-panel insert and countersunk screw in representative
  plywood before cutting. The revised positions give about 3.75 mm brace
  wood to the insert thread and 2.75 mm panel edge margin to the countersink.
- [ ] Correct or physically replace the DAE's plate-fixing washer/nut stack:
  its washers stop about 2 mm short of the rear-ply inboard bearing face, so
  the model does not show a clamped 4 mm residual plywood land. Trial the
  actual clamp and countersink in representative plywood before final cutting;
  see [mechanical design](MECHANICAL.md#21-aluminium-heatsink-plate).
- [ ] Check the completed ash-legged cabinet on the intended carpet: the
  plywood baffle starts 100 mm and the lower bumpers 90 mm above a hard floor.
  Confirm loaded clearance, level support, and unobstructed driver/inlet
  paths; extend legs or use firm bearing pads if necessary. Preserve a
  deliberate rear-wall gap: sink tips extend about 22 mm beyond the ash legs.
- [ ] Measure the assembled two-sink thermal performance under representative
  sustained operation and the bounded peak-output test, including accessible
  surfaces, potentiometers, room temperature and wall clearance. Assess the
  40 °C margin as described in [thermal design](THERMAL.md) and
  [prototype validation](VALIDATION.md).
- [ ] Resolve the TPA3251 package, PCB, and rear-plate stack mechanically and
  thermally; verify contact-land height/flatness, TIM compression, pocket
  clearances for parts and trimmed through-hole leads, and the actual heat
  path against package and assembly drawings on the received prototype.

## 4 Build and validate

- [ ] After bare-board fabrication, conduct the remaining proportionate
  assembly-fit, grounding, thermal and mains-construction reviews before
  energising the complete prototype. The user reports zero ERC, DRC and
  connectivity errors after the current refill; rerun affected checks if the
  electrical or PCB design changes. The user reports the board is in fabrication;
  the outcome of the prior rendered-preview check is not recorded.
- [ ] Build the rev0 prototype and perform the documented electrical, thermal,
  and acoustic validation.
- [ ] Record measured results, deviations, corrective actions, and final
  as-built values in the documentation; update provisional statements only
  when evidence supports doing so.
