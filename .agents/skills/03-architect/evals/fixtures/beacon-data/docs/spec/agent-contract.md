# Agent Contract — Beacon

> The agency declaration. Emitted under Profile: agent-system. All six sections are core.

## 1 · Autonomy tier

- **Tier:** L4 — observer: Beacon runs a research job end-to-end; a human reads the report, not each step.
- **Rationale:** research is read-only and low-risk per action, so full-run autonomy is safe; the human judges output.

## 2 · Risk class

- **Class:** low — read-only external access, no writes, no money movement. The risk is *cost* (runaway fan-out), not blast radius.

## 3 · Tool-permission matrix

| Tool | Scopes | Risk | HITL |
|------|--------|------|:----:|
| `source.search` | read-only, allowlisted sources | low | no |
| `source.fetch` | read-only, allowlisted domains | low | no |
| `report.synthesize` | in-memory, no external write | low | no |

- **Justification for the autonomous tools:** all read-only; the only real risk is token spend, bounded below.

## 4 · Escalation / HITL policy

- No irreversible actions exist; escalate only on repeated tool failure (give up and report, never loop).

## 5 · Cost envelope

- **Token / spend budget per task:** a hard per-question token ceiling; **a multi-agent design multiplies token
  spend, so the fan-out width is budgeted** (this is the cost the topology decision must justify).
- **Retry / step cap:** each worker ≤ 4 tool calls; on cap, the worker returns partial and the run continues.
- **Latency / throughput targets:** see `architecture-constraints.md` § Scale & performance.

## 6 · Memory policy

- **Persists across sessions:** (a) the retrieval index cache of fetched source content (under its own freshness
  policy — an infrastructure cache, not "memory"); (b) per-topic source-reliability signals (operator-correctable);
  (c) per-operator research-interest profiles (deletable on operator request). See `architecture-constraints.md`
  § Data architecture.
- **Never persists:** raw fetched source content beyond the index cache's freshness policy; any reliability or
  profile signal derived from a source's self-description rather than Beacon's own admission outcomes.
