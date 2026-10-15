# DipTrace data and tooling

> **Lifecycle:** Current tooling and evidence route  
> **Owns:** Locations, authority boundaries, and inspection rules for DipTrace
> project data and the shared Hub SDK route
> **Does not own:** Circuit values, PCB design decisions, manufacturing approval,
> measured results, or the source schematic/layout themselves  
> **Read when:** Inspecting, comparing, parsing, exporting, or proposing tooling
> for DipTrace schematic, PCB, component-library, or pattern-library data  
> **Current approved action:** Treat `diptrace/main_board.dchxml` as the canonical
> partial schematic; inspect it read-only for circuit questions
> **Next gate:** Complete the schematic, then validate its electrical details and
> any future PCB export against the selected design
> **Limitations:** An untracked PCB XML file is present but has not been reviewed
> or made authoritative; no live plug-in exchange has been inspected, and no
> parser or plug-in has been qualified
> **Last reviewed:** 2026-10-15

## 1 Authority and retained resources

The canonical schematic XML declares DipTrace version `5.3.0.3`. By the user's
2026-10-04 decision,
`diptrace/main_board.dchxml` is the canonical source for the current partial
schematic. It is a DipTrace schematic XML file with root type
`DipTrace-Schematic`, version `5.3.0.3`, and units `inch`. There is presently no
matching `.dch` file in `diptrace/`; do not require one as schematic authority.
An untracked `diptrace/main_board.dipxml` is now present; a root-only check on
15 October 2026 found `DipTrace-PCB`, version `5.3.5.1`, and units `mm`.
Its source, design state, and authority have not been reviewed. There is no
matching `.dip` file. Establish the PCB design authority before using this XML
as more than an unreviewed snapshot. PDF, BOM, pick-and-place, Gerber X2, and
drill exports remain secondary
evidence for their specific visual, assembly, or manufacturing purposes.

The shared DipTrace Plugin & XML AI Context Pack now lives in the Hub. Start
with the [Hub DipTrace tooling route](../../Hub/tools/diptrace/README.md),
which selects the relevant SDK reference for saved XML, libraries, or plug-in
work. The pack is reference material and templates, not an installed plug-in.
This project retains only its design data and project-specific decisions.

The complete official field catalogues also ship with DipTrace under
`C:\Program Files\DipTrace\Docs`. Use them for fields or enums absent from
the pack. Do not guess an undocumented field or runtime behaviour.

## 2 Minimal reading route

For DipTrace XML, first read the [Hub task dispatcher](../../Hub/tools/diptrace/README.md)
and only its selected SDK pages. Then read this project's relevant design
authority. For the current partial schematic, the needed dialect is schematic
XML; the PCB and reusable-library dialects are for their respective future
files. This routing keeps the large SDK out of routine electrical-design
context.

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

## 4 Interpretation rule ownership

The [Hub SDK route](../../Hub/tools/diptrace/README.md) and its selected
references own the reusable XML conventions: omitted defaults, units, frames,
transforms, segment properties, unknown data, and live-exchange merge rules.
Apply them to this project's saved schematic rather than maintaining a second
copy of those rules here. A read-only extractor needs substantially less
qualification than a writer or optimiser.

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

The [Hub SDK route](../../Hub/tools/diptrace/README.md) owns pack provenance,
refresh, and compatibility. Reconfirm its contracts against the DipTrace
version then in use; the pack explicitly does not guarantee every older or
future build. This project's reconstruction depends on the retained Hub pack
and its own `diptrace/main_board.dchxml` source.
