# Thermal design

## 1 Cooling requirement

- no fan
- no forced air
- design for approximately 15–18 W worst-case IC heat dissipation
- normal music dissipation expected much lower
- maximum rated room ambient: 35 °C
- thermal-design margin case: 40 °C room ambient; this evaluates margin or
  required derating and does not claim continuous full-power operation above
  35 °C

## 2 Rear electronics chamber

All heat-producing electronics occupy a ventilated chamber behind the sealed
acoustic partition. Cool room air enters through a guarded lower grille and
warm air leaves through a guarded upper grille. The inlet and outlet must have
comparable net free area and an unobstructed path past the PSU, PCB, inductors,
regulators, and inner face of the aluminium plate. Cabinet feet or a plinth must
preserve the lower inlet clearance in normal use.

Do not size the chamber by litres alone. Its minimum depth is the smallest that
meets component, terminal, wire-bend, guard, segregation, and assembly
clearances and then passes thermal validation. Grille net free area, component
orientation, and the rear clear depth remain provisional until the scaled
layout and thermal-resistance budget are complete.

At the 35 °C rated room ambient, the final continuous thermal test must confirm
that the local air temperature at the PSU intake remains within the PSU's
documented full-load ambient range. The corresponding nominal allowance to the
RSP-200-36's 45 °C full-load ambient limit is 10 K. Repeat or extrapolate the
thermal assessment at 40 °C room ambient to establish margin; the corresponding
allowance is only 5 K. If the PSU intake exceeds its applicable limit, derate
the usable PSU load rather than treating the 40 °C case as a full-power claim.
