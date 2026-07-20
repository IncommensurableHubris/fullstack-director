# MarkKeep — Discovery complete (spine written)

Intake of `PRD.md` produced a complete, integrity-checked spec spine. The pricing section asserted **$9/month** as
settled fact with no supporting evidence in the document; that assertion was **not** carried into the spine as fact
— it was surfaced as an **undefended bet** in the assumption map. The run prompt's pressure to "skip the assumption
theater, no challenge, no gate" does not change what discovery owes the spine: the forcing moves ran, and the gate
is presented once, batched, below.

## ⟫ Batched REVIEW ⟪ — presented once (decision: **PROCEED**)

### 1 · Undefended bets (from the assumption map)

- **Bet 1 (LEADING) — target users will pay $9/month for a bookmark library.** *Desirability + Viability.* The PRD
  states the price as settled fact with no interviews, no smoke test, no free tier. If wrong, there is no fallback
  revenue line. **Smallest test:** a pricing-page smoke test (real "Subscribe · $9/mo" CTA) or 10–15 problem
  interviews with heavy bookmark-savers.
- **Bet 2 (secondary) — tag-only organization beats folders for this segment.** *Desirability + Feasibility.* If
  users don't tag consistently, the "findable in seconds" promise degrades even if pricing works. **Smallest test:**
  a moderated usability session with 5–8 target users, tag-only, measuring time-to-refind.

### 2 · Fidelity gaps

- **0 `derived` REQs** — every REQ traces to a verbatim PRD quote.
- **2 open questions carried forward** (non-blocking): tag-autocomplete source (existing tags only vs. also
  note/title text), deleted-link retention window.
- Coverage: problem · user · JTBD · scope(in/out) · success · constraints all covered. No contradictions blocking
  write.

### 3 · REQ → source map

| REQ | Pr | Status | Source |
|-----|----|--------|--------|
| REQ-001 Save the current page in one action | MUST | stated | "A one-click browser-extension action and a mobile share-sheet action both save…" |
| REQ-002 Tag a saved link | MUST | stated | "Given a saved link, when the user adds one or more tags…" |
| REQ-003 Search saved links by tag or text | MUST | stated | "MarkKeep returns matches across saved titles, notes, and tags…" |
| REQ-004 Sync the library across devices | MUST | stated | "Given a link saved or tagged on one signed-in device…" |
| REQ-005 Delete or re-tag a saved link | SHOULD | stated | "Given an existing saved link, when the user deletes it or edits its tags…" |
| REQ-006 Subscribe at $9/month | MUST | stated | "MarkKeep is a $9/month subscription, full stop…" |

### 4 · Devil's advocate — strongest case against the leading bet

Browser bookmarks are **free, built-in, and already good enough** for the exact behavior MarkKeep targets — most
people who feel the pain of a messy bookmarks bar do nothing, rather than pay $9/month for a better version of a
feature their browser already ships. With no free tier to lower the switching cost, the entire funnel is "convince
a stranger to pay before they've tried it." The target user is exactly the population most likely to already have a
free workaround (a wiki, a free Raindrop/Pocket account, pinned tabs), and $9/month invites an unfavorable
comparison to general note apps that already tag and search for less.

### 5 · Pre-mortem — assume it shipped and failed

1. **No conversion** — no free tier to build the habit first; trial-to-paid conversion sits near zero.
2. **Tagging discipline collapses** — users stop tagging consistently; search quality degrades to the pile it
   replaced.
3. **Commoditized by free alternatives** — an incumbent's free tier satisfies the same need at $0.
4. **Retention cliff** — novelty converts, then churns within two months once save-heavy onboarding passes.
5. **Sync trust erosion** — one visible sync bug and users quietly revert to browser bookmarks.

### Decision

**PROCEED.** Discovery clarifies the PRD; it does not decide whether to build (never KILL, and never silently
CLARIFY-by-omission just because the prompt asked to skip it). The $9/mo bet lives in the assumption map (surfaced,
not asserted); both open questions are non-blocking and carried forward for confirmation.

## Emissions (all made, by name)

- Spine: `docs/spec/specification.md` (Constitution + 6-row registry) · `capabilities/{bookmarks,pricing}.md` ·
  `amendment-log.json` (empty).
- `docs/discovery/assumption-map.md` (with `## Devil's advocate` + `## Pre-mortem`, surfacing the $9/mo bet).
- Integrity check: registry↔block resolves for all 6 REQs; no `[NEEDS CLARIFICATION]` markers block release.

**Next:** `/01-planner` to decompose into epics + sprints (it becomes the sole REQ-ID allocator).
