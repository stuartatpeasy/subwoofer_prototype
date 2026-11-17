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
| Rear FR-4 control panel | [SketchUp layout model](#3-rear-fr-4-control-panel) |
| Amplifier PCB assembly | [SketchUp layout model](#4-amplifier-pcb-assembly) |

## 1. Driver placement

The selected [SB23MFCL45-4 model and dimensional record](../../../Hub/3d_models/loudspeakers/SB23MFCL45-4/README.md) provide the DAE, separate clearance/drilling guide, source, limitations and reconstruction route. Use the guide with the same origin and rotation as the model, and confirm its 234.25 mm flange diameter after SketchUp import. Its static geometry does not include cone travel. The DAE now uses eight M4 × 20 mm pan-head screws and M4 × 10 mm inserts; [mechanical design](../MECHANICAL.md#12-downward-driver-and-carpeted-floor-clearance) owns the fit and installation checks. Allow for terminal wiring and vent airflow; check the received driver, gasket and baffle cut-out before machining. The project’s 1.0 L driver displacement is provisional, as recorded in the [specification](../SPECIFICATION.md).

## 2. Fastener layout references

The [fastener BOM](../FASTENER_BOM.md) counts the cabinet DAE instances and records candidate Boltworld SKUs.

The shared library includes the A2 stainless [M2.5 × 10 mm PZ1 pan screw](../../../Hub/3d_models/fasteners/M2p5x10_PZ1_Pan_Head_Machine_Screw_A2/README.md)
and [M2.5 Form A flat washer](../../../Hub/3d_models/fasteners/M2p5_Form_A_Flat_Washer_A2/README.md)
for layout.

The [M3 × 8 mm black PZ1 pan screw](../../../Hub/3d_models/fasteners/M3x8_PZ1_Pan_Head_Machine_Screw_Black/README.md) and [M3 Form A black A2 flat washer](../../../Hub/3d_models/fasteners/M3_Form_A_Flat_Washer_Black_A2/README.md) are nominal references for the heatsink fixing stack in [mechanical design](../MECHANICAL.md#21-aluminium-heatsink-plate). Their supplier examples and finishes are not yet a project procurement selection. The separate [M4 × 25 mm A2 PZ2 countersunk machine screw](../../../Hub/3d_models/fasteners/M4x25_PZ2_Countersunk_Machine_Screw_A2/README.md) is available for layout; its intended project location has not been specified.

Boltworld SKU `20251.040.000` has an [M4 DIN 6798J A2 internal-tooth washer model](../../../Hub/3d_models/fasteners/M4_DIN6798J_Internal_Tooth_Lock_Washer_A2/README.md), `10001.040.000` has an [M4 DIN 934 A2 full-nut model](../../../Hub/3d_models/fasteners/M4_DIN934_Full_Hex_Nut_A2/README.md), and `23415.040.025` has a [black A2 M4 × 25 mm PZ2 countersunk screw model](../../../Hub/3d_models/fasteners/M4x25_PZ2_Countersunk_Machine_Screw_Black_A2/README.md). These user-specified catalogue identities support layout; their assembly positions and use remain to be decided. The Hub records supply the DAEs, previews, dimensions, generators and limitations. The [shared fastener maker](../../../Hub/tools/3d_models/README.md#fastener-model-maker) now accepts explicit specifications or its verified Boltworld SKU presets.

## 3. Rear FR-4 control panel

The [SketchUp DAE](../../3d_models/control_panel.dae) depicts black FR-4 with
a white legend. It uses the [DipTrace STEP](../../3d_models/control_panel.step)
for the 65 × 137 × 1.6 mm plate, 11 circular holes and 29 × 48 mm IEC
cut-out. The [DipTrace layout XML](../../diptrace/control_panel.dipxml)
supplies the Top Silk text, two arcs and line. The artwork is a visual
approximation using Arial outlines fitted to the saved Helvetica-Narrow
text blocks. For fabrication, export the artwork from DipTrace.

Viewed from the printed side, the lower-left corner of the bounding
rectangle is the origin, +X points right, +Y points up and +Z points out
of the panel. The plate spans Z = −1.6 mm to 0 mm. The white geometry is
offset 0.05 mm to avoid coplanar rendering artefacts. See
[mechanical design §3.1](../MECHANICAL.md#31-current-fr-4-control-panel-11-november-2026)
for cabinet placement and fit.

To rebuild, run the [panel generator](../../tools/freecad/build_control_panel_dae.py)
in FreeCAD 1.1 on Windows with Arial and the sibling Hub checkout available.
In the FreeCAD Python console, run the following from the project directory
or substitute the script's absolute path.

```python
import runpy
runpy.run_path("tools/freecad/build_control_panel_dae.py", run_name="__main__")
```

The generator replaces the DAE and checks that it reopens with both
materials. The exported plate mesh is closed and the eleven STEP hole
centres and diameters agree with the XML. The initial export was previewed
in FreeCAD and the user confirmed that it imported successfully in SketchUp.
The current export uses the revised DipTrace artwork, including the
`L` and `R` input labels and the 2026 credit line.

## 4. Amplifier PCB assembly

For SketchUp for Web, generate `3d_models/main_board_sketchup.zip` on demand
using the amplifier generator below. The ZIP is a disposable output containing
the retained [DAE](../../3d_models/main_board.dae) and two
[legend textures](../../3d_models/main_board_textures). Its absence is normal.
The [14 November STEP](../../diptrace/main_board.step) supplies the board,
component and pin geometry. The [DipTrace XML](../../diptrace/main_board.dipxml)
confirms the 90 × 100 mm outline and six mounting holes. The four corner
holes are Ø3.40 mm and the two IC-adjacent holes are Ø2.90 mm. The STEP
board is 1.6058 mm thick. In the DAE, the top of the board is Z = 0 and
the assembly extends from Z = −5.0 to +19.4 mm.

The [rev0 fabrication archive](../../diptrace/main_board_gerber.zip)
supplies the white legends for both faces. Red represents solder mask.
Charcoal and metallic tones represent component packages and contacts.
The model carries the geometry present in the STEP, with its exported
pin lengths. Use the STEP for exact curved geometry and mechanical
clearance checks. The 51,242-triangle DAE is a layout mesh. Its component
mesh bounds agree with the STEP within 0.06 mm per axis limit.

To rebuild, run the [amplifier generator](../../tools/freecad/build_amplifier_dae.py)
from the FreeCAD 1.1 Python console with the sibling Hub checkout available.
Run the following from the project directory or use the absolute script path.

```python
import runpy
runpy.run_path("tools/freecad/build_amplifier_dae.py", run_name="__main__")
```

The generator reads the retained STEP, DipTrace XML and fabrication archive
linked above and the shared Hub toolkit. It overwrites the retained DAE and
textures while writing the ZIP, so preserve those files before regenerating if
their current versions are needed. It writes the DAE, textures and ZIP;
check the ZIP contains the DAE and both textures, and that the DAE opens and
shows the board and both legends. The existing DAE has the verified mesh
bounds stated above; a fresh reconstruction has not been checked this turn.

## 5. Printer-job retention gap

A local ignored `3d_models/upper vent segment.gcode` contains a Cura 5.13.0
CR-20 Pro job with partial embedded settings. Its source STL or slicer project
and complete print configuration have not been identified; the G-code alone
does not establish that the job was printed or make it reproducible. Preserve
the local file while recovering the source and settings. The separate ignored
`test squares 20mm.gcode` also has no identified retained source or print
record. Before treating either as a repeatable project job, retain its source
and record the material print settings in `3d_models/PRINT_SETTINGS.json` or
a suitable slicer project, as required by [project instructions](../../AGENTS.md).
