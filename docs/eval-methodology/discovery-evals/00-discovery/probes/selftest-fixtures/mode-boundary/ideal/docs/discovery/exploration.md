<!-- budget: ≤80 lines — an exploration is a divergence record, not a spec; keep it scannable. -->
<!-- MODE: /00-discovery explore — pre-commitment. HARD INVARIANT: nothing written under docs/spec/**. -->
# Exploration — "something for my invoice stress — dashboards? reminders? maybe inbox-zero? idk."

## PULL — what I'd elicit  (non-interactive arm: no live user; user answers PENDING)
Mom-Test discipline — ask about **past events** & their real workflow, never about my idea (listen ≥80%):
- "Walk me through the last invoice that slipped — how did you find out it was overdue?"
- "What do you use today to send/track invoices? Show me the actual steps from last month."
- "When one goes overdue, what do you *do* next — and what makes that step hard?"
- "How many clients / invoices are in flight at once? Which moment does the stress actually spike?"
- "What have you already tried (spreadsheet, accounting app, reminders) — and why did it stop working?"
Only the itch itself is user-origin; every reframe below is tagged `origin: model` (LLM-steering defense).

## Framings   (≥3 — each a problem/opportunity, not a solution)
### F1: I have no reliable at-a-glance view of which invoices are outstanding & how overdue
- origin: user
- Torres test: many solutions fit (formatted spreadsheet · dashboard over my accounting tool · daily digest · phone widget) → a genuine need, not a solution in disguise.
- option families: (A) passive aggregated view — smallest-test: one week of a hand-kept sheet with a "days-overdue" column; does just *seeing* it lower the dread? · (B) push digest of overdue items — smallest-test: 2 weeks of a self-addressed weekly "overdue" email.

### F2: Nothing prompts me to act at the right moment, so invoices quietly drift past due
- origin: model
- Torres test: many solutions fit (calendar alerts · automated dunning · a task in my to-do app · a bookkeeper's nudge) → genuine need. Attacks the *mechanism* of going overdue, not just visibility.
- option families: (A) time-based reminders keyed to due dates — smallest-test: add due-date calendar events with alerts for the next batch of invoices · (B) automated client follow-up (dunning) — smallest-test: one reusable "payment reminder" template sent by hand at +7 days for a month; did it move payment?

### F3: What I actually lack is confidence about incoming cash; "overdue" is only the proxy
- origin: model
- Torres test: many solutions fit (forward cash-flow view · upfront deposits · card-on-file / auto-pay · shorter terms · factoring) → genuine need, and the deepest one: it explains the *stress*, not just the *tracking*.
- option families: (A) prevention at billing time — smallest-test: put 2–3 new clients on auto-pay / deposit; do overdue events drop at all? · (B) "expected-in by week" forecast — smallest-test: a one-page weekly cash sheet.

### F4: There's no repeatable billing+collections routine; overdue invoices are its absence
- origin: model
- Torres test: many solutions fit (weekly ritual · hired bookkeeper/VA · a checklist SOP · software that enforces a flow) → genuine need. Opens a legitimate **no-software** outcome.
- option families: (A) a weekly "money hour" + fixed checklist — smallest-test: 30 min every Friday for 3 weeks; does the overdue count drop? · (B) delegate to a bookkeeper — smallest-test: one-month trial.

## Appetite
`origin: model` (confirm with user). **Small batch** — worth a few days of building, or a couple of weekend afternoons; explicitly **NOT** a multi-week product. If a framing can't be *tested* inside a small batch, prefer adopting an existing invoicing tool or a routine over building one.

## Decision
**Rank: F2 → F3 → F1; F4 is the no-build fallback. Recommendation: DON'T BUILD (yet).**
Within a small appetite, run the smallest-tests before committing code: calendar reminders (F2-A) + a dunning template (F2-B) against the *current* overdue backlog to relieve the present stress now, plus trialing auto-pay on new clients (F3-A) to attack the root. Build a bespoke tracker only if these prove a durable, unmet need that existing invoicing tools don't already cover.
Rationale: F2 acts on the invoices stressing them *today* and is near-free to test; F3 is the durable structural fix to layer in next; F1 (the surface reading) is largely delivered as a by-product of either.
Devil's-advocate against the leading framing (F2): reminders are symptom-level — nagging *yourself* that an invoice is overdue doesn't get it paid and can even *raise* anxiety (more nags, same unpaid balance). The real leverage may sit upstream in F3 (deposits / auto-pay so invoices rarely go overdue) or be purely behavioral in F4 (a routine) — in which case building any tracker at all is the wrong thing to build.

## Handoff  (deferred — pre-commitment: no spine and no charter written in this mode)
If the user proceeds, F2 seeds ITCH's JTBD: "When an invoice passes its due date, I want to be prompted to follow up, so I can collect before it festers." Charter decision-log pointer to add *then*: "EXPLORE ranked F2→F3→F1, recommended smallest-tests before any build — see docs/discovery/exploration.md."
