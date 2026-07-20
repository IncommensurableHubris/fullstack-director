# agent-mini iteration-1 — WS3 composed run (covers Tasks 3.7 / 3.8 / 3.10)

Per the Phase-3 A/B policy, **3.7 (05 eval-floors) · 3.8 (06 G8/G9) · 3.10 (status routing)** are **not** A/B'd
individually — they are covered by **ONE composed `agent-mini` with_skill run** through the live chain. Each seat's
deterministic grader was validated grader-first on hand-ideals + degenerates in its own commit; this run proves the
three also pass on a **real Sonnet arm** running the seats in sequence.

## Setup

Seed = the **real 04-builder output** from `04-builder/iteration-3` (a built `Profile: agent-system` slice: the Beacon
spine with a REQ-002 eval-suite block, the feature spec with a `VC-02 eval-suite` row, `src/` + `tests/` + an eval
harness `evals/run.py`, and 04's build-handoff). One Sonnet arm ran **`/05-reviewer` → `/06-release` → `/status`**.

## Results — all three agent graders green

| Seat | Grader | Grade | What the real arm did |
|------|--------|:-----:|-----------------------|
| **05** | `check_review.py --case agent` | **5/5** | re-executed the REQ-002 eval floor at `final_commit` (`evals_run: 1`, scored 1.00 ≥ 0.80 → **`eval_floors_met: true`**); ran the **grader hack-resistance** spot-check (both degenerate probes — empty + all-uncited — FAILED as required); verdict SHIP; also re-ran its own anti-tautology mutations |
| **06** | `check_release.py --case agent` | **4/4** | gate PASS incl. **G8** (read `eval_floors_met: true`) and **G9** (captured a real span-smoke `dispatch → worker×5 → citation_gate` + a drift note); status BLOCKED only because no platform/human was available to approve a deploy — *not* a gate failure, honestly recorded |
| **status** | `check_status.py --case agent` | **7/7**¹ | integrity **PASS** (L1–L6); `AGENTS.md` re-emitted carrying **`- **Profile:** agent-system`** (the S7 mirror); routed a single next command; `docs/spec/**` + `src/**` **byte-identical** (status never touched truth) |

¹ The first grade read 6/7 — a **composed-run seeding artifact**, not a status violation: all three seats wrote in
one uncommitted session, so `truth_changed` (anchored to the seed commit, which predated the 05/06 outputs) saw
`docs/quality/` + `docs/release/` as "changed". `git diff HEAD -- docs/spec src docs/architecture` was **empty**
(proving status touched no truth); re-graded against the correct **pre-status anchor** (root = the committed post-06
chain state), status is **7/7**. In a real chain each seat commits before the next runs, so this artifact does not
occur.

## What this demonstrates

Sonnet-with-skill, driving the composed agent chain, produces the exact machine-readable contract the seats hand each
other: 05's `eval_floors_met`/`evals_run` tally + hack-resistance → 06's G8/G9 gate → status's profile-aware routing +
AGENTS.md mirror. The honest portability claim holds across the chain, not just per seat.
