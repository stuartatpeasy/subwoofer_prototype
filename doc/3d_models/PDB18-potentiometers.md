# PDB18 rear controls in this project

> **State — current project placement note; reviewed 11 November 2026.** The [reusable model and dimensional record](../../../Hub/3d_models/electronics/PDB181-E420K-103A2/README.md) is owned by the Hub. This page owns only the placement and fit consequences for this project. Use the model as a layout reference; check SketchUp scale and actual hardware before machining.

## 1. Project use

The selected level control is [PDB181-E420K-103A2](../../../Hub/3d_models/electronics/PDB181-E420K-103A2/README.md), and the selected cutoff control is [PDB182-K420K-203B](../../../Hub/3d_models/electronics/PDB182-K420K-203B/README.md). Both are placed in the 1.6 mm FR-4 control panel. Their 6.5 mm threaded bushings have nominal length for this panel; verify the supplied hardware, actual knob fit, panel strength and wiring. The cutoff part retains PC pins; the alternative GTRB2 controls were rejected in [analogue front end](../FRONT_END.md).

The 11 November cabinet DAE currently instantiates PDB181 at **both** knob
positions. Replace one instance with the selected PDB182 model and recheck
its 2 mm greater rear body depth and six PC pins before using the layout for
panel or harness decisions. The intended left/right assignment is not
established by the mesh. The project [DAE inspection declarations](../../3d_models/dae-inspect.json)
now check both part counts and return a mismatch until this correction is made.

## 2. Model route

Open the [Hub part record](../../../Hub/3d_models/electronics/PDB181-E420K-103A2/README.md) for the DAE, guide, preview, dimensional source, limitations, generator and reconstruction command.
