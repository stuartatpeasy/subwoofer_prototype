# System specification

> **State — current system authority; reviewed 2026-10-11.** Owns locked
> architecture and cross-subsystem constraints; detailed plate geometry and
> finish belong to [mechanical design](MECHANICAL.md). Read for system-level
> changes. Current direction permits CNC plate reliefs, components on both
> PCB sides and justified through-hole parts. The 6061/finish choice and
> completed thermal/mechanical stack remain provisional.

## 1 Locked decisions

Do not revisit without measured/simulation evidence:

- SB23MFCL45-4
- sealed enclosure
- 390 × 390 × 390 mm nominal external cabinet envelope
- 36 mm laminated front baffle; 18 mm remaining cabinet panels and
  full-width/full-height transverse partition
- separate sealed front acoustic chamber and ventilated rear electronics chamber
- 20.0 L net geometric front-chamber air volume, after subtracting solid
  intrusions and before assigning any apparent-volume benefit to wadding
- 36 V main rail
- Mean Well `RSP-200-36` main PSU
- Schurter `DD11.0111.1111` C14 inlet with two-pole switch, one-pole line fuse,
  and no additional Rev-A inlet filter
- Schurter `T2AH250V` 2 A time-lag ceramic appliance fuse
- dedicated M4 rear-plate protective-earth stud used as the PE distribution
  point to the plate and PSU frame-ground terminal
- TPA3251 PBTL
- approximately 140–150 W
- nominal 600 kHz switching frequency
- passive cooling
- 35 °C maximum rated room ambient; use 40 °C as a thermal-design margin
  case without claiming continuous full-power operation above 35 °C
- use the TPA3251's internal protection and latched-fault behaviour; serious
  faults may require a user power cycle
- no normally visible fault indicator; retain `FAULT` and `CLIP_OTW` only as
  diagnostic test points
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
  MP4541 feedback path; the loaded headroom margin remains to be verified in
  [Power amplifier](POWER_AMPLIFIER.md).
- OPA1678/OPA1679
- single 15 V analogue rail
- buffered 7.5 V VMID
- stereo RCA input
- approximately 47 kΩ input impedance
- active mono averaging
- 2nd-order Butterworth Sallen-Key LPF
- dual-gang linear crossover pot
- approximately 40–100 Hz range
- mono level control
- selectable 0°/180° polarity
- differential TPA3251 drive
- IHLP5050FDER100M5A inductors
- amplifier-board component technology and side chosen by electrical layout and
  the verified machined-plate clearance; through-hole parts are permitted
- X7R MLCC output-filter capacitors
- nominal 6 mm CNC-machined aluminium rear plate with local PCB-clearance
  reliefs and a continuous TPA3251 thermal land
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
- one electrically partitioned four-layer PCB; no two-layer fallback

The former 1050A-H14 flat plate, painted-exterior process, SMD-only board,
and front-side-only support-component rules are superseded by the CNC-relieved
plate and component-placement permissions above. JLCCNC 6061 and ordinary
matt-black anodising are preferred **provisional** material/finish choices,
subject to the thermal and fabrication gates in [Mechanical design](MECHANICAL.md).

The previous 15 V converter feeding separate 12 V amplifier and analogue
post-regulators is superseded by the current power-plan revision. The partial
[canonical schematic](../diptrace/main_board.dchxml) now shows an MP4541GN
candidate 36 V-to-approximately-17.36 V buck feeding an `XC6701DF02FR-G` 15 V
analogue regulator and an `NCP1117ST12T3G` 12 V amplifier regulator. The buck
ground split and exposed-pad mapping have been revised. The 12 V regulator's
three leads and output-connected tab are now mapped correctly. Its ceramic
output-capacitor stability, thermal, and cross-domain return issues remain;
the present PGND–AGND–GNDAMP links are unpopulated placeholders, and a
single-net `GND` schematic revision is proposed. Its
amplifier load is not yet drawn. Prior
component analysis remains
in [power and grounding](POWER_AND_GROUNDING.md) as superseded context, not
an active procurement or assembly instruction.

## 1.1 PCB architecture and proposed grounding revision

- one mechanically unified PCB, partitioned into analogue-front-end and
  Class-D power-amplifier domains
- four copper layers for Rev A
- physically controlled analogue and amplifier return regions; one common
  schematic `GND` net is proposed, with the actual copper topology open
- separate power and return entries for the two domains, preserving the
  deliberate external branching defined in
  [Power and grounding](POWER_AND_GROUNDING.md)
- a placement corridor between analogue circuitry and Class-D switching
  nodes; route the balanced audio pair together and retain suitable local
  return references for any crossing

The one-board, four-layer architecture remains locked; the common `GND` net
and return-copper layout are a proposed revision to the earlier split-net
scheme. Four layers are a project requirement even though they are not a functional
requirement of the TPA3251 itself. The exact fabricator stack-up, component
placement, milled plate reliefs, and thermal interface between the rear-mounted
top-exposed PowerPAD and aluminium plate remain to be finalised before layout.

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

Locked architecture:

- material: two laminated 18 mm plywood layers at the front baffle; 18 mm
  plywood for the remaining walls and partition
- a vertical transverse partition, parallel to the front and rear panels,
  spans the full internal width and height
- the airtight front chamber contains only the driver, its cable/feed-through,
  necessary bracing, and wadding
- the front chamber has `20.0 L` geometric net air volume after solid
  displacement; wadding is not credited as extra geometric volume
- the smaller rear chamber contains all electronics and is isolated from the
  acoustic pressure volume
- lower intake and upper exhaust grilles provide an unobstructed natural-
  convection path through the rear chamber

Current bracing conclusion: the full-width/full-height partition is the sole
intentional cabinet brace. No front-to-partition strut, window brace, or extra
side-wall brace is required for the present 390 mm cube and plywood thicknesses,
provided that the partition is continuously bonded and sealed to all four
adjoining panels. Local cleats or a shallow housing used to make that joint are
joinery rather than additional acoustic bracing.

The earlier `360 × 340 × 300 mm` envelope and subsequent 360 mm width/height
planning constraint are superseded. The nominal external envelope is locked at
`390 × 390 × 390 mm`. The scaled packaging and thermal work must now fit within
that envelope; failure to do so would be evidence to reopen the decision.

For a cube with exterior edge `E` in millimetres, the clear width and height are
both `E - 36`. Inspection of the manufacturer section drawing gives a
provisional effective driver displacement of approximately `0.8 ± 0.2 L`, net
of the forward structure embedded in the 36 mm baffle. Use `1.0 L` as the
conservative cabinet-sizing allowance. The cable gland or grommet displacement
is negligible, and partition-joint cleats should be placed on the electronics
side. The front chamber therefore requires 21.0 L gross for planning.
Retaining the provisional 140 mm rear clear depth gives the self-consistent
sizing equation:

```text
E = 72 + 140 + 21,000,000 / (E - 36)²
```

The `72 mm` term is the 36 mm baffle, 18 mm partition, and 18 mm rear wall. The
solution is `E = 384.7 mm`; the locked 390 mm cube therefore retains about
5.3 mm aggregate depth margin over this planning model. At 390 mm the internal
cross-section is `354 × 354 mm`, the front clear depth is 167.6 mm, and the rear
clear depth is 150.4 mm. The rear chamber is about 18.85 L: more than the
electronics require by volume, but this is the consequence of retaining a
full-width/full-height partition and cubic exterior while satisfying the PSU's
115 mm plan depth.

The inspection estimate is not a manufacturer specification. The drawing fixes
the 130 mm motor diameter and 122.1 mm mounting depth, but does not dimension
the motor length, basket-rib sections, cone profile, or internal cavities. The
estimate treats the roughly 130 × 50 mm motor envelope as about 0.66 L before
allowing for its vent and reliefs, then adds the rear basket, suspension, and
voice-coil structure visible behind the inner baffle plane. The resulting
0.6–1.0 L plausible range is adequately covered by the 1.0 L allowance.

Reasonable uncertainty does not destabilise the cabinet estimate. With the
1.0 L driver allowance, rear clear depths of 130, 140, and 150 mm require cube
edges of approximately 379.7, 384.7, and 389.8 mm respectively. Thus the
390 mm envelope preserves useful packaging margin. The completed scaled layout
must confirm that the PCB, PSU, inlet and guards, wiring bend radii, assembly
access, and validated convection fit within it.

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
- switching frequency: nominal 600 kHz, set by the 10.0 kΩ `FREQ_ADJ`
  resistor in TI's PBTL reference design. The earlier 450 kHz requirement had
  no recorded rationale; the 2026-10-11 review retained the reference resistor
  and corrected the requirement. The output-filter values remain provisional
  pending their existing validation gates.
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
- full electrical, mechanical, cooling, mains-inlet, fusing, earthing, and
  approval details are owned by [Power and grounding](POWER_AND_GROUNDING.md)
