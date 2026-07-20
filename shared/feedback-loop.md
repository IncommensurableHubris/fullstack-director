# Feedback Loop — dogfood → distill → upstream (the framework improving itself)

> **One contract, read by both sides.** This file is **vendored into every consumer project** (by
> `tools/vendor.py`) so the consumer capturing friction and the master repo triaging it follow the same rules.
> It applies the framework's own amendment discipline to the framework itself: structured capture, tiered
> dispositions, an append-only log, and a durability rule — a fix that leaves no regression guard behind is not
> done. Evidence base: `_artifacts/wsb-vendor-research.md` (Chromium/Android upstream-first · Mozilla bug-writing
> · Google dogfooding · Husain/Braintrust/Anthropic eval loops · ADR immutability).

## The loop at a glance

```
consumer repo (dogfooding)                    master repo (fullstack-director)
────────────────────────────                  ─────────────────────────────────
friction → FB entry in                        triage ritual (batched, before a
docs/framework-feedback.md      ──────────►   re-vendor): dispose EVERY entry
(append-only, SHA-stamped)                    fix / eval-case / doctrine-line /
                                              defer(+revisit trigger)
        ▲                                                   │
        │                                     every fix terminates in an eval
re-vendor (tag-gated, atomic):                case or a dated doctrine line
entries marked resolved-in <sha>  ◄──────────  tag → sync each consumer
```

## 1 · Capture — at the point of friction, in the consumer

Append an entry to **`docs/framework-feedback.md`** (seeded by `vendor.py sync`; create it if absent). One entry
per finding, **at the moment it happens** — not from memory at day's end. The template:

```markdown
### FB-NNN · <date> · <one-line title>
- **framework:** <source_commit from .director/vendor-manifest.json>
- **harness:** claude-code | codex | gemini-cli
- **seat:** <00-discovery … status | shared | vendor>
- **severity:** blocks-gate | wrong-but-recoverable | friction-only
- **expected:** <what the framework/skill should have done>
- **actual:** <what happened>
- **repro:** <minimal steps / the command>
- **artifact:** <path to transcript/diff/spine file>
- **status:** open | superseded-by FB-NNN | resolved-in <master sha>
```

Rules that keep the ledger high-signal:

- **Every entry is SHA-stamped** (`framework:` from the manifest). Feedback against an unknown version is
  unfalsifiable — it cannot indict or exonerate a specific framework state.
- **Append-only, immutable.** A wrong entry is **superseded** by a new one, never edited (the ADR rule). Never
  summarize or compact the ledger — detail erodes with every rewrite (the context-collapse failure mode).
- **`expected` vs `actual` + minimal `repro`** are the load-bearing fields (the Mozilla discipline). An entry
  without them is a mood, not a finding.
- **severity vocabulary (fixed, three values):** `blocks-gate` — a gate/verdict was wrong or unreachable;
  `wrong-but-recoverable` — incorrect output the operator corrected; `friction-only` — worked, but cost real time.
- The **`artifact:`** pointer is the trace (a transcript path, a diff, the offending spine file) — the raw
  material the master-side error analysis reads.

### Activation — capture is never memory-dependent

Two triggers, one clerk:

- **Narrated (any moment):** the user says *"framework friction: …"* / *"log framework feedback"* — the
  **`feedback` skill** (vendored with the set) does the clerical work: stamps the SHA from the manifest, numbers
  the entry, appends it, and returns to the interrupted work. The user never hand-writes the block.
- **Structural (the seats self-report):** when a seat **HALTs, BLOCKs, or misroutes** and the cause traces to the
  **framework itself** (a wrong gate condition, a contradictory template, a skill misfiring) rather than to this
  project's code or spine, the agent runs the `feedback` skill **before the session ends** — the machinery already
  stopped; capturing why is part of stopping honestly. (A cause in the project's code → the normal chain; in the
  spine → the amendment protocol. The `feedback` skill's routing test decides.)

**Loop B's activation** is the maintainer, in the **master** repo, saying *"run the dogfood triage"* — batched,
typically when `vendor.py sync`/`check` report open entries (the tool counts them and reminds you), or before any
planned re-vendor.

## 2 · Upstream-first — vendored files are never edited in a consumer

- A fix belongs in the **master repo**, arriving by re-vendor — never a silent patch to `.agents/skills/**`,
  `.claude/skills/**`, or `shared/**` in the consumer. Silent downstream patches make the next sync
  unreviewable and the fix unshareable (the Chromium/Android lesson).
- **Emergency escape hatch:** a local patch is permitted to unblock work, but it MUST get a ledger entry
  (severity `blocks-gate`, the patch described under `actual:`) — and it is mechanically visible regardless:
  `python tools/vendor.py check` flags every locally-modified vendored file by hash. An unledgered local patch is
  drift, and the next `sync` will refuse to touch it (skip + report) until resolved.

## 3 · Triage — in the master repo, batched, before each re-vendor

Read every consumer's ledger (`open` entries). Dispose **each entry exactly once**, logging the disposition
append-only in **`_artifacts/dogfood-triage.md`** (`FB-ref · disposition · rationale · what landed`):

| Disposition | Meaning | Lands as |
|---|---|---|
| **fix** | the skill/template/tool is wrong | a master-repo change **+ the durability rule below** |
| **eval-case** | the failure is gradeable and worth guarding directly | a fixture/degenerate in the owning seat's `evals/` (or the integration cases) |
| **doctrine-line** | the skill was right but underspecified | a **dated, appended** line in the owning skill's `references/` or `shared/` — appended, never rewritten in place |
| **defer** | acknowledged, not actioned | a backlog row **with a revisit trigger** (a defer without a trigger is a silent drop — the loop-killer) |

**The durability rule:** every **fix** terminates in **an eval case or a dated doctrine line** — a fix that leaves
no trace of *why* can silently regress. Anti-bloat nuance (Husain/Braintrust): promote **one representative eval
case per failure cluster**, not one per incident; reserve automated cases for failures that would persist past a
text fix. **Convergence signal:** the same workaround appearing in independent runs/repos is the strongest
evidence a skill should absorb it.

## 4 · Re-vendor — batched and tag-gated, never a drip

1. Triage lands (≥1 fix / eval-case / doctrine-line committed, validators green).
2. Tag the master: `vendor/YYYY-MM-DD`.
3. `python tools/vendor.py sync --target <consumer>` — one atomic act per consumer.
4. Mark the resolved ledger entries `resolved-in <sha>` (close the loop — unanswered feedback kills reporting;
   that applies to future-you too).

Continuous re-vendoring between triages erodes the meaning of the `framework:` stamp — batch it.

## Anti-patterns (each one broke someone; don't repeat them)

1. Silently patching the vendored copy (unreviewable divergence; lost fixes).
2. Feedback without the `framework:` SHA (unfalsifiable).
3. A fix with no eval case and no doctrine line (regresses silently).
4. Collecting feedback and never disposing it (kills the reporting habit).
5. One eval case per incident instead of per cluster (suite bloat, noise).
6. Summarizing/compacting the ledger or a doctrine log (context collapse — append, supersede, never rewrite).
7. Overfitting a fix to the one transcript that reported it (check the skill's general intent).
8. Free-text feedback scattered outside the ledger (unsearchable, untriageable).
9. Drip re-vendoring without tags (the version stamp stops meaning anything).
