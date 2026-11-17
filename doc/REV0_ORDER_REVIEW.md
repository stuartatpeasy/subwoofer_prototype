# Rev0 system order review — 13 November 2026

> **HISTORY:** This is a dated review, not a current order procedure. The user
> reports on 17 November that the PCB and P01 plate are in fabrication and
> clearance is adequate for prototyping. Physical fit and thermal validation
> remain open. Current next actions are in [the action list](TODO.md).

> **Lifecycle:** Dated, read-only design review with one inspector-declaration repair; not an assembled qualification.
>
> **Owns:** Evidence and order disposition at this checkpoint. Current design details remain in [PCB layout](PCB_LAYOUT.md), [mechanical design](MECHANICAL.md), [thermal design](THERMAL.md), [power and grounding](POWER_AND_GROUNDING.md), and [system specification](SPECIFICATION.md).
>
> **Read when:** Auditing the historical 13 November order review. Use current authorities for present actions.
>
> **Historical conclusion:** No confirmed electrical or CAD hole-centre mismatch prevented a prototype PCB and P01 trial plate order. P01 was an intentional contact-stack trial. The dated order gates below describe the position at the time, not current actions.
>
> **Next gate:** Follow the current [action list](TODO.md) and [validation](VALIDATION.md) on received parts.
>
> **Limitations:** No live DipTrace DRC/connectivity report, JLCPCB rendered upload preview, JLCCNC quotation, physical parts, assembled temperature, or electrical measurements were obtained in this review.
>
> **Last reviewed:** 2026-11-13

**16 November update:** This dated review records the 13 November export.
The current DAE now contains the selected PDB182 as well as the PDB181,
resolving the model identity discrepancy in OR-05; its physical fit remains
open. The current geometry report passes. The driver and PSU fixing changes
and their remaining fit checks are owned by [mechanical design](MECHANICAL.md).
Other findings below remain historical evidence, not an assertion that every
feature of the later export has been requalified.

## 1 Scope and evidence

This review integrated the actual saved schematic, PCB XML, main-board fabrication ZIP, cabinet DAE and inspection declarations, control-panel XML, PCB STEP, P01 FreeCAD/STEP/PDF/ZIP, and current subsystem decisions. It separates checks of saved geometry and file correspondence from physical fit and prototype performance. It does not reopen the locked driver, cabinet envelope, 36 V RSP-200-36 PSU, analogue architecture, PBTL stage, accepted output-fault risk, or the bounded 140–150 W peak-output target.

The saved schematic, PCB and Gerber ZIP SHA-256 values match the [PCB release record](PCB_LAYOUT.md#1-reviewed-design-state-and-scope): `8D2DF8FC…`, `3744A783…`, and `7F4FC583…`. The ZIP passes CRC inspection and contains four copper layers plus separate plated and non-plated drills. Its six NPTH holes match the enlarged saved-board holes. The P01 order ZIP contains byte-for-byte copies of the linked [STEP](../output/pdf/Thermal%20spreader%20plate%20-%20P01.step) and [drawing](../output/pdf/Thermal%20spreader%20plate%20-%20P01.pdf). The STEP reimports as one valid 152 × 137 × 8 mm solid, volume 126817.184 mm³. Its hole centres and pilots match the drawing's dimensional scheme, but STEP pilots do not encode finished threads or selective finish.

The current PCB's four Ø3.40 mm NPTH centres at (5, 5), (85, 5), (5, 95), (85, 95) mm and two Ø2.90 mm centres at (44, 21), (44, 46) mm map to the six P01 tapped seats exactly under the documented plate coordinates `Xplate = 31 + Xpcb`, `Yplate = 118.5 − Ypcb`. The retained `main_board.step` predates the hole enlargement and still represents Ø3/Ø2.5 mm holes, so use the current XML and drill file for hardware clearances. The STEP remains useful as a nominal component-envelope model, subject to its date and actual component heights.

**14 November export update.** The STEP reviewed above has since been
replaced. The [current amplifier CAD export](3d_models/README.md#4-amplifier-pcb-assembly)
was verified against the saved PCB mounting-hole centres and diameters.

The cabinet DAE's plate rebate is 154 × 139 × 8 mm and the P01 blank is 152 × 137 × 8 mm. At their documented common centres, this gives a nominal 1 mm edge gap on all four sides and places the plate at the designed rear-face depth. This is a positive fit check for the metal outline; manufacturing, finish, wood-cut and fastening tolerances still need the received-part trial.

After correcting four vent leaf names in `3d_models/dae-inspect.json`, the shared inspector again reports 22.563884 L declared gross acoustic volume, 1.259100 L closed brace solids, and 20.304784 L provisional net with a **declared, unmeasured** 1.0 L driver allowance. It reports 135.83 cm² lower and 99.53 cm² upper projected open area. The run still exits 1 because the DAE contains two single-gang PDB181s instead of one PDB181 and the selected dual-gang PDB182. These are geometric screens, not measured displacement or airflow results.

## 2 Findings and consequences

| ID | Severity | Evidence state | Finding and practical consequence |
| --- | --- | --- | --- |
| OR-01 | High | Saved files verified; live checks absent | The 12 November drill enlargement was exported correctly, but an inspectable post-change DipTrace DRC/connectivity result and JLCPCB rendered upload preview are absent. A saved `DRCDone` flag does not establish either. Perform the specific checks in §3 before bare-board payment; see [PR-009/010](PCB_LAYOUT.md#2-findings). |
| OR-02 | High | P01 geometry verified; manufacturing acceptance absent | P01 STEP contains tap-drill bores. Its PDF defines twelve M3 sink threads, four M3 board threads, two M2.5 IC-seat threads, fixing/PE countersinks, 6061-T6, bare and unblasted thermal/PE zones, and seat/land heights. A STEP-only quote could omit features needed for assembly, cooling or earthing. Obtain explicit supplier acceptance of the PDF and finish alternatives in §3. |
| OR-03 | High | Nominal calculation; real stack unmeasured | The nominal PCB rear plane is 4.00 mm above the pocket floor, the IC land is 2.75 mm above it, and the CAD PowerPAD projects 1.25 mm from the board: `4.00 − 2.75 − 1.25 = 0 mm` nominal gap. Package, solder, PCB and machining variation may leave a thick grease gap or make the IC carry corner-clamping force. Select shims and, if required, matched corner spacers by dry fit; P01 may need a second plate. Do not tighten a rocking board against the IC. |
| OR-04 | Medium | DAE geometry verified | The modelled plate-fixing washer stack ends around Y = 470 mm, while the rear-ply inboard bearing face is at Y = 472 mm: approximately 2 mm of nominal air, so the depicted hardware does not clamp the panel. Size and place the actual washer/nut stack against the 4 mm residual plywood land; trial the insert, countersink and wood bearing before final rear-panel cutting. This does not establish a P01 CNC error. |
| OR-05 | Medium | Model discrepancy verified | The DAE has two PDB181 control bodies, although the selected crossover control is PDB182 with about 2 mm more rearward reach and six PC pins. The 65 × 137 × 1.6 mm FR-4 control-panel XML has no fabrication export yet. Correct the model, check real pot/switch/inlet/RCA mounting and cover clearances, then export and preview the separate panel before ordering or cutting it. |
| OR-06 | Medium | Inventory verified | There is no consolidated build BOM or system purchasing list. The schematic and PCB have 132 matching electrical reference identities and values; 121 non-test-pad references have manufacturer-part fields, while eleven test pads appropriately are not purchased. Deduplicate quantities and add mates, pigtails, PSU, inlet/fuse/drawer, driver, sinks, controls, FR-4 panel, fasteners, washers, terminals, guards and wiring before the **component** order. Check live availability and exact orderable suffixes then. This does not block bare-board fabrication. |
| OR-07 | Medium | Saved net assignment verified; manufacturer detail open | U5 MP4581GN-Z's exposed pad is assigned to GND in the PCB. The available [MPS datasheet](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP4581GN) identifies SOIC-8EP and pin 7 GND but does not clearly state the exposed pad's electrical connection in the inspected text. Obtain MPS or evaluation-board copper confirmation before populating; seek it before board payment if it could change the land connection. No incorrect connection was established. |
| OR-08 | Medium | Model and thermal estimate; assembly unmeasured | The cabinet DAE omits the amplifier PCB and plate pocket, so it cannot prove the installed component, lead, sink-screw-tip and PSU clearances. The present two-sink screen at 35 °C room and 10 W IC heat predicts about 53 °C sink bases, 60–63 °C exposed seam and 77–81 °C IC junction, conditional on free air, sound joints and about 0.05 mm IC grease. The sink tips extend about 22 mm behind the ash legs, so placement must provide a deliberate wall gap. Check physical clearances and temperatures on the built unit; the model alone is not a reason to resize the accepted PSU or sinks. |
| OR-09 | High for first energisation | Construction still open | Fit the dedicated M4 PE stud before the left sink covers its head; bond each externally accessible anodised sink separately, and establish the one intentional board-GND-to-plate connection without accidental mounting bonds. Fit the inlet rear cover, PSU terminal guard, protected mains loom and independent PE paths. Verify protective continuity before mains energisation using [prototype validation](VALIDATION.md#1-mains-construction-and-protective-earth). |

The existing U9 DPAK tab land, test-pad paste, output-filter values, RESET/dropout margin, analogue noise and sustained thermal performance retain their documented prototype or stencil gates. This review did not find a new confirmed fault that warrants changing those accepted rev0 selections before a bare-board order. The [thermal screen](THERMAL.md#16-current-8-mm-plate-and-intermittent-output-12-november-2026) remains a model: for example, an actual IC grease gap of 0.10 mm instead of 0.05 mm approximately doubles its ideal bulk film resistance, so witness and temperatures matter more than another nominal decimal place.

## 3 Bounded pre-payment checks

1. **Bare PCB:** Rerun affected DipTrace DRC and net-connectivity checks on the saved board after the six enlarged NPTH holes. Upload the [current Gerber ZIP](../diptrace/main_board_gerber.zip) for a rendered JLCPCB preview and confirm Top/Inner 1/Inner 2/Bottom in order, 90 × 100 mm outline, six non-plated mounting holes at the current diameters, mask/silk alignment, and standard four-layer 1.6 mm options. Do not substitute the older PCB STEP for this check. If a stencil is ordered, remove paste from TP1–TP11 as [PR-013](PCB_LAYOUT.md#2-findings) describes.
2. **P01 plate:** Submit the matched [P01 ZIP](../output/thermal%20spreader%20plate.zip) and require the quotation/production acknowledgement to incorporate the PDF's tapped threads, countersinks, 6061 material/temper, selectively bare/unblasted contact zones and finished land/seat dimensions. If selective finish is unavailable, the documented as-machined alternative is preferable to silently anodising PE or thermal contacts. JLCCNC's [finish guidance](https://jlccnc.com/blog/how-to-remove-anodizing) says bare zones and boundaries should be explicit in the drawing; supplier acceptance is still unobserved here.
3. **Component order:** Prepare a counted BOM with external items and check current stock, suffixes and mating connector forms. Resolve U5 exposed-pad confirmation. Order the separate FR-4 panel only after its own export/preview and real control/inlet fit review.

These are separate release gates for different orders, rather than a demand to finish acoustic and heat measurements before purchasing a prototype PCB.

## 4 Received-part dry fit and bounded first build

1. Check all six PCB screws enter P01 without forcing the board; check actual hole clearances and any insulating sleeves. Compare trimmed rear lead/component heights, six inner sink screw tips and pocket floor. Seat four corners first, measure each inner shim gap and IC pad-to-land gap, then establish a thin, continuous grease witness without board bow or rocking. If the IC contacts before the supports seat, use a matched trial spacer set and remeasure; redesign the plate if the contact cannot be made repeatably.
2. Trial the plate-to-plywood clamp stack and rear-panel support. Trial each sink slot and washer, verify no unsafe tip projection, and add independent sink bonds. Confirm control-panel stiffness, correct PDB182 and switch lug paths, inlet cover and wiring bend clearance, PSU 3 mm maximum underside screw penetration, and service slack for mains, DC, signal and driver harnesses.
3. Reconcile actual driver displacement and all sealed-chamber intrusions against the 20.0 L geometric target before final cabinet cuts. Keep the partition and driver cable feed-through airtight. Check loaded carpet clearance and unobstructed bottom-to-upper-rear airflow at the intended wall spacing.
4. Before first mains energisation, complete the small number of credible safety checks in [validation](VALIDATION.md#1-mains-construction-and-protective-earth). Then measure loaded 17V3/15VA/12VAMP, RESET timing, output DC and bounded clean output. Use representative sustained operation for the temperature check; the target does not require continuous 150 W audio output.
