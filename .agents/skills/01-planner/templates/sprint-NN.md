<!-- Filename: docs/planning/sprints/sprint-NN.md  (zero-padded: sprint-01, sprint-02, … sprint-10). -->

# Sprint NN — <slice goal>

**Goal:** <one sentence: what a user can observably do, end-to-end, after this sprint>.
**Slice shape:** <walking skeleton | widen the path | edge/rules> · spans domains: <domain-a, domain-b, …>.
**REQs:** <count> — <n> MUST / <n> SHOULD / <n> MAY.

## REQs in this sprint — frozen acceptance snapshot

> **Sprint-freeze.** Each REQ below is referenced by ID **and** carries a *frozen snapshot* of its outcome-level
> Gherkin **as it read in the spine at slice time**. This is a deliberate, dated snapshot — not a live duplicate —
> so the builder's target stays stable even if the spine is amended mid-sprint. The spine (`docs/spec/`) remains the
> live source of truth; if an amendment lands, re-freeze on the next planning pass. (This is the one sanctioned copy
> of declaration text; everywhere else, realizations *reference* `REQ-NNN` and never paste its prose.)

### REQ-NNN: <name>   (MUST|SHOULD|MAY)   →   `docs/spec/capabilities/<domain>.md`

```gherkin
# frozen from spine @ sprint-NN
Given <context>
When <user-observable action>
Then <user-observable outcome>
```

### REQ-NNN: <name>   (MUST|SHOULD|MAY)   →   `docs/spec/capabilities/<domain>.md`

```gherkin
# frozen from spine @ sprint-NN
Given <context>
When <user-observable action>
Then <user-observable outcome>
```

## Done When

> The **coarse, observable, end-to-end** definition of done for the whole slice — the outcome-acceptance of this
> sprint's REQs, traceable to their IDs. Not a re-paste of every detailed UI step (those are skill 03's feature-spec
> Verification Contracts). A reviewer must be able to verify each item unambiguously, end-to-end.

- [ ] <observable end-to-end outcome>  _(REQ-NNN)_
- [ ] <observable end-to-end outcome>  _(REQ-NNN)_
- [ ] <observable end-to-end outcome>  _(REQ-NNN)_

## Implementation order

> Dependency order **within** this sprint. Foundation first (not user-facing but everything needs it), the
> user-facing thread last so the slice is demonstrably end-to-end.

1. <foundation work — e.g. accounts / auth / data model>  _(REQ-NNN)_
2. <the core action that depends on #1>  _(REQ-NNN)_
3. <the output the user reads, closing the end-to-end loop>  _(REQ-NNN)_

## Sprint boundary

- **In scope:** <the thin thread this slice delivers — be specific>.
- **Out of scope:** <related capability deliberately deferred to a later sprint, even though it's tempting>.

## Risks & open questions

> Pull forward any `[NEEDS CLARIFICATION]` markers on this sprint's REQs, and any Unknown+Important bet from
> `docs/discovery/assumption-map.md` this slice is meant to de-risk.

- <risk / open question that could affect this slice — e.g. the assumption this walking skeleton is built to test>
