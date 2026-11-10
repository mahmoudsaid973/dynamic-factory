# Mahmoud OS — Feature Priority Classification v2.1

> **Purpose:** Classify every capability in the Mahmoud OS master blueprint into **Must for first working release (P1–P4)**, **Must for complete product (P5–P11)**, **Should**, and **Future / Nice-to-have**. This is a planning document; no code is changed.
> **Source:** `plans/mahmoud-os-master-blueprint-v2.1.md`
> **Version:** 2.1
> **Date:** 2026-11-11

---

## Summary

| Bucket | Definition |
|---|---|
| **Must (first working release, P1–P4)** | Required for the first shippable Mahmoud OS. P4 is the first working release with explicit included requirements. |
| **Must (complete product, P5–P11)** | Still required for the complete Mahmoud OS release, but scheduled after P4. A deferral needs a named reason, owner, and follow-up. |
| **Should** | Planned usability/depth enhancements; deferral needs a named reason, owner, and follow-up. They do not replace Must functionality. |
| **Future / Nice-to-have** | Outside the required initial complete release; do not add costs, installs, or complexity merely to include them. |

---

## 1. Must-have capabilities — first working release (P1–P4)

| # | Capability | Why it is a must | Phase | Depends on | Acceptance |
|---|---|---|---|---|---|
| 1 | **The Bridge gateway module** | Central gateway for all shells; required before routing/execution can exist. | P1 | Clerk identity, workspace policy | Request record created with ID, workspace, source, language, correlation ID |
| 2 | **JEV Routing Agent** | Required request-management component; every request must be classified into lookup/quick/planned. | P1 | The Bridge | Deterministic rules pass lookup without model; quick answer bounded; planned work creates run; explanation shown |
| 3 | **3-path request gateway (Tier 1/2/3)** | Lookup (zero model), quick answer (bounded model), and planned work (versioned workflow) are the core routing contract. | P1 | JEV Routing Agent | Same as above |
| 4 | **Conversation/request identity & correlation** | Required to preserve context across shells and resume work tomorrow. | P1 | The Bridge | Same request visible in web and Obsidian; no duplicate execution |
| 5 | **Project Hub: create/import project** | Core user journey: create/select project. Required before any binding. | P1 | Workspace identity | Blank project created; GitHub repo linked read-only; empty state visible |
| 6 | **Project → workflow binding** | A project must be linked to one or more published workflow versions. | P1 | Project Hub, Workflow Studio | Binding record links project + workflow version + inputs + version policy |
| 7 | **Workflow Studio** | Separate workspace for reusable workflow definitions before any project exists. | P1 | Web shell | Draft created, edited, published as immutable version |
| 8 | **Idea-driven recommendations (creator journey)** | The user explicitly promoted this. Describe an idea and receive editable plan + catalog-backed component choices. | P1 | Workflow Studio | Typed idea produces editable plan with component cards showing fit/source/permissions/cost |
| 9 | **Versioned workflow definitions (draft → publish → freeze active runs)** | Active runs must not be silently mutated. | P1/P2 | Workflow Studio | Published version immutable; active runs pinned |
| 10 | **Schema-preserving copy/paste of whole workflow or selected fragments** | Required for reuse and composition; preserves definitions, ports, edges, contracts; remaps IDs; surfaces unresolved ports. | P1 | Workflow Studio | Paste creates new IDs; internal edges remapped; external dependencies surfaced |
| 11 | **Safe sharing/import/export** | Private by default; no credentials/approvals/state leakage. | P1 | Workflow Studio | Exported package strips secrets; destination binds own connections |
| 12 | **Knowledge Vault with Obsidian sync** | Required native interface. Bidirectional Markdown sync. | P1 | Markdown storage, file watcher | Note created in Obsidian appears in web and vice versa; conflict detection works |
| 13 | **Obsidian plugin (basic interface)** | Must deliver an actual packaged plugin, not just Markdown export. Pair, ask JEV, send note/selection, save responses, show task/run status, disconnect/revoke. | P1 | Knowledge Vault, The Bridge | Plugin loads in test vault; saved lookup uses zero model calls; planned task visible on web |
| 14 | **Web shell: Login/Today/Workflow Studio/Project Hub/Monitor** | Primary user-facing surface. | P1/P2 | The Bridge, Workflow Studio | Screens render bilingual, RTL, accessible; no fixture-by-default in monitor |
| 15 | **English + Arabic with true RTL** | Required inclusive interface; identifiers/paths stay LTR. | P1 | Web shell | Locale switch mirrors layout; LTR identifiers preserved |
| 16 | **WCAG 2.2 AA accessibility** | Required for keyboard, focus, screen-reader, reduced-motion. | P1/P2 | Web shell | Keyboard/focus/screen-reader tests pass |
| 17 | **Information icons (v2-info pattern)** | Contextual help without leaving the screen. | P1 | Web shell | Info icon opens explanation panel |
| 18 | **Categorized global search** | Search grouped by screens, projects, tasks, agents, skills, connectors, knowledge. | P1 | Web shell | Ctrl+K search returns grouped results |
| 19 | **Minimal provider registry** | Register providers, route calls, record usage. | P1/P2 | The Bridge | Providers configurable; usage recorded |
| 20 | **Minimal MCP/connector registry UI** | List connectors, show status/permissions, "Not connected"/"Demo" labels. | P1/P2 | The Bridge | Demo connector listed; disconnected shown truthfully |
| 21 | **Preflight validation without dispatch** | Missing credentials/runner/permission remains a truthful blocker. | P1/P2 | Workflow binding | Preflight report lists blockers; run cannot start |
| 22 | **Forge Method Engine (11 phases as reusable template)** | Optional SDLC template for projects that need it. | P2 | Request gateway | 11 phases defined; inspectable before run; cycles refused |
| 23 | **Small work items with identity, dependencies, I/O, checks** | Atomic unit of planned work. | P2 | Forge engine | Items have identity, dependencies, I/O, checks |
| 24 | **Live monitor: actual run graph, not fixture** | Open execution plan reaches the matching project's selected run or "No run yet". | P2 | Durable runner | Monitor opens actual run; no default fixture |
| 25 | **Security boundaries (identity, roles, credentials, instruction separation)** | Required for trust. | P0/P1 | Clerk identity | Credentials not in config rows; instructions not policy |
| 26 | **Performance Rules inventory (31 criteria)** | All 31 criteria listed, applicability flags set, baseline status recorded before any performance edit. | P0 | Repository, CI | 31-row audit exists with status/evidence |
| 27 | **Idempotency, reconciliation, and first-failure tests** | Required whenever external-action handling is enabled; production safety. | P3/P4 | Durable runner, MCP gateway | Duplicate invocation returns prior receipt; first failure preserved; reconciliation tests pass |
| 28 | **Obsidian conflict detection and bounded loop prevention** | Required whenever Obsidian sync is enabled; safe sync. | P1/P4 | Obsidian plugin, file watcher | Conflicting edits detected; bounded retry prevents infinite loops; user receives conflict prompt |
| 29 | **Live recovery after worker/control-plane restart** | Required whenever durable execution is enabled; no silent lost work. | P3/P4 | Durable runner, event archive | Incomplete run resumes from last checkpoint; orphan attempt detected and surfaced |
| 30 | **Basic nested workflows, conditions, branches and joins** | Core composition contract; required for any non-trivial workflow. | P2/P4 | Versioned workflow engine | Subworkflow calls execute; if/else branches and join nodes evaluate; errors surface to caller |

### P4 first-working-release acceptance rule

A user can: ask a request → see it routed with explanation → get a quick answer or a planned workflow → inspect small items → run/pause/resume → see evidence → create a workflow before a project exists → bind it to a project → start a run → see that run's actual graph in the monitor → read the same knowledge in Obsidian and the web UI.

The following runtime and control capabilities are required for that journey and are therefore first-release Must items (rows 27–34):

- Durable execution records (run/invocation/attempt).
- Pause / resume / cancel with safe-boundary preview and settlement semantics.
- Human Approval Checkpoint before externally consequential or destructive actions.
- Safe external-action handling (idempotency keys, bounded retries, reconciliation, first-failure preservation).
- Event + Evidence Archive for every execution.
- Allowance Governor enforcing per-window/provider/team cap and reserve.
- Preflight validation that blocks dispatch when credentials, runner, permissions, budget or effect class are missing.
- Basic nested workflows, conditions, branches and joins.

P4 is the first working release, not the first sketch.

---

## 2. Must-have capabilities — complete product (P5–P11)

| # | Capability | Why it is a must | Phase | Depends on | Acceptance |
|---|---|---|---|---|---|
| 31 | **Durable execution records (run/invocation/attempt)** | Required for pause/resume/recovery and no duplicate external effects. | P3 | Forge engine, workflow engine | Run/invocation/attempt records durable |
| 32 | **Pause / resume / cancel with settlement semantics** | Core user control over owned execution. | P3 | Durable runner | Pause/resume/cancel settle state correctly |
| 33 | **Native Execution Engines (CLI adapters)** | Execution must cover CLI tools, not only APIs. | P3 | Durable runner, provider registry | CLI invoked as subprocess with streamed output and artifact capture |
| 34 | **Human Approval Checkpoint** | Explicit pause before tool/model execution when side effects/cost/policy thresholds exceeded. | P3 | Durable runner, tool registry | Consequential action blocks until approved; denial stops branch |
| 35 | **Safe external-action handling** | Idempotency, reconciliation, bounded retries, first-failure preservation. | P3 | Durable runner, MCP gateway | No duplicate external actions; first failure preserved |
| 36 | **Event + Evidence Archive** | Versioned, sanitized, auditable records. | P3 | Durable runner | Every execution produces events with first-failure preservation |
| 37 | **Agent Studio (profiles + snapshots at admission)** | Reusable agents; snapshots preserve trust. | P4 | Durable execution | Profile edits affect future admissions only |
| 38 | **Skill & Instruction Channel** | Separates trusted instructions from retrieved knowledge. | P4 | Agent studio | Skill reference versioned/hash-checked |
| 39 | **Hermes Self-Improvement Review** | Required governed learning loop. | P4 | Agent studio, skill channel, evidence archive | Review produces draft proposal; user approval before apply |
| 40 | **Allowance Governor** | Cross-request/provider budget tracking, holds, failover, stop on exhaustion. | P2/P3 | Provider registry | Exhausted allowance stops calls; probe policy preserves budgets |
| 41 | **Real connectors (Gmail, Calendar, Drive, GitHub)** | Core connector foundation; YouTube separately scoped. | P4/P6 | MCP gateway | Real demo adapter connects and executes scoped read |
| 42 | **LLM Council Adapter (governance review + workflow node)** | Required bounded council workflow with perspective mode. | P5 | Provider registry | Council runs end-to-end; produces evidence not acceptance |
| 43 | **Agent Swarm / Coordinator** | Multi-agent orchestration for complex planned work. | P5 | Agent studio, durable runner | Team delegates and aggregates within declared bounds |
| 44 | **Durable schedules and notifications** | Manual/scheduled triggers, timezone/overlap/missed-run, in-app notifications. | P8 | Durable runner | Schedule triggers without duplicate execution |
| 45 | **Full Performance Rules Engine + CI gates** | 31 criteria feeding automated gates. | P8 | Performance inventory, RUM | CI scan reports drift; PR gates trigger review |
| 46 | **Operations and delivery packaging** | Reproducible startup, migrations, backup/restore, health, runbooks. | P8/P10 | Deployment infra | Docker Compose stack starts; runbook verified |
| 47 | **Independent acceptance and security closure** | All confirmed security findings resolved with verified evidence; security findings cannot be waived or owner-accepted. Independent reviewer approval. | P10/P11 | All Must items | Evidence ledger complete; no fabricated acceptance |

---

## 3. Should-have capabilities

| # | Capability | Why it is a should | Phase | Depends on |
|---|---|---|---|---|
| 1 | **Speech Service** | Arabic/English push-to-talk, transcription preview, optional read-back. | P3/P9 | Web shell, Obsidian sync |
| 2 | **JARVIS HUD web shell polish** | Dashboard + chat + voice orb + terminal tab aesthetic. | P1/P8 | Web shell, speech service |
| 3 | **Real-time SSE/live updates with reconnect/replay** | Mandatory sub-acceptance of live monitor; polling may substitute only for early dev builds. | P3 | Durable runner, event archive |
| 4 | **Help center + rich knowledge discovery** | Semantic search and Graphify-backed relationships after verification. | P7 | Knowledge vault |
| 5 | **Secondary workspaces** | Projects, workflows, agents, skills, providers, evidence, activity, decisions, settings. | P7 | Core engine, registry data |
| 6 | **Nested subworkflows, conditions, branches, joins — editor polish** | Richer editor conveniences (auto-layout, visual diff, preview) remain Should. | P6/P7 | Versioned workflow engine |
| 7 | **Idempotency/reconciliation testing for external side effects** | Mandatory sub-acceptance of safe external-action handling; not optional. | P3 | MCP gateway, durable runner |
| 8 | **RUM feedback loop** | Feeds 31-criteria engine with real data. | P8 | Performance rules engine |
| 9 | **CI performance/security/market validation gates** | Required ongoing quality. | P0/P8 | CI workflows, rules engine |
| 10 | **Operational runbook, backup/restore, upgrade guide** | Required for production operations. | P8 | Deployment packaging |
| 11 | **Hermes `/os` skill with full command surface** | Existing `/factory` skill evolves. | P9 | Most core features |
| 12 | **LLM Council ranking UI with de-anonymization display** | Transparency for council results. | P5 | LLM Council adapter |
| 13 | **Agent/MCP marketplace publishing (local sharing)** | Reuse beyond single user. | P6/P7 | Market infrastructure |
| 14 | **Conflict detection and bounded file-watcher loop prevention for Obsidian** | Mandatory sub-acceptance whenever Obsidian sync is enabled. | P1/P7 | Obsidian sync |
| 15 | **Responsive layouts beyond basic adaptation** | Tablets and narrow screens. | P1/P8 | Web shell |
| 16 | **Advanced council analysis** | Side-by-side critique, configurable panels, disagreement exploration. | P5/P7 | LLM Council adapter |
| 17 | **Rich marketplace authoring** | Natural-language draft assistance, guided I/O examples. | P6/P7 | Marketplace |
| 18 | **"How Mahmoud OS works" view** | User-facing architecture explanation. | P7 | All core components |

---

## 4. Future / nice-to-have capabilities

| # | Capability | Why it is future | Earliest consideration |
|---|---|---|---|
| 1 | **Voice input/output wake-word / always-on** | Privacy/performance requirements first. | P9+ |
| 2 | **Obsidian mobile / cross-device vault sync** | Outside current scope unless already present. | After P8 |
| 3 | **Dedicated CLI shell beyond Hermes skill** | Useful automation; web + Hermes skill cover primary interaction. | P9+ |
| 4 | **Mobile app / PWA optimization** | Responsive web is baseline. | After P8 |
| 5 | **Community/public marketplace with payments** | Public commercial storefront. | Future major release |
| 6 | **Multi-tenant SaaS deployment** | Single-user/local/private-cloud is baseline. | After P8 |
| 7 | **Advanced observability dashboards** | OpenTelemetry traces/metrics are enough initially. | After P8 |
| 8 | **AI-generated documentation from evidence** | Built on top of evidence archive later. | After P7 |
| 9 | **Advanced Arabic voice recognition** | Additional ASR quality risk. | After voice prioritized |
| 10 | **Custom themes beyond light/dark** | Polish. | After P8 |
| 11 | **Social/collaboration features** | Personal OS baseline first. | Future major release |
| 12 | **Public REST API for external integrations** | Internal API is Must. | After P8 |
| 13 | **Advanced workflow animation / 3D graph views** | Motion should explain state; excessive animation discouraged. | Future polish, if ever |
| 14 | **Credits/payment packs and commerce** | Preserved from forge-ai scope but outside first release. | After P8 |
| 15 | **Enterprise multitenancy / compliance reporting** | Beyond current project requirements. | Future major release |

---

## 5. Dependency map across buckets

```
Must (first release P1–P4)
├── The Bridge ──→ JEV Routing Agent ──→ 3-path routing
├── Project Hub ──→ Project-workflow binding
├── Workflow Studio ──→ Idea assistant + Versioning + Copy/paste + Sharing
├── Knowledge Vault ──→ Obsidian plugin + Obsidian sync
├── Minimal provider registry
├── Minimal MCP/connector registry UI
├── Web shell (Login/Today/Explore/Project/Workflow/Monitor) + EN/AR + accessibility + info icons + categorized search
├── Preflight without dispatch
├── Forge Method Engine (optional template) ──→ Small work items
└── Performance Rules inventory

Must (complete product P5–P11)
├── Durable runner ──→ Pause/resume/cancel ──→ Event + Evidence archive
├── Native Execution Engines ──→ CLI adapters (Claude Code, Codex, OpenCode, Ollama)
├── Human Approval Checkpoint ──→ Safe external-action handling
├── Agent Studio ──→ Skill/Instruction channel ──→ Hermes Self-Review
├── Allowance Governor
├── Real connectors (Gmail, Calendar, Drive, GitHub)
├── LLM Council adapter + node
├── Agent Swarm / Coordinator
├── Schedules/notifications
├── Full Performance Rules Engine + CI gates
├── Operations/delivery packaging
└── Independent acceptance / security closure

Should (build on Must)
├── Speech Service
├── JARVIS HUD polish
├── Real-time SSE
├── Help + rich knowledge discovery
├── Secondary workspaces
├── Advanced workflow constructs
├── Idempotency/reconciliation tests
├── RUM + CI gates
├── Operational docs
├── Hermes `/os` skill
├── Council ranking UI
└── Marketplace publishing

Future (build on everything above)
├── Wake-word/always-on voice
├── Obsidian mobile sync
├── Dedicated CLI shell
├── Mobile / SaaS multi-tenant
├── Community/public marketplace
├── Public API
└── Commerce/credits
```

---

## 6. Build order recommendation

### First working release (end of P4)

All Must items in rows 1–26 must be present with evidence. This is the smallest thing that can be called Mahmoud OS.

### Complete product (end of P11)

All Must items in rows 1–43 must be present with evidence. This is the full Mahmoud OS release.

### Future expansion

Select Future items based on actual usage. Do not start these until the user confirms they are needed and the core is green on CI.

---

## 7. User-specific clarifications

Based on your explicit requests, these items were promoted to **Must (first release or complete product)**:

- **Obsidian plugin (basic interface)** — Must P1; actual packaged plugin, not just Markdown export.
- **Hermes Self-Improvement Review** — Must P4; governed learning loop.
- **JEV / routing agent** — Must P1; required system capability, not optional.
- **CLI execution engines** — Must P3; execution covers CLI tools.
- **Idea-driven workflow/agent/skill/MCP/tool recommendations** — Must P1.
- **Project creation/import + project-workflow binding** — Must P1.
- **Workflow Studio as separate reusable template workspace** — Must P1.
- **Schema-preserving copy/paste** — Must P1.
- **Safe sharing/import/export** — Must P1.
- **Preflight without dispatch** — Must P1/P2.
- **Live monitor actual run, not fixture** — Must P2.
- **LLM Council** — Must P5; bounded council workflow with perspective mode.
- **Durable schedules and notifications** — Must P8.
- **Information icons** — Must P1.
- **Categorized search** — Must P1.
- **Safe external-action handling** — Must P3.

These providers are explicitly included in the pluggable provider registry:

- OpenAI, Anthropic, Google, xAI, Mistral, OpenCode, Ollama, NVIDIA, Zhipu, and any available provider via adapter pattern.

These connectors are explicitly included in the first market set:

- Gmail, Calendar, Drive, GitHub, plus Files, APIs, Browser, Tests, and CLI processes. YouTube is separately scoped.

---

## 8. What this classification changes in the blueprint

This classification is the scheduling lens for the blueprint. The phased roadmap in the blueprint reflects this priority:

- **P1–P4:** First working release Must items.
- **P5–P11:** Complete product Must items.
- **Should items:** Interleaved where feasible.
- **Future items:** After complete product evidence.

If you want to accelerate, the only safe cuts are Future items. No Should item should be cut before its dependent Must item is evidence-complete. A Must item scheduled after P4 is still required for the complete product and cannot be silently downgraded.

---

*End of classification. No code changes made.*