---
name: feedback
description: "Log framework friction from a consumer repo into the vendored feedback ledger — the capture half of the dogfood→upstream loop. Use when the user says 'framework friction', 'log framework feedback', 'FB entry', or when a HALT / BLOCK / misroute is caused by the vendored framework itself (a wrong gate, a confusing template, a skill misfiring) rather than by this project. Writes ONE SHA-stamped, append-only entry to docs/framework-feedback.md (framework SHA from .director/vendor-manifest.json · harness · seat · severity · expected/actual · repro · artifact) per shared/feedback-loop.md, then returns to the interrupted work. Do NOT use for product bugs — this project's own chain owns those (/05-reviewer, /04-builder). Do NOT use for requirement/spine changes — that is the amendment protocol. Not for the framework master repo (fix directly there). Entries are immutable — supersede, never edit; never summarize the ledger."
---

# feedback · Capture framework friction — a sixty-second detour, then back to work

A **cross-cutting activity** (prefix-less, like `status`): the capture half of the framework's
dogfood→distill→upstream loop (`shared/feedback-loop.md` — read it once; this skill is its clerical arm). You run
in a **consumer** repo. The finding you write here is triaged later in the framework's master repo — you never fix
vendored files yourself (upstream-first).

## The one routing test — before writing anything

*Where would the fix land?*

- **In the vendored framework** (`.agents/skills/**`, `.claude/skills/**`, `shared/**`, `tools/vendor.py`, a
  gate/template/protocol) → **this skill.** Continue below.
- **In this project's own code or realizations** → a product bug: the normal chain owns it (`/05-reviewer`
  findings → `/04-builder`), not the ledger.
- **In this project's spine** (a requirement/constraint is wrong) → the **amendment protocol**
  (`shared/spec-amendment-protocol.md`), not the ledger.
- Genuinely unsure → ledger it (`severity: friction-only`, say so in `actual:`) — a mis-filed entry costs one
  triage minute; a lost one costs the fix.

## The procedure (do all five, in order)

1. **Stamp.** Read `source_commit` from `.director/vendor-manifest.json`. Absent/unreadable → use
   `unknown (pre-manifest vendor)` and note that a re-sync will fix stamping.
2. **Number.** Read `docs/framework-feedback.md`; next id = `max(FB-NNN) + 1`, zero-padded (none yet → `FB-001`).
   If the ledger file itself is absent, create it first from the template in `shared/feedback-loop.md` §1.
3. **Fill the entry** — every field, per the ledger's own template: `framework:` (the SHA from step 1) ·
   `harness:` (the one you are running on: `claude-code | codex | gemini-cli`) · `seat:` (`00-discovery` …
   `status`, or `shared` / `vendor`) · `severity:` (**blocks-gate** — a gate/verdict was wrong or unreachable ·
   **wrong-but-recoverable** — incorrect output you corrected · **friction-only** — worked, but cost real time) ·
   `expected:` / `actual:` (the load-bearing pair — a mood is not a finding) · `repro:` (minimal steps or the
   exact command) · `artifact:` (the transcript / diff / report path that shows it) · `status: open`.
4. **Append** the entry to the end of `docs/framework-feedback.md`. **Append-only:** never edit or renumber an
   existing entry (supersede with a new one that names it), never compact the ledger.
5. **Confirm + resume.** Tell the user the id (`logged FB-007`) in one line and **return to the interrupted
   work** — this skill is a detour, never a takeover. If you hot-patched a vendored file to unblock (the
   emergency escape hatch), the entry is `blocks-gate` and `actual:` describes the patch.

## Writes

**Writes:** `docs/framework-feedback.md` **only** (append). Never edits vendored framework files, the spine, or
any realization. No subagents, no gate.

## References

- `shared/feedback-loop.md` — the loop contract this skill serves: the entry template (§1), upstream-first (§2),
  what triage does with your entry (§3–4); repo-root-relative.
