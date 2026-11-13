# System specification

> **State — current system authority; reviewed 2026-11-11.** Owns locked
> architecture and cross-subsystem constraints; detailed plate geometry and
> finish belong to [mechanical design](MECHANICAL.md). Read for system-level
> changes. Current direction permits CNC plate reliefs, components on both
> PCB sides and justified through-hole parts. The 6061/finish choice and
> completed thermal/mechanical stack remain provisional. Two external sinks
> and a smaller plate are the preferred, unqualified cooling direction; see
> [thermal design](THERMAL.md) and [mechanical design](MECHANICAL.md).
> The 140–150 W clean
> output target is peak capability; sustained full output is not required.
> The user has locked the 300 × 470 × 320 mm structural cabinet to provide
> another 10 mm in the electronics compartment. Ash legs, bumpers and later
> decoration may extend beyond that plywood envelope. The current rear control
> panel is insulating 1.6 mm FR-4 over a cut-out in the 12 mm plywood;
> its fixing and completed wiring remain to be checked.

## 1 Locked decisions

Do not revisit without measured/simulation evidence:

- SB23MFCL45-4
- sealed enclosure
- 300 × 470 × 320 mm nominal bare structural-cabinet outer envelope; the
  extra 10 mm depth belongs to the electronics compartment. Ash legs,
  edge bumpers, later veneer and other decorative trim may extend beyond it
  without changing the structural-envelope decision
- downward-firing, recessed SB23MFCL45-4 driver
- sloped partition separating the sealed acoustic chamber from the
  electronics chamber and bonded around its perimeter
- separate sealed acoustic chamber and naturally ventilated electronics chamber
- 20.0 L net geometric acoustic-chamber air volume, after subtracting solid
  intrusions and before assigning any apparent-volume benefit to wadding
- electronics-chamber inlet through the bottom panel and outlet through the
  upper half of the rear panel, with the sloped partition shaping the airflow
  route; the hole fields and free areas remain to be designed
- 36 V main rail
- Mean Well `RSP-200-36` main PSU
- first-prototype auxiliary supply selection: MP4581GN-Z buck at approximately
  17.36 V, `XC6701DF02FR-G` 15 V analogue regulator, and
  `L78M12ABDT-TR` 12 V amplifier regulator; U5 replaces the originally selected
  MP4541GN for sourcing, using the same pinout and circuit. Change these only
  if built-prototype measurements justify it; see
  [power and grounding](POWER_AND_GROUNDING.md)
- Schurter `DD11.0111.1111` C14 inlet with two-pole switch, one-pole line fuse,
  and no additional Rev-A inlet filter
- Schurter `T2AH250V` 2 A time-lag ceramic appliance fuse
- dedicated M4 rear-plate protective-earth stud used as the PE distribution
  point to the plate and PSU frame-ground terminal
- TPA3251 PBTL
- approximately 140–150 W clean output capability for bounded peaks into the
  nominal 4 Ω load; continuous output at that level is not a design requirement
- nominal 600 kHz switching frequency
- passive cooling
- 35 °C maximum rated room ambient; use 40 °C as a thermal-design margin
  case without claiming continuous full-power operation above 35 °C
- use the TPA3251's internal protection and latched-fault behaviour; serious
  faults may require a user power cycle
- add board-level `FAULT` and `CLIP_OTW` diagnostic LEDs for testing while
  retaining both test points; no front-panel indicator is required
- no external differential-DC detector, speaker relay, output MOSFET
  disconnect, or switched-PVDD DC-fault protection; accept the residual risk
  to the internally connected driver from a PBTL output fault
- analogue RESET supervision with delayed turn-on and prompt power-down mute;
  no MCU and no automatic fault retry
- two Texas Instruments `TPS3762-Q1` undervoltage supervisors with wire-ORed
  open-drain RESET outputs: fixed 30 V `TPS3762EUVF4DDFRQ1` monitors 36 V
  PVDD; adjustable `TPS3762EUV02DDFRQ1` monitors the approximately 17.36 V
  buck output. Both are powered from 36 V. Use a separate 130 kΩ/7.5 kΩ,
  1% E24 SENSE divider near the amplifier's `17V3` feed, independent of the
  U5 feedback path; the loaded headroom margin remains to be verified in
  [Power amplifier](POWER_AMPLIFIER.md).
- OPA1678/OPA1679
- single 15 V analogue rail
- buffered 7.5 V VMID
- stereo RCA input
- REAN `NYS367-9` white left and `NYS367-2` red right panel RCA sockets
  (Mouser `568-NYS367-9` and `568-NYS367-2`); the 1.6 mm FR-4 control panel
  fits their 3 mm maximum effective mounting thickness
- approximately 47 kΩ input impedance
- active mono averaging
- 2nd-order Butterworth Sallen-Key LPF
- dual-gang linear crossover pot
- approximately 40–100 Hz range
- mono level control
- selectable 0°/180° polarity
- E-Switch `100DP1T1B1M1REH` gold-contact DPDT ON–ON polarity switch
  (Mouser `612-100-F1112` is the purchasing reference); FR-4 panel mounting
  detail and physical lever mapping remain assembly checks
- differential TPA3251 drive
- IHLP5050FDER100M5A inductors
- amplifier-board component technology and side chosen by electrical layout and
  the verified machined-plate clearance; through-hole parts are permitted
- nominal 8 mm CNC-machined aluminium rear plate as the current design basis,
  with PCB clearance reliefs and a continuous TPA3251 thermal land. See
  [mechanical design](MECHANICAL.md#21-aluminium-heatsink-plate).
- use 12 mm plywood for the structural rear panel alone and mount all user
  controls and external connectors on its attached insulating FR-4 control
  panel, with no control or connector penetration through
  the aluminium heat-spreader plate; the plate retains its PCB, thermal and
  PE-bond roles
- matt-black external plate finish
- no fan
- no MCU/firmware
- TPA3251 faces the plate; selected nearby support components may share its
  plate-facing PCB side in machined reliefs
- through-hole parts are allowed where their electrical/mechanical benefit and
  finished lead clearance justify them
- use leaded SMD IC packages with externally accessible pins; do not use BGA,
  CSP, DFN, QFN, or similar leadless packages
- prefer larger-pitch packages such as SOIC where they are reasonably
  available; pin pitches down to 0.50 mm are acceptable when necessary
- one four-layer PCB with physically controlled analogue and power regions;
  no two-layer fallback

The former 1050A-H14 flat plate, painted-exterior process, SMD-only board,
and front-side-only support-component rules are superseded by the CNC-relieved
plate and component-placement permissions above. JLCCNC 6061 and ordinary
matt-black anodising are preferred **provisional** material/finish choices,
subject to the thermal and fabrication gates in [Mechanical design](MECHANICAL.md).
The former X7R MLCC output-filter technology preference is also superseded:
through-hole film is permitted, with exact selection still provisional in
[Power amplifier](POWER_AMPLIFIER.md).

The previous 15 V converter feeding separate 12 V amplifier and analogue
post-regulators is superseded by the selected first-prototype supply in the
[canonical schematic](../diptrace/main_board.dchxml). The buck exposed pad
and the 12 V regulator's ground tab are drawn; check final footprint geometry,
fabrication outputs, and the assembled rail and thermal behaviour. This
selection is final for the prototype, not a measured qualification.
The former `PGND`, `AGND`, and `GNDAMP` nets have been merged into one `GND`
net, and the unpopulated R1/R2 links have been removed. The TPA3251's 12 V
feeds are drawn, but their loaded current, L78M12 thermal behaviour, and the
physical bypass and return paths remain open. The selected nominal 1 µF C36
input bypass meets the local capacitance target on the user's DC-bias data;
its placement remains a PCB check.
Prior component analysis remains
in [power and grounding](POWER_AND_GROUNDING.md) as superseded context, not
an active procurement or assembly instruction.

## 1.1 PCB architecture and grounding

- one mechanically unified PCB, partitioned into analogue-front-end and
  Class-D power-amplifier domains
- four copper layers for Rev A
- physically controlled analogue and amplifier return regions; the schematic
  uses one common `GND` net, and the current PCB review records the joined
  local ground copper beneath U3
- a common 36 V/GND board entry at J6, with three paired positive/return
  cables planned to the common Mean Well terminals as described in
  [Power and grounding](POWER_AND_GROUNDING.md)
- selected through-hole, latching board connections for the 36 V input and
  driver output; exact pairs and remaining harness/layout gates are owned by
  [power and grounding](POWER_AND_GROUNDING.md) and
  [power amplifier](POWER_AMPLIFIER.md), respectively
- a placement corridor between analogue circuitry and Class-D switching
  nodes; route the balanced audio pair together and retain suitable local
  return references for any crossing

The one-board, four-layer architecture remains locked; the common `GND` net
supersedes the earlier split-net scheme. The current saved copper and its
remaining assembly checks are in [PCB layout review](PCB_LAYOUT.md).
Four layers are a project requirement even though they are not a functional
requirement of the TPA3251 itself. For the first bare-board order, JLCPCB
standard four-layer, 1.6 mm construction is selected; the final export and
order-option comparison remains open. The milled plate reliefs and thermal
interface between the rear-mounted top-exposed PowerPAD and aluminium plate
remain separate assembly design tasks.

## 2 Driver

- locked part: SB Acoustics `SB23MFCL45-4`
- source: manufacturer [REV.5 datasheet dated 2026-05-04](https://sbacoustics.com/wp-content/uploads/2026/05/8-inch-SB23MFCL45-4.pdf)
- nominal impedance: 4 Ω; `Re = 3.3 Ω`; `Le = 0.73 mH`
- `Fs = 27 Hz`; `Qms = 7.7`; `Qes = 0.36`; `Qts = 0.34`
- `Vas = 37 L`; `Sd = 210 cm²`; `Mms = 59 g`; `Bl = 9.6 Tm`
- `Cms = 0.59 mm/N`; `Rms = 1.3 kg/s`
- sensitivity: 87.5 dB at 2.83 V/1 m
- manufacturer-rated power: 150 W to IEC 268-5
- manufacturer-specified linear coil travel: 24 mm peak-to-peak, equivalent
  to ±12 mm geometric one-way travel; this is not a separate Klippel-derived
  linearity limit
- frame outside diameter: 234.25 mm; baffle cut-out: 203 mm; mounting depth:
  122.1 mm; overall depth: 137.7 mm; net mass: 4.7 kg

The manufacturer states that the Thiele/Small parameters are measured on
broken-in units. It publishes neither T/S tolerances nor cabinet-displacement
volume. Driver solid displacement must therefore come from the actual part or a
checked geometric model; the `Sd × travel` swept volume is not cabinet
displacement.

## 3 Cabinet

The locked direction is the nominal 300 × 470 × 320 mm **bare structural**
envelope, downward-firing recessed driver, sealed acoustic chamber separated
from the electronics by a sloped partition, and passive airflow from a
bottom-panel inlet field to an upper-rear-panel outlet field. Decorative
veneer, edge protection, and similar external trim may increase the finished
outside dimensions without breaching the bare-envelope decision. The current
[SketchUp enclosure model](../3d_models/Subwoofer%20cabinet.dae) is the layout
basis, not a final cutting or assembly drawing. The 36 mm laminated bottom
baffle and 18 mm other structural panels/partition remain its modelled
construction geometry, with 12 mm rear plywood. The current model includes
candidate acoustic braces and a rear perimeter brace, the accepted lower
inlet/PSU-mount geometry, a candidate upper rear outlet, a separate FR-4
control panel fastened to the rear ply, and a reduced aluminium plate with
two external sinks.
The extra 10 mm depth is in the electronics compartment. It also includes
four ash corner legs and eight ash edge bumpers, glued to the plywood core.
Joints, amplifier PCB, leg and trim detail, control-panel support and wiring,
and the plate's earthing and thermal-contact details remain to be designed.
The local
rear electronics floor is 18 mm thick; the sealed acoustic baffle and
partition foot retain the 36 mm laminated structure.

The rear wall is on the ventilated electronics side of the sealed partition.
Changing only this wall's thickness does not alter the modelled acoustic-chamber
volume or the 20.0 L net target. The DAE now depicts the 12 mm rear wall,
but the separate FR-4 control panel, the outlet and the sink fixings
need assembly checks before using it for final cut-outs or fabrication.

The sealed chamber target remains **20.0 L net geometric air volume** after
solid intrusions; wadding is not credited as geometric volume. The driver,
its airtight cable feed-through, necessary bracing, and wadding occupy that
chamber. The electronics chamber is isolated from acoustic pressure. The
partition must be continuously bonded and sealed to the adjoining panels.

The latest 10 mm cabinet-depth reduction removes about 0.702 L from the
previous acoustic-chamber estimate.
Using the present brace geometry and provisional 1.0 L driver allowance,
the planning net volume is about 20.305 L. Driver displacement remains
unmeasured; reconcile the actual driver and all other solid intrusions
against the 20.0 L target before cutting.
The current model's dimensions, volume calculation, placement limits, and
provisional floor-clearance range are owned by [Mechanical design](MECHANICAL.md).
The detailed vent route and thermal acceptance gate are in
[Thermal design](THERMAL.md). Final net volume and enclosure behaviour require
the assembled checks in [Prototype validation](VALIDATION.md).

Using the nominal driver parameters and exactly 20.0 L gives the ideal sealed-
box predictions:

```text
Qtc = Qts × sqrt(1 + Vas/Vb) = 0.574
Fc  = Fs  × sqrt(1 + Vas/Vb) = 45.6 Hz
```

These are small-signal model results, not completed-enclosure measurements.

## 4 Amplifier

- TI `TPA3251`
- mono PBTL
- 4 Ω load
- main rail: 36 V DC
- target clean output: approximately 140–150 W
- that target is available peak level, not a sustained music-output or thermal
  qualification requirement; [thermal design](THERMAL.md) owns the separate
  sustained-use and bounded full-output heat cases
- switching frequency: nominal 600 kHz, set by the 10.0 kΩ `FREQ_ADJ`
  resistor in TI's PBTL reference design. The earlier 450 kHz requirement had
  no recorded rationale; the 2026-10-11 review retained the reference resistor
  and corrected the requirement. The output-filter values remain provisional
  pending their existing validation gates.
- output-filter capacitor candidate: one TDK `B32701P4684K000` 680 nF
  metallised-polypropylene film shunt on each combined speaker-output side;
  prototype checks remain open in [Power amplifier](POWER_AMPLIFIER.md)
- passive cooling only

## 5 Main PSU

- locked part: Mean Well `RSP-200-36`
- enclosed Class-I mains SMPS with active PFC
- nominal output: 36 V DC, 5.56 A, 200.16 W
- fanless, free-air-convection cooling
- use at the nominal 36 V setting; do not use the 32.4–39.6 V adjustment
  range as normal operating margin
- no separately specified peak-power rating: design to the 200.16 W continuous
  rating and treat the overload range as protection behaviour, not usable output
  capacity
- the 200 W rating preserves supply headroom for bounded 140–150 W audio
  passages plus amplifier loss and auxiliary loads; ordinary music does not
  consume the rating continuously. The [PSU assessment](POWER_AND_GROUNDING.md#13-locked-36-v-supply-mean-well-rsp-200-36)
  retains this selected part after reviewing a smaller 36 V alternative
- full electrical, mechanical, cooling, mains-inlet, fusing, earthing, and
  approval details are owned by [Power and grounding](POWER_AND_GROUNDING.md)
