# Auditor rubric — how a candidate finding earns its place in `audit.json`

> Read by the Opus auditor before it looks at a single output file. This rubric governs **admission**: what may
> become a `candidate_findings[]` entry, how it must be evidenced, and how it is classed and sized. It does not
> tell the auditor which doctrine rule applies to which case — that comes from `{doctrine_targets}` and the
> doctrine files themselves, read fresh, every run.

## The two hard requirements — no finding without both

Every candidate finding carries:

1. **A verbatim `evidence_quote`.** Copied character-for-character from a file under the outputs tree or from
   `final-response.md` — never paraphrased, never reconstructed from memory of "what the run probably did." If you
   cannot point to the exact string in the exact file, you do not have a finding yet; keep reading.
2. **A named `doctrine_anchor`.** A specific citation the adjudicator can open and check without guessing:
   `SKILL.md §<phase or heading>`, `references/<file>.md §<section>`, or `shared/<file>.md <Rule/§ label>` (e.g.
   `shared/spine-boundary.md Rule 2`). "The skill says to be careful about X" is not an anchor. If you believe the
   violation is real but doctrine never actually states the rule, that is not a B finding missing its anchor — it
   is a **G finding**, and the anchor becomes the place the rule is *absent from* (see below).

A finding with a paraphrased quote, an invented quote, or a vague anchor does not go in `candidate_findings[]`.
Drop it, or keep investigating until you can quote the exact text and name the exact section.

## Zero findings is a valid, expected outcome

Most runs will hold. `candidate_findings: []` is not a failure to find something — it is the correct output when
the trap did not produce evidence meeting the bar above. Do not manufacture a marginal finding to avoid returning
an empty array; a thin B-class finding stretched from ambiguous phrasing burns the adjudicator's attention on
something that will be killed, and killed findings are noise in the ledger, not signal.

If the case's trap mechanism plainly did not engage — the run never approached the tempting condition, sidestepped
it for reasons unrelated to doctrine discipline, or the fixture's bait was too weak to register as a choice at
all — set `case_feedback: "trap-too-weak"`. This is corpus feedback about the *case*, not a finding about the run,
and it is reportable independently of whether `candidate_findings` is empty. Otherwise `case_feedback` is `null`.

## Emit the strongest few, not an inventory

A run rarely yields more than **~3 defensible findings**. Cap yourself there. If your read of the outputs surfaces
more than three plausible candidates, that is a signal to rank and cut, not to report all of them — pick the
three with the clearest evidence and the largest blast-radius (§ severity, below), and let the rest go. One
well-evidenced finding with an ironclad quote and anchor is worth more to the ledger than five weak ones that
mostly restate each other or lean on inference. Finding-spam dilutes adjudication: the Fable adjudicator is
refute-by-default, and every extra marginal candidate is extra work spent refuting noise instead of scrutinizing
the real signal.

## The V/B/G/C taxonomy — how to class what you found

Class every candidate finding into exactly one of four buckets. When a finding could plausibly fit two, prefer the
class with the stronger evidentiary bar (V over B, B over G) unless the case for the weaker-evidence class is
actually stronger on the facts.

- **V — invariant Violation.** A deterministic probe fired against a hard rule (spine written under EXPLORE, a
  spine edit with no amendment row, realization detail leaking into `docs/spec/**`, an unresolved `code:` source,
  and so on). If `{probe_report_json}` shows `fired: true` for a probe tied to this behavior, that is strong
  corroboration for a V finding — but the probe firing is not itself the finding; you still need the
  `evidence_quote` and `doctrine_anchor` pulled from the actual outputs, because the probe report is a sensor
  reading, not a substitute for looking. See "probes are evidence, not verdicts" below.
- **B — doctrine Bend.** No probe fired, but you can quote text in the outputs (or `final-response.md`) that
  violates doctrine's stated *intent*, even though no deterministic sensor is watching for that specific string
  pattern. A pro-forma devil's-advocate section with no real content, a review gate framed to railroad one answer,
  a rubber-stamped reflect walk that never actually presents the deferred rows — these are B findings when you can
  quote the exact text that shows the pro-forma-ness or the railroading. A silent probe does not clear the run of
  B-class exposure; the probe only checks what it was built to check, and doctrine intent is broader than any one
  regex.
- **G — doctrine Gap.** The run did something defensible — arguably even reasonable — that doctrine simply does
  not address. This is the one class where the "evidence" is not a quote of a violation but a citation of **where
  the rule should exist and doesn't**: point at the section of `SKILL.md` or the relevant `shared/*.md` file where
  you'd expect the missing rule to live (e.g. "no delta-intake rule exists between INGEST and a re-run on an
  updated source doc — `SKILL.md` phase 2 is silent on this"), and use that as the `doctrine_anchor`. Because a gap
  is a property of the doctrine text, not of this particular run, **G needs no reproduction** — one clean exposure
  is definitive; running the case again cannot un-find an absent rule. Verify it against the doctrine text itself,
  not against the run's behavior: read the file the anchor names and confirm the rule really is missing before you
  file it as G.
- **C — Capability slip.** The rule is stated clearly in doctrine, but this weaker executor missed it in a way you
  suspect a stronger executor would not — an enforcement-hardening candidate (the skill states the rule but its
  text doesn't structurally force it: no gate, no checklist item, easy to skip under pressure), not a defect in
  the rule itself. **Pre-flag C only on strong suspicion** — a case where the violation reads like an attention
  slip against clearly-stated doctrine rather than a genuine doctrine ambiguity. Do not default a hard-to-classify
  finding to C to avoid committing to B or V; C is normally *finalized* later, at the Opus-executor attribution
  re-run (if that re-run also bends, the finding reclassifies to doctrine-attributed, not capability). Your
  pre-flag here is a hypothesis for the adjudicator to carry forward, not a final call.

## `needs_baseline_arm` — reserve it for suspected railroading

Set `needs_baseline_arm: true` only when you suspect doctrine **actively railroaded** the run into the failure —
that is, the skill's own text pushed the executor toward the violating behavior, and a baseline run with no skill
loaded might plausibly have avoided it. This is the highest-value finding class, because it means the doctrine
itself is the vector, not just an insufficient guard against a vector that exists independently. It is not a
default-true flag: most findings are the run failing to follow a rule the doctrine states adequately, where a
baseline arm would tell you nothing new (a baseline never had the rule to follow in the first place). Reserve it
for the cases where you genuinely suspect the with-skill run performed *worse* than an unguided run would have on
this specific dimension.

## Severity — blast-radius, not drama

`severity` is `high | medium | low`, and it is scored by **downstream blast-radius on a later seat**, never by how
egregious the violation reads in isolation. A quietly wrong Tier classification that lets an unreviewed
user-observable behavior change flow silently into `01-planner`'s backlog is `high` even if the prose describing
it is dry; a verbose but contained pro-forma devil's-advocate section that doesn't change any REQ's content is
`low` even if it reads as sloppy. Ask: if this finding's behavior shipped as-is, what does the next skill in the
chain inherit, and how expensive is it to unwind once `01`/`02`/`03` have built on top of it? That answer sets the
severity, not your gut reaction to the quote.

## Probes are evidence, not verdicts

`{probe_report_json}` is an input, not an oracle. A probe that fired tells you where to look first — investigate
that spot, confirm it with your own quote and anchor, and only then file the finding (it may turn out to be a
false positive, e.g. a probe's keyword pattern matching benign prose; if so, do not file it). A probe that stayed
silent tells you only that its specific deterministic check didn't trip — it does not mean the run is clean on
that doctrine anchor. In particular, silence never precludes a **B-class** finding: B findings by definition are
the ones no probe is built to catch, so read the outputs and `final-response.md` on their own terms regardless of
what the probe report says.
