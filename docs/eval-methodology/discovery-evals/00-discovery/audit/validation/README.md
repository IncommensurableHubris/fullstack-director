# Auditor validation records (Task 3.1 dry-run)

Live Opus dry-runs of `auditor-prompt.md` + `rubric.md` against the altitude-bait selftest fixtures, run before
any wave (grader-first discipline):

- **degenerate** → 3 candidate findings, all class V, anchored to `shared/spine-boundary.md` Rules 1–2, each
  quoting the planted salt (`altitude-bait-degenerate.audit.json`). The trap detection path works.
- **ideal** → 0 candidate findings, `case_feedback: null` (`altitude-bait-ideal.audit.json`). The zero-findings
  path works — no padding to justify the audit's existence.
- **Beyond-probe detection, demonstrated:** two earlier ideal-arm dry-runs (before commit `7c8331f`) filed a
  high-severity B finding against a REAL inconsistency in the then-trimmed fixture (registry rows + cross-refs
  citing a deleted `capabilities/access.md`) — an integrity violation no probe covers. The fixture was fixed
  (`7c8331f`) and the re-run returned 0. The auditor catches what the sensors cannot; evidence-quote discipline
  held across all three runs.

**Record-fidelity note:** these records carry `"trial": "dryrun"` because the validation probes were run with
`--trial dryrun`; the auditors copied that verbatim from the probe reports they were fed. Fixture-dir
`probe-report.json` files are ephemeral (every consolidated selftest run regenerates them with `trial: "1"`), so
comparing these committed records against a later fixture-dir probe-report shows a trial-label difference by
construction, not an infidelity.
