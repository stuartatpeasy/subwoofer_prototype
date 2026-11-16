# Fastener bill of materials

> **State — current DAE inventory, 16 November 2026.** Owns the counted
> fastener instances and candidate Boltworld ordering references for one cabinet.
> Read for purchasing and reconciliation; [mechanical design](MECHANICAL.md)
> owns fit and assembly decisions and [power and grounding](POWER_AND_GROUNDING.md)
> owns the protective-earth stack. The model is a layout, not an approved
> purchasing list. Confirm the open items below and check current product,
> pack quantities and availability before ordering.

## 1. Modelled fasteners

Counts are individual fastener component instances in
[Subwoofer cabinet.dae](../3d_models/Subwoofer%20cabinet.dae), not packs and
without spares. The assembly breakdown makes the counts traceable. SKU
identities marked **old list** come from the earlier user-provided
`fastener_bom.txt` (no longer present), not a fresh product-page verification.
Where the DAE model does not specify material or finish, the listed SKU is a
candidate, not evidence of an exact match.

| Modelled part | Assembly and quantity | Total | Boltworld SKU and status |
| --- | --- | ---: | --- |
| M2.5 × 10 mm A2 PZ1 pan machine screw | PCB IC mounting 2 | 2 | `30021.025.010` — old list |
| M2.5 Form A A2 flat washer | PCB IC mounting 2 | 2 | `20206.025.000` — old list |
| M3 × 8 mm black PZ1 pan machine screw | Heatsinks 12 | 12 | `23413.030.008` — old list |
| M3 × 10 mm black PZ1 pan machine screw | PCB corners 4; mains inlet 2 | 6 | [`23413.030.010`](https://boltworld.co.uk/products/m3-x-10mm-pan-pozi-machine-screw-black-stainless-steel-a2-304-din-7985/) — Boltworld identity checked 16 November 2026 |
| M3 × 20 mm black PZ1 pan machine screw | Control panel 4 | 4 | `23413.030.020` — old list |
| M3 Form A flat washer, unspecified finish | PCB corners 4; control panel 4; inlet 2 | 10 | `20206.030.000` — old-list A2 candidate; finish of generic model unspecified |
| M3 Form A black A2 flat washer | Heatsinks 12 | 12 | `23493.030.000` — old list |
| M3 DIN 985 Nyloc nut | Control panel 4; inlet 2 | 6 | `20009.030.000` — old-list candidate; model material unspecified |
| M4 × 20 mm black countersunk machine screw | Rear panel 12; spreader 4 | 16 | `23415.040.020` — old list |
| M4 × 20 mm black PZ2 pan machine screw | Driver 8; PSU 4 | 12 | `23413.040.020` — old list; driver head and PSU penetration require the checks below |
| M4 × 25 mm A2 PZ2 countersunk machine screw | Protective-earth post 1 | 1 | `30022.040.025` — old list |
| M4 Form A flat washer | Spreader 4 | 4 | [`20206.040.000`](https://boltworld.co.uk/products/m4-form-a-flat-washer-stainless-steel-a2-304-din-125-4-3x9x0-8mm/) — A2 candidate; Boltworld identity checked 16 November 2026; check final clamp stack |
| M4 DIN 985 Nyloc nut | Spreader 4; protective-earth post 1 | 5 | `20009.040.000` — old-list candidate; model material unspecified |
| M4 DIN 6798J A2 internal-tooth washer | Protective-earth post 1 | 1 | `20251.040.000` — old list |
| M4 DIN 934 A2 full nut | Protective-earth post 1 | 1 | `10001.040.000` — old list |
| M4 × 10 mm Type E non-flanged timber insert | Rear brace 12; driver baffle 8 | 20 | `10130.040.010` — old-list zinc/yellow steel candidate; verify dimensions and pilot against supplied part |
| 3 × 15 mm black Pozidriv countersunk self-tapping screw | Lower vents 8; upper vent 4 | 12 | [`23581.290.016`](https://boltworld.co.uk/products/no-4-x-5-8-2-9-x-16mm-pozi-countersunk-self-tapping-screws-black-stainless-a2-304-din-7982/) — user-selected 2.9 × 16 mm near match; fit and penetration check required; page inaccessible during 16 November lookup, SKU from user and old list |

The existing list's 3.9 × 25 mm driver wood screw `23581.390.025`
is superseded by the modelled M4 driver screws and is excluded. Quantities
above replace the earlier list's quantities; the earlier file is no longer present.

## 2. Purchasing and fit gates

- Confirm the driver screw head bears correctly in the actual flange recess,
  and trial an insert in plywood. Check that the PSU screws do not exceed the
  3 mm penetration limit. The model's nominal PSU stack has no margin. See
  [mechanical design](MECHANICAL.md#12-downward-driver-and-carpeted-floor-clearance).
- The four modelled PCB-corner screws are M3 × 10 mm, while the current
  [plate stack proposal](MECHANICAL.md#21-aluminium-heatsink-plate) suggests
  M3 × 8 mm. Confirm the physical stack and blind-hole depth before choosing
  either length. The modelled spreader washer/nut stack also needs a physical
  bearing check before its final washers are selected.
- The DAE now depicts the selected full nut and outer Nyloc at the PE post.
  The nuts touch and the two ring terminals are not modelled, so check the
  final stack's ring-terminal bearing, full nylon engagement and temperature;
  see [power and grounding](POWER_AND_GROUNDING.md).
- Boltworld's M4 washer listing calls it 0.8 mm thick in its title but
  0.9 mm in its description and specification. Check the received thickness
  when sizing the spreader stack; do not assume either dimension is verified.
- Other omitted or unfinalised hardware, including the independent heatsink
  bonds and PCB spacers, is not counted. Panel-component supplied hardware,
  spares, and assembly consumables are not inferred from the DAE. Reconcile
  these with the electrical and mechanical authorities before ordering.

## 3. Inventory method

Run the [shared DAE inspector](../../Hub/tools/3d_models/README.md#read-only-dae-inspection)
from the project root:

```powershell
python ..\Hub\tools\3d_models\dae_inspect.py summary "3d_models\Subwoofer cabinet.dae" --all --limit 1000
```

Count named leaf component instances by assembly; do not count their parent
`SketchUp_Instance` wrappers as additional parts. Embedded fastener-shaped
geometry without a separate named component can escape this inventory. CAD
names and quantities do not establish the received items' fit or strength.
