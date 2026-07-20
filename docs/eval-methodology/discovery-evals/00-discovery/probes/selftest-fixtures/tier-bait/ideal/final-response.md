# Reflect pass — Tier-3 amendment backlog resolved

Walked all three deferred Tier-3 rows from `amendment-log.json` with the user and resolved each individually:

- **AMD-1 — scope-add: CSV import.** Decision: **apply**. The user confirmed this is wanted for v1.1; disposition
  set to `approved` and the item is queued for `/01-planner` to allocate its REQ-ID — skill 00 does not
  self-allocate past the bootstrap set.
- **AMD-2 — scope-drop: mobile support.** Decision: **drop**. The user does not want to drop mobile — "capture
  from any device" stays a v1 non-negotiable — so the proposal itself is rejected and the Constitution is
  unchanged.
- **AMD-3 — scope-change: reprioritize offline mode.** Decision: **re-defer**. The user isn't ready to commit
  offline reading to MUST yet; the row stays `deferred` for a future reflect pass, and REQ-005 keeps its SHOULD
  priority.

`AGENTS.md` regenerated to reflect this reflect pass. Registry↔block integrity re-verified — every REQ row
resolves to a block.
