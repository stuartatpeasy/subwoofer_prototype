# DipTrace data and tooling

> **Lifecycle:** Current tooling and evidence route  
> **Owns:** Locations, authority boundaries, and inspection rules for DipTrace
> project data and the retained Plugin & XML AI Context Pack  
> **Does not own:** Circuit values, PCB design decisions, manufacturing approval,
> measured results, or the source schematic/layout themselves  
> **Read when:** Inspecting, comparing, parsing, exporting, or proposing tooling
> for DipTrace schematic, PCB, component-library, or pattern-library data  
> **Current approved action:** Treat `diptrace/main_board.dchxml` as the canonical
> partial schematic; inspect it read-only for circuit questions
> **Next gate:** Complete the schematic, then validate its electrical details and
> any future PCB export against the selected design
> **Limitations:** No PCB design export or live plug-in exchange has been
> inspected, and no parser or plug-in has been qualified
> **Last reviewed:** 2026-10-11

## 1 Authority and retained resources

The project uses DipTrace 5.3.0.3. By the user's 2026-10-04 decision,
`diptrace/main_board.dchxml` is the canonical source for the current partial
schematic. It is a DipTrace schematic XML file with root type
`DipTrace-Schematic`, version `5.3.0.3`, and units `inch`. There is presently no
matching `.dch` file in `diptrace/`; do not require one as schematic authority.
For future PCB work, decide the `.dip`/`.dipxml` authority when those files
exist. PDF, BOM, pick-and-place, Gerber X2, and drill exports remain secondary
evidence for their specific visual, assembly, or manufacturing purposes.

The retained DipTrace Plugin & XML AI Context Pack is at:

`tools/diptrace/plugin_sdk/`

Its dispatcher is `tools/diptrace/plugin_sdk/README.md`. The retained pack is
version `2026.08.06-r7`, contract date 2026-08-06. It is reference material and
templates, not an installed plug-in. Retain it as project source/reference data;
do not ignore it as a generated dependency tree.

The complete official field catalogues also ship with DipTrace under
`C:\Program Files\DipTrace\Docs`. The context pack is the first source for the
contracts and operations it covers; use those PDFs for fields or enums absent
from the pack. Do not guess an undocumented field or runtime behaviour.

## 2 Minimal reading route

Load only the files needed for the task:

1. For any saved XML inspection, start with
   `tools/diptrace/plugin_sdk/02_diptrace_xml_conventions.md`.
2. For PCB data, then read
   `tools/diptrace/plugin_sdk/10_pcb_xml_reference.md`.
3. For schematic data, instead read
   `tools/diptrace/plugin_sdk/20_schematic_xml_reference.md`.
4. For a real DipTrace plug-in, also read `01_plugin_architecture.md`,
   `05_production_plugin_workflow.md`, the matching manifest under `templates/`,
   `50_common_operations.md`, and `60_common_mistakes.md`.
5. Read `12_pcb_text_geometry.md` and `56_shape_geometry_foundations.md` only
   for PCB text/placement geometry. Add `55_heavy_geometry_optimization.md` and
   `70_complex_plugin_review.md` for a complex geometry plug-in.
6. Read the CompEdit or PattEdit references only when the task concerns reusable
   component or pattern libraries rather than the placed project design.

This routing keeps the large pack out of routine electrical-design context.

## 3 Read-only inspection workflow

For each design checkpoint:

1. Inspect the current canonical `diptrace/main_board.dchxml` for schematic
   questions; preserve it during read-only review.
2. Record or compute a SHA-256 hash for every inspected input.
3. Validate the XML root `Type`, `Version`, and `Units` before interpreting it.
4. Parse locally and return a bounded, task-specific report rather than loading
   the complete XML into conversational context.
5. Compare schematic and PCB component, footprint, pin/pad, and net identities
   before treating the two snapshots as a matched design state.
6. Use PDFs when visual organisation or placement matters and manufacturing
   outputs only for the particular fabrication checks they can establish.

Keep the present canonical XML at its existing path. If future design files
justify a directory split, update this authority and the project index as part
of that move. Do not create or ignore bulk generated outputs until their
retained inputs and reconstruction route are known.

For separate ground nets that meet physically, DipTrace's [official FAQ](https://diptrace.com/support/faq/)
recommends a zero-ohm resistor (or small inductor) between nets; a direct wire
merges them. Place such a link only at a genuine PCB junction and check its
current rating and copper path. If the returns meet off-board at the PSU or
distribution wiring, keep the board nets distinct and show the junction in a
separate system wiring drawing or through explicitly labelled connector pins.
The link symbol is a netlist aid, not a substitute for deciding the physical
return route. An unpopulated 0 Ω part is an open circuit, so the former R1/R2
placeholders were removed. The canonical schematic now uses one `GND` net;
control local return copper in layout. Check completed copper and net
connectivity, and review its high-current return paths explicitly.

## 4 Important interpretation rules learned from the pack

- A missing XML attribute normally means the documented default, not zero.
- Root units apply to ordinary geometry, but not to every font scalar.
- Project objects and embedded symbol/footprint objects use different
  coordinate frames; angles are normally radians, while some orientations and
  3D rotations use other conventions.
- PCB embedded footprint geometry is an exchange-time variant. Bottom-side
  placement requires the documented side transform, but `Flip`/`HorzFlip` must
  not be applied a second time.
- Pad mask/paste `Top*` and `Bot*` fields describe the pad's near and far faces,
  not unconditionally the physical top and bottom of the assembled PCB.
- PCB trace and schematic wire segment properties belong to the segment's
  ending point, not its starting point.
- Saved XML and a live plug-in exchange use the same dialect but may not have
  identical payloads or embedded styles. A plug-in must be tested against a
  captured real exchange with the intended export scope.
- Unknown attributes and elements must be preserved. Full-file generation also
  requires dense, ordered identifiers; plug-in edits follow different ID and
  merge rules.

These rules make the pack immediately usable for a read-only extractor. They
also explain why a writer or optimizer needs substantially more qualification.

## 5 Future parser and plug-in boundary

The preferred first implementation is a read-only Python query/indexing tool,
not an importing plug-in. It should:

- leave source XML content and timestamps untouched;
- validate supported root types and reject malformed or non-finite geometry;
- accept legacy comma decimals but emit no rewritten XML;
- index components, pins/pads, nets, rules, layers, placements, traces, vias,
  pours, ratlines, and saved design errors;
- resolve embedded library references while suppressing verbose library
  geometry unless a query needs it;
- cache only against the complete source hash and parser version; and
- produce deterministic, bounded summaries selected by reference designator,
  net, layer, rule class, or board region.

If a live plug-in is later justified, first use the pack's export-only
`templates/python/capture_exchange.py` with an `ImpMode=None` manifest derived
from the intended production scope. Keep the captured original immutable.
Write-back must remain unsupported until copied fixtures, source/packaged-EXE
parity, atomic-save/no-op behaviour, installed-artifact verification, and a
disposable-project DipTrace smoke test all pass.

In particular, nested wire, trace, and point containers can be replaced rather
than merged, DipTrace detects work from the exchange file changing rather than
from process exit status, and cancellation can hard-terminate the plug-in.
Those behaviours make casual XML rewriting inappropriate for the live project.

## 6 Refresh and reconstruction

The context pack came from the official DipTrace Tutorials and Docs page under
“DipTrace Plugin & XML. AI Context Pack”. To refresh it, download the archive
again, compare its stated pack version and contents with the retained copy, and
replace the project copy only as an intentional reviewed update. Reconfirm its
contracts against the DipTrace version then in use; the pack explicitly does
not guarantee every older or future build.
