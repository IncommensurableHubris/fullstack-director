# Composed patch-lane chain — iteration-1 (Phase 1 exit, WS1 A/B policy)

The ONE composed with_skill live run covering Tasks 1.4–1.7 (per the approved simplification A/B policy;
baseline arms dropped for template-presence assertions). Five sequential FRESH subagent legs over one workspace
(`outputs/` — a git repo), each leg loading its seat's SKILL.md by explicit path:

```
seed  mid-life TeamPulse: spine + shipped sprint-01 (src/test green) + stand-in platform + .env(planted secret)
      planted bug: recordStandup's replace filter ignores the day — submitting a new day's standup silently
      deletes the member's PREVIOUS days' entries (REQ-001 "one per member per DAY"; REQ-010 reads past digests).
      Same-day tests + smoke flows stay green, so the bug shipped.

leg 1 /01-planner patch  → certify (P1–P5) · patch-001 record (no status field) · ## Patches row planned · dispatch
leg 2 /04-builder        → patch funnel: TDD-for-bugs fix + regression test · row → in-progress ·
                           build-handoff-patch-001.md (review_mode: patch; slice = the record)
leg 3 /05-reviewer       → fresh seed = handoff + record + owning REQ block · qa-report-patch-001.md (SHIP)
leg 4 /06-release        → G1–G7 (nothing waived) · stand-in deploy + health + smoke · release-report-patch-001.md
                           (RELEASED) · tag release/patch-001 · row → done
leg 5 /status            → truth byte-identical · integrity PASS · patch done ⇒ normal routing resumes
```

Graded between legs with the seats' own deterministic graders:
`check_patch.py --case patch-small` (no --fixture: the spine-identity half is asserted via git by the harness) ·
`check_build.py --case patch-build` · `check_review.py --case patch-review` · `check_release.py --case
patch-release` · leg-5 invariants asserted via git + the emitted CLAUDE.md (truth untouched; a single next
command; no open patch hijacking the route).

Results are appended below by the harness after each leg.

## Leg results — iteration-1 (live)

Five sequential FRESH subagent legs over one workspace (a git repo). Each seat's deliverable was **independently
verified** (git + file inspection) alongside its deterministic grader. **All five seats produced correct
deliverables; the composed invariants hold.** Commit chain: `fc50c4f`(seed)→`dffce18`(1)→`b910c65`+`03569c2`(2)→
`10b32d4`(.gitattributes)→`1e01d8b`(3)→`328332e`(4)→`a8e87e0`(5).

| Leg | Seat | Grader | Real | Deliverable |
|-----|------|--------|------|-------------|
| 1 | 01-planner | check_patch patch-small **7/8** | **8/8** | patch-001 certified (P1–P5 evidenced, no status field), ledger `planned`, dispatch `/04-builder` |
| 2 | 04-builder | check_build patch-build **22/22** | 22/22 | 1-line scope fix `&& e.day===standup.day` + cross-day RED→GREEN regression test; handoff `review_mode:patch`; ledger `in-progress`; budget 2f/22LOC ≤ 2/40 |
| 3 | 05-reviewer | check_review patch-review **10/10** | 10/10 | SHIP, Inferred=0, `spec_slice_hash` MATCH, oracle hash MATCH, context attestation present, isolated |
| 4 | 06-release | check_release patch-release **9/12** | **12/12** | RELEASED; G1–G7 all evaluated (nothing waived); deploy/health/smoke exit 0; tag `release/patch-001`; ledger `done` |
| 5 | status | invariants (git + CLAUDE.md) | **PASS** | integrity PASS; `Next command: /01-planner plan-sprint 2`; spine byte-identical; read-only to truth |

**Composed invariants proven end-to-end:**
- Patch lane composes `01→04→05→06→status`; `review_mode: patch` propagates via the handoff.
- `spec_slice_hash` bound the **patch record** and recomputed **MATCH** at review — the record threaded the whole chain.
- Honesty gates held (05 Inferred=0; fresh reviewer never built it; anti-tautology cross-check bit on the pre-fix baseline).
- All **G1–G7 evaluated** at release; nothing waived on the fast lane.
- **Spine byte-identical through ALL five legs** (`git diff fc50c4f -- docs/spec` empty) — the deepest truth-integrity guarantee.
- Router **resumed normal routing** once the patch reached `done` (no patch-in-flight hijack).

**Grader artifacts — real properties independently verified (the composed seed is richer/more realistic than the
unit fixtures, so unit-fixture-specific assumptions do not all hold — the documented `integration-grader-robustness`
class; NOT seat defects):**
- **Leg 1 — ceremony (check_patch):** flags the seed's **pre-existing** `docs/architecture/`. Verified: `git diff fc50c4f -- docs/architecture docs/design` empty; leg 1 changed only `docs/planning/**`.
- **Leg 4 — G5 identity (check_release PR5):** reads the qa-report from `docs/quality/` (the sprint path); live 05 writes the patch qa-report to `docs/planning/patches/` (co-located — where check_review found it, 06 read it). Verified: `git diff 1e01d8b..b910c65 -- src` empty; qa-report carries `final_commit: b910c65`; report records `gate_code_identity: match`.
- **Leg 4 — deploy exit-0 (check_release PR4):** regex `| 0 |` misses the report's bolded `| **0** |`. Verified: deploy exit 0; `_deploy/live/release.json` written (commit 1e01d8b).
- **Leg 4 — REQ-008 (check_release PR8):** hard-codes the unit fixture's REQ-008; the chain's patch owns REQ-001/REQ-010, which the release notes DO cite.
- **All legs — Windows CRLF (check_build/check_release mutation passes):** text-mode restore leaves CRLF, poisoning worktree-diffs; neutralized with a workspace `.gitattributes` (`* text=auto eol=lf`).

These four grader-robustness items are logged as follow-ups (not blockers): they make the **unit** graders chain-aware without weakening their degenerate-catching.
