# Project Documentation Review Procedure

Use this procedure for documentation architecture, review, consolidation, or handover work. It supplements `AGENTS.md`; direct user instructions still take precedence.

## 1. Purpose

Minimise documentation size and context cost without losing project-relevant evidence, provenance, safety information, decisions, or reproducibility. Prefer one authoritative statement of each fact and links from its consumers.

## 2. Review modes

Select one mode before loading the documentation corpus.

### 2.1 Targeted review

Use **TARGETED REVIEW** for a named topic, document set, link repair, formatting change, or authority-boundary improvement that does not claim to provide a complete project handover.

1. Read the root `README.md`, its route for the task, and the named or directly affected authorities.
2. Inspect Git status and preserve user-owned or unrelated changes.
3. Search for consumers of the affected facts, filenames, headings, and links.
4. Inspect only the artefacts and reconstruction routes affected by the change.
5. Update the affected authorities, indexes, routes, and links in the same turn.
6. Validate the changed scope and its direct consumers.

A targeted review does **not** require reading every tracked document, inventorying every binary artefact, creating a session-evidence ledger, or producing a comprehensive handover. Expand to comprehensive mode if the affected authority cannot be bounded confidently, unique evidence may otherwise be lost, or the user requests a project-wide consolidation or handover.

### 2.2 Comprehensive consolidation

Use **COMPREHENSIVE CONSOLIDATION** when the user requests a full documentation review, broad consolidation, project handover, or a change that reassigns several interacting authorities across the project.

This mode requires the complete inventory, full-corpus reading, evidence-ledger gate, route audit, and handover in Sections 5, 6, 10, and 11.

### 2.3 Repeat invocation

To repeat the same review-then-approval sequence used to establish this
architecture, the user may first ask:

> Perform the comprehensive documentation review in
> `doc/DOCUMENTATION_REVIEW.md`. Analyse the current documentation and propose
> optimisations, but do not change files.

After reviewing the proposal, the user may continue with:

> Implement all accepted recommendations from that review, complete its
> validation and handover, and do not commit or push unless I ask.

The first request invokes **COMPREHENSIVE CONSOLIDATION** through the analysis
and proposal stage only. The second authorises documentation moves, splits,
merges, and rewrites justified by the accepted proposal and this procedure.

For a one-stage review and implementation, the user may instead ask:

> Repeat the comprehensive documentation optimisation in
> `doc/DOCUMENTATION_REVIEW.md` and implement the justified changes. Do not
> commit or push unless I ask.

None of these forms authorises deleting non-document artefacts, changing
engineering facts without evidence, or committing/pushing. A narrower request
for analysis or recommendations only must not modify files.

The repeated optimisation has four primary goals:

1. minimise the material required to orient to a specific task;
2. reduce routine task-route and processing context, not merely total corpus
   size;
3. keep current authorities, procedures, qualification evidence, diagnostics,
   and history clearly separated; and
4. preserve unique evidence, provenance, safety gates, and reconstruction.

## 3. Review principles

1. Read `README.md` first and follow its documentation index and minimal reading routes.
2. Preserve verified measurements, conditions, units, dates, instruments, calculations, uncertainty, decisions, stop rules, and unresolved gates.
3. Keep verified measurements, derivations, published data, inferences, provisional decisions, user reports, and open items explicitly distinguished.
4. Preserve unique raw measurements, manually authored sources, and artefacts without a verified reconstruction path.
5. Remove conversational narration, repeated instructions, obsolete next actions, superseded UI troubleshooting, and project-irrelevant machine details once their decision-relevant conclusion is recorded.
6. Give each subject one authority. Consumers should state only the consequence they need and link to that authority.
7. Separate current operating instructions, qualification evidence, active diagnostics, and dated history.
8. Split or merge files only when topic ownership, reading routes, or current-versus-historical use becomes clearer.
9. Keep safety gates in the current procedure whenever omitting them from normal context could create a credible equipment or personal hazard.

## 4. Parallel review roles

Use agents only when they materially reduce review time. Give them non-overlapping scopes, such as:

1. session evidence not yet persisted;
2. distinct topic groups for duplication, stale content, scope, and reproducibility;
3. independent validation of links, index coverage, reconstruction, and contradictions; and
4. integration and final consistency.

Agents should normally report findings before overlapping files are edited. The integrating agent remains responsible for every change.

## 5. Comprehensive inventory and scope gate

This section applies only in **COMPREHENSIVE CONSOLIDATION** mode.

1. Inspect Git status and identify user-owned or unrelated changes.
2. Inventory every tracked and untracked project file.
3. Read every tracked Markdown and other documentation-bearing text file fully.
4. Establish the role, provenance, retention status, and reconstruction path of binary, CAD, measurement, and generated artefacts.
5. Record which document owns each major topic and which files merely consume it.
6. Record a baseline comprising the Markdown file count and total word count,
   the root `README.md` word count, the files and combined word count in each
   routine task route, and the largest routinely loaded authorities. Treat
   routine route cost as the primary optimisation measure and total corpus size
   as secondary because retained qualification and history should not be
   discarded merely to improve a global count.
7. Build or inspect the Markdown navigation graph from `README.md` and
   `AGENTS.md`; identify unreachable files, direct links that bypass a relevant
   dispatcher, and routes that load qualification or history unnecessarily.

## 6. Comprehensive session-evidence gate

This section applies only in **COMPREHENSIVE CONSOLIDATION** mode and must be completed before destructive consolidation.

Before moving, merging, or deleting documentation, make a recoverable temporary
snapshot of the in-scope source documents outside the tracked project tree or
in an already ignored temporary location. Record its path in the working notes.
The snapshot is a short-lived recovery aid, not a second project authority; do
not commit it, and remove any in-project temporary ledger before handover.

Create a temporary, ignored ledger with:

| Item | Evidence class | Current source | Intended authority | Preservation requirement |
| --- | --- | --- | --- | --- |

Capture at least:

- new measurements and their conditions;
- corrections to previously reported facts;
- calculations and assumptions affecting a decision;
- passed, failed, waived, and pending gates;
- superseded conclusions and why they changed;
- project-relevant hardware/software configuration;
- the exact next safe action and current stop conditions; and
- privacy-sensitive raw files whose decision-relevant results must instead be transcribed.

Do not remove a source record until every unique item has a durable destination and a comparison confirms that it remains recoverable.

## 7. Per-file review

For every file in the selected scope, determine:

1. its authoritative topic and intended reader;
2. whether each section is current procedure, current conclusion, qualification evidence, active diagnosis, dated history, or background;
3. whether another file states the same fact;
4. whether any value, status, filename, link, next action, or dependency is stale or contradictory;
5. whether the information is directly relevant to the project;
6. whether a concise table, equation, or authority link can replace repeated prose;
7. whether completed dialogue can be reduced to results, conditions, and decision rationale; and
8. whether enough information remains to reproduce or audit the work.

Prefer deleting a duplicate and linking to its authority. Do not summarise unique numerical evidence so aggressively that conditions, uncertainty, or supersession rationale are lost.

## 8. Split, merge, and archive decisions

Consider splitting a file when it mixes current procedure with extensive completed history, owns independent topics, or is routinely loaded for a small current section but dominated by archival material.

Consider merging or removing a file when it has no distinct authority, repeats another document, or adds navigation without reducing normal context.

When splitting:

1. keep current instructions and conclusions in the routinely read file;
2. move qualification evidence or chronology to clearly labelled records;
3. add reciprocal links and update the root index and reading routes;
4. search the project for the old filename and stale section references; and
5. preserve useful history in dated records and ordinary Git history, not duplicated current narrative.

## 9. Repeatability and reconstruction

For repeatable work, retain:

- inputs and raw source artefacts;
- equipment and relevant topology;
- software/tool and identifiable dependency versions;
- calibration and configuration;
- commands or complete manual procedure;
- units, tolerances, environmental conditions, and acceptance criteria; and
- the expected verification result.

If a generated output is intentionally uncommitted, retain and document all inputs, generator code, dependencies, configuration, command, and verification. Reassess `.gitignore` under `AGENTS.md`.

## 10. Validation

Use a local Markdown checker, when one is present in the repository, for links,
anchors, navigation reachability, and routine-route word costs. Run its targeted
file mode for a bounded change, or the full mode for a comprehensive
consolidation. A checker's results do not establish factual consistency or prove
external technical sources remain available. If no maintained checker is
present, perform the applicable checks below directly and record that limitation.

For both modes, validate the selected scope proportionately:

1. validate local Markdown links and anchors in changed files and direct consumers;
2. spot-check external links used as technical authorities;
3. confirm heading numbering is coherent;
4. confirm changed durable topic files are indexed and routed appropriately;
5. ensure routine routes reach current authorities without requiring qualification or history unnecessarily;
6. search for stale filenames, status phrases, release states, and next-action text;
7. inspect the actual diff while preserving unrelated changes;
8. inspect representative retained/ignored files if `.gitignore` changed;
9. check that no secrets, private host inventories, or unnecessary personal data entered the repository; and
10. run relevant reconstruction or documentation checks.

In **COMPREHENSIVE CONSOLIDATION** mode, additionally:

11. validate every local Markdown link and index entry;
12. exercise every minimal reading route;
13. compare every evidence-ledger entry with its final authority; and
14. confirm every durable Markdown file is reachable from `README.md` or
    `AGENTS.md` through the intended topic route or subtree dispatcher;
15. confirm only `README.md` and `AGENTS.md` remain as durable root Markdown and
    that documentation/data/source boundaries follow `AGENTS.md`;
16. compare the final Markdown and routine-route measurements with the baseline,
    explaining any route that did not become smaller; and
17. review the complete project diff as a coherent whole.

## 11. Comprehensive handover and Git gate

This section applies only in **COMPREHENSIVE CONSOLIDATION** mode.

The handover must state:

- current engineering state;
- exact next action and applicable safety gate;
- unresolved questions and deliberately closed investigations;
- files created, moved, merged, or removed;
- material retained only in qualification or history records;
- baseline and final routine-route costs, plus the secondary total-corpus
  comparison;
- validation performed and limitations; and
- Git commit and push status.

Commit or push only when requested. Before committing, inspect the full diff and status. After pushing, verify that the intended branch and remote commit agree.

## 12. Completion criteria

A targeted review is complete when its affected authorities, consumers, links, routes, and reconstruction checks are coherent and no unique in-scope evidence or user work has been lost.

A comprehensive consolidation is complete only when:

- every relevant session result is persisted exactly once in an appropriate authority or evidence record;
- current procedures contain no obsolete next actions;
- completed history does not dominate routine reading routes;
- routine task routes are no larger without a stated project-relevant reason;
- links, indexes, and reconstruction routes work;
- every durable Markdown file is reachable through the intended navigation
  hierarchy;
- temporary in-project ledgers and recovery copies have been removed;
- no unique evidence or user work has been lost;
- documentation remains sufficient to reproduce the work; and
- the final diff has been reviewed as a coherent whole.
