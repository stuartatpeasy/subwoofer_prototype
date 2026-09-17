# Project Working Instructions

These instructions apply to the entire project tree. A direct user instruction
for a particular task takes precedence.

## 1. Project orientation and authority

1. Begin project work by reading [README.md](README.md), then follow exactly one
   task-oriented reading route unless the task genuinely spans several topics.
2. Treat `README.md` as the high-level project source of truth and entry point.
   Treat each indexed topic file as the detailed authority for its subject.
3. Keep verified measurements, derivations, inferences, provisional decisions,
   and open items explicitly distinguished. Do not silently promote an estimate
   or exploratory result into a settled design decision.
4. Preserve user work and unrelated changes. Do not initialise Git, commit,
   delete artefacts, or untrack files unless the user asks.
5. Treat `CURRENT PROCEDURE` and current topic authorities as normal context.
   Load `QUALIFICATION` records only to audit a gate, change qualified hardware,
   or diagnose a failure. Load `HISTORY` only for provenance or a superseded
   decision. Do not routinely ingest history merely because it is linked.

## 2. Technical communication

Regarding technical topics: teach the user technical mathematics in small,
sequential chunks. Anchor abstractions in circuit or physical intuition, derive
important results rather than merely stating them, and follow each new idea with
a worked example.

Assume a rusty EE-undergraduate mathematical foundation: the user's conceptual
and engineering reasoning is sound, but calculus recall and algebraic fluency
need rebuilding. Do not over-simplify the engineering ideas, but avoid
unexplained mathematical jumps. If a concept does not settle immediately, park
it and revisit it from another direction later.

## 3. Proportionate project process and safety

1. Keep every proposed test procedure, measurement, safety verification, and
   other commissioning step proportionate to, and justified by, the nature and
   intended use of this project.
2. The objective is not laboratory-grade assurance or a product proven against
   every potentially applicable safety standard. It is a system that works
   well, can be reproduced at very limited scale, and has basic electrical and
   mechanical safety.
3. Before proposing any activity or process step, consider its likely practical
   value, the uncertainty or credible risk it addresses, and its cost in time,
   effort, complexity, and enjoyment. Do not add work merely because a more
   exhaustive or more precise process is possible.
4. Preserve checks that address credible electrical, mechanical, equipment, or
   personal-safety hazards, but distinguish those checks explicitly from
   optional characterisation, optimisation, or marginal confidence-building.
5. Treat this as a pleasant and absorbing hobby intended to produce work to a
   good standard. Do not turn it into tedious unpaid work by pursuing immaterial
   improvements or the last hundredth of a percent without a project-relevant
   justification.
6. Default to the smallest number of conversational gates that safely completes
   a task. Combine routine, reversible, low-risk checks, connections, settings
   changes, and test execution into one turn and one procedure when their safe
   order is already known.
7. When the user can directly judge a check, use a local conditional gate instead
   of requiring a separate report and reply: if the check passes, continue; if it
   fails, stop, leave the system safe, and report the failure. Ask for one
   consolidated report after the bounded sequence.
8. Require a separate turn boundary only when the next action depends on expert
   interpretation of a result not yet available, materially changes the risk,
   would energise uncertain wiring or equipment, is destructive or difficult to
   reverse, or needs fresh user authorisation. State the specific reason for the
   boundary.
9. For live measurements, ask once for the actual current physical power and
   wiring state when it has not already been supplied. Once that state is
   established, normally provide the complete bounded sequence from the
   no-signal audit through connections and settings to one controlled test, with
   explicit stop conditions. Do not request repeated confirmation of unchanged
   state during the same task unless a reported action or anomaly could have
   changed it.
10. Size procedures around meaningful engineering decisions rather than
    individual clicks or checks. Do not split a known safe sequence across turns
    merely to create conversational checkpoints.
11. Eliminate or reduce to the bare minimum any safety checks for systems and
    subsystems in which the maximum voltage that can plausibly be encountered is
    below 50V, unless:
    - there is a significant risk of destroying a valuable component, or
    - there is a plausible fault scenario which could result in the user being
      exposed to voltages greater than 50V.

## 4. Agent delegation

1. Use agents when independent or parallel work would materially reduce the
   wall-clock time needed to complete a task.
2. Select each agent's model and effort level deliberately to match the
   complexity, uncertainty, and consequence of its assigned work.
3. Do not delegate when coordination and review overhead would outweigh the
   likely time saving. The primary agent remains responsible for integrating
   and checking delegated results.

## 5. Keep Markdown current through a consolidated end-of-turn pass

1. During substantive investigation, calculation, measurement, implementation,
   and verification, track whether the work changes any documented fact,
   measurement baseline, calculation, decision, procedure, filename, dependency,
   reconstruction route, status, priority, or open item. Accumulate these
   consequences without editing Markdown after each intermediate result.
2. First complete the substantive work and allow the conclusions to stabilise.
   Then, near the end of the turn, perform one consolidated documentation-editing
   phase that updates every affected Markdown file before the final response.
3. Intermediate hypotheses, exploratory results, failed approaches, and
   conclusions superseded within the same turn do not require separate
   documentation updates unless they are themselves durable evidence or
   necessary provenance.
4. A consolidated documentation phase may update several files and may include
   a small corrective edit if the subsequent documentation checks reveal an
   error. It means one documentation stage, not an absolute limit of one
   filesystem operation.
5. Depart from this batching rule only when the user explicitly requests
   incremental documentation, a later step in the same turn must consume the
   updated document, an immediately corrected procedure is needed before a
   safety-relevant action, or delaying the record would risk losing unique
   evidence. Briefly state why when departing from the rule.
6. Do not knowingly finish the turn with affected documentation stale or defer
   an obvious update to a future turn.
7. Do not rewrite unrelated documents merely to create activity. “Keep current”
   means correcting documents affected by the work, not introducing churn.
8. When adding, renaming, moving, or deleting a durable Markdown file, update
   the nearest subtree dispatcher and any affected task-oriented reading route
   in [README.md](README.md). Add detailed qualification or history files to the
   root map only through their dispatcher. Search the whole project for stale
   filename and link references.
9. Keep the root and topic-document section/subsection hierarchy numbered.
10. Preserve dated history and superseded conclusions where they explain the
   engineering process. Label the new conclusion and why it supersedes the old
   one rather than rewriting history. When a measurement baseline is explicitly
   replaced, update every current conclusion and source reference that depends
   on it.
11. Keep specialised procedures under the corresponding documentation subtree
   (e.g. `doc/rew/` for REW work), while retaining measurement and project artefacts
   in their existing data directories (e.g. `rew/`, `vituixcad/`). Link procedures
   from the relevant indexed Markdown file.
13. Give each durable fact one current authority. Other current documents should
   state only the consequence they consume and link to that authority. A history
   record may repeat a fact as part of dated chronology but must identify itself
   as non-current context.
14. Begin each routinely loaded topic authority or procedure with a compact
    state card where applicable: lifecycle, owns, does not own, read-when rule,
    current approved action or conclusion, next gate, limitations, and
    last-reviewed date. Keep detailed results in their owning evidence record.
15. Whenever a generated output becomes intentionally uncommitted, document the
    complete reconstruction route: retained inputs, generator/tool, pinned or
    otherwise identified dependencies, configuration, command, and the expected
    verification result.
16. Keep `README.md` as a compact dashboard and router. It may state the current
    phase, the decision-relevant consequence for each subsystem, task routes,
    and immediate priorities, but it must not accumulate test transcripts,
    detailed derivations, qualification evidence, or chronological narrative.
    Put those details in their owning topic, qualification, or history record.
17. Keep durable project Markdown under `doc/`, except for the root `README.md`
    and `AGENTS.md`. Keep measurements, CAD, source code, and generated artefacts
    in their existing data/source trees rather than moving them under `doc/`.
    Add a subtree dispatcher only when it materially shortens or clarifies the
    task routes through that subtree.
18. Do not use a current procedure as an append-only work log. When a procedure
    step is completed, move durable results into the owning current authority or
    qualification record, retain decision-relevant superseded chronology in a
    dated history record, and revise the procedure to show only its current
    prerequisites, safe next action, stop rules, and unresolved gates.

## 6. Keep `.gitignore` current without losing information

1. Reassess `.gitignore` whenever work introduces a new tool,
   dependency manager, cache, temporary workspace, build directory, generated
   file class, export pipeline, or machine-specific output.
2. Apply this priority order:
   1. preserve unique information;
   2. preserve practical reproducibility;
   3. minimise committed payload.
3. Ignore a file only when it is disposable local state or its useful content
   can be reconstructed from committed sources. If the reconstruction inputs or
   settings are incomplete, retain the file or stop and ask the user before
   ignoring it.
4. Prefer narrow, explicit project paths over broad extension rules. Broad
   rules can silently hide a future source file that happens to share an output
   extension.
5. Never globally ignore measurement/project formats such as `.zma`, `.mdat`,
   `.frd`, `.vxp`, `.xlsx`, `.pdf`, `.stl`, `.dae`, `.stp`, `.obj`, `.lib`,
   `.png`, or `.jpg`. Some current scripted DAE/preview outputs are ignored only
   by explicit directory rules because matching generators are committed.
6. Keep raw measurements, manually authored CAD, imported reference geometry,
   fabrication sources, source images, and any artefact without a verified
   reconstruction path.
7. When ignoring a dependency tree or environment, commit the smallest adequate
   manifest or lock file needed to recreate it. Update that manifest when the
   relevant dependency versions change.
8. Keep 3D-printer G-code ignored, retain the source STL or slicer project, and
   update `3d_models/PRINT_SETTINGS.json` whenever a materially different print
   job becomes part of the project. Prefer committing future `.3mf` slicer
   projects because they preserve placement and complete slicing state.
9. Do not delete a file merely because it is ignored. Remember that adding an
   ignore rule does not untrack a file already committed.
10. Keep explanatory comments in `.gitignore` accurate, especially its explicit
    retained/ignored boundary. Remove or revise an ignore rule if its generator
    or reconstruction source ceases to exist.

## 7. Completion checks

For a user-requested comprehensive documentation review or handover, follow
[`doc/DOCUMENTATION_REVIEW.md`](doc/DOCUMENTATION_REVIEW.md) in addition to this file.

Before completing any task that changes project files:

1. search affected Markdown and the project index for stale facts, names, and
   links;
2. verify local Markdown link targets;
3. confirm new or changed current documents are indexed appropriately and that
   qualification/history records are reachable through a subtree dispatcher;
4. confirm every newly ignored output has a committed and documented
   reconstruction path;
5. inspect the actual ignore result for representative retained and excluded
   files when `.gitignore` changes;
6. inspect Git status if this directory has become a valid repository, while
   preserving unrelated user changes; and
7. report material documentation and ignore-policy updates in the handoff.
