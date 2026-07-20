#!/usr/bin/env python3
"""Deterministic grader for 03-architect evals. Structural + amendment-aware assertions over a realized architecture.

03-architect's lift is a *structured architecture contract* the next skills consume — an arc42/C4 `system.md` with a
strategic-DDD bounded-context map that references REQs, a MADR ADR registry with checkable Rules + an index, and
per-feature specs with mechanically-gradeable Verification Contracts + DM-coverage — PLUS the subagent-isolated
Reconcile that emits `amendment-log.json` rows. Architecture *beauty* is subjective and is NOT graded (a strong
baseline also architects well). So we grade structure + amendment/ADR semantics + coverage, never taste — no LLM judge.

The one move that makes an *architecture* contradiction gradeable deterministically is the **token-in-named-field
set-match**: a `stated` constraint naming a forbidden/required token (a technology · region · host · protocol) is
checked by set membership over a designated field (the `system.md` stack, the ADR *Decision*). A stated datastore
that cannot satisfy a stated availability requirement is a *computed* contradiction, so "did the skill catch it and
log a Tier-2 amendment row + a resolving ADR?" is an objective check — 03's analogue of 02's WCAG computation.

Usage:
    python check_architecture.py --outputs <dir> --case <clean-constraint|forbidden-token|underspecified-constraint>

The --outputs dir is the project root: it is seeded with the spine (docs/spec/, docs/planning/, docs/design/approved/)
and the skill ADDS docs/architecture/ and APPENDS docs/spec/amendment-log.json. Writes grading.json
({"expectations":[{text,passed,evidence}]}) into --outputs and prints a report.
"""
import os, re, json, argparse, sys
try:  # keep prints from crashing on a legacy (cp1252) Windows console — the grading.json is always utf-8
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

results = []
def check(text, passed, evidence=""):
    results.append({"text": text, "passed": bool(passed), "evidence": str(evidence)[:300]})

def read(p):
    try:
        with open(p, encoding="utf-8") as f: return f.read()
    except Exception: return None


# ---------- the token-in-named-field set-match (the deterministic heart) ----------
# A constraint token is checked by set membership over a named field of the realization. Tokens are matched
# case-insensitively as whole words/phrases so "us" doesn't match "status" and "sqlite" is caught inside "SQLite".

DB_CLIENT_SERVER = ["postgresql", "postgres", "mysql", "mariadb", "cockroachdb", "cockroach",
                    "sql server", "mssql", "aurora", "client-server", "client/server"]
DB_EMBEDDED      = ["sqlite"]
# concrete third-party IdP PRODUCT names only — a violation = the architect actually introduced one. (Generic
# descriptors like "third-party sso" are excluded: they appear in the honoring negation "no third-party SSO".)
THIRD_PARTY_SSO  = ["auth0", "okta", "google oauth", "google sign-in", "sign in with google", "cognito",
                    "firebase auth", "clerk.dev", "workos", "azure ad", "entra id"]
NON_EU_REGION    = ["us-east", "us-west", "united states", "n. virginia", "virginia", "oregon", "california",
                    "ap-southeast", "ap-northeast", "asia-pacific", "sa-east"]
EU_REGION        = ["eu region", "eu-west", "eu-central", "europe", "frankfurt", "ireland", "stockholm", "eu only",
                    "eu data", "in the eu"]

def tokens_in(text, tokens):
    """Which of `tokens` appear in `text` (case-insensitive, word/phrase boundary)."""
    if not text:
        return []
    t = text.lower()
    hits = []
    for tok in tokens:
        # phrase tokens (with space/hyphen) → substring; bare words → word boundary
        if re.search(r"[ /-]", tok):
            if tok in t:
                hits.append(tok)
        elif re.search(r"\b" + re.escape(tok) + r"\b", t):
            hits.append(tok)
    return hits


# ---------- root / spine / realization parsing ----------

def find_root(base):
    """Return the dir containing docs/spec/specification.md (the seeded spine) under base; fall back to base."""
    for dp, dn, fn in os.walk(base):
        if dp.replace("\\", "/").endswith("docs/spec") and "specification.md" in fn:
            return os.path.dirname(os.path.dirname(dp))
    return base

def amendments(root):
    al = read(os.path.join(root, "docs/spec/amendment-log.json"))
    if al is None:
        return None
    try:
        a = json.loads(al)
        return a.get("amendments") if isinstance(a.get("amendments"), list) else None
    except Exception:
        return None

def sprint_reqs(root):
    """The IN-SCOPE REQ-IDs — the frozen-snapshot `### REQ-NNN:` headers only, NOT out-of-scope prose mentions."""
    sp = read(os.path.join(root, "docs/planning/sprints/sprint-01.md")) or ""
    return sorted(set(re.findall(r"(?m)^#{2,4}\s+(REQ-\d+)\b", sp)))

def constraint_field(root, label):
    """The value text of a `- **<label>:** ...` line in architecture-constraints.md (the named constraint field)."""
    ac = read(os.path.join(root, "docs/spec/architecture-constraints.md")) or ""
    m = re.search(r"^\s*[-*]\s*\*\*" + re.escape(label) + r"[^:]*:\*\*\s*(.+)$", ac, re.I | re.M)
    return m.group(1).strip() if m else ""

def verify_live_techs(root):
    """The verify-live tech slugs declared in architecture-constraints.md's `## Verify-live` section (WS6). Each
    row `- **<tech>:** docs: … · source: …` names a tech whose record basename is `<tech>`. Labels may carry a
    descriptive qualifier (`- **BGE-M3 (embedding model):**`); the slug is normalized — trailing parenthetical
    stripped, lowercased — to the record-basename convention (shared/live-source-verification.md). Empty ⇒ none."""
    ac = read(os.path.join(root, "docs/spec/architecture-constraints.md")) or ""
    m = re.search(r"(?ims)^##\s+Verify-live\b.*?(?=^##\s|\Z)", ac)
    techs = set()
    if m:
        for line in m.group(0).splitlines():
            tm = re.match(r"^\s*-\s*\*\*([^*]+?):\*\*", line)
            if not tm:
                continue
            slug = re.sub(r"\s*\([^)]*\)\s*$", "", tm.group(1)).strip().lower()
            if re.fullmatch(r"[a-z0-9][\w.-]*", slug):
                techs.add(slug)
    return techs

def system_md(root):
    return read(os.path.join(root, "docs/architecture/system.md"))

def adr_dir(root):
    return os.path.join(root, "docs/architecture/adr")

def adr_files(root):
    d = adr_dir(root)
    out = []
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            if re.match(r"ADR-\d+\.md$", f):
                out.append(os.path.join(d, f))
    return out

def adr_ids(root):
    return sorted(int(re.search(r"ADR-(\d+)", os.path.basename(f)).group(1)) for f in adr_files(root))

def adr_blob(root):
    return "\n\n".join(read(f) or "" for f in adr_files(root))

def adr_decisions(root):
    """Concatenated text of each ADR's Decision Outcome section (the named field the token-check reads)."""
    blob = ""
    for f in adr_files(root):
        txt = read(f) or ""
        m = re.search(r"##+\s*Decision\s+Outcome(.+?)(?:\n##\s|\Z)", txt, re.I | re.S)
        blob += (m.group(1) if m else txt) + "\n"
    return blob

def feature_specs(root):
    d = os.path.join(root, "docs/architecture/specs")
    out = []
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            if f.endswith(".md"):
                out.append(os.path.join(d, f))
    return out

def specs_blob(root):
    return "\n\n".join(read(f) or "" for f in feature_specs(root))

def manifest_required_dms(root):
    """DM-IDs marked 'required' in the seeded 02 manifest (the forward-coverage target)."""
    man = read(os.path.join(root, "docs/design/approved/sprint-01/manifest.md")) or ""
    req = []
    for line in man.splitlines():
        m = re.match(r"\s*\|\s*(DM-\d+)\s*\|", line)
        if m and "required" in line.lower() and "optional" not in line.lower().split("required")[0]:
            req.append(m.group(1))
    # fall back: all DM-IDs if none flagged required
    return sorted(set(req)) or sorted(set(re.findall(r"DM-\d+", man)))

def tier2_rows(rows):
    return [r for r in (rows or []) if str(r.get("tier")) == "2"]

def source_quotes(rows):
    """Concatenated source_quotes of the Tier-2 rows — where the ORIGINAL declaration text is preserved after the
    tech-mandate flow amends the constraint file (so validity can still see the planted token post-amendment)."""
    return " ".join(str(r.get("source_quote", "")) for r in tier2_rows(rows))

def row_blob(r):
    return json.dumps(r, ensure_ascii=False).lower()

def resolving_adr_decisions(root, rows):
    """Decision-Outcome sections of the ADRs named by a Tier-2 row's `resolved_by` (the tech-mandate partners).
    We read the DECISION field (not the whole file) so a migration ADR that names SQLite as the *superseded* option
    in its Context isn't mistaken for re-affirming it — the Decision is where the chosen technology lives."""
    out = []
    for r in tier2_rows(rows):
        rid = str(r.get("resolved_by") or "")
        m = re.search(r"ADR-(\d+)", rid)
        if m:
            txt = read(os.path.join(adr_dir(root), f"ADR-{int(m.group(1)):03d}.md")) or ""
            dm = re.search(r"##+\s*Decision\s+Outcome(.+?)(?:\n##\s|\Z)", txt, re.I | re.S)
            out.append(dm.group(1) if dm else txt)
    return out


# ---------- WS4 Task 4.1 (D1): §10 quality scenarios name an executable fitness function ----------
# A §10 quality scenario is legal only if it names its fitness function — the executable check that verifies it (a
# command, a load-test script, an ArchUnit-style rule) — or carries `deferred:<why>`. Prose-only "-ility" claims stop
# being legal (design D1). Structural signal ONLY: an inline-code span that looks executable (a known tool, a script
# path, or a flagged command) OR a `deferred:` marker in the row. We grade the PRESENCE of a named, runnable oracle,
# never its quality — a strong baseline writes measurable scenarios too; the lift is the executable check beside them.
FITNESS_EXEC = re.compile(
    r"`[^`]*(?:"
    r"\b(?:k6|locust|jmeter|gatling|artillery|vegeta|wrk|hey|siege|bombardier|"
    r"pytest|jest|vitest|mocha|playwright|npm|pnpm|yarn|make|curl|http|bench|"
    r"archunit|dependency-cruiser|depcruise|eslint|tsc|lighthouse|axe|pa11y|zap|schemathesis)\b"
    r"|\.(?:py|sh|js|ts|mjs|yml|yaml)\b"       # a script/config path
    r"|\s--?[a-z]"                              # a flagged command token, e.g. `--vus`
    r")[^`]*`", re.I)
FITNESS_DEFERRED = re.compile(r"(?i)\bdeferred\s*:")


def quality_section(sysmd):
    """The §10 Quality Requirements section text (its heading → the next H2), where the measurable scenarios live."""
    m = re.search(r"(?im)^#{1,6}[^\n]*\bquality\b[^\n]*$", sysmd or "")
    if not m:
        return ""
    nxt = re.search(r"(?m)^##\s", sysmd[m.end():])
    return sysmd[m.start(): m.end() + nxt.start()] if nxt else sysmd[m.start():]


def grade_fitness_functions(root):
    """D1 — every §10 quality scenario names its executable fitness function (or carries deferred:<why>)."""
    sec = quality_section(system_md(root) or "")
    qrows = [ln for ln in sec.splitlines() if re.match(r"\s*\|\s*Q-\d+\s*\|", ln)]
    prose_only = [ln for ln in qrows if not (FITNESS_EXEC.search(ln) or FITNESS_DEFERRED.search(ln))]
    check("system.md §10: every quality scenario names an executable fitness function (or deferred:<why>) — "
          "no prose-only quality claims (D1)",
          bool(qrows) and not prose_only,
          f"Q-rows={len(qrows)}; prose-only(no fitness fn)={len(prose_only)}"
          + (f"; e.g. {prose_only[0].strip()[:80]}" if prose_only else ""))


# ---------- WS4 Task 4.2 (D2): § Test Strategy — declared shape + flake quarantine policy ----------
# CORE (graded on small fixtures): the section exists, names a test SHAPE (pyramid/trophy/honeycomb), and carries a
# flake policy with a ticket + owner + fix-or-remove SLA. Contract-testing / PBT rows are on-demand(<trigger>) and are
# NOT demanded here (the core/on-demand convention, shared/agentic-profile.md). We grade presence of the declared
# shape + the quarantine-with-governance floor, never taste.
TEST_SHAPES = re.compile(r"(?i)\b(pyramid|trophy|honeycomb)\b")

def section_text(sysmd, heading_word_re):
    """A named section's text (its heading line → the next H2), or '' if the heading is absent."""
    m = re.search(r"(?im)^#{1,6}[^\n]*" + heading_word_re + r"[^\n]*$", sysmd or "")
    if not m:
        return ""
    nxt = re.search(r"(?m)^##\s", sysmd[m.end():])
    return sysmd[m.start(): m.end() + nxt.start()] if nxt else sysmd[m.start():]

def grade_test_strategy(root):
    """D2 — § Test Strategy declares a named shape + a governed flake-quarantine policy (ticket + owner + SLA)."""
    sec = section_text(system_md(root) or "", r"\btest\s+strategy\b")
    present = bool(sec)
    has_shape = bool(TEST_SHAPES.search(sec))
    has_flake_sla = all(re.search(p, sec, re.I) for p in
                        (r"\bticket\b", r"\bowner\b", r"(?:\bsla\b|fix-or-remove|\d+\s*weeks?)"))
    check("system.md § Test Strategy (core): a named test shape (pyramid/trophy/honeycomb) + a flake-quarantine "
          "policy (ticket + owner + fix-or-remove SLA) (D2)",
          present and has_shape and has_flake_sla,
          f"section={present}; named shape={has_shape}; flake ticket+owner+SLA={has_flake_sla}")


# ---------- WS4 Task 4.3 (D3): feature-spec Observability row ----------
# A feature spec carries one Observability row — what it logs/emits, and what "healthy" means (one line each). The
# 06 SETUP ## Operations SLO builds on these. Structural: an Observability section with a table row naming a health
# notion; we grade presence, never taste.
def grade_observability(root):
    """D3 — a feature spec carries an Observability row (what it emits + what 'healthy' means)."""
    sb = specs_blob(root)
    m = re.search(r"(?is)#{1,6}[^\n]*\bobservab\w*[^\n]*\n(.*?)(?:\n#{1,6}\s|\Z)", sb)
    sec = m.group(1) if m else ""
    present = bool(m)
    healthy = bool(re.search(r"(?i)health", sec))
    has_row = bool(re.search(r"(?m)^\s*\|.*\|", sec))
    check("A feature spec carries an Observability row — what it logs/emits + what \"healthy\" means (D3)",
          present and healthy and has_row,
          f"Observability section={present}; 'healthy' notion={healthy}; table row={has_row}")


# ---------- WS4 Task 4.4 (D4): feature-spec migration contract (conditional) ----------
# When a feature's data-model change is DESTRUCTIVE (drop/rename/alter-type/truncate), its spec must carry a
# migration row — a forward-migration command + a rollback-compatibility statement (does rollback need a data
# action? is it destructive?). Additive/initial schemas (CREATE, add-column) are N/A. Conditional, like 06's G10.
MIGR_DESTRUCTIVE = re.compile(r"(?i)\b(?:drop\s+(?:table|column)|delete\s+from|truncate|drop\s+not\s+null"
                             r"|alter\s+\w+\s+drop|rename\s+(?:table|column)|change\s+column|destructive)\b")

def grade_migration_contract(root):
    """D4 — a destructive data-model change carries a migration row (forward command) + a rollback-compat statement."""
    sb = specs_blob(root)
    # Negation guard: "non-destructive" / "not destructive" (incl. the hyphen line-wrap "non-\ndestructive") is an
    # additive-migration DECLARATION, not a destructive marker — strip negated forms before the trigger search.
    trig = re.sub(r"(?is)\b(?:non|not)[-\s]*destructive\b", "", sb)
    if not MIGR_DESTRUCTIVE.search(trig):
        check("Migration contract (D4, conditional): N/A — no destructive data-model change in the feature specs",
              True, "no destructive DDL → migration row not required (additive/initial schema)")
        return
    m = re.search(r"(?is)#{1,6}[^\n]*\bmigrat\w*[^\n]*\n(.*?)(?:\n#{1,6}\s|\Z)", sb)
    sec = m.group(1) if m else ""
    has_forward = bool(re.search(r"`[^`]+`", sec)) or bool(re.search(r"(?i)forward", sec))
    has_rollback = bool(re.search(r"(?i)rollback", sec)) and \
        bool(re.search(r"(?i)(data|backfill|destructive|irreversible|forward-only|compat|no data)", sec))
    check("Migration contract (D4): a destructive data-model change carries a migration row (a forward command) + a "
          "rollback-compatibility statement",
          bool(m) and has_forward and has_rollback,
          f"migration section={bool(m)}; forward command={has_forward}; rollback-compat statement={has_rollback}")


# ---------- WS4 Task 4.6 (D6): § Threats considered — the design-time threat pass ----------
# system.md gains a § Threats considered section: the Four Questions walked over the C4 L1/L2 trust boundaries the
# diagram already draws, each threat → a mitigation (a constraint line / ADR / an explicit accepted-risk note). A
# ten-minute pass, not a workshop. Structural: the section exists, carries >=1 threat row/bullet, and names a
# mitigation notion. 07's completeness lens later cross-references this (a designed threat with no check = a gap).
def grade_threats(root):
    """D6 — § Threats considered: >=1 boundary-derived threat, each with a mitigation (link / ADR / accepted-risk)."""
    sec = section_text(system_md(root) or "", r"threats?\s+considered")
    present = bool(sec.strip())
    has_threat = present and bool(re.search(r"(?im)^\s*(?:\|\s*[^|\s]|[-*]\s|\d+\.\s)", sec))
    has_mitigation = bool(re.search(r"(?i)mitigat|accepted[- ]risk|accept the risk|\bADR-\d+\b|constraint|control", sec))
    check("system.md § Threats considered (D6): >=1 boundary-derived threat, each with a mitigation (a constraint / "
          "ADR / accepted-risk) — the Four Questions over the C4 trust boundaries",
          present and has_threat and has_mitigation,
          f"section={present}; threat row/bullet={has_threat}; mitigation notion={has_mitigation}")


# ---------- WS6 Task 6.3: verify-live ADR citation (conditional; the tech-mandate flow's live-source arm) ----------
# When architecture-constraints.md declares verify-live techs (## Verify-live), an ADR whose Decision NAMES one of
# them must cite the verification record: a `Verified-against: docs/verification/<tech>.md` line resolving on disk.
# No declared tech, or no ADR relying on one, is N/A (like S16 / 06's G10). See shared/live-source-verification.md.
def grade_verify_live_adr(root):
    """S18 — an ADR whose Decision names a declared verify-live tech carries a resolving `Verified-against:
    docs/verification/<tech>.md` citation. Conditional: N/A when nothing is declared or no ADR relies on one."""
    techs = verify_live_techs(root)
    if not techs:
        check("Verify-live ADR citation (S18, conditional): N/A — no verify-live tech declared",
              True, "no ## Verify-live block in architecture-constraints.md")
        return
    cited, uncited = [], []
    for f in adr_files(root):
        txt = read(f) or ""
        dec = re.search(r"##+\s*Decision\s+Outcome(.+?)(?:\n##\s|\Z)", txt, re.I | re.S)
        dec_txt = dec.group(1) if dec else txt
        named = sorted(t for t in techs if re.search(r"\b" + re.escape(t) + r"\b", dec_txt, re.I))
        if not named:
            continue                                    # this ADR does not rely on a verify-live tech
        va = re.search(r"(?im)Verified-against\**\s*:?\s*(\S+)", txt)
        ok = bool(va) and any(("docs/verification/%s.md" % t) in txt.lower()
                              and os.path.isfile(os.path.join(root, "docs/verification/%s.md" % t))
                              for t in named)
        (cited if ok else uncited).append("%s→%s" % (os.path.basename(f), ",".join(named)))
    if not cited and not uncited:
        check("Verify-live ADR citation (S18, conditional): N/A — no ADR Decision names a declared verify-live tech",
              True, "declared techs=%s; no ADR relies on one" % sorted(techs))
        return
    check("Verify-live ADR citation (S18): every ADR whose Decision names a verify-live tech cites a resolving "
          "docs/verification/<tech>.md (the confabulation guardrail's tech-mandate arm)",
          not uncited, "cited=%s; uncited=%s" % (cited or "none", uncited or "none"))


# ---------- shared structural assertions (the contract the next skills consume) ----------

def grade_structure(root, reqs):
    sys = system_md(root)
    if sys is None:
        check("system.md written at docs/architecture/system.md", False, f"no docs/architecture/system.md under {root}")
        sys = ""
    else:
        check("system.md written at docs/architecture/system.md", True, f"{len(sys)} chars")

    # S2 — C4: a Mermaid C4 block (canonical) OR an ASCII fallback diagram (bracketed nodes + arrows)
    has_mermaid_c4 = bool(re.search(r"c4context|c4container|c4component", sys, re.I))
    has_ascii_c4 = bool(re.search(r"```[^`]*\[[^\]]+\][^`]*(-->|--\w|→|\|)[^`]*```", sys, re.S))
    check("system.md carries a C4 diagram (Mermaid C4 canonical, or an ASCII fallback)",
          has_mermaid_c4 or has_ascii_c4,
          f"mermaid C4={has_mermaid_c4}; ascii C4 fallback={has_ascii_c4}")

    # S3 — strategic DDD: a bounded-context map with >=1 named context
    has_bc = bool(re.search(r"bounded[\s-]*context", sys, re.I))
    check("system.md has a strategic-DDD bounded-context map", has_bc,
          "found 'bounded context'" if has_bc else "no bounded-context map")

    # S4 — arc42 skeleton: >=4 of the distinctive arc42 sections present as headings
    arc = [k for k in ["constraints", "context", "solution strategy", "building block", "crosscutting",
                       "quality", "risk"] if re.search(r"^#{1,6}[^\n]*\b" + k, sys, re.I | re.M)]
    check("system.md follows the arc42 subset (>=4 sections incl. Crosscutting Concepts + Quality)",
          len(arc) >= 4 and "crosscutting" in arc and "quality" in arc, f"arc42 sections found={arc}")

    # S5 — the architecture references the spine by REQ-ID (traceability, not copied prose)
    sys_reqs = sorted(set(re.findall(r"REQ-\d+", sys)))
    check("system.md references the spine by REQ-ID (traceability, not copied requirement prose)",
          bool(sys_reqs), f"REQ refs in system.md={sys_reqs or 'none'}")

    # S6 — ADR registry: an index + >=1 ADR with MADR fields AND a checkable Rule (Binds/Prevents/Rule)
    idx = read(os.path.join(adr_dir(root), "README.md"))
    ab = adr_blob(root)
    has_madr = bool(re.search(r"status", ab, re.I) and re.search(r"decision", ab, re.I)
                    and re.search(r"consequence", ab, re.I))
    has_rule = bool(re.search(r"\bRule\b|Confirmation", ab) and re.search(r"Binds|Prevents", ab))
    check("ADR registry: adr/README.md index + >=1 MADR ADR with a checkable Rule (Binds/Prevents/Rule)",
          idx is not None and bool(adr_files(root)) and has_madr and has_rule,
          f"index={'yes' if idx else 'no'}; adr files={[os.path.basename(f) for f in adr_files(root)]}; "
          f"MADR fields={has_madr}; Rule+Binds/Prevents={has_rule}")

    # S7 — ADR allocation: contiguous from ADR-001, no duplicate/missing (sole-allocator max+1 discipline)
    ids = adr_ids(root)
    contiguous = ids == list(range(1, len(ids) + 1)) if ids else False
    check("ADR IDs are contiguous from ADR-001 with no gaps/dupes (max+1 allocation)",
          contiguous, f"ADR ids={ids or 'none'}")

    # S8 — >=1 feature spec referencing the sprint's REQs, WITH a Verification Contract (method + pass-criterion)
    sb = specs_blob(root)
    spec_reqs = sorted(set(re.findall(r"REQ-\d+", sb)) & set(reqs))
    has_vc = bool(re.search(r"verification contract", sb, re.I)
                  and re.search(r"api-contract|browser|unit|static-conformance", sb, re.I))
    check("A feature spec references the sprint's REQs and carries a Verification Contract (method + pass-criterion)",
          bool(feature_specs(root)) and bool(spec_reqs) and has_vc,
          f"specs={[os.path.basename(s) for s in feature_specs(root)] or 'none'}; "
          f"sprint-REQ refs={spec_reqs or 'none'}; VC with method={has_vc}")

    # S9 — REQ -> spec coverage: every in-scope sprint REQ appears in >=1 feature spec
    spec_all_reqs = set(re.findall(r"REQ-\d+", sb))
    missing_reqs = sorted(set(reqs) - spec_all_reqs)
    check("REQ coverage: every in-scope sprint REQ is covered by >=1 feature spec",
          bool(reqs) and not missing_reqs, f"sprint REQs={reqs}; uncovered by specs={missing_reqs or 'none'}")

    # S10 — DM -> spec coverage (forward): every required manifest DM-ID is covered by a feature spec
    req_dms = manifest_required_dms(root)
    spec_dms = set(re.findall(r"DM-\d+", sb))
    missing_dms = sorted(set(req_dms) - spec_dms)
    check("DM coverage (forward): every required 02-manifest DM-ID is covered by a feature spec",
          bool(req_dms) and not missing_dms, f"required DM-IDs={req_dms}; uncovered={missing_dms or 'none'}")

    # S11 — amendment log valid
    rows = amendments(root)
    check("amendment-log.json is valid JSON with an 'amendments' array",
          rows is not None, "valid" if rows is not None else "missing/invalid amendment-log.json")

    # S12 — reconciler isolation: a context attestation was recorded (Pass-2 isolation proxy; transcript-absence is
    #        the manual half, per shared/subagent-protocol.md)
    attest = _attestation_recorded(root)
    check("Reconciler isolation: a context attestation is recorded (fresh-spawner proxy; transcript check is manual)",
          attest, "attestation marker found" if attest else "no context-attestation marker in docs/architecture/")

    # S13 (WS4 D1) — every §10 quality scenario names an executable fitness function (or deferred:<why>).
    grade_fitness_functions(root)
    # S14 (WS4 D2) — § Test Strategy: a named shape + a governed flake-quarantine policy.
    grade_test_strategy(root)
    # S15 (WS4 D3) — a feature spec carries an Observability row (what it emits + what "healthy" means).
    grade_observability(root)
    # S16 (WS4 D4) — a destructive data-model change carries a migration + rollback-compat contract (conditional).
    grade_migration_contract(root)
    # S17 (WS4 D6) — § Threats considered: a boundary-derived threat pass with mitigations.
    grade_threats(root)

    return sys, rows


# ---------- Phase-1 data cases (design: _artifacts/data-architecture-phase1-design.md) ----------

DATA_FIXTURES = {"data-modules": "beacon-data", "data-nogate": "beacon-nogate"}

def data_line_values(root):
    """The declared `Data:` module values (the routing line; shared/agentic-profile.md § The Data line)."""
    sp = read(os.path.join(root, "docs/spec/specification.md")) or ""
    m = re.search(r"(?im)^\s*-\s*\*\*Data:\*\*\s*(.+)$", sp)
    if not m:
        return []
    return [v for v in ("retrieval", "grounded-writes", "memory")
            if re.search(r"\b" + v + r"\b", m.group(1), re.I)]

def _norm(s):
    return (s or "").replace("\r\n", "\n").replace("\r", "\n")

def _attestation_recorded(root):
    """The S12 attestation scan, shared by grade_structure and grade_data_arch."""
    blob = (system_md(root) or "") + "\n" + adr_blob(root) + "\n" + specs_blob(root) + "\n"
    for dp, dn, fn in os.walk(os.path.join(root, "docs/architecture")):
        for f in fn:
            if re.search(r"reconcile", f, re.I):
                blob += (read(os.path.join(dp, f)) or "") + "\n"
    return bool(re.search(r"context attestation|(realization|build)\s+conversation[^\n]{0,30}not provided",
                          blob, re.I))

def grade_capabilities_untouched(root, fixture_docs):
    """Spine integrity: capabilities/** content-identical (EOL-normalized) to the fixture — the smoke's manual
    REQ-text eyeball made deterministic. Content compare, not byte compare: the threat is edits, not CRLF."""
    fx = os.path.join(fixture_docs, "spec", "capabilities")
    ws = os.path.join(root, "docs", "spec", "capabilities")
    fx_files, diffs, extra = [], [], []
    for dp, dn, fn in os.walk(fx):
        for f in fn:
            rel = os.path.relpath(os.path.join(dp, f), fx).replace("\\", "/")
            fx_files.append(rel)
            if _norm(read(os.path.join(dp, f))) != _norm(read(os.path.join(ws, rel))):
                diffs.append(rel)
    if os.path.isdir(ws):
        for dp, dn, fn in os.walk(ws):
            for f in fn:
                rel = os.path.relpath(os.path.join(dp, f), ws).replace("\\", "/")
                if rel not in fx_files:
                    extra.append(rel)
    check("Spine integrity: docs/spec/capabilities/** content-identical to the fixture (EOL-normalized)",
          bool(fx_files) and not diffs and not extra,
          f"fixture files={len(fx_files)}; changed={diffs or 'none'}; extra={extra or 'none'}")

def grade_data_arch(root, reqs, case, fixture_docs):
    """Phase-1 data cases — a focused path like grade_agent_arch: a small core + the DA checks. The full webapp
    contract is the TeamPulse cases' job; topology economics is the agent case's job."""
    sysmd = system_md(root) or ""
    check("system.md written at docs/architecture/system.md", bool(sysmd.strip()), f"{len(sysmd)} chars")
    idx = read(os.path.join(adr_dir(root), "README.md"))
    check("ADR registry present (adr/README.md index + >=1 ADR)",
          idx is not None and bool(adr_files(root)),
          f"index={'yes' if idx else 'no'}; adrs={[os.path.basename(f) for f in adr_files(root)]}")
    rows = amendments(root)
    check("amendment-log.json is valid JSON with an 'amendments' array",
          rows is not None, "valid" if rows is not None else "missing/invalid amendment-log.json")
    check("Reconciler isolation: a context attestation is recorded (fresh-spawner proxy; transcript check is manual)",
          _attestation_recorded(root),
          "attestation marker found" if _attestation_recorded(root) else "no marker in docs/architecture/")
    sb = specs_blob(root)
    spec_reqs = sorted(set(re.findall(r"REQ-\d+", sb)) & set(reqs))
    has_vc = bool(re.search(r"(?i)verification contract", sb))
    check("A feature spec references the sprint's REQs and carries a Verification Contract",
          bool(feature_specs(root)) and bool(spec_reqs) and has_vc,
          f"specs={[os.path.basename(s) for s in feature_specs(root)] or 'none'}; "
          f"sprint-REQ refs={spec_reqs or 'none'}; VC={has_vc}")
    grade_capabilities_untouched(root, fixture_docs)

    declared = data_line_values(root)
    blob = sysmd + "\n" + adr_blob(root) + "\n" + sb
    missing = [v for v in declared if not re.search(r"\b" + v + r"\b", blob, re.I)]
    check("DA-T01 pairing: every declared Data: value appears in the realization (realized, or explicitly "
          "declined — silent omission fails either way)",
          bool(declared) and not missing, f"declared={declared}; unaddressed={missing or 'none'}")

    if case == "data-modules":
        grade_da_t02(root, sb + "\n" + adr_blob(root))
        grade_da_t03(sb + "\n" + adr_blob(root))
        grade_da_t04(root)
        grade_da_t05(root, blob)
        grade_da_t06(root, blob)
        grade_da_t07(root)
    else:
        grade_da_t04(root)
        grade_nogate(rows, sb)
    return rows

# Task-4 scoped scaffolding: the not-yet-written DA checks are stubs so the ideal scenario can run and RED stays
# scoped to one task. Each is fully implemented (and its degenerates added) in Tasks 5–8.
def grade_da_t02(root, blob):
    """DA-T02 — retrieval declared ⇒ >=1 eval-suite VC row whose golden-set dataset ref resolves on disk."""
    has_es = bool(re.search(r"(?i)eval-suite", blob))
    paths = sorted(set(re.findall(r"(docs/spec/evals/[\w./-]+\.jsonl)", blob)))
    resolving = [p for p in paths if os.path.isfile(os.path.join(root, p))]
    check("DA-T02 pairing: retrieval declared => an eval-suite VC row whose golden-set dataset ref resolves on disk",
          has_es and bool(resolving),
          f"eval-suite mentioned={has_es}; dataset refs={paths or 'none'}; resolving={resolving or 'none'}")

def grade_da_t03(blob):
    """DA-T03 — grounded-writes declared ⇒ a named write-path admission rule: >=2 chain stages + admit/commit,
    within one blank-line-delimited block."""
    ok, ev = False, "no admission-rule block found"
    for para in re.split(r"\n\s*\n", blob):
        stages = set(m.group(1).lower().replace(" ", "-")
                     for m in re.finditer(r"(?i)\b(schema|referential|business[- ]rule)\b", para))
        if len(stages) >= 2 and re.search(r"(?i)\b(admission|admit(s|ted)?|commit)\b", para):
            ok, ev = True, f"stages={sorted(stages)}"
            break
    check("DA-T03 pairing: grounded-writes declared => a named write-path admission rule (>=2 of "
          "schema/referential/business-rule + admit/commit in one block)", ok, ev)

DIMENSION_MARKERS = (r"(?i)dimension|§ ?1\b|rubric|workload shape|data-model fit|pacelc|scale envelope"
                     r"|operational maturity|team[- ]skill|choose[- ]boring|boring[- ]tech")

def grade_da_t04(root):
    """DA-T04 — the datastore ADR walks the §1 rubric. Candidate = an ADR whose Decision Outcome names a
    datastore token (the token-in-named-field pattern); >=1 candidate must satisfy every clause. Always-on."""
    best = None  # (score, name, clauses)
    for f in adr_files(root):
        txt = read(f) or ""
        dm = re.search(r"##+\s*Decision\s+Outcome(.+?)(?:\n##\s|\Z)", txt, re.I | re.S)
        dec = dm.group(1) if dm else txt
        # candidate = the datastore-selection ADR: either its Decision names a datastore token (a store was
        # chosen) OR it is a rubric-walked "no datastore" decision (a stateless app still makes the §1 call).
        no_store = re.search(r"(?i)\bno\s+(?:[\w-]+\s+){0,3}(?:datastore|database|persistent\s+(?:store|state)"
                             r"|persisted\s+state|dedicated\s+store|data\s+store|db\b)", dec)
        if not tokens_in(dec, DB_CLIENT_SERVER + DB_EMBEDDED) and not no_store:
            continue
        om = re.search(r"##+\s*Considered\s+Options(.+?)(?:\n##\s|\Z)", txt, re.I | re.S)
        n_opts = len(re.findall(r"(?m)^\s*(?:\d+\.|[-*])\s+\S", om.group(1))) if om else 0
        rt = re.search(r"(?im)^\s*[-*]?\s*\*\*Review-Trigger:\*\*\s*(.+(?:\n(?![ \t]*[-*#]).+)*)", txt)
        clauses = {
            "alts>=2": n_opts >= 2,
            "driver-REQ": bool(re.search(r"REQ-\d+", txt)),
            "dimension-map": bool(re.search(DIMENSION_MARKERS, txt)),
            "review-trigger(symptom)": bool(rt) and not re.search(
                r"(?i)periodic|every\s+\d+\s*(day|week|month|quarter)|quarterly|annually", rt.group(1)),
            "exit-cost": bool(re.search(
                r"(?i)one[- ]way|two[- ]way door|exit\s*/?\s*(cost|migration)|migration cost|reversib|irreversib"
                r"|lock[- ]in"
                r"|\b(migrat\w+|switch\w+|port\w+|swap\w+)\b[^.\n]{0,70}\b(cost|project|expensive|effort|"
                r"non-trivial|significant|hard|difficult|lift|painful|rework|undertaking|substantial|one-off)\b"
                r"|\b(cost|effort|expensive|hard|difficult|non-trivial|significant)\b[^.\n]{0,50}\bto\s+"
                r"(migrat\w+|switch\w+|move off|move away|exit|replace)\b", txt)),
            "durable-vs-vendor": any(
                re.search(r"(?i)vendor|managed|hosting|self[- ]hosted", para) and
                re.search(r"(?i)separate|two (separate )?decisions|deferred|distinct|its own (adr|decision)", para)
                for para in re.split(r"\n\s*\n", txt)),
        }
        score = sum(clauses.values())
        if best is None or score > best[0]:
            best = (score, os.path.basename(f), clauses)
    ok = best is not None and all(best[2].values())
    check("DA-T04: a datastore ADR walks the §1 rubric (>=2 alternatives · driver REQ + dimension map · symptom "
          "Review-Trigger · exit-cost · durable-vs-vendor split)",
          ok, "no ADR Decision names a datastore token" if best is None
          else "%s: %s" % (best[1], {k: v for k, v in best[2].items()}))
def grade_da_t05(root, blob):
    """DA-T05 — retrieval content clauses. `Stage N` is doctrine vocabulary the tooth itself mandates
    ("the stage declared") — a structural-lift discriminator, not corpus leakage."""
    stages = sorted(set(int(n) for n in re.findall(r"(?i)\bStage\s*([0-6])\b", blob)))
    chunk_ok = (bool(re.search(r"(?i)\d+[\s-]?token", blob)) and bool(re.search(r"(?i)overlap", blob))) \
        or bool(re.search(r"(?i)no[- ]chunk", blob))
    dims = bool(re.search(r"(?i)\b\d{3,4}\s*-?\s*dim(?:ension)?s?\b|vector\(\d{3,4}\)", blob))
    reindex = bool(re.search(r"(?i)re-?index|re-?embed", blob))
    k_ok = bool(re.search(r"(?i)k[- ]consisten", blob)) \
        or bool(re.search(r"(?i)\bk\b[^\n.]{0,80}(equal|same|match)", blob))
    hi = [s for s in sorted(set(int(n) for n in re.findall(r"(?i)\bStage\s*([0-6])\b", adr_decisions(root))))
          if s >= 3]
    esc_ok, esc_ev = True, "committed stage <3 => why-not-simpler N/A"
    if hi:
        esc_ok = bool(re.search(r"(?i)why not|simpler|measured gap|not justified", blob))
        esc_ev = f"stage {hi} committed; why-not-simpler={esc_ok}"
    check("DA-T05: retrieval content clauses (stage declared · chunking params or no-chunking rationale · "
          "embedding dims + reindex trigger · k-consistency · why-not-simpler on Stage>=3)",
          bool(stages) and chunk_ok and dims and reindex and k_ok and esc_ok,
          f"stages={stages or 'none'}; chunking={chunk_ok}; dims={dims}; reindex={reindex}; k={k_ok}; {esc_ev}")

def grade_da_t06(root, blob):
    """DA-T06 — grounding content clauses. The driver-layer clause is conditional on LLM-issued queries
    existing in the realization (its required direction is proven by the self-test's ADDITION degenerate)."""
    gt = bool(re.search(r"(?i)ground[- ]truth", blob))
    thr = any(re.search(r"(?i)threshold|tolerance", para)
              and re.search(r"(?i)\b(\d+(\.\d+)?%?|zero)\b", para)
              and re.search(r"(?i)\b(block(s|ed)?|drop(s|ped)?|refus\w+|regenerat\w+|auto-correct\w*|rout(e|ed|ing)|flag(s|ged)?)\b", para)
              for para in re.split(r"\n\s*\n", blob))
    fb = bool(re.search(r"(?i)fallback", blob)) and bool(re.search(r"(?i)refus|retry|degrade|escalat|drop", blob))
    llmq = bool(re.search(r"(?i)(llm|model)[- ](issued|generated)\s*(sql|quer)|text[- ]to[- ]sql|nl2sql", blob))
    if llmq:
        drv = bool(re.search(r"(?i)read[- ]only", blob)) and bool(re.search(r"(?i)driver|connection|permission", blob))
        drv_ev = f"LLM-issued queries present; driver-layer read-only={drv}"
    else:
        drv, drv_ev = True, "no LLM-issued queries in the realization => driver-layer clause N/A"
    check("DA-T06: grounding content clauses (named ground-truth source · numeric threshold + action · fallback "
          "per failure mode · driver-layer read-only when LLM-issued queries exist)",
          gt and thr and fb and drv, f"ground-truth={gt}; threshold+action={thr}; fallback={fb}; {drv_ev}")

def grade_da_t07(root):
    """DA-T07 — memory content clauses, on the Category: memory ADR (the doctrine's own contract: `Data: memory`
    backs the Category: memory ADR). The deletion pairing gates on the SPINE's promise line — structure, not
    vocabulary: present => the pairing is required; absent => N/A."""
    mem = None
    for f in adr_files(root):
        txt = read(f) or ""
        if re.search(r"(?im)^\s*[-*]?\s*\*\*Category:\*\*\s*memory\b", txt):
            mem = (os.path.basename(f), txt)
            break
    if mem is None:
        check("DA-T07: memory content clauses (Gate-0 trigger cited · per-kind substrate · lifecycle floor · "
              "sharing+authz named together · deletion=>derived-reach when promised)",
              False, "no Category: memory ADR found")
        return
    name, txt = mem
    paras = re.split(r"\n\s*\n", txt)
    gate0 = bool(re.search(r"(?i)gate[- ]?0", txt)) and bool(re.search(r"(?i)trigger", txt))
    kinds = bool(re.search(r"(?i)\b(semantic|episodic|procedural)\b", txt))
    substrate = bool(re.search(r"(?i)relational|table|store|\bkv\b|vector|graph|file", txt))
    life = bool(re.search(r"(?i)\bttl\b|decay|expir|retention", txt))
    # morphology: "share"/"shared"/"sharing" all name the dimension — a bridge run wrote the doctrine's own label
    # ("Sharing + authorization: N/A — <reason>") and the gerund escaped \bshared?\b. A reasoned N/A decline
    # counts: the clause demands the dimension be ADDRESSED with authz in one paragraph, not a positive policy.
    share = any(re.search(r"(?i)\bshar(?:e|ed|ing)\b|private", p) and
                re.search(r"(?i)authori[sz]|sole writer|only .{0,40}writes|write[- ]path", p) for p in paras)
    promise = bool(re.search(r"(?i)request\s+deletion",
                             read(os.path.join(root, "docs/spec/architecture-constraints.md")) or ""))
    if promise:
        reach = any(re.search(r"(?i)delet", p) and re.search(r"(?i)derived|summar|index|profile|cache|reach", p)
                    for p in paras)
        reach_ev = f"deletion promised in the spine; derived-reach pairing={reach}"
    else:
        reach, reach_ev = True, "no user-facing deletion promise in the spine => pairing N/A"
    check("DA-T07: memory content clauses (Gate-0 trigger cited · per-kind substrate · lifecycle floor · "
          "sharing+authz named together · deletion=>derived-reach when promised)",
          gate0 and kinds and substrate and life and share and reach,
          f"{name}: gate0={gate0}; kinds={kinds}; substrate={substrate}; lifecycle={life}; "
          f"sharing+authz={share}; {reach_ev}")

def grade_nogate(rows, sb):
    """Selectivity (design §5 principle 2): absence is read ONLY from structured commitment loci — Data-model +
    Components table rows — never prose, where a decline legitimately mentions stores in negation."""
    trows = [ln for ln in sb.splitlines() if re.match(r"\s*\|", ln)]
    r_hits = [ln.strip()[:80] for ln in trows if re.search(r"(?i)vector\s*\(|embedding|tsvector|hnsw|ivfflat", ln)]
    m_hits = [ln.strip()[:80] for ln in trows
              if re.search(r"(?i)\bmemor|reliab|profile", ln)
              and not re.search(r"(?i)in[- ]memory|in[- ]process|ephemeral|transient", ln)]
    check("Need-gate selectivity: no retrieval/memory substrate commitment in the structured loci "
          "(Data-model/Components table rows) — the declined modules stay declined",
          not r_hits and not m_hits,
          f"retrieval-commitment rows={r_hits or 'none'}; memory-commitment rows={m_hits or 'none'}")
    n = len(rows or [])
    check("False-positive bound: a declined Data: line yields <=1 amendment row (one line-narrowing proposal is "
          "defensible; invented findings are not)",
          rows is not None and n <= 1, f"{n} amendment row(s)")


# ---------- WS3 Task 3.5a: agentic ADR categories + eval-suite oracle ----------

# The topology ADR's required ~15x token-economics justification. The signal is the MULTIPLIER (a multi-agent system
# costs ~an order of magnitude more tokens), not a bare "token spend is bounded" — a topology ADR that weighs no cost
# multiplier against the value is an incomplete decision. Match "15x" / "token economics" (the phrase the skill
# mandates) / "N× tokens" / "N-fold" / "order of magnitude"; NOT a loose "token cost/budget/spend".
ECON_JUSTIFICATION = (r"15\s*[x×]|~\s*15|\b\d+\s*(?:times|-?fold)\b|token[- ]?econom"
                      r"|\d+\s*[x×]\s*(?:the\s*|more\s*)?tokens?|order of magnitude")


def grade_agent_arch(root, reqs):
    """WS3 Task 3.5a — under Profile: agent-system: agentic ADR categories (a multi-agent TOPOLOGY ADR REQUIRES the
    ~15x token-economics justification) + the eval-suite VC oracle for distributional REQs. Focused on the agentic
    additions; 03's full structural contract is validated by the webapp cases."""
    sysmd = system_md(root) or ""
    check("system.md written at docs/architecture/system.md", bool(sysmd.strip()), f"{len(sysmd)} chars")

    idx = read(os.path.join(adr_dir(root), "README.md"))
    check("ADR registry present (adr/README.md index + >=1 ADR)",
          idx is not None and bool(adr_files(root)),
          f"index={'yes' if idx else 'no'}; adrs={[os.path.basename(f) for f in adr_files(root)]}")

    # CORE 1 — a topology ADR carrying the ~15x token-economics justification.
    # Prefer the ADR whose Category IS topology; fall back to a topology/orchestration TITLE only if none declares
    # the category — a classic ADR that merely NAMES the orchestrator in its body must not be mistaken for it.
    topo_adr = None
    for f in adr_files(root):
        txt = read(f) or ""
        cat = re.search(r"(?im)^\s*[-*]?\s*\*\*Category:\*\*\s*(.+)$", txt)
        if cat and re.search(r"\btopology\b", cat.group(1), re.I):
            topo_adr = (f, txt)
            break
    if topo_adr is None:
        for f in adr_files(root):
            txt = read(f) or ""
            title = re.search(r"(?im)^#\s*ADR-\d+\s*:\s*(.+)$", txt)
            if title and re.search(r"topolog|orchestrat|swarm|multi-?agent", title.group(1), re.I):
                topo_adr = (f, txt)
                break
    topo_txt = topo_adr[1] if topo_adr else ""
    check("A topology ADR is present (Category: topology / an orchestration decision)",
          bool(topo_adr), os.path.basename(topo_adr[0]) if topo_adr else "no topology/orchestration ADR found")
    econ = bool(topo_adr) and bool(re.search(ECON_JUSTIFICATION, topo_txt, re.I))
    check("The topology ADR carries the ~15x token-economics justification (multi-agent cost weighed against value)",
          econ, "economics justification present" if econ else
          "no ~15x / token-economics justification in the topology ADR (an incomplete multi-agent decision)")

    # CORE 2 — >=1 Verification-Contract row uses the eval-suite oracle, tied to a dataset/floor (not a stray mention).
    sb = specs_blob(root)
    has_es = bool(re.search(r"(?i)eval-suite", sb))
    tied = bool(re.search(r"(?is)verification contract.*eval-suite", sb)) or \
        bool(re.search(r"(?im)eval-suite.{0,120}(?:dataset|floor|docs/spec/evals)", sb)) or \
        bool(re.search(r"(?im)(?:dataset|floor|docs/spec/evals).{0,120}eval-suite", sb))
    check(">=1 Verification-Contract row uses the eval-suite oracle (a distributional REQ, tied to a dataset/floor)",
          has_es and tied, "eval-suite VC row present" if (has_es and tied) else
          f"eval-suite mentioned={has_es}; tied to a VC row/dataset/floor={tied}")

    # base — a feature spec references the sprint REQs and carries a Verification Contract
    spec_reqs = sorted(set(re.findall(r"REQ-\d+", sb)) & set(reqs))
    has_vc = bool(re.search(r"(?i)verification contract", sb))
    check("A feature spec references the sprint's REQs and carries a Verification Contract",
          bool(feature_specs(root)) and bool(spec_reqs) and has_vc,
          f"specs={[os.path.basename(s) for s in feature_specs(root)] or 'none'}; "
          f"sprint-REQ refs={spec_reqs or 'none'}; VC={has_vc}")

    rows = amendments(root)
    check("amendment-log.json is valid JSON with an 'amendments' array",
          rows is not None, "valid" if rows is not None else "missing/invalid amendment-log.json")
    return sysmd, rows


# ---------- per-case assertions ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outputs")
    ap.add_argument("--case",
                    choices=["clean-constraint", "forbidden-token", "underspecified-constraint", "agent",
                             "data-modules", "data-nogate"])
    ap.add_argument("--self-test", action="store_true",
                    help="validate the S18 verify-live + data + tech-mandate-LINE graders against hand-built trees")
    ap.add_argument("--fixture-docs", help="override the fixture docs/ dir for the capabilities check")
    a = ap.parse_args()
    if a.self_test:
        ok = (_self_test_s18() and _self_test_data() and _self_test_mandate_line()
              and _self_test_migration_negation())
        raise SystemExit(0 if ok else 1)   # `sys` is shadowed as a local below (system.md content)
    if not a.outputs or not a.case:
        ap.error("--outputs and --case are required unless --self-test")
    root = find_root(a.outputs)
    reqs = sprint_reqs(root)

    if a.case == "agent":
        grade_agent_arch(root, reqs)
        grade_verify_live_adr(root)
        return emit(a)

    if a.case in DATA_FIXTURES:
        fixture_docs = a.fixture_docs or os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "fixtures", DATA_FIXTURES[a.case], "docs")
        grade_data_arch(root, reqs, a.case, fixture_docs)
        grade_verify_live_adr(root)
        return emit(a)

    sys, rows = grade_structure(root, reqs)
    datastore = constraint_field(root, "Datastore")
    availability = constraint_field(root, "Availability")
    realization = (sys or "") + "\n" + adr_decisions(root) + "\n" + adr_blob(root)

    if a.case == "clean-constraint":
        # 1) Validity — the stated datastore is a client-server DB compatible with the shared-store requirement.
        cs = tokens_in(datastore, DB_CLIENT_SERVER)
        emb = tokens_in(datastore, DB_EMBEDDED)
        check("Validity: the stated datastore is a client-server DB compatible with the availability requirement "
              "(a genuinely clean envelope)",
              bool(cs) and not emb, f"datastore constraint='{datastore[:80]}'; client-server={cs}; embedded={emb}")
        # 2) HONORS (token check, honored direction) — the realization SELECTS the stated client-server datastore.
        #    Check the POSITIVE presence of the stated token (named affirmatively in §5 / the stack), NOT the
        #    absence of forbidden tokens: a good system.md BANS the forbidden datastore/IdP in its §8 banned-list
        #    (and ADRs *Prevent* them) — honoring content a naive absence-check would misread as a violation. The
        #    no-third-party-SSO honoring is verified by the (human-gated) Pass-2 reconciler, not the token grader.
        stated_db = tokens_in(datastore, DB_CLIENT_SERVER)
        honored = bool(stated_db) and any(t in realization.lower() for t in stated_db)
        check("HONORS the envelope: the realization selects the stated client-server datastore (the "
              "token-in-named-field check, honored direction)",
              honored,
              f"stated datastore tokens={stated_db}; present in realization={honored}; "
              f"EU-region tokens in realization={tokens_in(realization, EU_REGION) or 'none'}")
        # 3) False-positive — a clean, honored envelope yields ~zero invented amendments (<=1).
        n = len(rows or [])
        check("False-positive check: a clean, honored envelope yields no invented amendments (<=1)",
              rows is not None and n <= 1, f"{n} amendment row(s) emitted")

    elif a.case == "forbidden-token":
        # 1) Validity — the planted contradiction is real: embedded SQLite vs a stated shared/multi-instance store.
        #    The tech-mandate flow AMENDS the Datastore line (SQLite -> a client-server DB), so post-run the token
        #    lives in the amendment `source_quote` (which preserves the original) rather than the constraint file.
        sqs = source_quotes(rows)
        emb = tokens_in(datastore, DB_EMBEDDED) or tokens_in(sqs, DB_EMBEDDED)
        shared_req = bool(re.search(r"share one datastore|shared|multiple|two or more|stateless instances|worker",
                                    availability + " " + sqs, re.I))
        check("Validity: the stated datastore (embedded SQLite) cannot satisfy the stated shared/multi-instance "
              "store requirement (the planted contradiction is real — in the constraint or the amendment source_quote)",
              bool(emb) and shared_req,
              f"datastore='{datastore[:50]}'; embedded token (file|source_quote)={emb}; shared/multi-instance={shared_req}")
        # 2) Discriminating core — a Tier-2 row catches the datastore contradiction, gated (not auto-applied),
        #    resolved by an ADR whose Decision names a client-server replacement (the tech-mandate flow).
        t2 = tier2_rows(rows)
        cites = [r for r in t2 if re.search(r"sqlite|datastore|embedded", row_blob(r))]
        gated = [r for r in cites if r.get("disposition") in ("gated", "approved", "pending")]
        not_auto = [r for r in cites if r.get("disposition") == "auto-applied"]
        with_adr = [r for r in gated if re.search(r"adr-\d+", str(r.get("resolved_by") or ""), re.I)]
        adr_decs = resolving_adr_decisions(root, rows)
        adr_fixed = any(tokens_in(t, DB_CLIENT_SERVER) for t in adr_decs)
        # A strong baseline may *reason out* SQLite→Postgres in prose, or silently swap the datastore — both are
        # invisible to /status, the release gate, and the next skills. The lift is the structured, gated row + the
        # resolving ADR: surfaced through the amendment channel, not silently resolved.
        check("Reconcile caught it: a Tier-2 amendment row cites the SQLite/datastore contradiction, gated "
              "(not auto-applied), resolved_by an ADR — surfaced through the amendment channel, not silent prose",
              bool(with_adr) and not not_auto,
              f"tier-2 rows={len(t2)}; citing-datastore={len(cites)}; gated+ADR={len(with_adr)}; "
              f"dispositions={[r.get('disposition') for r in cites] or 'none'}")
        check("Tech-mandate flow: the resolving ADR's Decision names a client-server datastore (not still SQLite)",
              adr_fixed, f"resolving ADR decisions={len(adr_decs)}; names a client-server DB={adr_fixed}")
        # 3) Both, or neither (SKILL.md § Architecture write-path) — the row + resolving ADR are only half the
        #    tech-mandate flow: the stated constraint LINE must itself be amended. Positive-presence only (the
        #    honored direction): the post-run line names a client-server datastore. Never forbidden-absence — a
        #    real amended line may annotate what it was amended FROM, so the old embedded token lawfully appears
        #    in honoring content (and validity above already reads it from the source_quote).
        check("Both, or neither: the stated Datastore line itself was amended to name the client-server "
              "replacement (not just the amendment row + resolving ADR)",
              bool(tokens_in(datastore, DB_CLIENT_SERVER)), f"post-run Datastore line='{datastore[:80]}'")

    elif a.case == "underspecified-constraint":
        # 1) Validity — the datastore decision was genuinely underspecified. The flesh-out AMENDS the line to a
        #    concrete datastore, so post-run the [NEEDS CLARIFICATION] marker lives in the amendment `source_quote`
        #    (which preserves the original) rather than the constraint file.
        CLARIF = r"needs clarification|not yet decided|not committed|not chosen|open decision"
        sqs = source_quotes(rows)
        marker = bool(re.search(CLARIF, datastore, re.I)) or bool(re.search(CLARIF, sqs, re.I))
        check("Validity: the datastore was genuinely underspecified ([NEEDS CLARIFICATION], preserved in the "
              "constraint file or the amendment source_quote)",
              marker, f"datastore now='{datastore[:50]}'; marker in file|source_quote={marker}")
        # 2) Flesh-out — a Tier-2 row resolves the missing datastore decision, resolved by an ADR.
        t2 = tier2_rows(rows)
        flesh = [r for r in t2 if re.search(r"datastore|needs clarification|persistence|database", row_blob(r))]
        with_adr = [r for r in flesh if re.search(r"adr-\d+", str(r.get("resolved_by") or ""), re.I)]
        check("Flesh-out: a Tier-2 amendment row resolves the underspecified datastore decision, resolved_by an ADR",
              bool(with_adr),
              f"tier-2 rows={len(t2)}; resolving-datastore={len(flesh)}; with ADR={len(with_adr)}; "
              f"dispositions={[r.get('disposition') for r in flesh] or 'none'}")
        # 3) Concrete decision — the realization now names a concrete datastore the envelope lacked.
        concrete = tokens_in(realization, DB_CLIENT_SERVER + DB_EMBEDDED)
        check("Concrete decision: the realization (system.md / an ADR Decision) names a concrete datastore the "
              "envelope lacked",
              bool(concrete), f"datastore tokens now in realization={concrete or 'none'}")
        # 4) Both, or neither — the flesh-out must land on the constraint LINE too: the field no longer carries
        #    the [NEEDS CLARIFICATION] marker and names a concrete datastore on the line. (The marker survives in
        #    the amendment source_quote / continuation prose — honoring content, not staleness; constraint_field
        #    reads the field line only.)
        check("Both, or neither: the Datastore line itself was fleshed out — marker cleared from the field, a "
              "concrete datastore named on the line",
              not re.search(CLARIF, datastore, re.I) and bool(tokens_in(datastore, DB_CLIENT_SERVER + DB_EMBEDDED)),
              f"post-run Datastore line='{datastore[:80]}'")

    grade_verify_live_adr(root)
    emit(a)


def _self_test_s18():
    """Grader-first bite proof for S18 (WS6): the ideal passes, the uncited degenerate fires, the no-verify-live
    tree is N/A — deterministic, over hand-built architecture trees. The check_build.py --self-test precedent."""
    import tempfile, shutil
    AC_DECL = ("# Architecture Constraints\n\n## Verify-live\n\n"
               "- **openclaw:** docs: https://openclaw.dev/docs · source: https://github.com/example/openclaw\n")
    AC_NONE = "# Architecture Constraints\n\n## Stack mandates\n\n- **Datastore:** PostgreSQL 16 (client-server).\n"
    AC_QUAL = ("# Architecture Constraints\n\n## Verify-live\n\n"
               "- **BGE-M3 (embedding model):** docs: https://example.dev/bge · source: https://github.com/example/bge\n")
    AC_UPPER = ("# Architecture Constraints\n\n## Verify-live\n\n"
                "- **BGE-M3:** docs: https://example.dev/bge · source: https://github.com/example/bge\n")
    ADR_CITED = ("# ADR-002: Adopt OpenClaw for the agent loop\n\n"
                 "- **Verified-against:** docs/verification/openclaw.md (openclaw@0.4.2)\n\n"
                 "## Decision Outcome\n\n**Chosen:** OpenClaw, because it is the mandated host framework.\n")
    ADR_UNCITED = ("# ADR-002: Adopt OpenClaw for the agent loop\n\n"
                   "## Decision Outcome\n\n**Chosen:** OpenClaw, because it is the mandated host framework.\n")
    ADR_BGE_CITED = ("# ADR-003: Embedding model\n\n"
                     "- **Verified-against:** docs/verification/bge-m3.md (bge-m3@1.0)\n\n"
                     "## Decision Outcome\n\n**Chosen:** BGE-M3, for one-pass dense+sparse embedding.\n")
    ADR_BGE_UNCITED = ("# ADR-003: Embedding model\n\n"
                       "## Decision Outcome\n\n**Chosen:** BGE-M3, for one-pass dense+sparse embedding.\n")
    RECORD = ("---\nverified_against: openclaw@0.4.2\n---\n\n## Verified claims\n\n"
              "| claim | citation | corrects |\n|---|---|---|\n"
              "| Claw.run(task) is the entry point | https://openclaw.dev/docs#loop | — |\n")
    RECORD_BGE = ("---\nverified_against: bge-m3@1.0\n---\n\n## Verified claims\n\n"
                  "| claim | citation | corrects |\n|---|---|---|\n"
                  "| emits dense and sparse vectors in one pass | https://example.dev/bge#modes | — |\n")

    def build(tmp, ac, adr, record, record_rel):
        def w(rel, s):
            p = os.path.join(tmp, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(s)
        w("docs/spec/architecture-constraints.md", ac)
        if adr is not None:
            w("docs/architecture/adr/ADR-002.md", adr)
        if record:
            w(record_rel, record)

    # name, ac, adr, record_text, record_rel, want_passed, want_na
    scenarios = [
        ("ideal (ADR cites a resolving record)", AC_DECL, ADR_CITED, RECORD,
         "docs/verification/openclaw.md", True, False),
        ("degenerate (verify-live ADR, no citation)", AC_DECL, ADR_UNCITED, RECORD,
         "docs/verification/openclaw.md", False, False),
        ("degenerate (citation to a missing record)", AC_DECL, ADR_CITED, None,
         "docs/verification/openclaw.md", False, False),
        ("N/A (no verify-live declared)", AC_NONE, ADR_CITED, RECORD,
         "docs/verification/openclaw.md", True, True),
        ("qualified label links + validates (real-output-shaped)", AC_QUAL, ADR_BGE_CITED, RECORD_BGE,
         "docs/verification/bge-m3.md", True, False),
        ("qualified label FIRES on an uncited ADR", AC_QUAL, ADR_BGE_UNCITED, RECORD_BGE,
         "docs/verification/bge-m3.md", False, False),
        ("uppercase bare label links the lowercase record", AC_UPPER, ADR_BGE_CITED, RECORD_BGE,
         "docs/verification/bge-m3.md", True, False),
    ]
    rows, ok = [], True
    for name, ac, adr, record, record_rel, want_passed, want_na in scenarios:
        tmp = tempfile.mkdtemp(prefix="s18-")
        try:
            build(tmp, ac, adr, record, record_rel)
            results.clear()
            grade_verify_live_adr(tmp)
            entry = next((r for r in results if "S18" in r["text"]), None)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        got_passed = bool(entry and entry["passed"])
        got_na = bool(entry and "N/A" in entry["text"])
        good = entry is not None and got_passed == want_passed and got_na == want_na
        rows.append((name, "passed=%s na=%s" % (want_passed, want_na), good,
                     "" if good else "got passed=%s na=%s entry=%s" % (got_passed, got_na, bool(entry))))
        ok = ok and good
    results.clear()
    w = max(len(r[0]) for r in rows)
    print("\n== check_architecture.py S18 (verify-live ADR citation) self-test ==")
    for name, exp, good, note in rows:
        print("  [%s] %s  %s  %s" % ("PASS" if good else "FAIL", name.ljust(w), exp, note))
    print("\n%s" % ("ALL GOOD — S18 bites (ideal passes, uncited/missing fire, no-decl is N/A)"
                    if ok else "S18 SELF-TEST FAILED"))
    return ok


def _ideal_modules_tree(tmp):
    """The ONE ideal data-modules tree; degenerates are single-element deletions of it (the mutation principle,
    design §6). Every DA check's positive element lives in exactly one place so a deletion isolates one clause."""
    def w(rel, s):
        p = os.path.join(tmp, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(s)
    w("docs/spec/specification.md",
      "# Specification — Beacon\n\n- **Profile:** agent-system\n"
      "- **Data:** retrieval(source-search) · grounded-writes(report-synthesis) · memory\n")
    w("docs/spec/capabilities/research.md",
      "# Research\n\n### REQ-001: Fan out research\nWorkers cover sources concurrently.\n"
      "### REQ-002: Grounded synthesis\nEvery claim cited.\n")
    w("docs/planning/sprints/sprint-01.md", "# Sprint 01\n\n## REQ-001: Fan out research\n## REQ-002: Grounded synthesis\n")
    w("docs/spec/architecture-constraints.md",
      "# Architecture Constraints — Beacon\n\n## Verify-live\n\n"
      "- **bge-m3:** docs: https://example.dev/bge · source: https://github.com/example/bge\n\n"
      "## Data architecture\n\n"
      "- **Retrieval corpus:** a persistent semantic index of fetched content; grows daily.\n"
      "- **Operator profiles:** per-operator research-interest profiles; operators may request deletion of their profile.\n")
    w("docs/spec/evals/research/synthesis.jsonl", '{"q": "seed", "expect_grounded": true}\n')
    w("docs/spec/amendment-log.json",
      '{"amendments": [{"id": "AMD-001", "req": null, "skill": "03-architect", "tier": 2,\n'
      '  "disposition": "approved", "source_quote": "Verify-live set", "supersedes": null, "resolved_by": "ADR-002"}]}\n')
    w("docs/verification/bge-m3.md",
      "---\nverified_against: bge-m3@1.0\n---\n\n## Verified claims\n\n| claim | citation | corrects |\n"
      "|---|---|---|\n| emits dense and sparse vectors in one pass | https://example.dev/bge#modes | — |\n")
    w("docs/architecture/system.md",
      "# System — Beacon\n\n## 9 · Reconcile\n\ncontext attestation: inputs [architecture realization, "
      "architecture-constraints + in-scope REQ blocks]; realization conversation: not provided\n")
    w("docs/architecture/adr/README.md", "# ADR index\n\n| ADR-001 | datastore |\n| ADR-002 | retrieval |\n| ADR-003 | memory |\n")
    w("docs/architecture/adr/ADR-001.md",
      "# ADR-001: Primary datastore\n\n- **Category:** classic\n"
      "- **Review-Trigger:** autovacuum lag persistently exceeds a healthy bound on the index table\n\n"
      "## Context & Problem Statement\n\nREQ-001 needs persistence. Decisive driver: data-model fit "
      "(rubric dimension 2) for REQ-001.\n\n"
      "## Considered Options\n\n1. PostgreSQL 16 (client-server)\n2. SQLite (embedded)\n\n"
      "## Decision Outcome\n\n**Chosen:** PostgreSQL 16 (client-server), the relational default.\n\n"
      "The durable commitment (relational + extensions) and the vendor/hosting pick (managed vs self-hosted) are "
      "two separate decisions — the vendor pick is deferred.\n\n"
      "Exit / migration cost: two-way door — standard SQL.\n")
    w("docs/architecture/adr/ADR-002.md",
      "# ADR-002: Retrieval — Stage-2 hybrid\n\n- **Category:** classic\n"
      "- **Verified-against:** docs/verification/bge-m3.md (bge-m3@1.0)\n\n"
      "## Decision Outcome\n\n**Chosen:** Stage 2 hybrid retrieval — lexical + dense fused by RRF; BGE-M3, "
      "1024 dimensions; reindex on an embedding swap or a chunking change.\n\n"
      "Chunking: a 512-token / 15% overlap baseline; short pages use document-level retrieval (an explicit "
      "no-chunk rationale).\n\nk-consistency: the eval metric's k equals the k sent to the generator.\n")
    w("docs/architecture/adr/ADR-003.md",
      "# ADR-003: Agent memory — semantic profiles\n\n- **Category:** memory\n\n"
      "## Context & Problem Statement\n\nGate-0 trigger: persistent entities across calls (operator profiles).\n\n"
      "## Decision Outcome\n\n**Chosen:** the semantic kind only, on a relational table; episodic and procedural "
      "have no fired trigger.\n\nLifecycle: a decay rule (with a TTL fallback) — unbounded retention is a named "
      "failure mode.\n\nSharing + authorization: shared read for the orchestrator; only the consolidator writes "
      "it (the authorization boundary).\n\nDeletion: an operator deletion request reaches derived forms — "
      "summaries, indices, and profile caches, not just source rows.\n")
    w("docs/architecture/specs/research.md",
      "# Feature Spec — Research\n\nServes: REQ-001, REQ-002 — the grounded-writes(report-synthesis) module.\n\n"
      "## Data-model changes\n\n| Table / field | Type | Constraints | Notes |\n|---|---|---|---|\n"
      "| research_jobs.id | uuid | pk | |\n\n"
      "## Components\n\n| Component | Layer | Responsibility | Location |\n|---|---|---|---|\n"
      "| CitationGate | backend | admission gate | src/gate.py |\n\n"
      "## Verification Contract\n\n| VC-ID | REQ | Method | Assertion |\n|---|---|---|---|\n"
      "| VC-01 | REQ-002 | eval-suite | dataset: docs/spec/evals/research/synthesis.jsonl; floor: 80% |\n\n"
      "Write-path admission rule: a schema check, then a referential check, then commit — enforced in code "
      "(the CitationGate component), which the model cannot bypass.\n\n"
      "Named ground-truth source: the job's own source-index snapshot, never sources generically.\n\n"
      "Threshold: 0 tolerance — a claim with an unresolvable citation is dropped before assembly.\n\n"
      "Fallback: refuse (drop the claim, terminal); no silent retry.\n")
    return tmp


def _ideal_nogate_tree(tmp):
    """The declined-direction ideal: Data declared, every trigger denied, need-gate declines with reasons.
    No Verify-live (S18 N/A), no substrate commitments, <=1 amendment row."""
    def w(rel, s):
        p = os.path.join(tmp, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(s)
    w("docs/spec/specification.md",
      "# Specification — Beacon\n\n- **Profile:** agent-system\n"
      "- **Data:** retrieval(handbook-lookup) · memory\n")
    w("docs/spec/capabilities/research.md",
      "# Research\n\n### REQ-001: Fan out research\nWorkers cover sources concurrently.\n"
      "### REQ-002: Grounded synthesis\nEvery claim cited.\n")
    w("docs/planning/sprints/sprint-01.md", "# Sprint 01\n\n## REQ-001: Fan out research\n## REQ-002: Grounded synthesis\n")
    w("docs/spec/architecture-constraints.md",
      "# Architecture Constraints — Beacon\n\n## Data architecture\n\n"
      "- **Reference handbook:** ~40 short, stable documents, revised quarterly; fits in a context window.\n"
      "- **Cross-session learning:** questions are independent; operators value a from-scratch read; no "
      "personalization is wanted.\n")
    w("docs/spec/amendment-log.json", '{"amendments": []}\n')
    w("docs/architecture/system.md",
      "# System — Beacon\n\n## 11 · Deferred\n\nretrieval declined: the handbook fits in context (Stage 0 — "
      "cache-and-stuff); memory declined: no Gate-0 trigger fires (independent questions, reproducibility "
      "valued).\n\n## 9 · Reconcile\n\ncontext attestation: inputs [architecture realization, "
      "architecture-constraints + in-scope REQ blocks]; realization conversation: not provided\n")
    w("docs/architecture/adr/README.md", "# ADR index\n\n| ADR-001 | datastore |\n")
    w("docs/architecture/adr/ADR-001.md",
      "# ADR-001: Primary datastore\n\n- **Category:** classic\n"
      "- **Review-Trigger:** autovacuum lag persistently exceeds a healthy bound on the jobs table\n\n"
      "## Context & Problem Statement\n\nREQ-001 needs persistence. Decisive driver: data-model fit "
      "(rubric dimension 2) for REQ-001.\n\n"
      "## Considered Options\n\n1. PostgreSQL 16 (client-server)\n2. SQLite (embedded)\n\n"
      "## Decision Outcome\n\n**Chosen:** PostgreSQL 16 (client-server), the relational default.\n\n"
      "The durable commitment (relational + extensions) and the vendor/hosting pick (managed vs self-hosted) are "
      "two separate decisions — the vendor pick is deferred.\n\n"
      "Exit / migration cost: two-way door — standard SQL.\n")
    w("docs/architecture/specs/research.md",
      "# Feature Spec — Research\n\nServes: REQ-001, REQ-002.\n\n"
      "## Data-model changes\n\n| Table / field | Type | Constraints | Notes |\n|---|---|---|---|\n"
      "| research_jobs.id | uuid | pk | |\n\n"
      "## Components\n\n| Component | Layer | Responsibility | Location |\n|---|---|---|---|\n"
      "| Orchestrator | backend | dispatches workers | src/orchestrator.py |\n\n"
      "## Verification Contract\n\n| VC-ID | REQ | Method | Assertion |\n|---|---|---|---|\n"
      "| VC-01 | REQ-001 | api-contract | POST /research returns 202 |\n")
    return tmp


def _self_test_data():
    """Grader-first bite proof for the data checks: the ideal passes everything; each degenerate is a
    single-element mutation and must flip exactly its target check (design §6, the mutation principle)."""
    import tempfile, shutil

    def run_case(tree, case, fixture_docs=None):
        results.clear()
        grade_data_arch(tree, sprint_reqs(tree), case, fixture_docs or os.path.join(tree, "docs"))
        grade_verify_live_adr(tree)
        return list(results)

    def entry(res, key):
        return next((r for r in res if key in r["text"]), None)

    rows, ok = [], True

    def expect(name, res, key, want_passed):
        nonlocal ok
        e = entry(res, key)
        good = e is not None and e["passed"] == want_passed
        rows.append((name, "%s passed=%s" % (key, want_passed), good,
                     "" if good else "got %s" % ("missing entry" if e is None else e["passed"])))
        ok = ok and good

    # 1 — the ideal tree passes every check
    tmp = tempfile.mkdtemp(prefix="da-")
    try:
        _ideal_modules_tree(tmp)
        res = run_case(tmp, "data-modules")
        bad = [r["text"] for r in res if not r["passed"]]
        good = not bad
        rows.append(("ideal data-modules tree: ALL checks pass", "all passed", good,
                     "" if good else "failing: %s" % bad[:3]))
        ok = ok and good
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    def mutated(mutate):
        """Build the ideal tree, apply one mutation, grade it, tear down."""
        t = tempfile.mkdtemp(prefix="da-")
        try:
            _ideal_modules_tree(t)
            mutate(t)
            return run_case(t, "data-modules")
        finally:
            shutil.rmtree(t, ignore_errors=True)

    def edit(t, rel, old, new):
        p = os.path.join(t, rel)
        s = read(p) or ""
        assert old in s, "mutation anchor missing: %s in %s" % (old[:40], rel)
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(s.replace(old, new))

    expect("T01 fires: memory declared, ADR-003 deleted (unrealized)",
           mutated(lambda t: os.remove(os.path.join(t, "docs/architecture/adr/ADR-003.md"))),
           "DA-T01", False)
    expect("T02 fires: dataset ref points at a missing file",
           mutated(lambda t: edit(t, "docs/architecture/specs/research.md",
                                  "docs/spec/evals/research/synthesis.jsonl",
                                  "docs/spec/evals/research/missing.jsonl")),
           "DA-T02", False)
    expect("T03 fires: the admission-rule paragraph removed",
           mutated(lambda t: edit(t, "docs/architecture/specs/research.md",
                                  "Write-path admission rule: a schema check, then a referential check, then "
                                  "commit — enforced in code (the CitationGate component), which the model "
                                  "cannot bypass.\n\n", "")),
           "DA-T03", False)

    expect("T04 fires: only one considered option",
           mutated(lambda t: edit(t, "docs/architecture/adr/ADR-001.md", "2. SQLite (embedded)\n", "")),
           "DA-T04", False)
    expect("T04 fires: Review-Trigger line removed",
           mutated(lambda t: edit(t, "docs/architecture/adr/ADR-001.md",
                                  "- **Review-Trigger:** autovacuum lag persistently exceeds a healthy bound on "
                                  "the index table\n", "")),
           "DA-T04", False)
    expect("T04 fires: Review-Trigger is 'review periodically'",
           mutated(lambda t: edit(t, "docs/architecture/adr/ADR-001.md",
                                  "autovacuum lag persistently exceeds a healthy bound on the index table",
                                  "review periodically each quarter")),
           "DA-T04", False)
    expect("T04 fires: exit-cost statement removed",
           mutated(lambda t: edit(t, "docs/architecture/adr/ADR-001.md",
                                  "Exit / migration cost: two-way door — standard SQL.\n", "")),
           "DA-T04", False)
    expect("T04 fires: durable-vs-vendor split paragraph removed",
           mutated(lambda t: edit(t, "docs/architecture/adr/ADR-001.md",
                                  "The durable commitment (relational + extensions) and the vendor/hosting pick "
                                  "(managed vs self-hosted) are two separate decisions — the vendor pick is "
                                  "deferred.\n\n", "")),
           "DA-T04", False)
    expect("T04 exit-cost recognized via migration-effort phrasing (data-modules with_skill triage)",
           mutated(lambda t: edit(t, "docs/architecture/adr/ADR-001.md",
                                  "Exit / migration cost: two-way door — standard SQL.",
                                  "Migrating off this engine later is a real migration project; accepted because "
                                  "standard SQL keeps the corpus contents movable.")),
           "DA-T04", True)
    expect("T04 recognizes a rubric-walked 'no datastore' decision (data-nogate with_skill triage)",
           mutated(lambda t: edit(t, "docs/architecture/adr/ADR-001.md",
                                  "**Chosen:** PostgreSQL 16 (client-server), the relational default.",
                                  "**Chosen:** no persistent datastore this sprint — run state is held in "
                                  "process only and discarded on completion.")),
           "DA-T04", True)

    expect("T05 fires: dims+reindex sentence removed",
           mutated(lambda t: edit(t, "docs/architecture/adr/ADR-002.md",
                                  "; BGE-M3, 1024 dimensions; reindex on an embedding swap or a chunking change",
                                  "")),
           "DA-T05", False)
    expect("T05 fires: chunking paragraph removed",
           mutated(lambda t: edit(t, "docs/architecture/adr/ADR-002.md",
                                  "Chunking: a 512-token / 15% overlap baseline; short pages use document-level "
                                  "retrieval (an explicit no-chunk rationale).\n\n", "")),
           "DA-T05", False)
    expect("T06 fires: threshold paragraph removed",
           mutated(lambda t: edit(t, "docs/architecture/specs/research.md",
                                  "Threshold: 0 tolerance — a claim with an unresolvable citation is dropped "
                                  "before assembly.\n\n", "")),
           "DA-T06", False)
    expect("T06 fires: LLM-issued queries added with no driver-layer rule (conditional, required direction)",
           mutated(lambda t: edit(t, "docs/architecture/specs/research.md",
                                  "Fallback: refuse (drop the claim, terminal); no silent retry.\n",
                                  "Fallback: refuse (drop the claim, terminal); no silent retry.\n\n"
                                  "Workers issue LLM-generated SQL queries against the corpus database.\n")),
           "DA-T06", False)
    expect("T07 fires: sharing+authz paragraph removed",
           mutated(lambda t: edit(t, "docs/architecture/adr/ADR-003.md",
                                  "Sharing + authorization: shared read for the orchestrator; only the "
                                  "consolidator writes it (the authorization boundary).\n\n", "")),
           "DA-T07", False)
    expect("T07 sharing morphology: a reasoned gerund-form decline ('Sharing + authorization: N/A — ...') "
           "still counts as named-together (2026-07 bridge-run shape)",
           mutated(lambda t: edit(t, "docs/architecture/adr/ADR-003.md",
                                  "Sharing + authorization: shared read for the orchestrator; only the "
                                  "consolidator writes it (the authorization boundary).",
                                  "Sharing + authorization: N/A — single-agent per run; ephemeral workers "
                                  "never touch the store; only the consolidator writes it.")),
           "DA-T07", True)
    expect("T07 fires: deletion promised but derived-reach paragraph removed",
           mutated(lambda t: edit(t, "docs/architecture/adr/ADR-003.md",
                                  "Deletion: an operator deletion request reaches derived forms — summaries, "
                                  "indices, and profile caches, not just source rows.\n", "")),
           "DA-T07", False)

    def _mut_no_promise_no_reach(t):
        edit(t, "docs/spec/architecture-constraints.md",
             "- **Operator profiles:** per-operator research-interest profiles; operators may request deletion "
             "of their profile.\n", "")
        edit(t, "docs/architecture/adr/ADR-003.md",
             "Deletion: an operator deletion request reaches derived forms — summaries, indices, and profile "
             "caches, not just source rows.\n", "")
    expect("T07 N/A direction: no promise in the spine + no reach paragraph still PASSES",
           mutated(_mut_no_promise_no_reach), "DA-T07", True)

    t_fx, t_ws = tempfile.mkdtemp(prefix="da-fx-"), tempfile.mkdtemp(prefix="da-ws-")
    try:
        _ideal_modules_tree(t_fx); _ideal_modules_tree(t_ws)
        edit(t_ws, "docs/spec/capabilities/research.md", "Every claim cited.", "Every claim cited, mostly.")
        results.clear()
        grade_data_arch(t_ws, sprint_reqs(t_ws), "data-modules", os.path.join(t_fx, "docs"))
        res = list(results)
    finally:
        shutil.rmtree(t_fx, ignore_errors=True); shutil.rmtree(t_ws, ignore_errors=True)
    expect("Capabilities check fires on an edited REQ file", res, "content-identical", False)

    def mutated_ng(mutate):
        """Build the ideal nogate tree, apply one mutation, grade it (data-nogate), tear down."""
        t = tempfile.mkdtemp(prefix="ng-")
        try:
            _ideal_nogate_tree(t)
            mutate(t)
            return run_case(t, "data-nogate")
        finally:
            shutil.rmtree(t, ignore_errors=True)

    # ideal nogate tree: ALL checks pass (mirror the modules all-pass row)
    tmp = tempfile.mkdtemp(prefix="ng-")
    try:
        _ideal_nogate_tree(tmp)
        res = run_case(tmp, "data-nogate")
        bad = [r["text"] for r in res if not r["passed"]]
        good = not bad
        rows.append(("ideal data-nogate tree: ALL checks pass", "all passed", good,
                     "" if good else "failing: %s" % bad[:3]))
        ok = ok and good
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    expect("selectivity fires: a vector-index Data-model row added",
           mutated_ng(lambda t: edit(t, "docs/architecture/specs/research.md",
                                     "| research_jobs.id | uuid | pk | |\n",
                                     "| research_jobs.id | uuid | pk | |\n"
                                     "| source_index.embedding | vector(1024) | HNSW index | |\n")),
           "selectivity", False)
    expect("selectivity fires: a memory-store Components row added",
           mutated_ng(lambda t: edit(t, "docs/architecture/specs/research.md",
                                     "| Orchestrator | backend | dispatches workers | src/orchestrator.py |\n",
                                     "| Orchestrator | backend | dispatches workers | src/orchestrator.py |\n"
                                     "| MemoryStore | backend | profile store | src/memory.py |\n")),
           "selectivity", False)
    expect("amendment bound fires: 2 rows on a declined line",
           mutated_ng(lambda t: edit(t, "docs/spec/amendment-log.json", '{"amendments": []}',
                                     '{"amendments": [{"id": "AMD-001", "tier": 2, "disposition": "approved", '
                                     '"source_quote": "a", "resolved_by": "ADR-001"}, {"id": "AMD-002", "tier": 2, '
                                     '"disposition": "approved", "source_quote": "b", "resolved_by": "ADR-001"}]}')),
           "False-positive bound", False)
    expect("T01 fires on nogate: silent omission (decline mentions scrubbed)",
           mutated_ng(lambda t: edit(t, "docs/architecture/system.md",
                                     "retrieval declined: the handbook fits in context (Stage 0 — "
                                     "cache-and-stuff); memory declined: no Gate-0 trigger fires (independent "
                                     "questions, reproducibility valued).", "data modules: none adopted.")),
           "DA-T01", False)
    expect("selectivity ignores an in-memory (ephemeral) Data-model row (data-nogate with_skill triage)",
           mutated_ng(lambda t: edit(t, "docs/architecture/specs/research.md",
                                     "| research_jobs.id | uuid | pk | |\n",
                                     "| research_jobs.id | uuid | pk | |\n"
                                     "| In-memory run state | fields | discarded on completion |\n")),
           "selectivity", True)

    results.clear()
    w = max(len(r[0]) for r in rows)
    print("\n== check_architecture.py data (DA-T01..T08) self-test ==")
    for name, exp, good, note in rows:
        print("  [%s] %s  %s  %s" % ("PASS" if good else "FAIL", name.ljust(w), exp, note))
    print("\n%s" % ("ALL GOOD — data checks bite" if ok else "DATA SELF-TEST FAILED"))
    return ok


def _self_test_migration_negation():
    """Bite proof for the D4 destructive-change trigger: prose that names 'destructive' only inside its own
    negation ('non-destructive', incl. a hyphen line-wrap 'non-\\ndestructive') must NOT fire the trigger — a
    2026-07 bridge run FAILED D4 for declaring its migration explicitly non-destructive. A real destructive
    marker still fires, and a compliant migration section still passes."""
    import tempfile, shutil
    SPEC_NEG = ("# Feature\n\n## Data model\n\n| col | type |\n|---|---|\n| id | uuid |\n\n"
                "Future columns extend this table additively — a forward-compatible, non-\n"
                "destructive migration when a later sprint picks them up.\n\n"
                "## Verification Contract\n\n| VC-1 | unit | boolean |\n")
    SPEC_DESTR_BARE = ("# Feature\n\n## Data model\n\nWe drop column legacy_flag this sprint.\n\n"
                       "## Verification Contract\n\n| VC-1 | unit | boolean |\n")
    SPEC_DESTR_OK = (SPEC_DESTR_BARE +
                     "\n## Migration\n\nForward: `alembic upgrade head` (drops legacy_flag).\n"
                     "Rollback: schema-only; the dropped data is irreversible — rollback restores the column "
                     "with no data (compat noted).\n")
    def build(tmp, spec):
        p = os.path.join(tmp, "docs/architecture/specs/feature.md")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(spec)
    scenarios = [
        ("negated 'non-destructive' (wrapped) does NOT fire — D4 is N/A", SPEC_NEG, True, True),
        ("bare destructive DDL with no migration section FIRES", SPEC_DESTR_BARE, False, False),
        ("destructive DDL with forward cmd + rollback-compat passes", SPEC_DESTR_OK, True, False),
    ]
    rows, ok = [], True
    for name, spec, want_passed, want_na in scenarios:
        tmp = tempfile.mkdtemp(prefix="d4-")
        try:
            build(tmp, spec)
            results.clear()
            grade_migration_contract(tmp)
            entry = next((r for r in results if "Migration contract" in r["text"]), None)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        got_passed = bool(entry and entry["passed"])
        got_na = bool(entry and "N/A" in entry["text"])
        good = entry is not None and got_passed == want_passed and got_na == want_na
        rows.append((name, "passed=%s na=%s" % (want_passed, want_na), good,
                     "" if good else "got passed=%s na=%s" % (got_passed, got_na)))
        ok = ok and good
    results.clear()
    w = max(len(r[0]) for r in rows)
    print("\n== check_architecture.py D4 destructive-trigger negation self-test ==")
    for name, exp, good, note in rows:
        print("  [%s] %s  %s  %s" % ("PASS" if good else "FAIL", name.ljust(w), exp, note))
    print("\n%s" % ("ALL GOOD — D4 ignores negations, still bites on real destructive DDL"
                    if ok else "D4 NEGATION SELF-TEST FAILED"))
    return ok


def _self_test_mandate_line():
    """Grader-first bite proof for the tech-mandate LINE checks — "Both, or neither" (SKILL.md § Architecture
    write-path). A run that records the Tier-2 row + resolving ADR but leaves the stated constraint line unamended
    must FAIL the line check; the amended-line twin must PASS it. The amended trees are real-output-shaped: an
    amended line may lawfully annotate what it was amended FROM (the old token appears in honoring content), which
    is why the line check is positive-presence only. Each pair differs in exactly the constraint line, and the
    pre-existing discriminating checks must pass on BOTH twins — so the delta isolates the line check alone.
    Scenarios invoke the script end-to-end (subprocess): the full production path, argparse included."""
    import tempfile, shutil, subprocess
    SPEC = "# Specification — TeamPulse\n"
    SPRINT = "# Sprint 01\n\n### REQ-001: Post a pulse\n"
    AVAIL = "- **Availability:** two or more stateless app instances and a separate worker share one datastore.\n"
    AC_FT_AMENDED = ("# Architecture Constraints\n\n## Stack mandates\n\n"
                     "- **Datastore:** PostgreSQL (shared, client-server). "
                     "<!-- AMD-001: amended from \"SQLite (embedded, single-file)\" -->\n" + AVAIL)
    AC_FT_STALE = ("# Architecture Constraints\n\n## Stack mandates\n\n"
                   "- **Datastore:** SQLite (embedded, single-file; no external database server).\n" + AVAIL)
    AC_UC_FLESHED = ("# Architecture Constraints\n\n## Stack mandates\n\n"
                     "- **Datastore:** PostgreSQL 16 — a single shared, client-server RDBMS.\n" + AVAIL)
    AC_UC_STALE = ("# Architecture Constraints\n\n## Stack mandates\n\n"
                   "- **Datastore:** **[NEEDS CLARIFICATION]** — not yet decided; shared persistence is needed.\n"
                   + AVAIL)
    LOG_FT = ('{"amendments": [{"id": "AMD-001", "skill": "03-architect", "tier": 2, "disposition": "approved", '
              '"source_quote": "Datastore: SQLite (embedded, single-file; no external database server).", '
              '"resolved_by": "ADR-002"}]}')
    LOG_UC = ('{"amendments": [{"id": "AMD-001", "skill": "03-architect", "tier": 2, "disposition": "approved", '
              '"source_quote": "Datastore: [NEEDS CLARIFICATION] — not yet decided.", '
              '"resolved_by": "ADR-002"}]}')
    ADR = ("# ADR-002: Replace the datastore\n\n## Decision Outcome\n\n**Chosen:** PostgreSQL (client-server), "
           "because the availability mandate requires one shared store across instances.\n")

    def build(tmp, ac, log):
        for rel, s in [("docs/spec/specification.md", SPEC), ("docs/planning/sprints/sprint-01.md", SPRINT),
                       ("docs/spec/architecture-constraints.md", ac), ("docs/spec/amendment-log.json", log),
                       ("docs/architecture/adr/ADR-002.md", ADR)]:
            p = os.path.join(tmp, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(s)

    KEY = "line itself"
    scenarios = [
        ("forbidden-token: amended line (with amended-from annotation) passes",
         "forbidden-token", AC_FT_AMENDED, LOG_FT, True),
        ("forbidden-token: stale line (row + resolving ADR only) FIRES",
         "forbidden-token", AC_FT_STALE, LOG_FT, False),
        ("underspecified: fleshed-out line passes",
         "underspecified-constraint", AC_UC_FLESHED, LOG_UC, True),
        ("underspecified: marker still on the line FIRES",
         "underspecified-constraint", AC_UC_STALE, LOG_UC, False),
    ]
    rows, ok = [], True
    for name, case, ac, log, want in scenarios:
        tmp = tempfile.mkdtemp(prefix="mline-")
        try:
            build(tmp, ac, log)
            subprocess.run([sys.executable, os.path.abspath(__file__), "--outputs", tmp, "--case", case],
                           capture_output=True)
            try:
                with open(os.path.join(tmp, "grading.json"), encoding="utf-8") as fh:
                    exps = json.load(fh)["expectations"]
            except Exception:
                exps = []
            entry = next((r for r in exps if KEY in r["text"]), None)
            others = [r for r in exps if ("Reconcile caught it" in r["text"] or "Tech-mandate flow" in r["text"]
                                          or "Flesh-out" in r["text"])]
            others_ok = bool(others) and all(r["passed"] for r in others)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        good = entry is not None and entry["passed"] == want and others_ok
        rows.append((name, "line-check passed=%s" % want, good,
                     "" if good else "got entry=%s passed=%s others_ok=%s"
                     % (bool(entry), entry["passed"] if entry else None, others_ok)))
        ok = ok and good
    w = max(len(r[0]) for r in rows)
    print("\n== check_architecture.py tech-mandate LINE (\"Both, or neither\") self-test ==")
    for name, exp, good, note in rows:
        print("  [%s] %s  %s  %s" % ("PASS" if good else "FAIL", name.ljust(w), exp, note))
    print("\n%s" % ("ALL GOOD — the LINE check bites (amended passes, stale fires, discriminators constant)"
                    if ok else "TECH-MANDATE LINE SELF-TEST FAILED"))
    return ok


def emit(a):
    ok = sum(1 for r in results if r["passed"])
    print(f"\n=== {a.case}: {ok}/{len(results)} assertions passed ===")
    for r in results:
        print(f"  [{'PASS' if r['passed'] else 'FAIL'}] {r['text']}")
        if r["evidence"]:
            print(f"         -> {r['evidence']}")
    gj = os.path.join(a.outputs, "grading.json")
    try:
        with open(gj, "w", encoding="utf-8") as f:
            json.dump({"expectations": results}, f, indent=2)
        print(f"\nwrote {gj}")
    except Exception as e:
        print(f"\n(could not write grading.json: {e})")


if __name__ == "__main__":
    main()
