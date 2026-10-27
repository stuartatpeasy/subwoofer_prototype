# Action list

Complete these in dependency order. Items described as locked in the
[system specification](SPECIFICATION.md) should be reopened only if analysis,
simulation, or measurement shows that they cannot meet the acceptance criteria.

The `rev0` bare-board design and export are frozen for prototype fabrication.
The user reports zero DRC and net-connectivity errors after the final trace/via
tidying and repour; the unchanged schematic previously passed ERC. The remaining
bare-board purchase gate is JLCPCB's rendered four-layer/NPTH upload preview
and selected standard 1.6 mm order options. Open items below concerning
component fit, harness, rear plate, mains assembly, rail noise, temperatures
and measured behaviour are deferred to assembly or prototype validation unless
their order-preview evidence reveals a bare-board defect. See [PCB layout
review](PCB_LAYOUT.md#5-current-release-disposition-27-october-2026).

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
  internal protection, permit user power-cycling for latched faults, add
  board-level diagnostic LEDs and plan test access without automatic retry,
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
  [power and grounding](POWER_AND_GROUNDING.md): keep the present MP4541GN
  approximately 17.36 V buck, C42–C44, XC6701 15 V and L78M12 12 V branches.
  Do not redesign them unless built-prototype measurements justify a change.
- [ ] Check the selected U5 SOIC-8EP, C42–C44 1210 and U9 DPAK land dimensions,
  U5 exposed-pad net, and local switching-current return before fabrication;
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
- [ ] Verify actual J3 harness load, physical DPDT 0°/180° mapping, and
  terminal identification.
- [ ] Verify the Sallen-Key filter transfer function, Q, adjustment range,
  component tolerances, and control tracking in simulation.
- [ ] Qualify the selected Bourns `PDB182-K420K-203B` 20 kΩ dual-gang linear
  crossover potentiometer by measuring both gangs and confirming that the
  panel-wired installation and +50 °C pot-body limit are met; select the level
  potentiometer.
- [x] Retain the saved RCA input coupling and RF network for the first
  bare-board prototype without adding a dedicated input ESD suppressor.
  This is a prototype design choice, not an ESD immunity qualification;
  revisit protection if handling or susceptibility testing reveals a problem.
- [ ] Extend the provisional white-noise review in
  [analogue front end](FRONT_END.md) after the TPA3251 input network is fixed:
  include real VMID/rail noise, the source, pot contact/excess noise, amplifier
  self-noise, and the relevant measurement bandwidth. Compare J3 and speaker
  noise with the estimates before changing resistor values.

## 3 Complete the physical and safety design

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
- [ ] Verify the joined 36 V and GND entry at J6 with the actual three closely
  paired feed/return cables and common Mean Well terminals. The saved board
  now takes the buck branch locally, resolving the previous asymmetric
  feed/return arrangement; see [PR-005](PCB_LAYOUT.md#2-findings). Parallel
  cables need not share current equally. Check the J6 contact and local copper
  capacity, the corrected Molex 7 A per-contact guideline with enclosure
  derating, both connector footprints, cable routes and clearances, strain
  support, polarity, and driver-end termination before assembly. Recheck
  Mouser availability and purchasing terms before ordering.
- [ ] Confirm the replacement Gerber ZIP's rendered layers, NPTH mounting
  holes and mask/silk alignment in JLCPCB's upload preview, then confirm the
  selected standard four-layer, 1.6 mm order options before payment. The
  read-only archive inspection found no remaining bare-board data defect
  ([PR-010](PCB_LAYOUT.md#2-findings)). The saved nominal stack uses 35 µm
  outer / 15.2 µm inner copper
  and 0.2104/1.065/0.2104 mm dielectric spacing, matching JLCPCB's published
  no-impedance-requirement example. The saved U9 now uses the larger `M` DPAK
  lands; inspect its solder joints and temperature on the built prototype
  ([PR-012](PCB_LAYOUT.md#2-findings)). If ordering a stencil, suppress paste
  on TP1–TP11 ([PR-013](PCB_LAYOUT.md#2-findings)).
  The [19 October power-stage review](POWER_AMPLIFIER.md#117-power-stage-copper-review-19-october-2026)
  provisionally supports JLCPCB's standard 35 µm outer / 15.2 µm inner copper
  at 150 W into 4 Ω. The current saved inner entry is 15.2 µm; revisit
  weight only if final routes or prototype results justify it.
  The saved C20/C26 bulk-capacitor feed and return now join the 36 V and GND
  planes. Check the resulting filled copper, C21/C22/C24/C25
  supply/return loops, output-via transitions and complete bootstrap loops
  without imposing a length-matching requirement. Recheck whether the two
  now-17-via `SPK+` fields or local 19-via `36V` field materially narrow either inner
  plane; trim only where copper continuity benefits. Check the close
  C20/C26 via-to-solder-land mask geometry and the C26 board-edge clearance;
  the selected 5 mm maximum fastener fits its 6 mm keep-out, closing
  [PR-003](PCB_LAYOUT.md#2-findings). The Bottom same-priority
  `36V`/`AMP_OUT_B,C` and `AMP_OUT_A`/`GND` pour warning cleared after
  reprioritising the output pours; verify that this did not narrow the U3
  supply or output paths. The latest inner-layer swap restores GND adjacent
  to U3 ([PR-006](PCB_LAYOUT.md#2-findings)); inspect the low-priority
  [PR-007](PCB_LAYOUT.md#2-findings) analogue reference trade-off if refining
  that region or investigating measured noise. The user reports passing DRC
  and net-connectivity checks on this board; see the
  [focused priority check](POWER_AMPLIFIER.md#116-bottom-copper-pour-priority-warning-18-october-2026).
  Validate the finished via construction and JLCPCB order options;
  rerun affected connectivity/DRC checks after any electrical, layout or rule change.
  See the [current whole-board review](PCB_LAYOUT.md) and earlier
  [power-stage layout review](POWER_AMPLIFIER.md#115-four-layer-output-and-supply-review-17-october-2026)
  and [via-field review](POWER_AMPLIFIER.md#113-via-field-current-and-plane-review-17-october-2026).
  The [local ceramic copper estimate](POWER_AMPLIFIER.md#114-local-pvdd-ceramic-copper-parasitic-estimate-17-october-2026)
  supports retaining C21/C22/C24/C25 while the final filled copper and
  prototype switching waveform remain open checks.
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

- [ ] After bare-board fabrication, conduct the remaining proportionate
  assembly-fit, grounding, thermal and mains-construction reviews before
  energising the complete prototype. The user reports zero ERC, DRC and
  connectivity errors after the current refill; rerun affected checks if the
  electrical or PCB design changes. The bare-board data inspection passed;
  JLCPCB's rendered upload preview remains under [PR-010](PCB_LAYOUT.md#2-findings).
- [ ] Build the Rev-A prototype and perform the documented electrical, thermal,
  and acoustic validation.
- [ ] Record measured results, deviations, corrective actions, and final
  as-built values in the documentation; update provisional statements only
  when evidence supports doing so.
