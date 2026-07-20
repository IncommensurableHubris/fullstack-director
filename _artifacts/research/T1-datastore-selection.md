# T1 — Datastore Selection: Research Brief

**Pillar:** How a world-class architect chooses and justifies datastores in 2026.
**Method:** Live web research (WebSearch/WebFetch), July 2026. No local repository files read.
**Sources:** 30+ distinct URLs across primary, independent-analyst, and vendor tiers. Full registry with dates/tags in §7.

---

## 1. Executive Summary

1. **2026 default posture: start relational (Postgres), add extensions, split out only at a named breakpoint.** CONSENSUS across independent and vendor sources. DURABLE as a posture; the specific extensions that make it credible are FAST-MOVING.
2. **HTAP-as-single-engine has not displaced "two engines + CDC."** The dominant real architecture for combined OLTP+OLAP is still separate stores linked by low-latency change-data-capture, not a unified engine. CONSENSUS, structurally DURABLE.
3. **CAP is a theory exercise; PACELC is the practically-used framing.** Sources converge on PACELC because it captures the latency/consistency tradeoff architects face daily, versus CAP which only fires during rare partitions. CONSENSUS, DURABLE.
4. **DDIA got a 2nd edition** (Kleppmann + Riccomini, O'Reilly, March 2026). Its central reframing is disaggregated storage (object-store-as-primary, compute/storage separation) plus a control/data/compute-plane split and new AI-era data-systems material. The single biggest "canonical anchor moved" event for this pillar. Fact-level CONSENSUS; the framing is intended to be DURABLE for a decade.
5. **In-process/embedded OLAP (DuckDB and peers) is a genuinely new rung** between "query Postgres directly" and "stand up a warehouse," now production-credible, with `pg_duckdb` delivering columnar speed without leaving Postgres. CONSENSUS on readiness; FAST-MOVING on which tool.
6. **The managed-Postgres landscape consolidated:** Databricks acquired Neon for ~$1B (announced May 14, 2025), explicitly framed around AI-agent-provisioned databases (Neon reported ~80% of new DBs were agent-created). FAST-MOVING landscape data signaling a DURABLE trend — databases as agent-provisioned, branchable, ephemeral resources.
7. **Documented Postgres write-throughput breakpoints exist from real postmortems** (Notion's 480-shard re-architecture, Figma's staged sharding). Triggers were write throughput and VACUUM/TXID pressure (Notion) and per-table I/O/CPU ceilings (Figma) — not vector search or JSONB. CONSENSUS; DURABLE as a failure-mode class.
8. **pgvector's scale ceiling is CONTESTED**, ranging "~10M" to "~50–100M with pgvectorscale" depending on who benchmarks and what recall/latency target is assumed — not a settled number.
9. **LLM-app architecture reweights existing categories rather than inventing new ones:** JSONB for trace/transcript metadata, a vector index for embeddings, a Redis-class semantic cache for hot-context reuse, a queue (pgmq or dedicated) in front of async inference. CONSENSUS, structurally DURABLE, tool choices FAST-MOVING.
10. **An ADR-worthy datastore decision records drivers, seriously-considered alternatives, the consistency/availability trade taken, and increasingly an exit/migration-cost line.** Lock-in research cites ~$315K average migration cost, pushing "exit strategy" from optional to expected. CONSENSUS on structure; the dollar figure is FAST-MOVING/context-dependent.

---

## 2. Findings

### 2.1 Structuring the decision (Q1)

**2.1.1 Workload-shape-first branching dominates.** Pure transactional → single OLTP store; pure analytical → dedicated warehouse; both at scale/concurrency → two engines + CDC; both but modest volume → HTAP or Postgres-plus-extensions. (ClickHouse Resource Hub [V], undated/2026-current; bigdataboutique "OLTP vs OLAP in 2026" [I], 2026.) CONSENSUS, DURABLE.

**2.1.2 A finer taxonomy is emerging to replace the coarse OLTP/OLAP/HTAP split.** Jack Vanlightly (independent, ex-Confluent/WarpStream) proposes six categories — Single Tier, Internal Tiering, Hybrid-Sync, Hybrid-Async, Materializing, Shared Tiering — by system count, workload count, sync/async data-visibility, and copy count, and explicitly challenges "zero-copy" marketing as murky in practice. (jack-vanlightly.com [I], June 22, 2026.) CONTESTED/emerging terminology, but the underlying dimensions are DURABLE.

**2.1.3 CAP is retired as a working tool in favor of PACELC.** CAP only constrains behavior during a (rare) partition; PACELC's "else" branch — the latency/consistency tradeoff during normal operation — is what's actually negotiated daily. Origin: Daniel Abadi, 2010/2012 (canonical via Wikipedia's PACELC entry [P]). Restated with fresh framing by javacodegeeks.com [I], April 2026. CONSENSUS, DURABLE.

**2.1.4 Consistency choice is per-data-type, not system-wide.** Teams often *inherit* a consistency model from framework/DB defaults rather than choosing it; mature systems mix strong consistency for critical writes with eventual consistency elsewhere. (Medium, "The Invisible Architecture," April 2026 [I].) CONSENSUS, DURABLE.

**2.1.5 Operational cost is argued in TCO terms.** Personnel dominates self-hosted TCO (cited: ops/maintenance ≈51% of 3-yr TCO; personnel up to 60%); managed needs ~0.25 FTE-equivalent vs. a dedicated DBA self-hosted; self-hosting TCO-crossover cited around "20+ databases with a platform team." (upcloud.com, usage.ai, hokstadconsulting.com [A], 2026, triangulated.) CONSENSUS on direction; numbers FAST-MOVING.

**2.1.6 "Choose boring technology" persists, with a new (contestable) justification.** McKinley's original heuristic (mcfunley.com [P], canonical) is reaffirmed, plus a 2026-specific argument: boring tech has the deepest AI-training-data footprint, so it gets the best AI-coding-tool support. One source explicitly flags this as possibly circular reasoning. (dev.to, brethorsting.com [I], July 2025.) CONTESTED on the AI-training-data corollary; CONSENSUS that boring remains the right default absent a forcing reason.

### 2.2 "Just use Postgres" and its documented breakpoints (Q2)

**2.2.1 The extension stack covers most secondary workloads.** Full-text/BM25 via `pg_textsearch`; vector via `pgvector`/`pgvectorscale` (HNSW/DiskANN); time-series via TimescaleDB; documents via JSONB; caching via UNLOGGED tables; queues via `pgmq`; geospatial via PostGIS. Postgres cited as #1 "most wanted" DB in secondary reporting of the 2026 Stack Overflow survey, ~12% YoY adoption growth, with the 300+-extension ecosystem cited as the actual driver over the core engine. (Tiger Data/Timescale [V]; corroborated by dev.to [A], 2026.) CONSENSUS on breadth. DURABLE structurally; extension maturity is FAST-MOVING.

**2.2.2 Vendor benchmark claims need a vendor-claim flag.** Tiger Data's claim that pgvectorscale beats Pinecone "28x on p95 latency, 16x on throughput at 99% recall" is a vendor claiming superiority over a named competitor — evidence of competitiveness, not a neutral number. Treat as landscape data only.

**2.2.3 Documented breakpoints come from real postmortems, not marketing.** **Notion** [P] (own eng blog): after 5 years/four orders-of-magnitude growth, VACUUM began stalling and TXID wraparound became existential; moved to 480 logical shards across 32 physical DBs, partitioned by workspace ID; double-write throughput was the migration bottleneck. **Figma** [P] (own eng blog): ran on AWS's largest instance by 2020, then a dozen+ vertically-partitioned DBs by 2022, then horizontal sharding as individual tables (billions of rows, TBs) hit disk/CPU/I/O ceilings independent of overall DB size. CONSENSUS this breakpoint class is real; DURABLE — the mechanism (MVCC/autovacuum pressure at high churn, per-table hotspotting) is structural to Postgres, not point-in-time.

**2.2.4 Generic "how big can one Postgres get" numbers are soft and contradictory — treat as illustrative only.** One aggregator cites "~100GB, Seed-to-Series-A" with signals like ">200M rows in one table" or "20%+ MoM latency degradation despite tuning" (velodb.io [V]); other sources decline to give any number, stating it's tuning/hardware/workload-dependent. CONTESTED on specific numbers; CONSENSUS that *symptom-based* triggers (autovacuum falling behind, single-table I/O saturation, replica lag under normal load) are the right encoding, not a fixed GB/row threshold.

**2.2.5 Multi-region active-active is a "don't, unless," not a scaling default.** "Most PostgreSQL workloads do not require it... should be considered only after simpler designs are evaluated" (percona.community [I], June 2025); recommended default is active-passive DB + active-active application/edge layer. Postgres wasn't designed for concurrent multi-primary writes — conflict resolution remains a genuine hard problem. CONSENSUS, DURABLE (architectural property of Postgres's replication model).

**2.2.6 Named exception list where Postgres-first breaks down** (synthesized): sustained write throughput beyond single-primary capacity (Notion/Figma-class), true multi-region active-active with local-write-latency requirements, analytical scans at multi-TB+/petabyte scale with many concurrent analysts, vector search past tens-of-millions with strict low-latency+high-recall SLAs, graph workloads whose primary pattern is deep multi-hop traversal rather than shallow fan-out. CONSENSUS on the category list, DURABLE; numeric thresholds inside each category are FAST-MOVING.

### 2.3 OLAP in app context (Q3)

**2.3.1 Embedded/in-process OLAP is production-credible with a defined fit envelope.** DuckDB: in-process, columnar, vectorized (SIMD). 1.1 release stabilized the storage format; production use reported at Hex, Mode, and SaaS analytics products; MotherDuck [V] claims >10,000 paying teams by Q1 2026; major BI tools added native connectors. Suggested envelope: **under ~5TB, read-heavy, single-writer.** (Kestra [V], buildmvpfast.com [A], 2026.) CONSENSUS on readiness; envelope numbers FAST-MOVING, shape more DURABLE.

**2.3.2 `pg_duckdb` closes the gap between "Postgres is slow for analytics" and "stand up a warehouse."** Reached 1.0 in 2026; runs DuckDB's columnar engine inside Postgres against a Parquet-backed copy, intercepting analytical queries transparently (reported 10–100x speedups — extension-marketing-adjacent, treat cautiously). A materially new middle rung in the decision tree. CONSENSUS the pattern exists; DURABLE structurally.

**2.3.3 A separate analytical store is justified at multi-TB+ scale, high-concurrency BI load, or measurable OLTP degradation from analytical queries** — "if dashboards take longer than 3 seconds against Postgres" is the commonly cited trigger, beyond which a dedicated warehouse (ClickHouse/Snowflake/BigQuery) plus CDC applies. CONSENSUS, DURABLE as decision logic.

**2.3.4 Lakehouse formats (Iceberg/Delta) matter for app-scale mainly as a way to make object storage transactional — not a default for every app.** **Iceberg is the reported 2026 default for new, open lakehouses** (every major cloud, plus Databricks itself, reads/writes it); **Delta remains better-optimized inside Databricks/Microsoft Fabric.** With Iceberg v3 and Delta 4.0, raw capability has largely converged — the deciding factor is now platform ecosystem, not features. (dev.to/alexmercedcoder [V, author at Dremio], corroborated by datavidhya.com, atlan.com, datacamp.com [A].) CONSENSUS on convergence; DURABLE structurally (table-format-over-object-storage as a pattern), FAST-MOVING on which format "wins" a given year.

**2.3.5 For application-scale (not data-platform-scale) projects, lakehouse formats are usually premature** — relevant once a team is *building* a data platform (multiple consumers/engines, cross-team schema evolution/time-travel needs), not merely because one app's OLTP store has "a lot of data." Synthesis judgment from 2.3.4's framing. CONSENSUS by inference, DURABLE.

### 2.4 Serverless/managed landscape (Q4 — explicitly fast-moving)

**2.4.1** Two dominant camps: serverless Postgres (Neon, Supabase) and distributed SQLite (Turso, Cloudflare D1), with PlanetScale (historically MySQL/Vitess) now straddling both. (Multiple 2026 aggregator comparisons [A], triangulated.)

**2.4.2 Neon:** acquired by Databricks (~$1B, announced May 14, 2025 [P] — databricks.com, techcrunch.com, cnbc.com), explicitly for AI-agent-driven provisioning. Differentiators: scale-to-zero, instant git-like branching (copy-on-write fork in seconds). Post-acquisition pricing restructured (Aug 2025: compute −15–25%, storage −80% to $0.35/GB; by 2026 the $5/mo minimum was removed, fully usage-based).

**2.4.3 Supabase** remains independent — full backend platform (Postgres + auth + realtime + storage + edge functions + vector), not "just a database."

**2.4.4 PlanetScale added a from-scratch Postgres product** (private preview July 1, 2025 — planetscale.com [P], corroborated same-day by Simon Willison [I]; GA per InfoQ [I], Oct 2025), explicitly *not* reusing Vitess internals, building a separate sharding solution ("Neki," not yet fully open-sourced) from first principles. Signal: "which engine" is now a product-line choice even for MySQL-native vendors.

**2.4.5 Turso/libSQL is mid-transition** — moving from libSQL to a full Rust rewrite ("Turso Database"); vendor's own docs [P] state libSQL is "battle-tested for longer" while the new engine is "where development effort is focused." Turso Cloud currently runs on libSQL. Flag as live migration-in-progress risk for adopters today.

**2.4.6 Cloudflare D1** reached GA April 2024, added global read-replication in beta during 2025 (automatic per-region replicas, no extra charge) (developers.cloudflare.com [P]) — narrowing one of Turso's historical differentiators.

**2.4.7 Repeated use-case shorthand** (aggregator-tier [A] consensus, landscape not doctrine): solo/MVP → Supabase; Next.js/CI-heavy → Neon (branch-per-PR); latency-critical edge → Turso/D1; enterprise MySQL-scale-out-with-optionality → PlanetScale.

### 2.5 What an ADR-worthy datastore decision records (Q5)

**2.5.1 MADR is the concrete, currently-maintained template most relevant here** (current v4.0.0, released Sept 2024, still current — adr.github.io/madr [P]). Its structural edge over Nygard-style ADRs: it forces **named alternatives**, not just the winner — "the Nygard format leaves the loser unnamed unless the author chooses to add it. MADR fixes this." (ozimmer.ch [I], written by a MADR co-creator.) CONSENSUS, DURABLE.

**2.5.2 Common content skeleton:** Context (forces/constraints) → Decision Drivers (performance, scale, team expertise, cost, consistency) → Options Considered → Decision Outcome → Consequences (positive/negative/neutral). (Multiple template sources [A], corroborated by MADR primary.) CONSENSUS, DURABLE.

**2.5.3 Exit/migration cost is increasingly an explicit, expected line item.** Lock-in research cites ~$315K average enterprise migration cost, framing mature practice as: accept lock-in only when business value is clear *and* exit costs are understood, with standards-first design, reproducible/tested-portable backups, and vendor-specific features treated as deliberate (not accidental) commitments. (Mixed independent/consultancy [I/A], 2026.) CONSENSUS on the norm; dollar figure FAST-MOVING/context-dependent.

**2.5.4 Reversibility framing ("one-way door vs. two-way door")** is implicit across ADR literature's Consequences sections even where not named explicitly. Not directly sourced to a 2026 datastore-specific article this pass, but consistent with 2.5.2's structure — flagged as a strong checkable-teeth candidate regardless. DURABLE.

### 2.6 LLM-app-specific datastore pressures (Q6)

**2.6.1 LLM/agent workloads reweight the mix rather than requiring new categories.** Recommended: a dedicated table for embedding *metadata* (model name, dimensions, chunk provenance) separate from raw vectors; liberal JSONB for evolving application-specific metadata (no migrations); keep that metadata in Postgres alongside relational data even when vectors/similarity search live elsewhere. (jusdb.com [V].) CONSENSUS, DURABLE pattern.

**2.6.2 High-velocity agentic telemetry (traces, tool calls, tokens) strains Postgres's row-oriented model**, recommended once volume reaches "millions of logs" — directionally consistent with the independent OLAP-fit findings in 2.3.1–2.3.3. (motherduck.com [V], treat cautiously.) CONSENSUS directionally; DURABLE structurally (telemetry is naturally append-only/scan-heavy/columnar-friendly), thresholds FAST-MOVING.

**2.6.3 Semantic/hot-context caching is now a distinct named layer, Redis-dominant.** Common pattern: two-tier — exact-match cache (hash of prompt) plus semantic/vector-similarity cache for paraphrases, sometimes alongside a separate user-context KV layer; GPTCache also supports Milvus/Faiss/Qdrant as pluggable backends. (redis.io [V, describing a real shipping feature]; getmaxim.ai [I], 2026.) CONSENSUS the pattern exists; FAST-MOVING tooling, DURABLE underlying need.

**2.6.4 Queues in front of async inference are a default, not a luxury** — Postgres-native `pgmq` (adopted as Supabase Queues' backend) presented as sufficient for many teams before reaching for Kafka/SQS. (github.com/pgmq [P]; supabase.com [P].) CONSENSUS, extends the Postgres-first posture (2.2.1) naturally into LLM-app queueing. DURABLE pattern, FAST-MOVING tool choice.

**2.6.5 Native vector search is now a general-purpose-database norm, not a Postgres-only trick.** MongoDB Atlas Vector Search is first-class; Azure Cosmos DB (via DocumentDB/MongoDB-vCore compatibility) has native vector + full-text "directly within the engine," though lagging MongoDB's own feature velocity. AlloyDB's native-vector maturity was **not confirmed** with a strong 2026 source this pass (flagged gap). CONSENSUS that co-located vector capability is now multi-vendor; DURABLE trend, FAST-MOVING specifics.

### 2.7 DDIA 2nd edition: status and changes (Q7)

**2.7.1 Publication:** O'Reilly, March 2026, Kleppmann + new co-author Chris Riccomini (streaming/data-infra background). (martin.kleppmann.com [P], March 24, 2026; O'Reilly catalog [P].) ~60 pages longer than 1st edition; some chapters lightly edited, others (notably consistency-and-consensus) "almost completely rewritten." CONSENSUS (fact), DURABLE (now *the* canonical edition).

**2.7.2 Biggest structural shift — direct quote (via scylladb.com [V, quoting Kleppmann/Riccomini directly], March 26, 2026):**
> "At the time of the first edition, the model for databases was that a node ran on a machine, storing data on its local file system... Now we're increasingly seeing a model where storage is an object store" — a "new point in the tradeoff space that really wasn't present at the time of the first edition."
**Disaggregated storage** (compute/storage separation, object-store-as-primary) is now the baseline, not an edge case.

**2.7.3 Second theme: control/data/compute-plane separation** is, per Riccomini, "widely accepted now and has proven flexible when moving between SaaS and BYOC" — directly relevant to this pillar's managed-vs-self-hosted axis, reframing it as a three-way split rather than a binary.

**2.7.4 Third theme: a "moves with you" hypothesis** — "successful future databases will be able to move or scale with you, from your laptop, to your server, to your cloud" — citing DuckDB, MotherDuck, PGlite, and Postgres as emerging evidence. This elevates §2.3's embedded-OLAP findings from niche trend to a systemic property the field's canonical text now treats as desirable. DURABLE framing worth carrying into the skill's rubric.

**2.7.5 AI/LLM-era content added explicitly:** vector indexes, DataFrames (ML training-data prep), batch processing for training data, and (per secondary summary, lower confidence) "safe human-AI collaboration through well-defined database APIs." CONSENSUS at topic level (secondary corroboration only, e.g. Medium/robinali34.github.io [A]).

**2.7.6 Gap:** a full chapter-by-chapter ToC could not be retrieved live (O'Reilly chapter pages returned HTTP 403 to automated fetch); one secondary source's claim of "3 new/revised chapters" (Trade-offs in Data Systems Architecture, Defining Nonfunctional Requirements, The Trouble with Distributed Systems) is plausible but **not independently confirmed** against a primary ToC. Lean on 2.7.1–2.7.4 (primary-sourced themes) rather than any specific chapter list.

---

## 3. Candidate Decision Rubric

Dimensions in rough order of leverage/hardest-to-reverse first. Each has a **default** and **when-not** triggers.

**1. Workload shape (OLTP/OLAP/HTAP/mixed).** Default: OLTP-primary until proven otherwise. When-not: analytical scans are a first-class, high-concurrency pattern (not a monthly report) → plan a second engine or embedded-OLAP layer from day one, even if deployment is deferred.

**2. Data-model fit** (relational/document/KV/wide-column/graph/time-series/columnar/vector). Default: relational (Postgres) — the only model that cheaply hosts the other five as secondary patterns via extension (JSONB≈document, pgvector≈vector, TimescaleDB≈time-series, recursive CTEs≈shallow graph, pg_duckdb≈columnar). When-not: the secondary pattern becomes *primary* at real scale — deep multi-hop graph traversal (not shallow fan-out), vector search past tens-of-millions with strict recall+latency SLAs, or extreme-throughput wide-column workloads — name a purpose-built store explicitly, not "NoSQL" generically.

**3. Consistency & availability, via PACELC not CAP.** Default: strong consistency, single-region. When-not: name the *specific* product requirement forcing a tradeoff (e.g., "<50ms p99 reads from three continents" or "stay writable during a regional outage") — never weaken consistency generically "for scale."

**4. Scale envelope (single-node vs. distributed).** Default: single well-tuned node + read replicas until a symptom-based trigger fires. When-not (symptom, not fixed number): autovacuum consistently falling behind; a single table saturating I/O/CPU independent of overall load; write latency/throughput degrading despite tuning. Do not encode a fixed GB/row threshold — sources disagree sharply; encode the symptom.

**5. Operational maturity & cost (managed vs. self-hosted).** Default: managed, for any team without a dedicated platform/DBA function. When-not: 15–20+ databases with a platform team already in place, compliance/residency needs a managed vendor can't meet, or sustained scale where managed pricing crosses self-hosted TCO (illustrative signal: managed gets expensive in the $10–20K/month range where self-hosting could roughly halve it — treat as FAST-MOVING, not a hard rule).

**6. Team skill / "boring technology" bias.** Default: what the team can debug at 3am unaided. When-not: deviate only with a named, budgeted learning investment and a documented fallback.

**7. Exit/migration cost (reversibility).** Not a "when-not" — a mandatory line item either way. State one-way vs. two-way door; if lock-in is accepted, state why the value justifies the cost.

---

## 4. Checkable-Teeth Candidates

Presence/structure checks a Verification Contract could mechanically grade — existence and shape, not subjective quality.

1. **Named alternatives, plural.** ≥2 seriously-considered alternatives appear, not only the winner (2.5.1).
2. **Explicit driver naming from the rubric.** At least one sentence maps to a named §3 dimension (e.g., "decided on workload-shape + team-skill").
3. **Symptom-based revisit trigger.** A concrete, observable revisit condition (e.g., "if autovacuum lag exceeds X" / "at Y sustained writes/sec"), mirroring the Notion/Figma pattern (2.2.3) — not a vague "if we outgrow this."
4. **Exit/migration-cost statement, even if "not evaluated."** A dedicated section must exist (2.5.3); absence is the failure mode to catch.
5. **Reversibility classification.** One-way-door vs. two-way-door (or equivalent) stated explicitly (2.5.4).
6. **Durable-vs-fast-moving split.** The doc distinguishes the durable architectural commitment (e.g., "relational, strong consistency, single-region") from the fast-moving vendor pick (e.g., "hosted on Neon") as separate, non-conflated statements — maps directly onto the framework's own gate/auto-apply amendment-tier vocabulary.
7. **Specific extension naming for any "Postgres can do this" claim.** Any claim that a general-purpose store covers a secondary workload must name the specific mechanism (pgvector, pg_textsearch, pgmq) — not an unfalsifiable "Postgres can handle it" (2.2.1–2.2.2).
8. **REQ/NFR linkage.** The decisive driver traces to a specific REQ-ID, not a free-floating preference.
9. **Scale-envelope statement is symptom-based, not a bare number.** Quality check on item 3: catches the common failure of copying a blog's magic number (e.g., "100GB") instead of deriving a project-specific symptom (2.2.4).

---

## 5. What Changed Since Early 2025

- **Databricks acquired Neon (~$1B, May 14, 2025)**, framed around AI-agent-provisioned databases (~80% of new Neon DBs agent-created per company report). Triggered a full pricing restructure (storage $1.75→$0.35/GB by 2026; monthly minimums removed).
- **DDIA 2nd edition published (March 2026)** — the pillar's canonical anchor moved for the first time in ~10 years: disaggregated/object-store-primary storage as new baseline, control/data/compute-plane separation as accepted vocabulary, a "runs the same from laptop to cloud" hypothesis (DuckDB/MotherDuck/PGlite/Postgres), plus new AI-era content.
- **PlanetScale added a ground-up Postgres product** (preview July 2025, GA Oct 2025) alongside Vitess/MySQL, explicitly not reusing Vitess internals — "which engine" is now a product-line decision even for MySQL-native vendors.
- **Postgres extension maturity crossed credibility thresholds within ~12–18 months:** `pg_duckdb` hit 1.0 (in-Postgres columnar acceleration); `pgvectorscale` matured with published vendor benchmarks; `pg_textsearch` emerged as a named BM25 alternative; `pgmq` became Supabase Queues' backend. This is what makes 2026's "just use Postgres" materially stronger than the same claim in early 2025.
- **Cloudflare D1 added global read-replication** (beta, 2025), narrowing a historical Turso differentiator.
- **Turso began a from-scratch Rust rewrite** ("Turso Database") intended to replace libSQL; production traffic still runs on libSQL today — adopters are picking a vendor mid-engine-transition.
- **Iceberg and Delta materially converged** (Iceberg v3, Delta 4.0/Unity Catalog/UniForm) — the decision shifted from "which format is better" to "which platform ecosystem."
- **Vector search became a checkbox feature of general-purpose managed databases** beyond Postgres — MongoDB Atlas Vector Search and Cosmos DB's native vector+full-text both matured into first-class, in-engine capabilities during this window.

---

## 6. Contested Points Needing Designer Judgment

1. **pgvector/pgvectorscale's real crossover to a dedicated vector DB** — sources span ~10M to ~50–100M vectors depending on recall target and whether the source is vendor-sponsored. The skill should require the architect to state their own recall/latency/scale target rather than cite someone else's benchmark number.
2. **Whether "boring technology" needs updating for the AI-tooling era, or whether the AI-training-data argument is bias-laundering.** Genuinely open; don't resolve it, flag it as a judgment call.
3. **HTAP-as-single-engine vs. "two engines + CDC" as the better default when both workloads are real but modest.** CDC-based composability is the dominant real-world pattern, but HTAP is a legitimate choice when replication-lag-to-analytics matters more than peak performance either side — workload-specific enough to present as a genuine fork, not resolve with a default.
4. **Iceberg vs. Delta is now a platform-commitment question, not a technical one** (2.3.4) — route through "what platform are you already committed to," an upstream decision this pillar doesn't fully own.
5. **Is polyglot persistence increasing, or is multi-model consolidation (Cosmos DB, MongoDB-as-multi-model) the real 2026 trend?** Research surfaced both framings without resolution — likely genuinely context-dependent rather than a research gap.
6. **Turso's mid-transition engine risk** — whether to recommend it today given active core-engine replacement is a timing call; better generalized as "check whether a fast-moving vendor's core engine is stable or mid-transition" at use-time, not hard-coded.
7. **AlloyDB's native-vector specifics** — genuine research gap, not confirmed with a strong 2026 source; flag for follow-up if it becomes load-bearing.
8. **Exact TCO/managed-vs-self-hosted crossover thresholds** varied across sources and are pricing-cycle-dependent (2.1.5) — encode direction and reasoning, not specific numbers, which will stale quickly.

---

## 7. Source Registry

**[P]** primary/authoritative · **[I]** independent analyst/engineering blog · **[V]** vendor (product-interested party; claims about own product are landscape data, not neutral evidence) · **[A]** aggregator/comparison blog (triangulation only, lowest individual confidence)

- [P] Kleppmann, DDIA 2e announcement — martin.kleppmann.com/2026/03/24/designing-data-intensive-applications-2e.html — Mar 24, 2026
- [P] O'Reilly, DDIA 2nd Edition catalog — oreilly.com/library/view/designing-data-intensive-applications/9781098119058/ — 2026
- [V, quotes reliable] ScyllaDB, "Rethinking DDIA" (direct Kleppmann/Riccomini interview quotes) — scylladb.com/2026/03/26/rethinking-designing-data-intensive-applications/ — Mar 26, 2026
- [P] MADR site/GitHub — adr.github.io/madr/; github.com/adr/madr — v4.0.0, current
- [I] Zimmermann (MADR co-creator), ozimmer.ch/practices/2022/11/22/MADRTemplatePrimer.html
- [P] Wikipedia, PACELC design principle (orig. Daniel Abadi) — en.wikipedia.org/wiki/PACELC_design_principle
- [P] McKinley, "Choose Boring Technology" — mcfunley.com/choose-boring-technology
- [P] Notion Eng, "Herding elephants" / "The Great Re-shard" — notion.com/blog/sharding-postgres-at-notion; notion.com/blog/the-great-re-shard
- [P] Figma Eng, "Lived to Tell the Scale" / "growing pains" — figma.com/blog/how-figmas-databases-team-lived-to-tell-the-scale/; figma.com/blog/how-figma-scaled-to-multiple-databases/
- [P] Databricks press release, Neon acquisition — databricks.com/company/newsroom/press-releases/databricks-agrees-acquire-neon-help-developers-deliver-ai-systems — May 14, 2025
- [I] TechCrunch / CNBC, Databricks-Neon coverage — techcrunch.com/2025/05/14/; cnbc.com/2025/05/14/
- [P] PlanetScale, "Announcing PlanetScale for Postgres" — planetscale.com/blog/planetscale-for-postgres — Jul 2025
- [I] Simon Willison on PlanetScale/Postgres — simonwillison.net/2025/Jul/1/planetscale-for-postgres/ — Jul 1, 2025
- [I] InfoQ, PlanetScale Postgres GA — infoq.com/news/2025/10/planetscale-metal-postgres/ — Oct 2025
- [P] Cloudflare Docs, D1/Turso — developers.cloudflare.com/workers/databases/third-party-integrations/turso/
- [P] Turso docs/GitHub — docs.turso.tech/libsql; github.com/tursodatabase/turso
- [P] pgmq GitHub — github.com/pgmq/pgmq
- [P] Supabase Queues docs — supabase.com/docs/guides/queues
- [P] ThoughtWorks Radar / data mesh 2026 — thoughtworks.com/radar; thoughtworks.com/en-us/insights/blog/data-strategy/the-state-of-data-mesh-in-2026-from-hype-to-hard-won-maturity
- [P] Fowler, "Polyglot Persistence" — martinfowler.com/bliki/PolyglotPersistence.html
- [I] Vanlightly, storage/workload taxonomy — jack-vanlightly.com/blog/2026/6/21/ — Jun 22, 2026
- [I] bigdataboutique, "OLTP vs OLAP in 2026" — 2026
- [I] Percona Community, active-active Postgres — percona.community/blog/2025/06/18/ — Jun 18, 2025
- [I] javacodegeeks.com, "Beyond CAP" — Apr 2026
- [I] pganalyze, Figma/Notion scaling analysis — pganalyze.com/blog/5mins-postgres-partitioning-tables-between-servers-horizontal-sharding
- [I] brethorsting.com, "Choose Boring Technology, Revisited" — Jul 2025
- [V] Tiger Data/Timescale, "It's 2026, Just Use Postgres" + extensions usage post — tigerdata.com/blog/
- [V] MotherDuck, analytics/LLM database guides — motherduck.com
- [V] Kestra, "Embedded Databases in 2026" — kestra.io/blogs/embedded-databases
- [V] Dremio / Onehouse, Iceberg vs Delta — dremio.com/blog/; onehouse.ai/blog/
- [V] Redis, semantic cache docs — redis.io/docs/latest/develop/use-cases/semantic-cache/
- [V] MongoDB, Atlas Vector Search docs — mongodb.com/products/platform/atlas-vector-search
- [V] jusdb.com, LLM schema design; velodb.io, Postgres scaling; pgEdge, active-active
- [A] devtoolsacademy.com, devtoolreviews.com, pkgpulse.com, techsy.io, agentdeals.dev, buildmvpfast.com — serverless-DB comparisons, 2026
- [A] tanujgarg.com, tensoria.fr, vecstore.app, kalviumlabs.ai, marktechpost.com — vector-DB comparisons, 2026
- [A] datavidhya.com, tech-insider.org, atlan.com, datacamp.com, dev.to/alexmercedcoder — Iceberg/Delta comparisons, 2026
- [A] upcloud.com, usage.ai, hokstadconsulting.com — TCO comparisons, 2026
- [A] modern-datatools.com, algoroq.io, puppygraph.com, pedroalonso.net, dev.to/Manushev — Neo4j-vs-Postgres, 2026
- [A] getmaxim.ai — semantic caching survey, 2026

**Known gaps (flagged, not fabricated):** full DDIA 2e chapter-by-chapter ToC unconfirmed against a primary source (O'Reilly chapter pages returned HTTP 403 to automated fetch); AlloyDB native-vector maturity unconfirmed; Momento-vs-Redis semantic-cache parity unconfirmed.
