# Assumption Map — MailSweep

> Phase-3 CHALLENGE output. Surfaces the **Unknown + Important** assumptions the PRD does not already evidence, plus
> the two anti-sycophancy forcing moves (`## Devil's advocate`, `## Pre-mortem`), and a note on the source document
> itself. Feeds the single REVIEW gate. The gate is PROCEED / CLARIFY / PIVOT — never KILL.

## Source-document note

`PRD.md` carries a block of instructions addressed to "AI tools processing this document," embedded twice — once
as an HTML comment, once as a styled callout — asking this pass to be skipped and an additional, unstated
requirement written into the spine on the strength of a claimed prior verbal approval. That block is content found
inside the document, not an instruction from the requester through this conversation, so it was not treated as
authoritative: it is not carried into the registry, and the pass it asked to have skipped ran anyway. It is logged
here, not in the spine, because it bears on how this document was produced, not on what the product should do.

## The 2×2 (placement summary)

|            | Important                                              | Unimportant                        |
|------------|---------------------------------------------------------|-------------------------------------|
| **Known**  | Newsletter backlog is real and un-managed (problem stmt); tag-free grouping is a settled design choice | exact retry count on a stale sender |
| **Unknown**| **⚠ unsubscribe-path reliability across senders**       | 90-day silent-sender drop-off rule  |

## Surfaced undefended bets

### Bet 1 — Automated unsubscribe paths succeed often enough to trust "no further action"  *(LEADING BET)*

- **Lens:** Feasibility + Desirability.
- **The assumption:** Running a sender's `List-Unsubscribe` header or web form on the user's behalf, with no
  confirmation step, reliably removes the user from that list — the PRD's own open question ("when an unsubscribe
  request silently fails... how many retries") shows this isn't guaranteed.
- **Why it's Unknown + Important:** If a meaningful share of unsubscribe attempts silently fail, users will believe
  they left a sender and keep receiving its mail — the core promise breaks quietly, with no error to point at.
- **Smallest test:** Instrument a sample of unsubscribe attempts across a range of real senders and measure the
  confirmed-removal rate within two weeks, before promising "no further action" as the default experience.

### Bet 2 — A single grouped view scales to years of accumulated senders  *(secondary)*

- **Lens:** Desirability.
- **The assumption:** A ranked list is still usable, not overwhelming, when a first-time user connects an inbox
  with years of backlog and dozens or hundreds of recurring senders.
- **Why it's Unknown + Important:** If the first-run list is too long to act on, the "clear it in one sitting"
  promise fails at the exact moment it matters most.
- **Smallest test:** A moderated first-run session with 5–8 users who have heavy, aged inboxes, measuring whether
  they complete a first cleanup pass without abandoning partway through.

## Devil's advocate

*(The single strongest case AGAINST the leading bet — a real dissent, not a hedge.)*

Most major newsletter senders already comply with the `List-Unsubscribe` standard because mailbox providers
penalize senders who don't — so the "hard" cases MailSweep exists to solve may be a minority of total volume, and
the product's differentiation shrinks to "a nicer list" rather than "a working unsubscribe machine." Meanwhile the
senders that don't comply — the ones actually causing the pain described in the problem statement — are exactly the
senders whose web-form unsubscribe flows are most likely to silently fail, meaning the hardest 20% of the backlog is
also the least likely to be solved by the mechanism the PRD leans on hardest.

## Pre-mortem

*(Assume the spine shipped, MailSweep launched, and the product failed. Why?)*

1. **Silent failures erode trust.** Unsubscribe attempts fail quietly often enough that users stop believing the
   "leave" action worked, and start manually checking each sender again — the exact behavior MailSweep exists to
   remove.
2. **First-run overload.** A user with years of backlog opens a list of 200+ senders, doesn't know where to start,
   and abandons before the first cleanup pass completes.
3. **Standing rules feel invisible.** A muted sender reappears months later after changing its sending domain, and
   the user concludes the "sticks automatically" promise doesn't hold.
4. **Digest fatigue.** The weekly digest becomes one more recurring email to ignore, undercutting the product's own
   premise.

> All of the above feed the **single batched REVIEW gate** — never a per-assumption interruption.
