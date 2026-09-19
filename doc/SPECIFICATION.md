# System specification

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
- XP Power `STH0548S15` non-isolated 36 V-to-15 V switching-regulator module
- Bourns `SRR7045-560M` 56 µH shielded power inductor in the populated Rev-A
  STH0548S15 input EMI filter
- generic 22 µF, 63 V-minimum, ±20%, 105 °C SMD aluminium-electrolytic
  capacitor at the STH0548S15 input, with measured ESR included in the filter
  damping assessment; 63 V is preferred and 100 V is an acceptable substitute
- KEMET `C1206C104K1RAC7867` 100 nF, 100 V, ±10%, X7R, 1206 for the
  STH0548S15 input and output bypasses and both LM2937 input bypasses; current
  manufacturer packaging aliases are documented in
  [Power and grounding](POWER_AND_GROUNDING.md)
- 250 mA maximum total design load on the 15 V rail, despite the module's
  400 mA component rating
- two Texas Instruments `LM2937ESX-12/NOPB` fixed 12 V, 500 mA
  DDPAK/TO-263 post-regulators, one each for `12V_AMP` and `12V_ANA`
- 0 Ω default prefilter link on `12V_AMP`; 10 Ω RC prefilter on `12V_ANA`
- KEMET `EEV226M035S9DAA` 22 µF, 35 V SMD aluminium electrolytic at each
  LM2937 input and output; approve the parts for assembly only after measured
  ESR and temperature behaviour meet the requirements in
  [Power and grounding](POWER_AND_GROUNDING.md)
- Schurter `DD11.0111.1111` C14 inlet with two-pole switch, one-pole line fuse,
  and no additional Rev-A inlet filter
- Schurter `T2AH250V` 2 A time-lag ceramic appliance fuse
- dedicated M4 rear-plate protective-earth stud used as the PE distribution
  point to the plate and PSU frame-ground terminal
- TPA3251 PBTL
- approximately 140–150 W
- 450 kHz switching frequency
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
- Texas Instruments `TPS3842A011DRLR` adjustable undervoltage supervisor for
  RESET control, in the six-pin 0.50 mm-pitch SOT-5X3 package
- OPA1678/OPA1679
- single 12 V analogue rail
- buffered 6 V VMID
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
- SMD-only amplifier board
- X7R MLCC output-filter capacitors
- 6 mm 1050A-H14 aluminium rear plate
- matt-black external plate finish
- no fan
- no MCU/firmware
- TPA3251 is the only rear-side PCB component and faces the aluminium plate
- all other PCB components are front-side SMD
- no through-hole components anywhere on the PCB
- use leaded SMD IC packages with externally accessible pins; do not use BGA,
  CSP, DFN, QFN, or similar leadless packages
- prefer larger-pitch packages such as SOIC where they are reasonably
  available; pin pitches down to 0.50 mm are acceptable when necessary
- one electrically partitioned four-layer PCB; no two-layer fallback

## 1.1 Locked PCB architecture

- one mechanically unified PCB, partitioned into analogue-front-end and
  Class-D power-amplifier domains
- four copper layers for Rev A
- no shared copper planes between the two domains
- separate power and return entries for the two domains, preserving the
  deliberate external branching defined in
  [Power and grounding](POWER_AND_GROUNDING.md)
- a copper-free inter-domain corridor crossed only by the balanced audio pair
  in the normal populated configuration

Four layers are a project requirement even though they are not a functional
requirement of the TPA3251 itself. The exact fabricator stack-up and the thermal
interface between the rear-mounted top-exposed PowerPAD and aluminium plate
remain to be finalised before layout.

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
- switching frequency: 450 kHz
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
