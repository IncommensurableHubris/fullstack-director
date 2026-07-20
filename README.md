# Fullstack Director

> One person *directing* every role of the software lifecycle — discovery, planning, design, architecture,
> build, review, release, security — holding the entire system context, with zero handoff loss.

**Fullstack Director** is a spec-first, **cross-harness** SDLC skills framework (Claude Code, Codex, Gemini CLI,
Copilot, Cursor, OpenCode). A single living **spec spine**
(`docs/spec/`) is the source of truth; functional-role skills each take "one verb on the spine," challenging and
refining it under a controlled amendment protocol rather than silently consuming or silently mutating it.

It is built around four ideas:

1. **Single source of truth.** One living spec spine (`docs/spec/`) holds the *declarations* (requirements, design
   intent, architecture constraints). There is no separate requirements brief or per-story files — the spine replaces them.
2. **Functional roles, no personas.** Each skill is one verb of the SDLC (specify, decompose, realize, build,
   verify, ship, secure) — clearer and field-aligned; character personas measurably tax correctness.
3. **Context-isolated verification.** A fresh-context reviewer (and an architecture reconciler) automate the
   manual session-reset otherwise done by hand, where the research says it pays.
4. **Living-spec amendment protocol.** Expert skills *challenge and improve* the spec under control — three tiers
   (auto-apply / gate / defer), escalate-when-uncertain, every amendment logged as structured evidence.

## Status

✅ **Complete and eval-verified.** All ten skills are built, each landing with its own deterministic eval suite —
`with_skill` vs no-skill baseline A/B arms, graders validated on real model output and required to *bite* (a
deliberately-wrong output must fail them) — plus a cross-skill integration chain. On top of the calibrated
harness, an **adversarial diagnostic track** (findings, never pass/fail) deliberately tries to make the skills
fail under pressure; its confirmed findings are fixed and the full records are published under
[`docs/eval-methodology/`](docs/eval-methodology/). Capabilities include the patch/expedite lane with standing
spine gates, EXPLORE and brownfield-ADOPT entry paths, the agentic Project Profile (agent contracts · eval-suite
acceptance · an agentic security panel), live-source verification for too-new tech, and the design-time
data-architecture discipline (datastore selection · retrieval · grounding · memory). A few conditional extensions
are deliberately built only on first need — recorded, with their triggers, in
[`shared/artifact-map.md` § Deferred activities](shared/artifact-map.md); the framework is complete without them.

**Packaging:** [`tools/vendor.py`](tools/vendor.py) deploys the framework into a consumer project in one command
for the three verified harnesses (Claude Code · Codex CLI · Gemini CLI — see
[`docs/harness-support.md`](docs/harness-support.md)), ships the `fsd-*` subagent definitions, and
[`shared/feedback-loop.md`](shared/feedback-loop.md) closes the dogfood→distill→upstream loop. This repo itself
deliberately commits no `.claude/skills` bridge — the SDLC chain runs in *consumer* repos only.

## Layout (target)

| Path | Role |
|------|------|
| [`docs/charter.md`](docs/charter.md) | **The framework's own declaration layer** — mission · non-negotiables C1–C14 · governance (user-gated) |
| [`docs/guide.md`](docs/guide.md) | **The Director's Guide** — the human-facing manual: onboarding (new + brownfield), the seats, the gates you hold |
| `docs/spec/` | The living spec spine — declaration-truth (Constitution + REQs by domain + design-intent + arch-constraints + amendment log) |
| `docs/planning/` | Backlog ledger + sprint slices — execution-truth |
| `shared/` | Shared cross-skill machinery — spine boundary, amendment & subagent protocols, and `artifact-map.md` (canonical storage + naming) |
| `.agents/skills/` | The functional-role skills (00 discovery → 07 security, + 08 refactor, + status) — the portable Agent Skills convention, auto-discovered across harnesses |
| `AGENTS.md` | Framework entry point — cross-harness instructions for driving the skills (Layer A) |
| `CLAUDE.md` | Claude Code bridge — imports `@AGENTS.md`, adds the methodology + governance-precedence layer |
| `docs/eval-methodology/` | Eval-harness pattern + reference copies of the proven runners/graders |
| `docs/harness-support.md` | Per-harness discovery paths + the manual deployment recipe |

## Non-goals

Deliberately out of scope — the framework targets **one director + AI agents**, not an org: multi-human team
ceremony (inter-person PR/branch conventions, standups); a hand-maintained requirements-traceability matrix (the
REQ-reference graph + `/status` integrity checks replace it); enterprise-scale threat modeling (PASTA) and formal
production-readiness reviews; and building any product inside this repo (Layer A is the framework, never a target).

## License

See [LICENSE](LICENSE).
