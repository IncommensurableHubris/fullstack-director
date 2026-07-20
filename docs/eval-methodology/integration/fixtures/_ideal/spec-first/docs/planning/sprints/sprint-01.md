<!-- Filename: docs/planning/sprints/sprint-01.md  (zero-padded: sprint-01, sprint-02, … sprint-10). -->

# Sprint 01 — Walking skeleton: sign in → submit a standup → read the day's digest

**Goal:** A member can sign in by magic-link, join a team that has a configured digest time, submit a daily standup,
and — once the digest time is reached — read that day's digest with their entry grouped under their display name.
**Slice shape:** walking skeleton · spans domains: team, standups, digest.
**REQs:** 6 — 6 MUST / 0 SHOULD / 0 MAY.

## REQs in this sprint — frozen acceptance snapshot

> **Sprint-freeze.** Each REQ is referenced by ID **and** carries a *frozen snapshot* of its outcome-level Gherkin as
> it read in the spine at slice time — a deliberate, dated snapshot, not a live duplicate.

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

- [ ] A person whose email is on a team can request a sign-in link, open it, and be signed in with no password.  _(REQ-007)_
- [ ] A lead can create a team and invite one or more members by email; each invited address receives an invitation.  _(REQ-004)_
- [ ] An invited person can open the invite link, set a display name, and become a member whose entries carry that name.  _(REQ-006)_
- [ ] A lead can set the team's digest time and timezone, and the digest is generated at that time in that timezone.  _(REQ-005)_
- [ ] A member can submit a standup answering the yesterday / today / blockers prompts, recorded for that day.  _(REQ-001)_
- [ ] When the configured digest time is reached, exactly one digest for that day is generated with each member's entry grouped under their display name.  _(REQ-008)_
- [ ] **End-to-end:** a member who signed in and submitted before the digest time can, after generation, read that day's digest and see their own entry under their display name. _(REQ-007 → REQ-001 → REQ-008)_

## Sprint boundary

- **In scope:** the thinnest happy-path thread of the whole product — all six MUST REQs, happy path only. A
  non-submitter is omitted from the digest (the PRD's decisive resolution); the day locks team-wide at the configured
  digest time (REQ-002's edit-lock, resolved decisively in the PRD — no surviving marker).
- **Out of scope (deferred to sprint 02):** editing a standup until lock (REQ-002), "needs help" surfacing (REQ-003,
  REQ-009), reading *past* digests (REQ-010), and all alternate/error paths.
