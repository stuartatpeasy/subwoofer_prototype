# 3D model catalogue

> **State — current project CAD route; reviewed 13 November 2026.** Generic component geometry, source evidence and generators live in the [Hub 3D library](../../../Hub/3d_models/README.md). This subtree records only this project’s model selections and placement consequences. The cabinet DAE remains project-specific in `3d_models/`. Read the part note needed for the current layout task, then its Hub leaf record.

| Project component | Project placement note |
| --- | --- |
| SB23MFCL45-4 driver | This page |
| RSP-200-36 PSU | [PSU](RSP-200-36.md) |
| DD11.0111.1111 inlet | [Inlet](DD11.0111.1111.md) |
| PDB181 and PDB182 controls | [Controls](PDB18-potentiometers.md) |
| NYS367 sockets and polarity switch | [Rear signal parts](Rear-signal-parts.md) |
| Provisional 557-140AB heatsink | [Heatsink](557-140AB.md) |
| Thermal spreader plate working model | [Mechanical design §2.1](../MECHANICAL.md#21-aluminium-heatsink-plate) |

## 1. Driver placement

The selected [SB23MFCL45-4 model and dimensional record](../../../Hub/3d_models/loudspeakers/SB23MFCL45-4/README.md) provide the DAE, separate clearance/drilling guide, source, limitations and reconstruction route. Use the guide with the same origin and rotation as the model, and confirm its 234.25 mm flange diameter after SketchUp import. Its static geometry does not include cone travel. The provisional [4.0 × 25 mm black countersunk wood-screw model](../../../Hub/3d_models/fasteners/4x25mm_Black_PZ2_Countersunk_Wood_Screw/README.md) supports the driver-fixing layout; [mechanical design](../MECHANICAL.md#12-downward-driver-and-carpeted-floor-clearance) owns the length and tip-clearance decision. Allow for terminal wiring and vent airflow; check the received driver, gasket and baffle cut-out before machining. The project’s 1.0 L driver displacement is provisional, as recorded in the [specification](../SPECIFICATION.md).

## 2. Fastener layout references

The [M3 × 8 mm black PZ1 pan screw](../../../Hub/3d_models/fasteners/M3x8_PZ1_Pan_Head_Machine_Screw_Black/README.md) and [M3 Form A black A2 flat washer](../../../Hub/3d_models/fasteners/M3_Form_A_Flat_Washer_Black_A2/README.md) are nominal references for the heatsink fixing stack in [mechanical design](../MECHANICAL.md#21-aluminium-heatsink-plate). Their supplier examples and finishes are not yet a project procurement selection. The separate [M4 × 25 mm A2 PZ2 countersunk machine screw](../../../Hub/3d_models/fasteners/M4x25_PZ2_Countersunk_Machine_Screw_A2/README.md) is available for layout; its intended project location has not been specified.

Boltworld SKU `20251.040.000` has an [M4 DIN 6798J A2 internal-tooth washer model](../../../Hub/3d_models/fasteners/M4_DIN6798J_Internal_Tooth_Lock_Washer_A2/README.md), `10001.040.000` has an [M4 DIN 934 A2 full-nut model](../../../Hub/3d_models/fasteners/M4_DIN934_Full_Hex_Nut_A2/README.md), and `23415.040.025` has a [black A2 M4 × 25 mm PZ2 countersunk screw model](../../../Hub/3d_models/fasteners/M4x25_PZ2_Countersunk_Machine_Screw_Black_A2/README.md). These user-specified catalogue identities support layout; their assembly positions and use remain to be decided. The Hub records supply the DAEs, previews, dimensions, generators and limitations. The [shared fastener maker](../../../Hub/tools/3d_models/README.md#fastener-model-maker) now accepts explicit specifications or its verified Boltworld SKU presets.
