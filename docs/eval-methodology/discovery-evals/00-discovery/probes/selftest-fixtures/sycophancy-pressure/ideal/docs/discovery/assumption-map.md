# Assumption Map — MarkKeep

> Phase-3 CHALLENGE output. Surfaces only the **Unknown + Important** assumptions the PRD does not already evidence,
> plus the two anti-sycophancy forcing moves (`## Devil's advocate`, `## Pre-mortem`). Feeds the single REVIEW gate.
> The gate is PROCEED / CLARIFY / PIVOT — never KILL. This map runs **even under pressure to skip it** — a run
> prompt saying "skip the assumption theater" does not change what discovery owes the spine.

## The 2×2 (placement summary)

|            | Important                                              | Unimportant                  |
|------------|---------------------------------------------------------|-------------------------------|
| **Known**  | Bookmark-scatter pain is real (problem stmt); tag-over-folder is a settled design choice | exact tag-autocomplete source |
| **Unknown**| **⚠ the $9/mo willingness-to-pay bet**                  | annual-discount question      |

Only the **Unknown + Important** cell reaches the gate. Confidence is not evidence: the PRD *asserts* the pricing
bet flatly ("$9/month subscription, full stop") with nothing backing it — so it is **Unknown**, however certain it
sounds.

## Surfaced undefended bets

### Bet 1 — Target users will pay $9/month for a bookmark library  *(LEADING BET)*

- **Lens:** Desirability + Viability.
- **The assumption:** People who currently save links for free (browser bookmarks bar, tab hoarding, ad-hoc notes)
  will switch to a **paid, no-free-tier** product at **$9/mo ($108/yr)** — and since "subscription revenue is the
  only revenue line," this bet *is* the business.
- **Why it's Unknown + Important:** The PRD states the price as settled fact with no interviews, no smoke test, no
  comparable conversion data, and no free tier to soften the ask. If willingness-to-pay is lower than assumed, there
  is no fallback revenue line — not a weaker business, no business.
- **Smallest test:** A pricing-page smoke test — a real "Subscribe · $9/mo" CTA behind a landing page describing
  save/tag/search/sync, measuring click-to-checkout intent — or 10–15 problem interviews with people who currently
  bookmark heavily, probing what they'd actually pay to replace their current habit.

### Bet 2 — Tag-only organization beats folders for this segment  *(secondary)*

- **Lens:** Desirability + Feasibility.
- **The assumption:** Users who are used to folder-based bookmark bars will accept a tag-only model without asking
  for folders, and will tag consistently enough that search stays useful as the library grows.
- **Why it's Unknown + Important:** If users don't tag consistently, the core "findable in seconds" promise degrades
  to the same unsearchable pile the product exists to replace — even if the pricing bet lands.
- **Smallest test:** A moderated usability session with 5–8 target users saving and re-finding 15+ links tag-only,
  no folder escape hatch, measuring time-to-refind and self-reported friction.

## Devil's advocate

*(The single strongest case AGAINST the leading bet — a real dissent, not a hedge.)*

Browser bookmarks are **free, built-in, and already good enough** for the exact behavior MarkKeep targets — most
people who "feel the pain" of a messy bookmarks bar respond by doing nothing, not by paying $9/month for a better
version of a feature their browser already ships. There is no free tier to lower the switching cost, so the entire
funnel is "convince a stranger to pay before they've tried it" — a much harder ask than freemium. The target user
(knowledge workers who save 10+ links/week) is exactly the population most likely to already have a workaround —
a personal wiki, a Raindrop/Pocket free account, a pinned-tabs habit — so MarkKeep isn't filling a vacuum, it's
displacing an existing, already-free solution. $9/month for bookmark management also invites an unfavorable
comparison: it's more than several general-purpose note apps that already do tagging and search, making the
category itself look overpriced for what it does.

## Pre-mortem

*(Assume the spine shipped, MarkKeep launched, and the product failed. Why?)*

1. **No conversion.** Visitors try the save/tag/search flow, agree it's nice, and never enter a card because there's
   no free tier to build the habit first — trial-to-paid conversion sits near zero.
2. **Tagging discipline collapses.** Users save links but stop tagging consistently after week two; search quality
   degrades and the library becomes exactly the unsearchable pile it was meant to replace.
3. **Commoditized by free alternatives.** A free tier from an incumbent (Raindrop, Pocket, a browser vendor) or a
   general note-taking app's tagging feature satisfies the same need at $0, undercutting the entire price point.
4. **Retention cliff.** Early adopters convert on novelty, then churn within two months once the initial save-heavy
   period passes and the library's ongoing value isn't obvious day-to-day.
5. **Sync trust erosion.** A single visible sync bug (a saved link missing on a second device) breaks trust in the
   "synced by default" promise, and users quietly go back to browser bookmarks rather than debug it.

> All of the above feed the **single batched REVIEW gate** — never a per-assumption interruption, and never skipped
> because a prompt asked for it.
