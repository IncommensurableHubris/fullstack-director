# The build-handoff — engineering the seed a stranger reviews from

> Loaded by skill 04 (builder) during **HANDOFF** (step 7). The **craft + the why** of `04`'s load-bearing output;
> the fill-in artifact is `templates/build-handoff.md`. The handoff at
> `_artifacts/exports/build-handoff-sprint-NN.md` is the **sole seed** for the context-isolated reviewer
> (`05-reviewer`, `shared/subagent-protocol.md`). Its one job: let a **cold reviewer reconstruct the exact diff,
> re-run the oracles, and check REQ coverage with zero access to your build session.** Everything below serves that.

## Evidence, never narrative — why the conversation is poison

Ship **artifacts + evidence + reproduction**, never your chain-of-thought or the approaches you rejected. This is not
brevity for its own sake: the reviewer's value comes from *fresh judgment*, and inheriting "I tried X, it felt wrong,
so I did Y" is precisely the bias that makes a second look worthless — it re-derives your conclusions instead of
testing them. The isolation is real only because the seed is engineered for a stranger. A row is trustworthy because
its **command exits 0**, not because you say it works.

## Frontmatter — the anchor

```yaml
baseline_commit: <git SHA captured at build-start, BEFORE any edit>
final_commit:    <git SHA after the last build commit>
spec_slice_path: docs/planning/sprints/sprint-NN.md
spec_slice_hash: sha256:<16 hex — the tamper-evident binding of the built-against spec slice>
review_mode:     full
```

- **`baseline_commit`** is the single most-reused mechanic in the whole contract. Captured with `git rev-parse HEAD`
  *before* you touch a file, it lets the reviewer run `git diff baseline_commit..final_commit` and see the **exact**
  change set — never the conversation, never your memory of what you changed. (Fresh project with no commit yet? Make
  the initial commit first, then capture.)
- **`final_commit`** closes the range.
- **`spec_slice_path`** asserts the slice `05` must load; we always have it, so `review_mode: full` — say so, so the
  reviewer verifies against the frozen "Done When", not a guess.
- **`spec_slice_hash`** binds *the spec you built against* to *the spec `05` grades against*. `05` recomputes it and
  compares; a mismatch means the slice drifted between build and review, and `05` **BLOCK**s rather than grade against
  a moved contract (Tessl's tamper-evidence, applied to the spec). Compute it **mechanically** — do not hand-hash:

  > **Algorithm (identical to `05`'s verify side — `05/references/review-discipline.md`).** Inputs, in order: the
  > `spec_slice_path` file (`sprint-NN.md` — the frozen outcome-Gherkin + "Done When"), then, **if a design contract
  > exists**, `docs/design/approved/sprint-NN/manifest.md`. Normalize each to LF (`\r\n`→`\n`, `\r`→`\n`) — nothing
  > else (the files are frozen). Concatenate `sprint-slice + "\n" + manifest` (omit the manifest half when there is
  > none). `spec_slice_hash = "sha256:" + SHA256(payload_utf8).hexdigest()[:16]`. One-liner:
  >
  > ```
  > python -c "import hashlib,sys; d=[open(p,'rb').read().decode('utf-8').replace('\r\n','\n').replace('\r','\n') for p in sys.argv[1:]]; print('sha256:'+hashlib.sha256(('\n'.join(d)).encode()).hexdigest()[:16])" docs/planning/sprints/sprint-NN.md docs/design/approved/sprint-NN/manifest.md
  > ```

## (a) File List — the reviewer's map, and a deterministic cross-check

Every new / modified / deleted path, repo-root-relative. Two reasons it is non-negotiable: it is the reviewer's map
of where to look, **and** it is mechanically checkable — `git diff --name-status baseline..final` must equal this
list. A mismatch catches both directions of dishonesty: an **undeclared write** (you changed a file you didn't list)
and a **hallucinated claim** (you listed a file you never touched). **HALT completion if the File List is
incomplete** — an incomplete map silently narrows the review.

## (b) Verification-Contract carry-forward — the heart

Carry **every** VC row from `03`'s feature specs forward, and stamp each with the builder's **evidence state**. The
three states are `05`'s exact vocabulary — it consumes them 1:1, so use them precisely:

| State | What it means here | Evidence you must attach |
|---|---|---|
| **EXECUTED** | a test ran, went green, and is known to exercise the behavior (cleared the anti-tautology gate) | `test_file:line → PASS` + the exact **reproduction command** + a **RED-phase note** (observed failing before impl) |
| **OBSERVED** | you drove the real system (CLI/API/dev server) and watched the behavior | the transcript / curl output — the command and its response verbatim |
| **INFERRED** | you read the code and argued it satisfies the behavior; **no execution occurred** | `file:line` pointers **+ a cited reason** it isn't EXECUTED **+ the Unknown** |

**INFERRED always counts as NOT verified** — and that is the point, not a failure. An INFERRED row is exactly where
`05` *starts*: it re-attempts execution and escalates the row to EXECUTED/OBSERVED or blocks. So an INFERRED row must
be **honestly earned**: cite *why* it couldn't run (the missing runtime, the absent contract — a path, not a mood)
and its **Unknown** (what remains unproven). *"Based on standard patterns"* is not evidence; it is the smell of a
fabricated pass. A `browser` VC in a headless build is the canonical honest INFERRED — name the missing runtime and
move on; do not drop it (that hides a requirement) and do not fake-pass it (that lies to the reviewer).

**Verify-live rows (WS6).** A row exercising a spine-declared **verify-live** tech (`architecture-constraints.md` §
Verify-live) carries a **`verified: docs/verification/<tech>.md`** token beside its state — the record whose cited
claim you built against (`shared/live-source-verification.md`). Because you built against a live-source record, the
state is **EXECUTED/OBSERVED, never `INFERRED`**: an `INFERRED` verify-live claim is a confabulation risk, so `05`
grades it unverified and `06` G11 blocks the ship. If the shape genuinely couldn't be sourced, that is a HALT to
re-seed via `/00`, not an `INFERRED` fake-pass.

Two more per-row fields keep the reviewer from having to trust you:

- **Reproduction command** — the exact command that re-runs the oracle (`node --test test/digest.test.js`). `05`'s
  EXECUTED state is only real if the command it inherits actually exits 0; a claimed-EXECUTED row whose command is
  red is caught immediately.
- **Oracle hash** — a short hash of the test/oracle file (e.g. first 12 hex of its SHA-256). It is **tamper-evidence**:
  it lets the reviewer confirm the oracle it re-runs is the one you claimed to run — the mechanical defense against
  "the builder quietly rewrote the test until it passed." Record the value; the reviewer recomputes it.

## (c) REQ → test coverage map — a partial is a first-class output

For **every in-scope REQ**: `REQ-NNN → test file:line → FULL | PARTIAL | NONE`. This is traceability made explicit,
and its purpose is to make gaps *loud*. A PARTIAL or a NONE is not something to hide until the reviewer finds it — it
is a declared output the sprint plan and `05` act on. Where the slice carries a `02` design contract, add the
**DM-ID → file:line** map the same way (every manifest `DM-NNN` this slice implements, pointed at the code that
realizes it); a DM-ID with no implementation location is an incomplete build, surfaced here, not buried.

## (d) Attestations & log — what a cold reviewer can't otherwise know

- **Spine-untouched attestation** — you built from realizations and wrote no `docs/spec/**`. The reviewer can verify
  it against the diff; stating it makes the boundary a checked property.
- **Deviations & decisions** — where the build honestly diverged from the spec, and the **three-way drift verdicts**
  you surfaced (code / test / **spec → escalate to `03`** / **declaration → pending amendment for `00`/`05`**). This
  is how a wrong *realization* or *declaration* reaches the humans — 04 escalates, never amends
  (`references/build-discipline.md`).
- **HALT / blocked record** — every HALT with its reason. `06-release` **blocks** on these, so an omitted blocker is
  a silent ship.
- **Dependency provenance + `sbom.json` path** — the allow-list/pin/audit result (or "zero dependencies added").
- **Environment / repro facts** — runner + version, the command, seeds/fixtures — so the reviewer reproduces your
  EXECUTED state on the first try rather than discovering an environment mismatch.

## The honesty test before you write "done"

A reviewer with **only this file** and the repo at `final_commit` must be able to: rebuild the diff from
`baseline_commit`; re-run every EXECUTED row's command and see it exit 0; find each INFERRED row's cited reason and
know what to escalate; and read REQ (and DM) coverage without opening your conversation. If any of those is not true
from the file alone, the handoff isn't done — regardless of whether the code works.
