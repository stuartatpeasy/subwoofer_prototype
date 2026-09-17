# Mechanical design

## 1 PCB and mechanical constraints

Amplifier PCB sits parallel to rear aluminium plate.

Critical constraint:

```text
PCB underside to aluminium plate clearance ≈ 1.2 mm
```

Therefore:

- no through-hole parts anywhere on amplifier board
- all parts SMD
- avoid unplanned bottom-side parts
- TPA3251 may be mounted on the PCB underside so its exposed thermal pad faces
  the aluminium plate; verify the complete package/PCB/TIM/plate stack against
  the manufacturer package and assembly requirements before layout

### 1.1 Aluminium heatsink/control plate

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

### 1.2 Plate installation

- inset into structural plywood rear panel
- do not replace entire rear wall with aluminium
- closed-cell perimeter gasket
- dense perimeter fastening
- external surface exposed to room air

### 1.3 Thermal interface

Preferred:

- very thin TIM
- thermal grease or phase-change material
- thin compliant pad only if tolerance requires it

Avoid thick silicone pads.

## 2 Rear-panel structure

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
