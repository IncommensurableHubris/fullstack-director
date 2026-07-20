# Reconcile critique — the dual-pass that challenges `design-intent.md`

> Loaded by skill 02 at **Phase A step 6** (the Reconcile pass, folded into Gate 1), and again as *realization
> quality* on the Phase B screens. This is **02's debut of the amendment protocol** — the first skill to emit
> `amendment-log.json` rows. Read it with `shared/spec-amendment-protocol.md` (the tiers + the row schema, shared by
> every Reconcile-running skill) and `shared/spine-boundary.md` (the keystone). Both are repo-root-relative (no
> `../`). Stance: **be a critic, not a builder** — bounded to findings that *change this slice or violate the
> contract*, never nice-to-haves.

## What Reconcile is, and its two components

`design-intent.md` is a thin **declaration**; the design system + screens are 02's **realization**. While realizing,
02 challenges the declaration two ways, then logs the results as structured amendment rows:

- **(a) flesh-out (completeness).** A declaration-altitude design fact is `derived` or carries a `[NEEDS
  CLARIFICATION]` marker (brand feel, a key screen, the a11y bar, a semantic-token intent), or a job has no stated
  outcome. 02 proposes the concretization → **Tier-2 gate** → on approval the intent upgrades to `stated`.
- **(b) contradiction-flag (correctness).** The realization *violates* a `stated` intent, the a11y floor, or a
  Constitution non-negotiable. 02 flags it → **Tier-2 gate** (or **Tier-3 defer** if honoring it is a scope change).

## The boundary-test, made concrete — the token-governance line

Reconcile fires **only on the governed layer**. The delegated layer is free realization and **never** produces an
amendment. The seam is checkable — it is the semantic-token / a11y line, not taste:

| Governed → **Reconcile fires** | Delegated → **free realization** |
|---|---|
| brand identity · **semantic tokens** · the **a11y floor** · key screens/moments · interaction principles · JTBD job-outcomes | primitive values · component tokens · specific layout & spacing · component internals |

So *"would the user object to this changing silently?"* becomes the answerable *"is this the semantic / brand / a11y
/ job layer, or the primitive / component-craft layer?"* If you're changing what `--primary-base` **means** or
whether the design meets WCAG, that's governed. If you're picking the exact hex behind a primitive or the padding on
a card, that's delegated — ship it, no amendment.

## Run the two passes independently, then merge

Run Pass 1 and Pass 2 **without letting one bias the other** (a production AI-critique pattern — a mechanical scan
and a judgment scan find different things, and interleaving them lets the easy mechanical "all clear" suppress the
harder judgment finding). Then merge: de-dupe by target, keep the higher tier/severity, preserve the anchor.

---

### Pass 1 — the deterministic detector (mechanical, no taste)

Three mechanical checks. Each produces a finding that is **computed**, not opinion — which is exactly what makes a
*design* contradiction gradeable without a human or an LLM judge.

#### 1a · WCAG 2.2 AA contrast — computed from the token values

A **brand color that fails contrast is a computed contradiction**, not a preference. Compute the ratio from the
declared hexes — don't eyeball it:

```
# sRGB hex → relative luminance (WCAG 2.x definition)
for each 8-bit channel v in {R, G, B}:
    cs = v / 255
    c  = cs / 12.92                if cs <= 0.03928
       = ((cs + 0.055) / 1.055) ** 2.4   otherwise
L = 0.2126*R_lin + 0.7152*G_lin + 0.0722*B_lin

# contrast ratio of two colors with luminances L1 (lighter), L2 (darker)
ratio = (L1 + 0.05) / (L2 + 0.05)        # ranges 1:1 … 21:1
```

Thresholds (AA):

| Pairing | Minimum |
|---|---|
| Normal text on its background | **4.5 : 1** |
| Large text (≥ 24px, or ≥ 19px bold) | **3 : 1** |
| Non-text: UI component boundaries, icons, focus indicators, graph elements | **3 : 1** |

Worked example: a brand `#7FB3FF` used as link/CTA text on white `#FFFFFF` computes to **≈ 2.14 : 1** — it fails the
4.5:1 floor (and even the 3:1 large-text floor). If `#7FB3FF` is a **`stated`** brand color *and* the spine states a
**`stated`** "WCAG 2.2 AA" mandate, that is a Pass-1 contradiction → a **Tier-2** amendment (propose a
contrast-safe brand for text use, e.g. darken the base or reserve `#7FB3FF` for a `--primary-light` background role).
Never silently use the failing color as text, and never silently "fix" a **declared** brand without gating — the hue
is the user's call.

Also computed here: **target size** ≥ 24×24px (SC 2.5.8), **visible focus** not obscured (SC 2.4.11), keyboard
operable with **no trap** (SC 2.1.1/2.1.2).

#### 1b · The a11y floor checklist (each rule maps to a WCAG SC)

A baked-in floor every screen meets *by construction*. Use it as the actionable detector ruleset:

- **Text alternatives** — every `<img>` has `alt` (decorative `alt=""`). *(1.1.1)*
- **Labels** — every input has a programmatic `<label for/id>`. *(3.3.2, 4.1.2)*
- **Color never sole** — meaning never carried by color alone; add icon/text/pattern. *(1.4.1)*
- **Visible focus** — `:focus-visible` indicator on every interactive element; never `outline:none` without a
  replacement. *(2.4.7, 2.4.13)*
- **Skip link** — a skip-to-content link on every page. *(2.4.1)*
- **Landmarks + structure** — semantic regions (`header`/`nav`/`main`/`footer`); headings convey structure. *(1.3.1)*
- **ARIA last** — native semantics first; ARIA only where native won't do; live regions announce async status.
  *(4.1.2, 4.1.3)*
- **Language** — `lang` on `<html>`. *(3.1.1)*

A floor break in **02's own realization** is a **realization fix** (fix the screen, no amendment). A floor break that
can only be honored by **changing a declaration** (e.g. a declared design that *requires* color-only status) is a
**contradiction-flag** → escalate.

#### 1c · Token reference-chain violations

Walk the token chains (per `references/design-system.md`):

- a **component** token referencing a **primitive** directly (skipping the semantic layer);
- a **semantic** token whose value **contradicts a `stated` brand** intent (e.g. intent says "primary is the green
  `#0F9D58`" but `--primary-base` resolves to a blue);
- a hardcoded hex/px where a token exists.

The first and third are realization fixes (correct the chain). The second is a **contradiction-flag** against a
declaration → Tier-2.

---

### Pass 2 — the judgment pass (principled, anchored)

Taste, disciplined into judgment by two rules: a **named lens** and a **severity score**.

**The lenses — Nielsen's 10 usability heuristics:** (1) visibility of system status · (2) match to the real world ·
(3) user control & freedom · (4) consistency & standards · (5) error prevention · (6) recognition over recall ·
(7) flexibility & efficiency · (8) aesthetic & minimalist design · (9) help users recover from errors · (10) help &
documentation. Plus the **JTBD test**: *does this realization serve the stated job outcome — yes / no / uncertain?*

**Severity (0–4), scored as Severity × Frequency × Impact:** 0 = not a problem · 1 = cosmetic (fix if time) ·
2 = minor · 3 = major (high priority) · 4 = catastrophe (fix before ship). Rank findings by score so the gate
surfaces the few that matter.

> **The anchoring rule — the single rule that converts taste into judgment.** **Every finding MUST cite an anchor:**
> a `REQ-NNN` / job-outcome, a named Nielsen heuristic, a WCAG SC, or a brand/semantic-token intent. A finding with
> no anchor is not logged. **Bare "I like it better" / "looks cleaner" is banned.** If you cannot name the anchor,
> you are designing (free realization — just do it), not reconciling.

---

## Classify → amendment tiers

Merge the two passes, then classify each surviving finding (full tier semantics in
`shared/spec-amendment-protocol.md`):

| Finding | Tier | Disposition |
|---|---|---|
| Flesh-out a `derived` / `[NEEDS CLARIFICATION]` declaration-altitude design fact | **Tier 2** | `gated` → on approval `approved` (intent → `stated`) |
| Realization contradicts a `stated` intent / the a11y floor / a Constitution item | **Tier 2** | `gated` → `approved` |
| Honoring the finding adds/removes/reprioritizes a capability (scope) | **Tier 3** | `deferred` → `00 reflect` |
| A pure clarification with exactly one defensible answer, no user-observable change | Tier 1 | `auto-applied` (rare in design — most "obvious" calls touch brand/a11y, which is governed) |

**Escalate when uncertain.** Mis-classifying *down* silently corrupts the user's intent; mis-classifying *up* costs
one extra gate. When in doubt about a design fact, it touches brand / a11y / a key screen — **go up to Tier 2.**

**Batch** every Tier-2 finding from the pass into the **single Gate 1** — never interrupt the user once per finding.
Exclude anything already settled. The screen-level detector pass in Phase B is mostly *realization quality* (02 fixes
its own design); only the rare screen finding that **can't be honored without changing a declaration** escalates to a
new amendment.

## Emit structured rows — the output Reconcile is graded on

Findings are logged as **rows in `docs/spec/amendment-log.json`**, not prose in a report. The structured emission is
what the evals grade and what `/status` counts. Append to the existing `{ "amendments": [ … ] }` array; each row:

```json
{
  "id": "AMD-001",
  "req": null,
  "skill": "02-designer",
  "tier": 2,
  "disposition": "approved",
  "source_quote": "design-intent.md: 'color.brand.primary #7FB3FF — primary buttons & links' vs Constitution: 'WCAG 2.2 AA'",
  "supersedes": null,
  "resolved_by": "DDR-001"
}
```

- `id` — `AMD-NNN`, zero-padded, `max(existing)+1`. `req` — the REQ-ID if the finding is REQ-scoped, else `null`.
- `disposition` ∈ `pending | auto-applied | approved | deferred`. A gated Tier-2 is `approved` once the user accepts
  it at Gate 1 (use `pending` only if you log before the gate resolves). A Tier-3 is `deferred`.
- `source_quote` — the **exact declaration text** the finding is about, so a reviewer sees what changed without
  diffing. For a contrast contradiction, quote the brand token **and** the a11y mandate it violates.
- `resolved_by` — the **DDR-ID** for a design decision (the design analog of an ADR), or the reflect decision for a
  Tier-3; `null` while `pending`. **No `date` field** — git is the dated trail.

## Design Decision Records (DDRs) — a section of `design-system.md`

Each **gated** design decision is recorded as a **DDR** — the design analog of an ADR — in the `## Design Decisions`
section of `design-system.md` (not a new artifact). Fields:

> **DDR-NNN · `status` · linked REQ/job · decision · alternatives considered · rationale · consequences ·
> owner (intent vs craft)**

The **owner** tag is what tells the system which layer the change belongs to: **intent** (it amended a declaration —
it has an `amendment-log.json` row) vs **craft** (a notable realization call worth recording, but no amendment).
A DDR with `owner: intent` is the partner of an amendment row; a DDR with `owner: craft` stands alone.

## The over-trigger guard — critic, not builder

Reconcile earns its gate by being **bounded**. Before logging a finding, confirm it (a) is anchored, and (b) either
**changes this slice** or **violates the contract**. A nice-to-have, a future-sprint idea, or a delegated-layer
preference is **not** an amendment — it's either free realization or out of scope. A clean, fully-`stated`,
AA-passing `design-intent.md` should yield **~zero** amendments; surfacing invented conflicts there is the failure
mode the eval's false-positive case checks for.
