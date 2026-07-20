#!/usr/bin/env python3
"""Spine integrity gate — mechanical checks over `docs/spec/` (the spec spine).

Emitted into the project by discovery at WRITE SPINE so the spine's integrity rules hold on every
commit and in CI, not only while a skill is running. Wire-up samples (pre-commit, GitHub Actions)
are documented in `docs/README.md`; this script is the contract.

    python scripts/verify-spine.py [--json] [--hash] [--root PATH]

Exit 0 = pass (warnings allowed) · 1 = any FAIL-severity check failed.
`--json` prints exactly: {"result": "PASS|FAIL", "checks": [{"id", "severity", "ok", "detail"}]}
`--hash` prints a sha256 over docs/spec/** (sorted relative-path + bytes) — the spine's release identity — and
exits 0 (with `--json`: {"spine_hash": "..."}). 06 stamps it into the release report's Provenance block (D7).

Checks (registered below; adding one = a @register_check function, nothing else):
  FAIL  L1_registry_file_resolves   every REQ-registry row's File resolves on disk
  FAIL  L2_leaf_contains_block      that file holds the delimited `### REQ-NNN:` ... `<!-- /REQ-NNN -->` block
  FAIL  L3_no_orphan_blocks         no capability block lacks a registry row
  FAIL  L4_no_duplicate_req_ids     every REQ id appears exactly once (registry and blocks)
  FAIL  L5_amendment_log_valid      amendment-log.json parses; every row carries exactly the frozen schema keys
  FAIL  L6_dataset_refs_resolve     every REQ eval-block `dataset:` path resolves on disk (in-spine golden datasets)
  FAIL  L7_verify_live_records      every declared verify-live tech has a cited docs/verification/<tech>.md; no orphan record; no uncited claim
  WARN  W1_surviving_markers        [NEEDS CLARIFICATION ...] markers (legitimate pre-release, so WARN)
  WARN  W2_ledger_registry_sync     backlog ledger REQ set == registry set, exactly once each (when ledger exists)
  WARN  W3_id_zero_padding          TYPE-NNN ids are zero-padded to three digits
  WARN  W4_profile_missing          specification.md declares a known `- **Profile:**` field (absent ⇒ webapp, so WARN)
  WARN  W5_spine_density            spine prose lines per REQ stay under 40 (excluding evals/**) — terseness

Stdlib only, Python 3.8+.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

FROZEN_AMENDMENT_KEYS = {"id", "req", "skill", "tier", "disposition", "source_quote", "supersedes", "resolved_by"}

# WS3 project profiles (v1). Absent ⇒ webapp (backward compatible). See shared/agentic-profile.md.
KNOWN_PROFILES = ("webapp", "agent-system", "mcp-server", "skill-pack")

CHECKS = []  # (check_id, severity, fn) where fn(spine) -> (ok, detail); severity in {"FAIL", "WARN"}


def register_check(check_id, severity):
    def deco(fn):
        CHECKS.append((check_id, severity, fn))
        return fn
    return deco


def read(path):
    return path.read_text(encoding="utf-8")


class Spine:
    """One parse of the spine; every check reads from here."""

    def __init__(self, root):
        self.root = root
        self.spec_dir = root / "docs" / "spec"
        self.spec_path = self.spec_dir / "specification.md"
        self.spec_text = read(self.spec_path) if self.spec_path.is_file() else None

        # Project profile (WS3): the `- **Profile:** <value>` field, above the Constitution. Absent ⇒ webapp.
        self.profile = None
        if self.spec_text:
            pm = re.search(r"(?im)^\s*-\s*\*\*Profile:\*\*\s*`?([A-Za-z][A-Za-z-]*)`?", self.spec_text)
            self.profile = pm.group(1) if pm else None

        # REQ registry rows: (req_id, file_cell) in row order.
        self.registry = []
        if self.spec_text:
            for line in self.spec_text.splitlines():
                m = re.match(r"^\|\s*`?\*{0,2}(REQ-\d+)\*{0,2}`?\s*\|", line)
                if m:
                    cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
                    self.registry.append((m.group(1), cells[-1]))

        # Delimited blocks in capability leaves: file -> (heading ids, closing-delimiter ids).
        self.cap_blocks = {}
        cap_dir = self.spec_dir / "capabilities"
        for p in sorted(cap_dir.glob("*.md")) if cap_dir.is_dir() else []:
            text = read(p)
            self.cap_blocks[p] = (re.findall(r"(?m)^###\s+(REQ-\d+)\b", text),
                                  re.findall(r"<!--\s*/(REQ-\d+)\s*-->", text))

        # Amendment log: parse error message, or the rows.
        self.log_path = self.spec_dir / "amendment-log.json"
        self.log_rows, self.log_error = None, None
        if not self.log_path.is_file():
            self.log_error = "amendment-log.json not found"
        else:
            try:
                data = json.loads(read(self.log_path))
                if not isinstance(data, dict) or not isinstance(data.get("amendments"), list):
                    self.log_error = 'top level must be an object with an "amendments" array'
                else:
                    self.log_rows = data["amendments"]
            except json.JSONDecodeError as e:
                self.log_error = "not valid JSON (%s)" % e

        # Execution ledger (owned by the planner; absent pre-decomposition).
        self.ledger_path = root / "docs" / "planning" / "backlog.md"
        self.ledger_ids = None
        if self.ledger_path.is_file():
            self.ledger_ids = re.findall(r"(?m)^\|\s*(REQ-\d+)\s*\|", read(self.ledger_path))

        self.spec_md_files = sorted(self.spec_dir.rglob("*.md")) if self.spec_dir.is_dir() else []

        # Verify-live declarations (WS6): the `## Verify-live` section of architecture-constraints.md. Each row
        # `- **<tech>:** docs: <url> · source: <repo>` names a tech whose record basename is `<tech>`. Absent
        # section ⇒ no declared techs (the webapp default). See shared/live-source-verification.md.
        self.verify_live_techs = set()
        ac_path = self.spec_dir / "architecture-constraints.md"
        if ac_path.is_file():
            m = re.search(r"(?ims)^##\s+Verify-live\b.*?(?=^##\s|\Z)", read(ac_path))
            if m:
                for line in m.group(0).splitlines():
                    tm = re.match(r"^\s*-\s*\*\*([A-Za-z0-9][\w.-]*?):\*\*", line)
                    if tm:
                        self.verify_live_techs.add(tm.group(1))

        # Verification records (WS6): docs/verification/<tech>.md — a realization ledger OUTSIDE docs/spec (so it
        # is excluded from spine_hash and a patch may update it). Parse each record's `## Verified claims` table
        # into (claim, citation) rows; an empty citation cell is an unverified claim (L7).
        self.verification_records = {}   # tech -> (path, [(claim, citation), ...])
        vdir = self.root / "docs" / "verification"
        for p in sorted(vdir.glob("*.md")) if vdir.is_dir() else []:
            sec = re.search(r"(?ims)^##\s+Verified\s+claims\b.*?(?=^##\s|\Z)", read(p))
            rows = []
            for line in (sec.group(0).splitlines() if sec else []):
                if not line.strip().startswith("|"):
                    continue
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cells) < 2:
                    continue
                if set("".join(cells)) <= set("-: "):                       # separator row
                    continue
                if cells[0].lower().startswith("claim") and cells[1].lower().startswith("citation"):
                    continue                                                # header row
                rows.append((cells[0], cells[1]))
            self.verification_records[p.stem] = (p, rows)

    def rel(self, path):
        return path.relative_to(self.root).as_posix()


@register_check("L1_registry_file_resolves", "FAIL")
def l1_registry_file_resolves(s):
    if s.spec_text is None:
        return False, "docs/spec/specification.md not found"
    if not s.registry:
        return False, "no `| REQ-NNN |` registry rows found in specification.md"
    missing = sorted({f for _r, f in s.registry if not (s.spec_dir / f).is_file()})
    if missing:
        return False, "unresolvable File cells: %s" % ", ".join(missing)
    return True, "%d registry rows; every File resolves" % len(s.registry)


@register_check("L2_leaf_contains_block", "FAIL")
def l2_leaf_contains_block(s):
    broken = []
    for req, f in s.registry:
        path = s.spec_dir / f
        if not path.is_file():
            continue  # unresolvable file is L1's finding
        text = read(path)
        has_heading = re.search(r"(?m)^###\s+%s\b" % re.escape(req), text)
        has_closer = re.search(r"<!--\s*/%s\s*-->" % re.escape(req), text)
        if not (has_heading and has_closer):
            broken.append("%s in %s (%s)" % (req, f, "no heading" if not has_heading else "no closing delimiter"))
    if broken:
        return False, "blocks missing or undelimited: %s" % "; ".join(broken)
    return True, "every registered REQ has its delimited block"


@register_check("L3_no_orphan_blocks", "FAIL")
def l3_no_orphan_blocks(s):
    registered = {r for r, _f in s.registry}
    orphans = []
    for path, (headings, closers) in s.cap_blocks.items():
        for req in sorted(set(headings) | set(closers)):
            if req not in registered:
                orphans.append("%s in %s" % (req, s.rel(path)))
    if orphans:
        return False, "blocks without a registry row: %s" % "; ".join(orphans)
    return True, "no orphan blocks in capabilities/"


@register_check("L4_no_duplicate_req_ids", "FAIL")
def l4_no_duplicate_req_ids(s):
    dupes = []
    reg_ids = [r for r, _f in s.registry]
    dupes += ["%s x%d in the registry" % (r, reg_ids.count(r)) for r in sorted(set(r for r in reg_ids if reg_ids.count(r) > 1))]
    headings = [(req, path) for path, (hs, _cs) in s.cap_blocks.items() for req in hs]
    all_heads = [req for req, _p in headings]
    for req in sorted(set(r for r in all_heads if all_heads.count(r) > 1)):
        dupes.append("%s block defined %d times (%s)" % (
            req, all_heads.count(req), ", ".join(s.rel(p) for r, p in headings if r == req)))
    if dupes:
        return False, "; ".join(dupes)
    return True, "every REQ id appears exactly once"


@register_check("L5_amendment_log_valid", "FAIL")
def l5_amendment_log_valid(s):
    if s.log_error:
        return False, s.log_error
    bad = []
    for i, row in enumerate(s.log_rows):
        if not isinstance(row, dict):
            bad.append("row %d is not an object" % i)
            continue
        keys = set(row)
        extra, absent = keys - FROZEN_AMENDMENT_KEYS, FROZEN_AMENDMENT_KEYS - keys
        if extra or absent:
            bad.append("%s: %s" % (row.get("id", "row %d" % i),
                                   " ".join(filter(None, ["extra keys %s" % sorted(extra) if extra else "",
                                                          "missing keys %s" % sorted(absent) if absent else ""]))))
    if bad:
        return False, "frozen-schema violations: %s" % "; ".join(bad)
    return True, "%d amendment rows, frozen schema holds" % len(s.log_rows)


@register_check("L6_dataset_refs_resolve", "FAIL")
def l6_dataset_refs_resolve(s):
    # Eval-suite acceptance (WS3): a REQ's `dataset:` path is an in-spine golden dataset — it must resolve, same
    # discipline as registry↔leaf (L1). Scan spec prose (never the datasets themselves) for `dataset:` refs.
    refs = []  # (source_file, dataset_path)
    for p in s.spec_md_files:
        if "evals" in p.relative_to(s.spec_dir).parts:   # only docs/spec/evals/** — not an "evals" ancestor of the root
            continue
        for m in re.finditer(r"(?im)^\s*dataset:\s*`?([^\s()`]+)", read(p)):
            refs.append((s.rel(p), m.group(1)))
    if not refs:
        return True, "no eval-suite dataset refs — nothing to resolve"
    missing = sorted({d for _f, d in refs if not (s.root / d).is_file()})
    if missing:
        return False, "unresolvable eval dataset refs: %s" % ", ".join(missing)
    return True, "%d eval dataset ref(s); every one resolves" % len(refs)


@register_check("L7_verify_live_records", "FAIL")
def l7_verify_live_records(s):
    # Live-source verification (WS6): the confabulation guardrail's standing gate. Bidirectional + citation —
    #   (a) every spine-declared verify-live tech has a resolving docs/verification/<tech>.md,
    #   (b) no orphan record (a docs/verification/*.md with no declaration row — the registry↔leaf family),
    #   (c) no claims-table row with an empty citation ("absence of contradiction is not verification").
    # Vacuously PASS when nothing is declared and no records exist (the webapp default). Mirrored by status's
    # load-bearing set — the two must never diverge. See shared/live-source-verification.md.
    declared, records = s.verify_live_techs, s.verification_records
    if not declared and not records:
        return True, "no verify-live techs declared — nothing to resolve"
    problems = []
    for tech in sorted(declared - set(records)):
        problems.append("declared '%s' has no docs/verification/%s.md" % (tech, tech))
    for tech in sorted(set(records) - declared):
        problems.append("orphan record docs/verification/%s.md — not declared in architecture-constraints.md" % tech)
    for tech in sorted(set(records) & declared):
        _p, rows = records[tech]
        for claim, citation in rows:
            if not citation.strip():
                problems.append("docs/verification/%s.md: claim %r has an empty citation" % (tech, claim[:50]))
    if problems:
        return False, "; ".join(problems)
    return True, "%d verify-live tech(s) declared; every record resolves, every claim cited" % len(declared)


@register_check("W1_surviving_markers", "WARN")
def w1_surviving_markers(s):
    hits = []
    for path in s.spec_md_files:
        n = len(re.findall(r"\[NEEDS CLARIFICATION", read(path)))
        if n:
            hits.append("%s (%d)" % (s.rel(path), n))
    if hits:
        return False, "surviving markers: %s — resolve before release" % ", ".join(hits)
    return True, "no surviving [NEEDS CLARIFICATION] markers"


@register_check("W2_ledger_registry_sync", "WARN")
def w2_ledger_registry_sync(s):
    if s.ledger_ids is None:
        return True, "no ledger at docs/planning/backlog.md (pre-decomposition) — skipped"
    reg, led = {r for r, _f in s.registry}, set(s.ledger_ids)
    problems = []
    if reg - led:
        problems.append("in registry, not in ledger: %s" % ", ".join(sorted(reg - led)))
    if led - reg:
        problems.append("in ledger, not in registry: %s" % ", ".join(sorted(led - reg)))
    problems += ["%s x%d in the ledger" % (r, s.ledger_ids.count(r))
                 for r in sorted(set(r for r in s.ledger_ids if s.ledger_ids.count(r) > 1))]
    if problems:
        return False, "; ".join(problems)
    return True, "ledger and registry agree (%d REQs, exactly once each)" % len(reg)


@register_check("W3_id_zero_padding", "WARN")
def w3_id_zero_padding(s):
    ids = [r for r, _f in s.registry] + list(s.ledger_ids or [])
    for _path, (headings, closers) in s.cap_blocks.items():
        ids += headings + closers
    for row in s.log_rows or []:
        if isinstance(row, dict):
            ids += [v for v in (row.get("id"), row.get("req"), row.get("resolved_by"))
                    if isinstance(v, str) and re.match(r"^(REQ|AMD|ADR)-\d+$", v)]
    unpadded = sorted({i for i in ids if re.match(r"^(REQ|AMD|ADR)-\d{1,2}$", i)})
    if unpadded:
        return False, "unpadded ids (TYPE-NNN wants three digits): %s" % ", ".join(unpadded)
    return True, "all ids zero-padded"


@register_check("W4_profile_missing", "WARN")
def w4_profile_missing(s):
    if s.spec_text is None:
        return False, "specification.md not found — profile undeterminable (defaulting webapp)"
    if s.profile is None:
        return False, ("no `- **Profile:** <value>` field — defaulting webapp; declare one "
                       "(%s; see shared/agentic-profile.md)" % " | ".join(KNOWN_PROFILES))
    if s.profile not in KNOWN_PROFILES:
        return False, "unknown Profile %r (expected: %s)" % (s.profile, ", ".join(KNOWN_PROFILES))
    return True, "profile declared: %s" % s.profile


@register_check("W5_spine_density", "WARN")
def w5_spine_density(s):
    reqs = len({r for r, _f in s.registry})
    if not reqs:
        return True, "no registry rows — density not computable (L1 already fails)"
    lines = sum(len(read(p).splitlines()) for p in s.spec_md_files
                if "evals" not in p.relative_to(s.spec_dir).parts)   # exclude docs/spec/evals/** datasets only
    density = lines / reqs
    if density > 40:
        return False, ("%d prose lines / %d REQs = %.0f per REQ (>40) — likely restated methodology or copied "
                       "prose; one home per fact" % (lines, reqs, density))
    return True, "%d prose lines / %d REQs = %.0f per REQ (<=40)" % (lines, reqs, density)


def spine_hash(root):
    """A sha256 over docs/spec/** — sorted (relative-path, bytes) — the spine's content identity ("which spec state
    shipped in release N"). The path is folded in so a rename/move changes the hash; the bytes so any content edit
    does. Same mechanism family as spec_slice_hash (WS4 D7). Empty/absent spec dir → the hash of nothing (stable)."""
    spec_dir = root / "docs" / "spec"
    h = hashlib.sha256()
    files = sorted((p for p in spec_dir.rglob("*") if p.is_file()),
                   key=lambda p: p.relative_to(root).as_posix()) if spec_dir.is_dir() else []
    for p in files:
        h.update(p.relative_to(root).as_posix().encode("utf-8") + b"\0")
        h.update(p.read_bytes())
    return h.hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser(description="Verify the spec spine's integrity (docs/spec/).")
    ap.add_argument("--json", action="store_true", help="machine-readable output for CI")
    ap.add_argument("--hash", action="store_true",
                    help="print a sha256 over docs/spec/** (the spine release identity) and exit 0")
    ap.add_argument("--root", default=".", help="project root (default: cwd)")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()

    if args.hash:
        digest = spine_hash(root)
        print(json.dumps({"spine_hash": digest}) if args.json else digest)
        return 0

    spine = Spine(root)
    results = []
    for check_id, severity, fn in CHECKS:
        ok, detail = fn(spine)
        results.append({"id": check_id, "severity": severity, "ok": ok, "detail": detail})

    failed = [r for r in results if r["severity"] == "FAIL" and not r["ok"]]
    verdict = "FAIL" if failed else "PASS"
    if args.json:
        print(json.dumps({"result": verdict, "checks": results}, indent=2))
    else:
        for r in results:
            mark = " ok " if r["ok"] else ("FAIL" if r["severity"] == "FAIL" else "WARN")
            print("[%s] %-28s %s" % (mark, r["id"], r["detail"]))
        warned = [r for r in results if r["severity"] == "WARN" and not r["ok"]]
        print("RESULT: %s%s" % (verdict, " (warnings: %s)" % ", ".join(r["id"] for r in warned) if warned else ""))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
