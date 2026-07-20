# Refactor Execution — baby steps, explicit move-typing, and the behavior-preservation oracle

> Loaded by `08` at **EXECUTE**. The discipline here is what makes a refactor *safe* rather than a rewrite in
> disguise. Read with `references/refactoring-catalog.md` (the moves) and `references/health-assessment.md` (the
> scope). Sequential — no subagents.

## The behavior-preservation oracle (the honesty gate — establish it BEFORE any move)

LLM refactors silently alter behavior in a meaningful fraction of edits (6–8% of edits; up to ~76% of naive
Extract-Method attempts), so a *biting* test oracle is the **only** real defense. The oracle is four layers, each
objective:

1. **Green before and after.** The suite passes at the **pre-refactor commit** (capture it: `git rev-parse HEAD`
   before any edit) **and** after each move — with a **positive executed-test count** (never "0 tests, exit 0").
2. **The oracle is UNCHANGED.** You **never edit the pre-existing tests** to make them pass. A refactor that rewrites
   its own golden master proves *nothing* — it is the single most dangerous cheat. New characterization tests are
   **additive**; the existing suite is read-only to you.
3. **The oracle BITES.** A **mutated** implementation (flip a comparison / a boolean / a branch) must make the suite
   **fail**. A suite still green on a broken impl is *tautological* — not a safety net. If it doesn't bite, strengthen
   it (or write a real characterization test) **before** refactoring.
4. **Characterize the gaps FIRST.** For any target the existing suite doesn't cover, write **characterization tests**
   (golden-master / approval): capture the *current* input→output — **bugs included** (Two Hats: you preserve behavior,
   you don't fix it here). Commit them separately (`test(scope): characterize <module>`) before the first move.

**If you cannot establish a biting oracle for a target, do not refactor it.** Say so and stop — an unguarded refactor
is a bet, not an improvement.

## Baby steps — one typed move at a time

```
1. Make ONE refactoring move — named by TYPE (Extract Method, Move Function, Inline, Rename, Replace Conditional…).
   Telling yourself the exact move type is the biggest accuracy lever (ICSE: 15.6% -> 86.7% vs "clean this up").
2. Run the oracle + the full suite.
3. ALL green  -> commit: refactor(scope): <the move>   (small, atomic, conventional).
   ANY red     -> REVERT the move immediately. Do NOT debug it. Revert, rethink, try a different move.
```

- **Never batch moves in one commit.** If a test fails you must know *exactly* which move caused it.
- **Never mix a behavior change into a refactor commit** (Two Hats). A bug you spot mid-refactor is **noted and
  routed** (`fix(scope):` is a *separate* commit *after* the refactor, or a route to `/05`) — never smuggled in.
- **Never touch an out-of-scope file to make a move work.** If the move needs a change outside the scope (a bootstrap
  import, a wiring line), record it as a follow-up (a `/04` wiring task) — do not expand the blast radius.

## HALT conditions (surface, don't push through)

- The target has **no biting oracle** and you cannot characterize it safely.
- A move keeps going red after 3 attempts — the structure is fighting you; re-scope or defer.
- The refactor would require a **new dependency** (a zero-dep envelope forbids it — that's a declaration question →
  `reconcile-refactor.md`), or a **structural migration** (Strangler Fig is **plan-only** — route to `/03`→/04`).
- You discover the "duplication" is a **false duplication** — two look-alike paths that differ subtly. **Do not
  collapse them** (the oracle will catch it if you do). Extract only the genuinely-shared part and parameterize the
  divergence, or leave them and note why.

**Never fake a pass.** A refactor that ends red, or that only stays green because the oracle was weakened, is a
BLOCKED verdict — recorded honestly — not a CLEAN one.
