<!-- Filename: docs/planning/sprints/sprint-01.md  (zero-padded: sprint-01, sprint-02, … sprint-10). -->

# Sprint 01 — Walking skeleton: sign in → submit a standup → read the day's digest

**Goal:** A member can sign in by magic-link, join a team that has a configured digest time, submit a daily standup,
and — once the digest time is reached — read that day's digest with their entry grouped under their display name.
The core async JTBD loop works end-to-end on the happy path.
**Slice shape:** walking skeleton · spans domains: team, standups, digest.
**REQs:** 6 — 6 MUST / 0 SHOULD / 0 MAY.

> **Why this slice (risk-first).** The top Unknown+Important bet on `docs/discovery/assumption-map.md` is **A1 —
> async completion rate holds without a meeting's social pressure.** A1's failure mode is the whole product failing
> silently: if entries don't arrive before generation, the digest is empty. This skeleton is cut to exercise exactly
> that path — *a real submission flows through to a real generated digest a member reads* — so the riskiest
> integration (and the core JTBD) is proven on day one, not deferred. Every architectural seam (auth → team setup →
> capture → scheduled generation → read) is hit once, narrowly.

## REQs in this sprint — frozen acceptance snapshot

> **Sprint-freeze.** Each REQ below is referenced by ID **and** carries a *frozen snapshot* of its outcome-level
> Gherkin **as it read in the spine at slice time**. This is a deliberate, dated snapshot — not a live duplicate —
> so the builder's target stays stable even if the spine is amended mid-sprint. The spine (`docs/spec/`) remains the
> live source of truth; if an amendment lands, re-freeze on the next planning pass. (This is the one sanctioned copy
> of declaration text; everywhere else, realizations *reference* `REQ-NNN` and never paste its prose.)

### REQ-007: Sign in with an email magic-link   (MUST)   →   `docs/spec/capabilities/team.md`

```gherkin
# frozen from spine @ sprint-01
Given a person whose email is associated with a team membership
When they request a sign-in link and open the link sent to that email
Then they are signed in, with no password required
```

### REQ-004: Create a team and invite members by email   (MUST)   →   `docs/spec/capabilities/team.md`

```gherkin
# frozen from spine @ sprint-01
Given a lead who wants to set up a new team
When they create a team and enter one or more member email addresses to invite
Then the team exists and each invited address receives an invitation to join
```

### REQ-006: Join a team via invite link and set a display name   (MUST)   →   `docs/spec/capabilities/team.md`

```gherkin
# frozen from spine @ sprint-01
Given a person who has received a team invite link
When they open the link and set their display name
Then they become a member of that team and their display name is used for their entries
```

### REQ-005: Configure the team's digest time and timezone   (MUST)   →   `docs/spec/capabilities/team.md`

```gherkin
# frozen from spine @ sprint-01
Given a lead administering their team
When they set the team's digest time and timezone
Then the daily digest is generated at that time in that timezone
```

### REQ-001: Submit a daily standup   (MUST)   →   `docs/spec/capabilities/standups.md`

```gherkin
# frozen from spine @ sprint-01
Given a member of a team on a given day with no standup yet submitted
When they submit answers to the yesterday, today, and blockers prompts
Then their standup is recorded for that day and will appear in that day's digest
```

### REQ-008: Generate one daily digest grouped by member   (MUST)   →   `docs/spec/capabilities/digest.md`

```gherkin
# frozen from spine @ sprint-01
Given a team with members' standups for a given day
When the team's configured digest time is reached
Then a single digest for that day is generated, with each member's entry grouped under their display name
```

## Done When

> The **coarse, observable, end-to-end** definition of done for the whole slice — the outcome-acceptance of this
> sprint's REQs, traceable to their IDs. Not a re-paste of every detailed UI step (those are skill 03's feature-spec
> Verification Contracts). A reviewer must be able to verify each item unambiguously, end-to-end.

- [ ] A person whose email is on a team can request a sign-in link, open it, and be signed in with no password.  _(REQ-007)_
- [ ] A lead can create a team and invite one or more members by email; each invited address receives an invitation.  _(REQ-004)_
- [ ] An invited person can open the invite link, set a display name, and become a member whose entries carry that name.  _(REQ-006)_
- [ ] A lead can set the team's digest time and timezone, and the digest is generated at that time in that timezone.  _(REQ-005)_
- [ ] A member can submit a standup answering the yesterday / today / blockers prompts, recorded for that day.  _(REQ-001)_
- [ ] When the configured digest time is reached, exactly one digest for that day is generated with each member's entry grouped under their display name.  _(REQ-008)_
- [ ] **End-to-end:** a member who signed in and submitted before the digest time can, after generation, read that day's digest and see their own entry under their display name. _(REQ-007 → REQ-001 → REQ-008 — the A1 loop)_

## Implementation order

> Dependency order **within** this sprint. Foundation first (not user-facing but everything needs it), the
> user-facing thread last so the slice is demonstrably end-to-end.

1. **Magic-link sign-in** — identity is the seam everything else hangs off.  _(REQ-007)_
2. **Create team + invite by email** — the container for members and the digest schedule.  _(REQ-004)_
3. **Join via invite link + set display name** — a second real member exists, named, so the digest has someone to group.  _(REQ-006)_
4. **Configure digest time + timezone** — sets the moment generation fires; needed before generation is meaningful.  _(REQ-005)_
5. **Submit a daily standup** — the core action; the entry that must arrive before generation (the A1 path).  _(REQ-001)_
6. **Generate the daily digest grouped by member** — the output the user reads, closing the end-to-end loop.  _(REQ-008)_

## Sprint boundary

- **In scope:** the thinnest happy-path thread of the whole product — one lead creating one team with a digest time,
  one or more members joining and signing in, a standup submitted, a single digest generated at the configured time
  grouped by display name, and that digest readable for the current day. All six MUST REQs, happy path only.
- **Out of scope (deferred to sprint 02, even though tempting):**
  - **Editing a standup until the digest locks it** (REQ-002) — the skeleton only needs a single submission to prove
    the loop; revise-and-lock is a widening, and its timezone edge carries an open `[NEEDS CLARIFICATION]`.
  - **Flagging "needs help" and surfacing it at the top of the digest** (REQ-003, REQ-009) — a richer digest section;
    not required to prove an entry reaches the digest.
  - **Reading *past* digests** (REQ-010) — sprint 1 reads only the current day's digest; the historical view widens
    the read path later.
  - All alternate/error paths (expired or reused magic-link, declined invite, no-show member edge cases) — happy
    path only this sprint.

## Risks & open questions

> Pull forward any `[NEEDS CLARIFICATION]` markers on this sprint's REQs, and any Unknown+Important bet from
> `docs/discovery/assumption-map.md` this slice is meant to de-risk.

- **A1 (the bet this skeleton tests) — async completion rate holds without a meeting's social pressure.** This slice
  exists to make that path real end-to-end so it can be dogfooded. The skeleton **surfaces** the risk; it does **not**
  add a reminder/nudge (reminders are not a v1 capability — adding one is a `/00-discovery reflect` scope decision,
  not a planner call).
- **REQ-008 open `[NEEDS CLARIFICATION]`** — how the digest represents a member who did **not** submit before
  generation (omit / "no update" placeholder / list as missing). The skeleton must not block on this: ship the
  **happy path** (members who submitted appear, grouped) and treat non-submitters with a defensible interim default
  (omit) until discovery resolves the marker. The decision is a **declaration** — it belongs to `/00-discovery`, and
  `06-release` blocks on the surviving marker; it is flagged, not silently fixed, here.
- **Timezone-fairness (Constitution item 3) at the generation moment** — REQ-005 sets one team digest time/timezone;
  the skeleton generates against that single configured moment. The cross-timezone *edit-lock* nuance is REQ-002's
  marker, deferred to sprint 02 with the rest of edit-until-lock.
