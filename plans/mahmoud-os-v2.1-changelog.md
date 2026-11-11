# Mahmoud OS v2.0 → v2.1 Change Log

> **Purpose:** Show how each finding from the independent v2.1 review was resolved, disputed, or deferred.
> **Date:** 2026-11-11

---

## Critical findings

| # | Finding | Resolution in v2.1 | Status |
|---|---|---|---|
| C1 | Next.js web shell contradicts New-forge Vite/React | Replaced every "Next.js web shell" reference with "React/Vite/React Flow web shell"; added explicit note that implementation extends `New-forge/apps/web`; `dynamic-factory` Next.js scaffold is now described as planning-file host only. | ✅ Resolved |
| C2 | Must items scheduled after P4 | Split "Must" into two buckets: "Must (first working release, P1–P4)" and "Must (complete product, P5–P11)". Re-phased Provider Registry, Allowance Governor, MCP Registry, Performance Rules Engine, LLM Council, Agent Studio dependencies so every P1–P4 Must is schedulable by P4. | ✅ Resolved |
| C3 | JEV Routing Agent is a "first-class agent" before Agent Studio | Kept JEV required (not optional). Clarified that JEV is a required system capability with a versioned system profile/routing configuration; it does not depend on Agent Studio's general editing UI. Added explicit schedule: JEV gateway module is P1; optional agent-based routing review is P4. | ✅ Resolved |
| C4 | Canonical hierarchy forces milestones/epics on every project | Added two explicit tracks: **Simple workflow track** (default) and **Forge SDLC track** (opt-in per project). Simple track is `Project → Workflow binding → Run → Step → Attempt`. | ✅ Resolved |
| C5 | P0 gate "base branch green on CI" unrealistic | Kept existing wording which already allows blocker reporting. Added emphasis: "baseline branch pinned; CI state and blockers honestly reported; non-waivable security controls enforced." No change needed. | ✅ Disputed / already correct |
| C6 | "Lossless copy/paste is impossible" | Replaced "lossless" with **"schema-preserving"** and defined exact scope: preserves workflow definition, nodes, groups, ports, edges, I/O contracts, required capabilities, provenance; explicitly excludes secrets, approvals, execution state, environment-specific config. | ✅ Resolved |
| C7 | The Bridge is a component but not scheduled | Added The Bridge as a P1 deliverable with explicit responsibilities in §5.3 and §18 P1 acceptance. | ✅ Resolved |

---

## High findings

| # | Finding | Resolution in v2.1 | Status |
|---|---|---|---|
| H1 | Provider Registry + Allowance Governor conflated as one P5 item | Split into: `Minimal Provider Registry` (Must P1/P2), `Allowance Governor` (Must P2/P3), and `Advanced failover / model rebinding` (Should P5). | ✅ Resolved |
| H2 | MCP/Connector Registry marked Must P6, but creator journey needs it earlier | Split into: `Minimal MCP/Connector Registry UI` (Must P1/P2) and `Real connectors (Gmail/Calendar/Drive/GitHub)` (Must P4/P6). | ✅ Resolved |
| H3 | Exact 31 performance criteria not listed | Added **Appendix A** with all 31 criteria (PERF-01 through PERF-31), detection methods, and priorities, copied verbatim from Mahmoud OS prompt v2.0 §28. | ✅ Resolved |
| H4 | Project import mentioned but undefined | Defined four import modes with Must/Should/Future classification: blank project, GitHub repo link, document upload, New-forge project fork, forge-ai legacy import. | ✅ Resolved |
| H5 | workflow-observer role unresolved | Added explicit disposition: "Bounded monitoring/UI adapter pattern; optional module." Retained as open decision #7 because final retirement vs. reuse still needs user confirmation, but no longer blocks architecture description. | ⚠️ Partially resolved / open decision |

---

## Medium findings

| # | Finding | Resolution in v2.1 | Status |
|---|---|---|---|
| M1 | "OpenCode Go" vs "OpenCode CLI" inconsistency | Standardized on "OpenCode CLI" for user-facing references and "OpenCode Go" only when referring to the service binary implementation. | ✅ Resolved |
| M2 | F01–F50 mapping lacks disposition verbs and owners | Updated F-table with precise verbs (Preserve as-is, Extend, Reuse, Reimplement, Add, Out of scope) and added an Owner column. | ✅ Resolved |
| M3 | 70/30 quota policy asserted without source | Cited exact source: New-forge `AGENTS.md` line 36, `C-007/C-007a`. Added reference in §15. | ✅ Resolved |
| M4 | Hermes safeguards were policy without mechanism | Added §10.3 "Concrete isolation and write-approval mechanisms" with read-only API role, proposal staging, dual approval gate, version binding, future-only effect, no recursive self-review, no executable installation through memory approval. | ✅ Resolved |
| M5 | P4 acceptance omitted provider/connector state | Updated P4 acceptance rule and Must matrix to include: tool/model call respects minimal provider registry; disconnected connector shown as Not connected. | ✅ Resolved |

---

## Full-product commitments restored

| Commitment | Where added in v2.1 |
|---|---|
| Obsidian basic plugin/interface | §18 P1: actual packaged plugin, pair, ask JEV, send note/selection, save responses, show status, disconnect/revoke. Feature priority row 13: Must P1. |
| LLM Council | §9 full section; feature priority row 38: Must P5. |
| Information icons | §14: v2-info pattern; feature priority row 17: Must P1. |
| Categorized search | §14 and §18 P1; feature priority row 18: Must P1. |
| Schedules and notifications | §18 P8; feature priority row 40: Must P8. |
| Safe external-action handling | §18 P3; feature priority row 31: Must P3. |

---

## Disputed prior recommendations

| Original recommendation | Dispute | Final v2.1 treatment |
|---|---|---|
| Put every Must feature before P4 | User/GPT: P4 is the first working release; later Must features remain required for complete product. | Split Must into "first working release (P1–P4)" and "complete product (P5–P11)" buckets. |
| Make JEV agent optional | User/GPT: Keep JEV required; its system profile can exist before Agent Studio UI. | JEV is required P1 system capability; optional agent-based review P4. |
| Change P0 because CI must already be green | User/GPT: existing wording already allows blocker reporting; discovery continues; non-waivable controls enforced. | No wording change needed; clarified emphasis only. |
| "Lossless copy/paste is impossible" | User/GPT: define scope as preserving supported definitions/ports/edges/contracts; remap identities; exclude secrets/state. | Replaced with "schema-preserving" and defined exact inclusions/exclusions. |
| Move planning files out of dynamic-factory | User/GPT: optional housekeeping; location does not determine architecture. | Retained in place; noted as optional future housekeeping. |
| Treat 70/30 policy as unconfirmed | User/GPT: it is recorded in New-forge owner-decision application; cite it. | Cited `AGENTS.md:36` and `C-007/C-007a`; preserved accounting conditions. |

---

## Files changed

| File | Change |
|---|---|
| `plans/mahmoud-os-master-blueprint-v2.1.md` | New corrected blueprint |
| `plans/mahmoud-os-feature-priority-v2.1.md` | New corrected priority/milestone matrix |
| `plans/mahmoud-os-v2.1-changelog.md` | This change log |

No existing source files were modified.

---

## Remaining open decisions

| # | Decision | Why it still blocks |
|---|---|---|
| 1 | New-forge baseline branch (`main` vs `develop`) | P0 cannot start without a pinned baseline. |
| 2 | Repository location (`dynamic-factory` vs new Mahmoud OS repo) | Affects branch strategy and how New-forge is consumed. |
| 3 | workflow-observer role (reuse vs retire) | Final adapter/retirement decision needs user confirmation. |
| 4 | Obsidian sync mode (filesystem watcher vs plugin REST bridge) | Affects P1 implementation and security model. |
| 5 | Voice (required vs experimental) | Affects P1/P3 scope. |
| 6 | Deployment target (local-only vs private cloud vs SaaS-ready) | Affects operations packaging priority. |

---

*No application changes or installations made.*
