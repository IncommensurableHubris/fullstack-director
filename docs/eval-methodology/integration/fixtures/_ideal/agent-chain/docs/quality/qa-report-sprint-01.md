---
verdict: SHIP
eval_floors_met: true
evals_run: 2
findings_high: 0
must_gap: false
final_commit: 1111111111
---
# QA Report — Sprint 01

The declared eval floors were re-run at `final_commit` with pinned seeds; both met (VC-01 grounded 93% ≥ 90%,
VC-02 ASR 0% ≤ 0%). The grader hack-resistance spot-check re-ran the grader-bites degenerate: it still FAILs.
