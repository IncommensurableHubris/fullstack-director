# Refactoring Catalog — the moves, with AI-prompt patterns

> Loaded by `08` at **EXECUTE**. Always name the **exact move type** before you make it — explicit move-typing is the
> biggest LLM-refactor accuracy lever (ICSE 2025: 15.6% → 86.7% vs "clean this up"). Every move is **behavior-
> preserving**: verify against the oracle (`references/refactor-execution.md`) after each one, and **revert on red.**

## Characterization tests come first (for any uncovered target)

Before a move on code the existing suite doesn't cover, capture current behavior as a **golden-master** test — bugs
included (Two Hats). They're additive (never edit the existing oracle) and guard the move. Examples:

```js
// Characterize a pure function's current input->output (node:test).
test('assembleDigest characterization — groups by member, needs-help first', () => {
  const d = assembleDigest([{ member: 'a', day: 'D', needsHelp: true, blocker: 'x' }], 'D');
  assert.equal(d.members.length, 1);
  assert.equal(d.needsHelp.length, 1);   // lock in the CURRENT behavior, even if surprising
});
```

## The moves

| Move | When | AI-prompt pattern (be specific) | Verify |
|------|------|--------------------------------|--------|
| **Extract Method** | a function > ~30 lines or a duplicated block | "Extract lines N–M of `f` in `file` into `g(params) -> T`; keep `f` calling `g`; change no behavior." | oracle on `f` still green |
| **Extract Module / Split File** | a god file (> ~300 lines, unrelated exports) | "Split `file` by responsibility into `a.js` (fns …) / `b.js` (fns …); re-export for compatibility; no signature changes." | all imports resolve; oracle green |
| **Move Function** | a fn used more by another module than its home | "Move `f` from `old` to `new`; update every import; keep the signature." | imports compile; no new cycle |
| **Inline** | a single-use wrapper that only delegates | "Inline `wrapper` in `file`; replace call sites with its body; delete it." | oracle on call sites green (watch for hidden defaults) |
| **Rename** | a name that no longer matches purpose | "Rename `old`→`new` in `file` and every reference (imports, calls, types, test assertions, error-string literals)." | grep `old` → zero non-history hits |
| **Replace Conditional with Polymorphism** | a switch/if-chain on a type discriminator | "Replace the switch in `f` with a strategy: interface `I{process()}`, one impl per case, a map/factory to select; keep the external API." | oracle across all cases green (high-risk — review each impl) |
| **Dead-Code Elimination** | an export with zero importers, an unreachable branch | "Remove these zero-importer exports from `file`: […]; remove helpers that become unreachable." | **grep the whole tree (incl. tests/config/strings) first** — static "0 importers" can miss dynamic refs; then build + oracle green |
| **Introduce Parameter Object** | a fn with > 4 params, several always passed together | "Group params [a,b,c] of `f` into an options object; update call sites; no behavior change." | call sites updated; oracle green |

## De-duplication — but beware the FALSE duplication

The common win is **Extract Function**: two verbatim (or near-verbatim) blocks → one shared helper both call. But
first confirm the blocks are *truly* the same: two look-alike paths that **differ by one operator** (e.g. an exact-day
filter vs a cumulative filter) are **not** duplicates — collapsing them changes behavior (the oracle will go red).
Extract only the genuinely-shared part and **parameterize the divergence**, or leave them and note why. "Remove the
duplication" reflexively is the classic behavior-breaking refactor.

## Strangler Fig / Branch by Abstraction — PLAN ONLY

For a major migration (datastore swap, framework change, monolith→services) that can't be one behavior-preserving
pass: `08` writes the **plan** (introduce an abstraction → implement the new impl behind it → remove the legacy), and
**routes execution to the normal `/03-architect` → `/04-builder` chain** across dedicated sprints. Do **not** attempt a
structural migration inside a refactor pass — the skill chain exists for a reason. If the migration is forced by a
**declaration** contradiction (a stated constraint the code can't honor), that's an **amendment** first
(`reconcile-refactor.md`).

## Dependency upgrade / modernization

Read the real changelog (or `chub` for curated migration docs) — not training recall — for the breaking changes;
update the version; fix each break one commit at a time; run the full suite. A **new** dependency beyond a stated
zero-dep / envelope constraint is a **HALT** → a declaration question, not a silent add.
