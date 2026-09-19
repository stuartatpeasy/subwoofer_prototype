# Mechanical design

## 1 Two-chamber cabinet architecture

The cabinet has a 36 mm laminated plywood front baffle and 18 mm remaining
panels. It uses a transverse 18 mm plywood partition parallel to the front
and rear panels. It spans the full internal width and height, forms the pressure
boundary behind the driver, and braces the top, bottom, and sides. Seal every
perimeter joint. Pass only the driver cable through it, using an abrasion-
protected feed-through that remains airtight after wiring.

The front chamber is a 20.0 L net geometric air volume after subtracting the
driver and other material solid intrusions. The small cable gland or grommet is
neglected. Wadding belongs only in this chamber, must remain clear of the cone,
suspension, motor vents, and terminals, and is not counted as recovered
geometric volume. The current 1.0 L driver allowance is conservative enough for
cabinet sizing; replace it from actual-part geometry only if greater precision
later becomes useful.

The rear chamber contains all electronics and is ventilated rather than part of
the acoustic enclosure. A lower intake and upper exhaust create a chimney flow.
Provide bottom clearance with feet or a plinth, keep both flow paths clear of
looms and boards, and use guarded or labyrinthine grilles that prevent access
and direct foreign-object paths to mains terminals. The inlet rear cover and
PSU terminal cover remain required.

### 1.1 Bracing conclusion

No separate internal brace is required in the current baseline. The partition
is a complete shelf brace: in the locked 390 mm cube it reduces the
front-chamber side, top, and bottom spans to approximately `354 × 176 mm`.
The front baffle is 36 mm laminated plywood, and its centred 203 mm driver
cut-out still leaves broad material around the basket.

The partition itself is the largest remaining pressure-loaded panel at
approximately `354 × 354 × 18 mm`. A deliberately approximate, simply supported
isotropic plate check using plywood modulus `6–12 GPa`, density `650 kg/m³`, and
Poisson ratio 0.3 puts its first bending mode at roughly `415–587 Hz`. The
smaller `354 × 176 × 18 mm` panels calculate at roughly `1.05–1.48 kHz`.
Continuous glued perimeter restraint should raise these frequencies relative
to that simply supported estimate.

As a separate stiffness sanity check, taking the driver's full ±12 mm swept
volume as an extreme sealed-box compression gives approximately 1.8 kPa peak
internal pressure. Even with the low 6 GPa modulus, the same plate model gives
less than 0.04 mm partition-centre deflection. This is small enough that another
brace is not justified by the present acoustic or structural evidence.

This conclusion depends on construction:

- continuously glue and seal the partition to the top, bottom, and both sides;
- use a shallow housing/dado or continuous plywood/hardwood cleats if needed to
  locate and strengthen the joint, placing any cleats on the electronics side
  so that they do not consume acoustic volume;
- keep the partition solid except for the small sealed driver-cable feed-
  through; and
- revisit the conclusion if the material is materially less stiff than sound
  18 mm plywood, the perimeter joint cannot be made continuous, or testing
  reveals an audible panel or joint resonance.

Do not add front-to-partition struts merely as insurance. They would obstruct
the driver, complicate assembly, and consume acoustic volume without addressing
a presently credible weakness.

### 1.2 Depth calculation

For a cube of exterior edge `E`, with a 36 mm front baffle and 18 mm remaining
panels:

```text
internal width = internal height = E - 36 mm
front clear depth = gross front volume / (E - 36)²
E = 72 mm + front clear depth + rear clear depth
```

The `72 mm` term is the 36 mm front baffle, 18 mm partition, and 18 mm rear
wall. Using 21.0 L front gross volume and 140 mm rear clear depth gives:

```text
E = 212 + 21,000,000 / (E - 36)²
E = 384.7 mm
```

The locked 390 mm cube gives a `354 × 354 mm`
internal cross-section, 167.6 mm front clear depth, and 150.4 mm rear clear
depth. The resulting rear chamber volume is approximately 18.85 L.

Orient the horizontal PSU with its 215 mm length across the 354 mm internal
width and its 115 mm width front-to-back. A 140 mm rear chamber provides 25 mm
combined clearance in that direction; the 390 mm cube provides 150.4 mm, or
35.4 mm total clearance. The PSU terminal row is at an end of the 215 mm
dimension, so its
wiring allowance is primarily taken from the remaining cabinet width rather
than by increasing depth. Confirm that assumption with the terminal cover and
actual wire routing in the scaled layout.

Complete the scaled arrangement within the locked 150.4 mm rear clear depth,
including component clearances, unobstructed PSU ventilation, wiring bends,
assembly access, mains segregation, guarding, and the thermal validation
criteria. Mean Well's general installation instructions require ventilation
openings to remain unobstructed; they do not define a smaller product-specific
clearance that would justify packing the 115 mm PSU tightly into the chamber.

With the 1.0 L driver allowance, 130–150 mm rear depth gives a 379.7–389.8 mm
cube. This supports the locked 390 mm value with packaging margin. Panel cutting
dimensions must still account for the selected joint geometry and fabrication
tolerances.

### 1.3 Driver-displacement estimate

The manufacturer does not publish displacement. Its section drawing provides
enough information for a planning estimate but not an exact solid model:

- the dominant rear motor is 130 mm diameter and appears approximately 50 mm
  long, giving a 0.66 L cylindrical envelope before subtracting the central
  vent, bevels, and external reliefs;
- the basket is mostly open; its rear ribs, spider support, voice-coil former,
  and other structure add much less volume than their conical envelope;
- the 36 mm baffle embeds the flange and forward basket region, so those parts
  do not displace the rectangular chamber behind the inner baffle face; and
- air spaces open to the chamber through the basket and motor vent count as box
  air, not solid displacement.

Together these observations support approximately `0.8 ± 0.2 L` effective
driver displacement behind the inner baffle face. Use `1.0 L` in the volume
budget. This estimate is deliberately more conservative than its likely effect:
at the present cabinet size, a 0.2 L error changes the required linear depth by
only about 1.6 mm and the self-consistent cube edge by less than 1 mm.

The driver's published 137.7 mm overall depth fits comfortably within the
expected front-chamber depth, but verify the actual unit and maintain clearance
behind its vent before cutting panels.

## 2 PCB and mechanical constraints

The Rev-A implementation is one partitioned four-layer PCB carrying
both the amplifier and analogue front end. It sits parallel to the rear
aluminium plate while preserving separate electrical domains as defined in
[Power and grounding](POWER_AND_GROUNDING.md).

Critical constraint:

```text
PCB underside to aluminium plate clearance ≈ 1.2 mm
```

In the amplifier domain, therefore:

- no through-hole parts anywhere on the PCB; protruding leads are incompatible
  with the plate clearance and no partial plate insulation will be used
- mount only the TPA3251 on the rear side, with its top-exposed thermal pad
  facing the aluminium plate
- mount every other component on the front side as SMD
- verify the TPA3251 package/TIM/plate compression and board-flatness stack;
  there are no neighbouring rear-side component-height accommodations
- keep rear-side copper, solder, and via finishes other than the intended
  TPA3251 ground/thermal contact clear of the plate under worst-case board bow,
  spacer, and assembly tolerances
- keep analogue-domain mounting points electrically isolated from the plate and
  do not bridge the PCB-domain partition with mounting hardware

### 2.1 Aluminium heatsink/control plate

Locked material:

- 1050A-H14 aluminium
- 6 mm thick
- use largest practical plate fitting cabinet
- inner face bare
- outer face matt black painted

Surface treatment:

- degrease
- lightly abrade
- aluminium-compatible etch primer
- thin matt-black top coat

Keep bare:

- TPA3251 thermal-contact area
- intended grounding/bonding points

The plate must also accommodate the front-screw-mounted Schurter
`DD11.0111.1111` inlet and its rear cover. Use the supplier drawing/CAD for the
cut-out and mounting holes. The 6 mm plate is within the inlet's 8 mm maximum
panel thickness. Reserve an independently mounted M4 protective-earth stud
close to the inlet; its final hardware and wiring are defined in
[Power and grounding](POWER_AND_GROUNDING.md).

The selected Mean Well `RSP-200-36` envelope is 215 × 115 × 30 mm. Its final
internal position must preserve free-air convection, keep the terminal guard
accessible for assembly, respect the manufacturer's mounting-screw penetration
limits, accommodate the Mean Well `TBC-09` terminal cover, and prevent mains
wiring from sharing the signal/DC loom space.

### 2.2 Plate installation

- inset into structural plywood rear panel
- do not replace entire rear wall with aluminium
- closed-cell perimeter gasket
- dense perimeter fastening
- external surface exposed to room air

### 2.3 Thermal interface

Preferred:

- very thin TIM
- thermal grease or phase-change material
- thin compliant pad only if tolerance requires it

Avoid thick silicone pads.

## 3 Rear-panel structure

Use:

```text
18 mm plywood structural rear wall
+
large inset 6 mm aluminium amplifier plate
```

Reasons:

- plywood provides cabinet stiffness/damping
- aluminium handles heat spreading/rejection
- smaller aluminium span reduces resonance risk
- plate also carries controls/connectors/PCB

The acoustic partition, rather than this outer rear wall, now contains the
driver pressure. The rear structure must still carry the electronics safely,
retain the plate, preserve cabinet stiffness, and provide the top/bottom
ventilation openings and service access without exposing live parts.
