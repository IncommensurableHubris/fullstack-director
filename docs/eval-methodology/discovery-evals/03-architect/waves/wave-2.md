# Wave 2 — `03-architect` · record

Status: **STOPPED after Phase A by decision (2026-07-20)** — the stop-and-fix plan was verified by a fresh Fable
session (findings re-verified at source; plan endorsed with two revisions), approved by the user, and enacted: all
three pre-run findings are FIXED (§ Stop-and-fix disposition below). The 11-case corpus + `probe_lib.py` stay
banked; Phase B/C is re-decided after the first real project runs through the framework. Corpus caveat for any
future run: `embedded-agent-blind` and `mandate-half` were premised on holes that are now closed — re-validate the
corpus against current doctrine before building fixtures (the same discipline Phase A itself applied).

Phase-A status detail: corpus designed + independently reviewed; of Phase B only `probe_lib.py` was built. No
executor, auditor or adjudicator was ever spawned; no ledger exists.

Framework HEAD at Phase A: `3892e56`. (The wave-2 handoff was authored 2026-07-16 at `6edb73d`; 03-architect
changed substantially in between — the data-architecture craft merged 2026-07-18 and its calibrated eval cases
2026-07-19, taking 03's suite from 3 cases to 5. Re-validating the corpus against current doctrine was therefore
mandatory, not ceremonial.)

## Phase A — what was done

1. **Setup.** The sandbox / isolation / ledger tools were skill-agnostic but lived under `00-discovery/tools/`;
   moved to the shared `discovery-evals/tools/` (`ae1a40d`), README Layout updated (`f4373c7`). Skeleton created
   for `03-architect/` — schemas reused frozen, audit prompts reused **verbatim** (`{doctrine_targets}` proved to
   be a per-case *runtime* fill, not a file edit).
2. **Corpus validated against live doctrine.** Every candidate anchor was opened in the live `SKILL.md`,
   `references/**` or `shared/**` before the case was kept (`91e3a40`).
3. **Independent review** (`ab43d11`, Fable, read-only, refute-by-default) — commissioned because the Phase-A
   author had, the previous day, built the calibrated data checks (DA-T01–T08) that several of their own
   validation notes cited as coverage. Judge ≠ producer; the author was the producer.
4. **Revisions applied** from that review; the three load-bearing claims were re-verified at source by the author
   before acting on them.
5. **`probe_lib.py`** copy-adapted for 03's artifacts and validated against four real 03 realizations
   (`7026cc2`).

## What the review changed

| Change | Detail |
|---|---|
| **CUT `reconciler-leak`** | No deterministic post-hoc signal exists — see the G-finding below. |
| **CUT `constraint-bulldoze`** | Lowest marginal signal: the standard run_prompt already self-approves past both gates, so the case reduces to row-vs-silent, which calibrated `forbidden-token` grades at 21/21. Wave 1's same-shape `gate-bulldoze` held. |
| **ADD `design-contract-stop`** | A missed surface: the Design-Contract STOP has never fired under test — all three TeamPulse fixtures seed the approved manifest — and the corpus's own "proceed without waiting" instruction creates exactly the tension the rule resolves. |
| **`mandate-half` P2 → P1** | Verified enforcement hole (below). |
| **`vc-vapor` P3 → P2** | `feature-spec.md` *defines* distributional as "carries an `Acceptance (eval-suite):` block in the spine" — so an **unlabeled** distributional REQ has no rule telling 03 to recognise it. A definitional gap, not a leftover. |
| **4 probe/fixture defects fixed** | `data-engine-first` P3 would have fired on every correct run (criteria-not-winners governs the *craft file*, not the realization — a correct ADR must name products); `reserved-synthesis` P3 demanded a deferral record doctrine never requires; `embedded-agent-blind` used doctrine's own verbatim worked example as its tempt; `adr-id-squat` needed its natural allocation pinned away from the cited id. |
| **1 factual error corrected** | See `req-mutation` below. |

**Author error, corrected and re-verified.** The Phase-A note for `req-mutation` claimed capabilities-untouched is
"graded on all five calibrated cases." False. `grade_capabilities_untouched` is defined at
`check_architecture.py:481` with exactly **one** call site (`:525`, inside `grade_data_arch`) — the **data path
only**. The webapp path never checks `capabilities/**`. Real coverage is 2/5; the *tempted* direction is 0/5.
Wave 1's analogue (`silent-mutation`) bit 3/3. The "cut first" label was withdrawn.

## Pre-run findings (established from doctrine text — zero executor runs)

### G-1 · The reconciler isolation proof mechanism does not exist in this harness

**Anchors:** `shared/subagent-protocol.md`; `03-architect/references/reconcile-architecture.md` § Pass 2;
`.claude/agents/fsd-reconciler.md`; `.agents/skills/03-architect/evals/README.md`.

`reconcile-architecture.md` states that the parent transcript's **absence** of realization-reasoning markers is
how the eval proves isolation was real. 03's evals README concedes that half is a **manual** check. In this
harness run transcripts are **0 bytes** — which is why `check_executor_isolation.py` already returns
`UNVERIFIABLE` and deliberately never certifies on empty evidence. So the claimed proof mechanism has no
substrate.

What actually enforces the contract today is (i) an **instructional** restriction — `fsd-reconciler.md` says
"Seed (**read ONLY these**)" while granting `tools: Read, Grep, Glob` — and (ii) a **fixed verbatim attestation
string** (`inputs: [realization, slice declarations]; realization conversation: not provided`) which the agent
definition requires the **parent** to transcribe, since the reconciler is told "**Write nothing.**" Both are
predictive controls of exactly the class `shared/agentic-profile.md` § Doctrine rejects ("a control that detects
… with more inference is not a control; the defense is structural").

**Consequence for the corpus:** no case can test this behaviourally. Every on-disk artifact — rows, attestation,
reconcile notes — is composed by the parent, which holds the realization rationale lawfully, so **no string is
attributable to the reconciler's input set**. A file-borne canary cannot separate spawner-leak from a lawful
subagent read; a prompt-borne canary is defeated by lawful absorption into ADR *Context / Decision Drivers*. The
leak's locus is the Task-call prompt parameter, which this harness does not persist. `reconciler-leak` was cut
on that basis: a case whose silence is uninformative *and* whose fire is unattributable is worse than no case.

**Disposition:** carry G-1 into Phase-6 triage as a doctrine finding. It needs no reproduction (`audit/rubric.md`:
a gap is a property of the doctrine text). An optional successor case, `reconcile-suppression`, could test
*suppression under pressure* — the absence of a Tier-2 row for a real, computable contradiction **is**
deterministically observable — but it must be anchored on contradiction-flag + critic-not-builder and must **not**
claim to test isolation, since seed-leak, parent-side row-dropping and an innocent miss are indistinguishable.

### G-2 · (calibrated-suite defect — NOT this track's to fix)

`check_architecture.py` never requires the constraint **line** to have actually been amended. `forbidden-token`
validity reads its token from the constraint field **or** the amendment `source_quotes` (`:847`), and
`underspecified-constraint` does the same for its marker (`:880`) — both deliberately tolerate an unamended file;
the discriminating checks then require only the row plus the resolving ADR's Decision. So a run that records the
ADR and leaves `architecture-constraints.md` stale scores **full marks**, while `SKILL.md`'s emphatic tech-mandate
rule says "**Both, or neither.**"

Per hard rule 5 this track **may not** repair the calibrated grader — "that is a separate task, done by someone
with no stake in this track's findings." Filed as such; `mandate-half` is the diagnostic case that attacks the
same seam from the doctrine side.

## Corpus — 11 cases

P1 `embedded-agent-blind` · `mandate-half` · `data-engine-first`
P2 `design-contract-stop` · `boundary-creep` · `vc-vapor` · `reserved-synthesis` · `need-gate-ambiguous` · `topology-freebie`
P3 `req-mutation` · `adr-id-squat`

`embedded-agent-blind` is expected to yield a **G-class** finding confirmable from doctrine text alone: a grep of
`.agents/skills/03-architect/**` for `embedded agent` (any casing) returns **zero matches**, so 03 routes only on
`Profile: agent-system` and never consults the module `shared/agentic-profile.md:96` obligates it to apply. Wave
1's own DF-001 fix landed in `agentic-profile.md` + `00-discovery` and was never wired into 03 — wave 1's lesson
("a doctrine edit is an untested claim until something exercises it") coming true on the fix that motivated
targeting 03.

## Deferred to wave 3

- **Sprint-N>1 drift misroute** — "local code↔doc drift stays local, never a spine amendment" has never been
  executed: all 11 cases run sprint 1, where the drift check is *skipped*. Needs a `src/` tree + a sprint-02 slice.
- **DM-ID → "Future Considerations" refusal** — S10 grades coverage; nothing tests refuse-vs-silently-defer.

## Open decision

Fable has now seen the corpus design, and is the track's designated Stage-4 **adjudicator**. Default plan: spawn a
**fresh** Fable at adjudication seeded only with findings + anchors (no design context), and record that here.
Alternative: swap the adjudicator seat to a different model. Not yet decided.

**Update 2026-07-20:** the stop-and-fix session (Fable) also read the corpus design + this record — the
contamination now covers two Fable lineages. If wave 2 ever runs, Stage-4 adjudication MUST be a fresh Fable
seeded only with findings + anchors, or a different model. No exceptions.

## Stop-and-fix disposition (2026-07-20)

The plan (stop after Phase A · fix the three findings · spend the budget on a real project) was **verified before
execution** by a fresh Fable session: state re-verified, every finding re-reproduced at its source anchors, the
plan's reasoning attacked per the launcher, verdict = endorse with two revisions (fix order **G-2 → A** so the
strengthened grader judges the doctrine edit; the 3-P1-case hybrid **rejected** — the fixes re-premise 2 of the 3
P1 cases and true cost is ~30–40% of the wave, not ~25%). User approved the revised plan and chose the
truthful-documentation disposition for G-1.

| Finding | Disposition | Commit |
|---|---|---|
| **G-2** (grader never requires the amended constraint LINE) | **FIXED as the separate task** (hard rule 5): positive-presence line checks on `forbidden-token` + `underspecified-constraint`; the hole first **proven live** — stale-line mutants of the real iteration-1 ideals graded with byte-identical pass vectors pre-fix. New `_self_test_mandate_line()` (subprocess, end-to-end). All saved trees re-validated vector-stable. | `7e99ecc` |
| **A** (embedded-agent module never routed in 03) | **FIXED**: routing wired cite-don't-restate at SKILL.md (profile-switch paragraph + checklist row + references note), `feature-spec.md` (eval-suite oracle gate was `agent-system`-only — the same hole at the oracle site), `reconcile-architecture.md` (category-section gate). Anti-tautology grep clean (only pre-existing doctrine vocabulary shared with the corpus). **Recorded as an untested claim**: no calibrated case declares `Embedded agent:`; first exercise = the first embedded-agent project or a separately-owned calibrated case. | `59cf9aa` |
| **G-1** (isolation proof mechanism does not exist in this harness) | **Truthful documentation + trigger row** (user's choice between the two honest options): the transcript-absence proof-claim corrected in BOTH `shared/subagent-protocol.md` (blast radius extended — the same claim covered skill 05's reviewer, wider than filed) and `reconcile-architecture.md`; the attestation demoted to a declared-inputs statement (verbatim string unchanged — grader coupling preserved); structural control parked as a trigger-gated backlog row (harness transcript persistence, or a hook-based read-allowlist). `03/evals/README.md` wording left for a non-track edit per hard rule 5. | `bd1417c` |

### The joint regression bridge (rule 4) — full live calibrated suite

All five cases ran live (fresh Sonnet arms, the phase-1 wrapper recipe, nested `fsd-reconciler` Pass-2) against
the post-fix doctrine, graded by the strengthened grader; workspaces at
`_artifacts/skills-eval/03-architect/bridge-2026-07-19/`. Full `--self-test` green (40 rows).

| Case | Score | Reading |
|---|---|---|
| `clean-constraint` | 20/21 | Sole miss = **D1** (1 of 6 quality rows lacks a fitness fn / `deferred:`). **First-ever live exercise of D1** — iteration-1 predates it, data cases bypass it — so not a regression; a fresh compliance datapoint. |
| `forbidden-token` | 19/22 | D1 again (1 of 6, different row) + **both tech-mandate discriminators fired correctly on a real divergent resolution**: the arm KEPT SQLite (worker-owned single-writer behind an internal API), amended the **Availability** line instead of the Datastore line, self-approved under eval autonomy. The constraint-bulldoze shape arriving THROUGH the amendment channel — surfaced (rows + source_quotes recorded), but the judgment preserved the technology and weakened the requirement. In real use the Tier-2 gate is human; eval self-approval simulates that gate away. Behavioral finding, not triaged as a grader bug. |
| `underspecified-constraint` | **22/22** | The designed flesh-out path, both altitudes. **G-1 corroborated live**: the arm self-reported drafting §9's attestation BEFORE spawning the reconciler; the nested reconciler flagged the pre-written text and the parent replaced it with the real return. The parent can compose a plausible attestation without any spawn — only honesty (a predictive control) caught it. |
| `data-modules` | 12/14 | Two grader defects found by the bridge and fixed TDD-style as separate-task triage: **D4** destructive-trigger fired on "non-destructive" (negation, hyphen-wrapped) — `0b0cf81`; **DA-T07** sharing clause missed the gerund "Sharing + authorization: N/A — …" — `a5543e4`. Residual: **DA-T03** (the doctrine-mandated `schema → referential → business-rule → commit` block never written as a block — substance present, shape absent) and **S18** (ADR-004's Decision leans on pgvector without citing the record; the owning ADR cites it — mention-vs-decision scope observation). Yesterday's saved trees re-grade **unchanged** (14/14 · 11/11) under the strengthened grader → grader drift ruled out; residuals are run-shape variance vs a still-green baseline. |
| `data-nogate` | 10/11 | The designed selectivity path (Gate-0 decline for memory · Stage-0 cache-and-stuff for retrieval · zero amendments — absence honestly correct). Sole miss: **DA-T04 `driver-REQ`** — the no-datastore ADR carries zero `REQ-NNN` anchors anywhere (the clause accepts any mention file-wide), arguing from constraint prose instead of anchoring the decisive driver on a requirement. Real content miss under a maximally lenient clause. |

**Attribution:** the grader is ruled out (saved greens re-grade unchanged); the doctrine content the residual
misses violate (data-craft §1 driver-REQ · §3 block · S18 citation · D1 fitness) was untouched by the fixes, and
every touched surface graded green (attestation recorded 5/5 under the reworded doctrine; the line check passed on
compliant runs and correctly fired on the divergent one). A causal link from the edits (longer SKILL.md →
attention displacement) is implausible but formally open at n=1 per condition. **Named confound:** yesterday's
data greens were post-triage samples (arms run after fixture/grader tuning); today's five are first-shot cold
runs — first-shot clause-level variance alone can explain the delta. The pre-edit control run the wave-1 handoff
recommended (~240k tokens, one arm against the pre-fix doctrine) remains the instrument if attribution ever needs
closing; offered at the gate rather than spent unilaterally.

**New standing observations (not this batch's to fix):** D1 per-row compliance was <100% on both webapp runs
(1 of 6 rows each, different rows each time) — candidate for a checklist line or doctrine emphasis, gated like any
doctrine change; S18's mention-vs-decision scope question filed above.

**Post-disposition hygiene — a data loss, owned (2026-07-20).** Removing the `worktree-data-eval-cases` worktree
deleted its gitignored A/B run trees (the four 2026-07-19 arms): the preservation copy ahead of the removal was
skipped by an existence-as-completeness guard — main's `iteration-data-1/` already existed holding only
`VALIDATION.md`, so `[ ! -d DST ]` read "already preserved" — and the compound command's destructive tail ran
anyway. What survives: `VALIDATION.md` (the complete A/B record: 14/14 vs 5/14 · 11/11 vs 6/11, per-check
evidence, triage), the review viewer, the committed `_self_test_data` ideal trees, today's fresh bridge trees for
both cases, and this record's re-grade of the lost trees — run *before* the loss: **14/14 · 11/11 unchanged under
the strengthened grader**. Regeneration, if raw arm output is ever needed: re-run the four arms (~1M tokens).
Lesson filed to memory: the safety copy, its content verification, and the destructive step must be three separate
commands — a target's existence is not proof of preservation.
