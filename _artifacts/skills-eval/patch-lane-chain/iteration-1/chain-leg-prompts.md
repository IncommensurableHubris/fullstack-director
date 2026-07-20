# Composed patch-lane chain — runbook + leg prompts (iteration-1)

> Reconstructed 2026-07-07 after the prior session's scratchpad (holding the original `chain-leg-prompts.md`) was
> lost to the `claude-opus-4-8` classifier outage. Grounded in the seeded workspace + the chain README grading map.
> **Do not push.** All paths Windows-absolute.

## Progress — ✅ CHAIN COMPLETE (2026-07-08)

All five legs ran live as fresh isolated subagents; every seat's deliverable independently verified; spine
byte-identical through the whole chain. Full results + grader-artifact catalogue: `README.md` (this dir).
Commits: `fc50c4f`→`dffce18`(1)→`b910c65`+`03569c2`(2)→`10b32d4`(.gitattributes)→`1e01d8b`(3)→`328332e`(4)→`a8e87e0`(5).
Graders: leg1 8/8 real · leg2 22/22 · leg3 10/10 · leg4 12/12 real · leg5 PASS.

- **Pre-flight gate:** ✅ GREEN — `validate_script.py` 12/12 · `validate_grader --case all` sound · seed HEAD `fc50c4f` · `node --test` 3/3 on seed.
- **Leg 1 (01-planner):** ✅ DONE + committed **`dffce18`**. `check_patch --case patch-small` 7/8; the lone FAIL ("Ceremony declined → docs/architecture/") is a **grader-fixture false positive** — the mid-life seed legitimately ships `docs/architecture/`; git confirms leg 1 touched only `docs/planning/**` (arch/design byte-identical to seed). Effective 8/8.
- **Leg 2 (04-builder):** ✅ DONE + self-committed `b910c65`(build)+`03569c2`(handoff). Graded **`check_build --case patch-build` 22/22**. 1-line scope fix `&& e.day === standup.day`; genuine cross-day RED→GREEN regression test; patch-mode handoff (File List + VC carry-forward); ledger→`in-progress`; spine untouched; budget 2 files/22 LOC ≤ 2/40.
  - **⚠ Windows EOL gotcha (fixed):** `check_build.py`'s mutation pass restores source files via text-mode writes → leaves **CRLF** on Windows, which poisoned PB4's *worktree-diff* budget check (all source files showed as changed). Fixed by committing **`.gitattributes` (`* text=auto eol=lf`)** so git normalizes EOL in diffs; the true budget (commit-diff `dffce18..b910c65`) was always 2 files/22 LOC. Same class as memory `mutation-grader-robustness`. `.gitattributes` also protects legs 3–5.
- **Legs 3–5 (05 / 06 / status):** ⏳ 05 dispatching now.
- **RESUME HERE →** Leg 3 (05-reviewer). If a later grader shows spurious full-file source diffs, `git checkout -- .` (LF) before grading.

- **REPO** = `D:\_CODE\2026-06-29_fullstack-director`
- **WS** (project root, a git repo) = `REPO\_artifacts\skills-eval\patch-lane-chain\iteration-1\outputs`
- **Seed commit** = `fc50c4f7cb` (must be HEAD of WS at start; `node --test` green over the planted cross-day bug)
- **Planted bug** — `src/digest.js` `recordStandup` filters by `member` only, so a new day's standup deletes the
  member's earlier days (violates REQ-001 "one per member per **day**"; breaks REQ-010 past-digest reads). Same-day
  tests + smoke stay green. Fix = scope the filter: `!(e.member === standup.member && e.day === standup.day)`.
- **Isolation doctrine** — each leg is a FRESH subagent (Agent tool, `general-purpose`). It receives ONLY the WS
  path + "load this SKILL.md by path, run this verb." No leg inherits a prior leg's reasoning; the handoff is
  strictly the shared artifacts on disk. Relax `<SUBAGENT-STOP>` for leg 3 (05) — the harness spawns it.
- **Commit division** — seats **04 and 06 commit their own work** (04 emits a fresh `final_commit`; 06 commits +
  tags). The **harness** commits the artifacts of legs **1, 3, 5** after grading them, so 06's tree-clean gate holds.

## Pre-flight (harness, before leg 1) — deterministic regression gate
Run from `REPO`; all must be green (they were at prior-session exit — this is the regression re-check):
```
python docs/eval-methodology/integration/validate_script.py          # 12/12 (ideal + 10 degenerates + check_budget self-test)
python docs/eval-methodology/integration/validate_grader.py --case all
git -C _artifacts/skills-eval/patch-lane-chain/iteration-1/outputs log --oneline -1   # == fc50c4f7cb…
git -C _artifacts/skills-eval/patch-lane-chain/iteration-1/outputs status --porcelain # clean
node --test  (cwd = WS)                                              # green on the seed (bug latent, uncaught)
```
If any red → STOP, diagnose, do not start the live chain.

---

## Leg 1 — `/01-planner patch` (harness grades + commits)
**Dispatch (fresh subagent):**
> You are running the **01-planner** skill in PATCH mode on a real project. First READ IN FULL and then follow
> exactly: `D:\_CODE\2026-06-29_fullstack-director\.agents\skills\01-planner\SKILL.md` (its patch-mode section).
> Project root: `…\patch-lane-chain\iteration-1\outputs` — a mid-life TeamPulse (spine in `docs/spec/`, backlog +
> shipped `sprint-01` in `docs/planning/`, code in `src/`, tests in `test/`).
> Run: `/01-planner patch "Standups submitted on a new day silently delete the member's previous days' entries —
> recordStandup in src/digest.js filters by member only, dropping earlier days. Keep one standup per member per day
> across days (REQ-001); past days must stay readable (REQ-010). Fix the retention scope."`
> No interactive user — proceed autonomously through the light gate. **Do NOT implement the fix** — certify
> patch-class (P1–P5, each evidenced), write the patch record, add the ledger row, and dispatch. Do not touch
> `docs/spec/**`; create no sprint/design/architecture artifacts. **Do not git-commit** (the harness commits).
> Return: the record path, owning REQ-IDs, and the dispatch target.

**Grade + commit (harness):**
```
python .agents/skills/01-planner/evals/check_patch.py --outputs <WS> --case patch-small   # NO --fixture
git -C <WS> diff --name-only fc50c4f7cb -- ':!docs/planning'   # MUST be empty (spine + code untouched; only docs/planning/** changed)
git -C <WS> add -A && git -C <WS> commit -m "leg1(01-planner): certify patch-001 (cross-day retention, REQ-001)"
```
Expect: `patch-001.md` (no `status:` field, owning reqs incl. REQ-001, size_budget), one `## Patches` row `planned`,
dispatch `/04-builder`, all 5 checks evidenced, spine byte-identical.

## Leg 2 — `/04-builder` (self-commits)
**Dispatch (fresh subagent):**
> You are running the **04-builder** skill. READ IN FULL then follow: `…\.agents\skills\04-builder\SKILL.md`.
> Project root: `…\iteration-1\outputs`. A patch is certified: read `docs/planning/patches/patch-001.md` and its
> dispatch. Run the **patch funnel**: fix the bug TDD-for-bugs style (write the failing cross-day regression test
> FIRST, observe RED, then the minimal fix in `src/digest.js`), stay inside the record's certified file/LOC budget,
> advance the `## Patches` ledger row to `in-progress`, and emit `docs/planning/patches/build-handoff-patch-001.md`
> with frontmatter `review_mode: patch`, `patch: patch-001`, and the spec-slice binding to the patch record. If the
> budget is exceeded, HALT (name P4) and mark the row `escalated` — do not silently widen. Commit your work per the
> skill (fresh `final_commit`). No interactive user — proceed autonomously. Return: the handoff path + final_commit SHA.

**Grade (harness):**
```
python .agents/skills/04-builder/evals/check_build.py --outputs <WS> --case patch-build
node --test   (cwd = WS)        # the new cross-day regression test is GREEN; same-day tests still green
```

## Leg 3 — `/05-reviewer` (harness grades + commits)
**Dispatch (fresh subagent — relax `<SUBAGENT-STOP>`):**
> You are running the **05-reviewer** skill as a FRESH reviewer who did NOT build this. READ IN FULL then follow:
> `…\.agents\skills\05-reviewer\SKILL.md`. Project root: `…\iteration-1\outputs`. SEED (patch variant): the handoff
> `docs/planning/patches/build-handoff-patch-001.md` + the patch record + the owning REQ block(s) in the spine.
> Review the patch slice under the standard honesty gates (isolation preserved; SHIP unreachable while any behavior
> is INFERRED). Emit `docs/planning/patches/qa-report-patch-001.md` (patch-keyed) with your verdict. No interactive
> user — proceed autonomously; **do not git-commit** (harness commits). Return: verdict + qa-report path.

**Grade + commit (harness):**
```
python .agents/skills/05-reviewer/evals/check_review.py --outputs <WS> --case patch-review
git -C <WS> add -A && git -C <WS> commit -m "leg3(05-reviewer): SHIP patch-001 qa-report"
```
Expect: attestation present + valid, seed manifest lists the patch record, verdict SHIP, Inferred = 0.

## Leg 4 — `/06-release` (self-commits + tags)
**Dispatch (fresh subagent — pre-grant the single deploy gate):**
> You are running the **06-release** skill. READ IN FULL then follow: `…\.agents\skills\06-release\SKILL.md`.
> Project root: `…\iteration-1\outputs`. A SHIP `docs/planning/patches/qa-report-patch-001.md` is in place. Gate the
> patch release: evaluate **all** G1–G7 (nothing waived), verify code identity against the patch review's
> `final_commit`, run the stand-in platform (`scripts/deploy.js`, `health.js`, `smoke.js`), and — **the single human
> deploy approval is PRE-GRANTED for this run** — proceed to release. Emit `release-report-patch-001.md`
> (`release_mode: patch`, `patch: patch-001`, RELEASED), create the `release/patch-001` tag, and flip the `## Patches`
> ledger row `in-progress → done`. Never print secrets from `.env`. Commit + tag per the skill. No interactive user.
> Return: release verdict, report path, tag name.

**Grade (harness):**
```
python .agents/skills/06-release/evals/check_release.py --outputs <WS> --case patch-release
git -C <WS> tag --list 'release/patch-001'      # exists
```

## Leg 5 — `/status` (harness grades + commits)
**Dispatch (fresh subagent):**
> You are running the **status** skill. READ IN FULL then follow: `…\.agents\skills\status\SKILL.md`. Project root:
> `…\iteration-1\outputs`. Derive current state and emit the standard views (`CLAUDE.md` § Current State + the
> `AGENTS.md` emission). The patch lane has completed (patch-001 done). Stay strictly read-only w.r.t. truth
> (`docs/spec/**` and realizations byte-identical). No interactive user — do not git-commit (harness commits).
> Return: integrity verdict + the single next command.

**Grade + commit (harness) — leg-5 invariants via git + CLAUDE.md:**
```
# truth untouched since the seed except the sanctioned patch-lane artifacts:
git -C <WS> diff --name-only fc50c4f7cb -- docs/spec        # EMPTY (spine byte-identical across the whole chain)
# status wrote only its derived views this leg:
git -C <WS> status --porcelain                              # only CLAUDE.md / AGENTS.md untracked/modified
# emitted CLAUDE.md: integrity PASS · exactly one `Next command:` slug · patch done ⇒ normal routing (NOT a patch-in-flight hijack)
git -C <WS> add -A && git -C <WS> commit -m "leg5(status): derive end-state (integrity PASS, patch done)"
```

---

## Post-chain (harness)
1. Append the five legs' results (assertion tallies + one-line notes) to
   `_artifacts/skills-eval/patch-lane-chain/iteration-1/README.md` under `## Leg results`.
2. Tick the plan's **Phase 1 exit** line in `_artifacts/revision-implementation-plan.md` (add a dated PASS note).
3. Commit the phase-exit docs (`_artifacts/` is gitignored — force-add, as the design records were):
   ```
   git add -f _artifacts/phase-2-continuation.md _artifacts/skills-eval/patch-lane-chain/iteration-1/README.md _artifacts/skills-eval/patch-lane-chain/iteration-1/chain-leg-prompts.md
   git add _artifacts/revision-implementation-plan.md   # tracked already
   git commit -m "test(phase-1-exit): composed patch-lane chain green (01→04→05→06→status)"
   ```
4. **Do not push.** Phase 2 resumes from `_artifacts/phase-2-continuation.md` in a fresh session.
