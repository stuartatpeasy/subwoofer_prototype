# DipTrace data and tooling

> **Lifecycle:** Current tooling and evidence route  
> **Owns:** Locations, authority boundaries, and inspection rules for DipTrace
> project data and the retained Plugin & XML AI Context Pack  
> **Does not own:** Circuit values, PCB design decisions, manufacturing approval,
> measured results, or the source schematic/layout themselves  
> **Read when:** Inspecting, comparing, parsing, exporting, or proposing tooling
> for DipTrace schematic, PCB, component-library, or pattern-library data  
> **Current approved action:** Read-only inspection of retained exports; do not
> modify/import XML or create/deploy a plug-in without task-specific authorization  
> **Next gate:** Retain the first project `.dchxml` and `.dipxml` snapshots and
> validate their root type, version, units, and correspondence to the native files  
> **Limitations:** No project design export or live plug-in exchange has yet been
> inspected, and no parser or plug-in has yet been implemented or qualified  
> **Last reviewed:** 2026-09-17

## 1 Authority and retained resources

The project uses DipTrace 5.3.0.3. Native `.dch` and `.dip` files remain the
authoritative editable schematic and PCB sources. Corresponding `.dchxml` and
`.dipxml` files are the preferred machine-readable inspection snapshots; PDF,
BOM, pick-and-place, Gerber X2, and drill exports are secondary evidence for
their specific visual, assembly, or manufacturing purposes.

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

1. Preserve the matching native `.dch` or `.dip` file.
2. Save/export the corresponding `.dchxml` or `.dipxml` snapshot without
   replacing the native authority.
3. Record or compute a SHA-256 hash for every inspected input.
4. Validate the XML root `Type`, `Version`, and `Units` before interpreting it.
5. Parse locally and return a bounded, task-specific report rather than loading
   the complete XML into conversational context.
6. Compare schematic and PCB component, footprint, pin/pad, and net identities
   before treating the two snapshots as a matched design state.
7. Use PDFs when visual organisation or placement matters and manufacturing
   outputs only for the particular fabrication checks they can establish.

When project design files are introduced, use a narrow retained tree such as
`diptrace/source/` for native files, `diptrace/exchange/` for XML snapshots, and
`diptrace/review/` for intentionally retained visual or tabular exports. Do not
create or ignore bulk generated outputs until their retained inputs and
reconstruction route are known.

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
