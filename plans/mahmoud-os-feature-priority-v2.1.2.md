# Mahmoud OS Feature Priority v2.1.2

> **Single source of truth:** `plans/mahmoud-os-requirements-matrix-v2.1.2.csv`  
> This file is regenerated from that CSV. Do not edit ranges by hand; update the CSV and regenerate.

## Release membership

- **First working release (P4):** R001–R038 (38 requirements)
- **Complete product (P11):** R039–R066 (28 requirements)
- **Should:** S001–S018 (18 items)
- **Future:** FTR001–FTR016 (16 items)

## 1. Must-have capabilities — first working release (R001–R038)

| ID | Capability | Why it is a must | Phase | Depends on | Acceptance |
|---|---|---|---|---|---|
| R001 | **The Bridge gateway module** | A00-PLATFORM.md#boundaries-and-responsibilities | P1-P4 | Clerk identity, workspace policy | Request record created with ID, workspace, source, language, correlation ID |
| R002 | **JEV Routing Agent** | P18-DISCOVERY-AND-SCOPE.md; P20-RUN-CHANNELS-AND-CHANGE-REQUESTS.md | P1-P4 | The Bridge | Deterministic rules pass lookup without model; quick answer bounded; planned work creates run; explanation shown |
| R003 | **3-path request gateway (Tier 1/2/3)** | P18-DISCOVERY-AND-SCOPE.md; P20-RUN-CHANNELS-AND-CHANGE-REQUESTS.md | P1-P4 | JEV Routing Agent | Each path explained; planned work creates versioned run |
| R004 | **Conversation/request identity and correlation** | P20-RUN-CHANNELS-AND-CHANGE-REQUESTS.md#durable-conversation-model-and-consistency | P1-P4 | The Bridge | Same request visible in web and Obsidian; no duplicate execution |
| R005 | **Project Hub: create/import project** | P21-SOFTWARE-DELIVERY-AND-SDLC.md (pending); P04-RUNTIME.md | P1-P4 | Workspace identity | Blank project created; GitHub repo linked read-only; empty state visible |
| R006 | **Project to workflow binding** | P21-SOFTWARE-DELIVERY-AND-SDLC.md (pending); P04-RUNTIME.md | P1-P4 | Project Hub, Workflow Studio | Binding record links project + workflow version + inputs + version policy |
| R007 | **Workflow Studio** | P02-REGISTRY.md#contracts-and-publication; P03-EDITOR.md#building-and-configuring-workflows | P1-P4 | Web shell | Draft created, edited, published as immutable version |
| R008 | **Idea-driven recommendations (creator journey)** | P18-DISCOVERY-AND-SCOPE.md#data-contracts; P23-GUARDIAN-RESEARCH-AND-LEARNING.md | P1-P4 | Workflow Studio | Typed idea produces editable plan with component cards showing fit/source/permissions/cost |
| R009 | **Versioned workflow definitions** | P02-REGISTRY.md; P03-EDITOR.md | P1-P4 | Workflow Studio | Published version immutable; active runs pinned |
| R010 | **Schema-preserving copy/paste** | P03-EDITOR.md | P1-P4 | Workflow Studio | Paste creates new IDs; internal edges remapped; external dependencies surfaced |
| R011 | **Safe sharing/import/export** | P02-REGISTRY.md; P03-EDITOR.md | P1-P4 | Workflow Studio | Exported package strips secrets; destination binds own connections |
| R012 | **Knowledge Vault with Obsidian sync** | P11-KNOWLEDGE.md | P1-P4 | Markdown storage, file watcher | Note created in Obsidian appears in web and vice versa; conflict detection works |
| R013 | **Obsidian plugin (basic interface)** | P11-KNOWLEDGE.md | P1-P4 | Knowledge Vault, The Bridge | Plugin loads in test vault; saved lookup uses zero model calls; planned task visible on web |
| R014 | **Web shell: Login/Today/Workflow Studio/Project Hub/Monitor** | A00-PLATFORM.md; P03-EDITOR.md; P05-RUN-INSPECTION.md | P1-P4 | The Bridge, Workflow Studio | Screens render bilingual, RTL, accessible; no fixture-by-default in monitor |
| R015 | **English + Arabic with true RTL** | A00-PLATFORM.md; P03-EDITOR.md | P1-P4 | Web shell | Locale switch mirrors layout; LTR identifiers preserved |
| R016 | **WCAG 2.2 AA accessibility** | A00-PLATFORM.md; P03-EDITOR.md | P1-P4 | Web shell | Keyboard/focus/screen-reader tests pass |
| R017 | **Information icons (v2-info pattern)** | P03-EDITOR.md | P1-P4 | Web shell | Info icon opens explanation panel |
| R018 | **Categorized global search** | P03-EDITOR.md; P11-KNOWLEDGE.md | P1-P4 | Web shell | Ctrl+K search returns grouped results |
| R019 | **Minimal provider registry** | P12-MODELS.md#contracts-and-routing; P12A-PROVIDERS-AND-FAILOVER.md | P1-P4 | The Bridge | Providers configurable; usage recorded |
| R020 | **Minimal MCP/connector registry UI** | P08-CONNECTIONS.md#contracts-and-flows; P09-TOOLS.md | P1-P4 | The Bridge | Demo connector listed; disconnected shown truthfully |
| R021 | **Preflight validation without dispatch** | P03-EDITOR.md; P13-EVALUATIONS.md | P1-P4 | Workflow binding | Preflight report lists blockers; run cannot start |
| R022 | **Forge Method Engine (11 phases as reusable template)** | P21-SOFTWARE-DELIVERY-AND-SDLC.md (pending); P04-RUNTIME.md | P1-P4 | Request gateway | 11 phases defined; inspectable before run; cycles refused |
| R023 | **Small work items with identity, dependencies, I/O, checks** | P04-RUNTIME.md; P20-RUN-CHANNELS-AND-CHANGE-REQUESTS.md | P1-P4 | Forge engine | Items have identity, dependencies, I/O, checks |
| R024 | **Live monitor: actual run graph, not fixture** | P05-RUN-INSPECTION.md; P20-RUN-CHANNELS-AND-CHANGE-REQUESTS.md | P1-P4 | Durable runner | Monitor opens actual run; no default fixture |
| R025 | **Security boundaries (identity, roles, credentials, instruction separation)** | P01-IDENTITY.md | P0-P4 | Clerk identity | Credentials not in config rows; instructions not policy; Clerk org claims cannot elevate access |
| R026 | **Performance Rules inventory (31 criteria)** | P13-EVALUATIONS.md; P21-SOFTWARE-DELIVERY-AND-SDLC.md | P0 | Repository, CI | 31-row audit exists with status/evidence |
| R027 | **Durable execution records (run/invocation/attempt)** | P04-RUNTIME.md#contracts | P1-P4 | Forge engine, workflow engine | Run/invocation/attempt records durable |
| R028 | **Pause / resume / cancel with settlement semantics** | P04-RUNTIME.md; P19-RELIABILITY-AND-EVOLUTION.md | P1-P4 | Durable runner | Pause/resume/cancel settle state correctly |
| R029 | **Human Approval Checkpoint** | P13-EVALUATIONS.md; P19-RELIABILITY-AND-EVOLUTION.md; P09-TOOLS.md | P1-P4 | Durable runner, tool registry | Consequential action blocks until approved; denial stops branch |
| R030 | **Safe external-action handling** | P09-TOOLS.md#external-effects-and-sandboxing; P19-RELIABILITY-AND-EVOLUTION.md | P1-P4 | Durable runner, MCP gateway | No duplicate external actions; first failure preserved |
| R031 | **Event + Evidence Archive** | P10-ARTIFACTS.md#contracts-and-lifecycle | P1-P4 | Durable runner | Every execution produces events with first-failure preservation |
| R032 | **Allowance Governor** | P12B-SUBSCRIPTION-QUOTA-AND-ROUTE-SEQUENCE.md; P04-RUNTIME.md | P1-P4 | Provider registry | Exhausted allowance stops calls; probe policy preserves budgets |
| R033 | **Native Execution Engines (CLI adapters)** | P09-TOOLS.md; P16-OPERATIONS.md | P1-P4 | Durable runner, provider registry | CLI invoked as subprocess with streamed output and artifact capture |
| R034 | **Basic nested workflows, conditions, branches and joins** | P03-EDITOR.md; P04-RUNTIME.md | P1-P4 | Versioned workflow engine | Subworkflow calls execute; if/else branches and join nodes evaluate; errors surface to caller |
| R035 | **Idempotency/reconciliation tests for external side effects** | P09-TOOLS.md; P13-EVALUATIONS.md | P1-P4 | MCP gateway, durable runner | Duplicate invocation returns prior receipt; reconciliation tests pass |
| R036 | **Obsidian conflict detection and bounded loop prevention** | P11-KNOWLEDGE.md | P1-P4 | Obsidian plugin, file watcher | Conflicting edits detected; bounded retry prevents infinite loops; user receives conflict prompt |
| R037 | **Live recovery after worker/control-plane restart** | P25-INTEGRATIONS-AND-REMOTE-RUNTIMES.md; P04-RUNTIME.md | P1-P4 | Durable runner, event archive | Incomplete run resumes from last checkpoint; orphan attempt detected and surfaced |
| R038 | **Discovery questions in idea assistant** | P18-DISCOVERY-AND-SCOPE.md#browser-and-api-flow | P1-P4 | Idea-driven recommendations | Idea input surfaces editable scope questions before plan is accepted |

### P4 first-working-release acceptance rule

A user can: ask a request → see it routed with explanation → get a quick answer or a planned workflow → inspect small items → run/pause/resume → see evidence → create a workflow before a project exists → bind it to a project → start a run → see that run's actual graph in the monitor → read the same knowledge in Obsidian and the web UI.

All **R001–R038** must be present with evidence. In particular, the execution journey requires the runtime and control capabilities R027–R037:

- **R027** Durable execution records (run/invocation/attempt).
- **R028** Pause / resume / cancel with safe-boundary preview and settlement semantics.
- **R029** Human Approval Checkpoint before externally consequential or destructive actions.
- **R030** Safe external-action handling (idempotency keys, bounded retries, reconciliation, first-failure preservation).
- **R031** Event + Evidence Archive for every execution.
- **R032** Allowance Governor enforcing per-window/provider/team cap and reserve.
- **R033** Native Execution Engines (CLI adapters) for tools beyond APIs.
- **R034** Basic nested workflows, conditions, branches and joins.
- **R035** Idempotency/reconciliation tests for external side effects.
- **R036** Obsidian conflict detection and bounded loop prevention.
- **R037** Live recovery after worker/control-plane restart.

P4 is the first working release, not the first sketch.

## 2. Must-have capabilities — complete product (R039–R066)

| ID | Capability | Why it is a must | Phase | Depends on | Acceptance |
|---|---|---|---|---|---|
| R039 | **Agent Studio (profiles + snapshots at admission)** | P06-AGENTS.md | P5-P11 | Durable execution | Profile edits affect future admissions only |
| R040 | **Hermes Self-Improvement Review** | P23-GUARDIAN-RESEARCH-AND-LEARNING.md | P5-P11 | Agent studio, skill channel, evidence archive | Review produces draft proposal; user approval before apply |
| R041 | **Skill and Instruction Channel** | P07-SKILLS.md | P5-P11 | Agent studio | Skill reference versioned/hash-checked |
| R042 | **Real connectors (Gmail, Calendar, Drive, GitHub)** | P08-CONNECTIONS.md; P09-TOOLS.md | P5-P11 | MCP gateway | Real demo adapter connects and executes scoped read |
| R043 | **LLM Council Adapter (governance review + workflow node)** | P13-EVALUATIONS.md; P19-RELIABILITY-AND-EVOLUTION.md | P5-P11 | Provider registry | Council runs end-to-end; produces evidence not acceptance |
| R044 | **Agent Swarm / Coordinator** | P06-AGENTS.md; P24-SUPPORT-AND-ORGANIZATION.md | P5-P11 | Agent studio, durable runner | Team delegates and aggregates within declared bounds |
| R045 | **Durable schedules and notifications** | P20-RUN-CHANNELS-AND-CHANGE-REQUESTS.md; P14-NOTIFICATIONS.md | P5-P11 | Durable runner | Schedule triggers without duplicate execution |
| R046 | **Full Performance Rules Engine + CI gates** | P13-EVALUATIONS.md; P21-SOFTWARE-DELIVERY-AND-SDLC.md | P5-P11 | Performance inventory, RUM | CI scan reports drift; PR gates trigger review |
| R047 | **Operations and delivery packaging** | P15-ADMINISTRATION.md; P16-OPERATIONS.md | P5-P11 | Deployment infra | Docker Compose stack starts; runbook verified |
| R048 | **Model removal/rebinding and provider constraints** | P12A-PROVIDERS-AND-FAILOVER.md; P12B-SUBSCRIPTION-QUOTA-AND-ROUTE-SEQUENCE.md | P5-P11 | Provider registry, Allowance Governor | Provider can be paused/rebound; context constraints enforced |
| R049 | **Provider pause and context constraint enforcement** | P12A-PROVIDERS-AND-FAILOVER.md | P5-P11 | Provider registry | Paused provider rejects new calls; context window exceeded returns graceful error |
| R050 | **LLM cache, telemetry and cost tracking** | P12-MODELS.md; P20-RUN-CHANNELS-AND-CHANGE-REQUESTS.md | P5-P11 | Provider registry, Event archive | Per-call usage recorded; cache hits reported; cost estimate shown before run |
| R051 | **Replay snapshots from event archive** | P05-RUN-INSPECTION.md; P10-ARTIFACTS.md | P5-P11 | Event archive, Live monitor | Historical run can be replayed visually; deterministic outputs reproducible |
| R052 | **Artifact/review comments on evidence** | P10-ARTIFACTS.md; P13-EVALUATIONS.md; P20-RUN-CHANNELS-AND-CHANGE-REQUESTS.md | P5-P11 | Event archive | Reviewer can add threaded comments linked to a specific event/artifact version |
| R053 | **GitHub issues/repository sync connector** | P25-INTEGRATIONS-AND-REMOTE-RUNTIMES.md; P21-SOFTWARE-DELIVERY-AND-SDLC.md | P5-P11 | MCP gateway, Project Hub | GitHub repo issues sync bidirectionally; webhook updates reflected |
| R054 | **Repository upload/ingestion for project import** | P25-INTEGRATIONS-AND-REMOTE-RUNTIMES.md; P10-ARTIFACTS.md | P5-P11 | Project Hub, Knowledge Vault | Upload/clone produces indexed project artifacts with provenance |
| R055 | **Code graph/import closure** | P25-INTEGRATIONS-AND-REMOTE-RUNTIMES.md; P21-SOFTWARE-DELIVERY-AND-SDLC.md | P5-P11 | Repository ingestion, Project Hub | Static analysis produces dependency graph; missing imports surfaced |
| R056 | **Architecture/document production workflows** | P21-SOFTWARE-DELIVERY-AND-SDLC.md; P10-ARTIFACTS.md; P11-KNOWLEDGE.md | P5-P11 | Workflow Studio, Knowledge Vault | Workflow generates structured document from evidence; exports to Markdown/PDF |
| R057 | **Market research/competitive analysis workflows** | P23-GUARDIAN-RESEARCH-AND-LEARNING.md; P11-KNOWLEDGE.md | P5-P11 | Knowledge Vault, Hermes Review | Research query produces cited comparison table; sources traceable |
| R058 | **Pattern library/derived principles** | P11-KNOWLEDGE.md; P07-SKILLS.md; P23-GUARDIAN-RESEARCH-AND-LEARNING.md | P5-P11 | Knowledge Vault, Skill Channel | Reusable patterns extracted from provenance; versioned and attributed |
| R059 | **Templates/gallery/project reuse** | P17-PARITY.md; P02-REGISTRY.md; P03-EDITOR.md | P5-P11 | Workflow Studio, Registry | Published workflows discoverable in gallery; templates forkable with new IDs |
| R060 | **Data-source authorization/provenance** | P18-DISCOVERY-AND-SCOPE.md; P08-CONNECTIONS.md; P11-KNOWLEDGE.md | P5-P11 | Connector registry, Knowledge Vault | Every imported fact carries source, retrieval time, and authorization scope |
| R061 | **Race/adaptive execution and confidence bounds** | P21-SOFTWARE-DELIVERY-AND-SDLC.md; P19-RELIABILITY-AND-EVOLUTION.md; P12A-PROVIDERS-AND-FAILOVER.md | P5-P11 | Durable runner, Provider registry | Adaptive retries bounded by confidence threshold; fallback provider selected deterministically |
| R062 | **Independent acceptance and security closure** | P01-IDENTITY.md; P09-TOOLS.md; P13-EVALUATIONS.md; P21-SOFTWARE-DELIVERY-AND-SDLC.md | P10-P11 | R001-R061 | Confirmed security findings must be resolved with verified evidence. They cannot be waived or owner-accepted. Evidence ledger complete. |
| R063 | **Credits/payment packs** | P22-COMMERCE-CREDITS-AND-QUOTES.md | P5-P11 | Allowance Governor, Measured usage | Deferred until after first delivery and real usage measured |
| R064 | **Native mobile delivery** | P21-SOFTWARE-DELIVERY-AND-SDLC.md; P25-INTEGRATIONS-AND-REMOTE-RUNTIMES.md | P5-P11 | Complete product web delivery | Deferred until after first delivery per owner V-H01 |
| R065 | **Design and wireframes** | P21-SOFTWARE-DELIVERY-AND-SDLC.md; P25-INTEGRATIONS-AND-REMOTE-RUNTIMES.md | P5-P11 | Workflow Studio | Design-to-code workflows; deferred post-first-delivery |
| R066 | **Support desk/SLA routing** | P24-SUPPORT-AND-ORGANIZATION.md | P5-P11 | Run channels, Notifications | Support request traceable; SLA routing deferred |

### P11 complete-product acceptance rule

All **R001–R066** must be present with evidence. This includes R039–R066 (agent studio, skills, council, swarm, schedules, performance engine, packaging, connector provenance, research/patterns, and the deferred full-product outcomes commerce/mobile/design/support), which are required full-product outcomes. Every F01–F50 area is therefore in scope for the complete product; nothing is silently downgraded.

## 3. Should-have capabilities

| ID | Capability | Why it is a must | Phase | Depends on | Acceptance |
|---|---|---|---|---|---|
| S001 | **Speech Service** | P20-RUN-CHANNELS-AND-CHANGE-REQUESTS.md | Should | Web shell, Obsidian sync | Arabic/English push-to-talk, transcription preview, optional read-back |
| S002 | **JARVIS HUD web shell polish** | P03-EDITOR.md | Should | Web shell, speech service | Dashboard + chat + voice orb + terminal tab aesthetic |
| S003 | **Real-time SSE/live updates with reconnect/replay** | P05-RUN-INSPECTION.md; P20-RUN-CHANNELS-AND-CHANGE-REQUESTS.md | Should | Durable runner, event archive | Mandatory sub-acceptance of live monitor; polling may substitute only for early dev builds |
| S004 | **Help center + rich knowledge discovery** | P11-KNOWLEDGE.md | Should | Knowledge vault | Semantic search and Graphify-backed relationships after verification |
| S005 | **Secondary workspaces** | P03-EDITOR.md | Should | Core engine, registry data | Projects, workflows, agents, skills, providers, evidence, activity, decisions, settings |
| S006 | **Nested subworkflows, conditions, branches, joins - editor polish** | P03-EDITOR.md; P04-RUNTIME.md | Should | Versioned workflow engine | Richer editor conveniences (auto-layout, visual diff, preview) remain Should |
| S007 | **Idempotency/reconciliation testing for external side effects** | P09-TOOLS.md; P13-EVALUATIONS.md | Should | MCP gateway, durable runner | Mandatory sub-acceptance of safe external-action handling; not optional |
| S008 | **RUM feedback loop** | P12-MODELS.md; P20-RUN-CHANNELS-AND-CHANGE-REQUESTS.md | Should | Performance rules engine | Feeds 31-criteria engine with real data |
| S009 | **CI performance/security/market validation gates** | P13-EVALUATIONS.md; P21-SOFTWARE-DELIVERY-AND-SDLC.md | Should | CI workflows, rules engine | Required ongoing quality |
| S010 | **Operational runbook, backup/restore, upgrade guide** | P16-OPERATIONS.md | Should | Deployment packaging | Required for production operations |
| S011 | **Hermes /os skill with full command surface** | P23-GUARDIAN-RESEARCH-AND-LEARNING.md | Should | Most core features | Existing /factory skill evolves |
| S012 | **LLM Council ranking UI with de-anonymization display** | P13-EVALUATIONS.md | Should | LLM Council adapter | Transparency for council results |
| S013 | **Agent/MCP marketplace publishing (local sharing)** | P07-SKILLS.md; P17-PARITY.md | Should | Market infrastructure | Reuse beyond single user |
| S014 | **Conflict detection and bounded file-watcher loop prevention for Obsidian** | P11-KNOWLEDGE.md | Should | Obsidian sync | Mandatory sub-acceptance whenever Obsidian sync is enabled |
| S015 | **Responsive layouts beyond basic adaptation** | P03-EDITOR.md | Should | Web shell | Tablets and narrow screens |
| S016 | **Advanced council analysis** | P13-EVALUATIONS.md | Should | LLM Council adapter | Side-by-side critique, configurable panels, disagreement exploration |
| S017 | **Rich marketplace authoring** | P07-SKILLS.md; P17-PARITY.md | Should | Market infrastructure | Natural-language draft assistance, guided I/O examples |
| S018 | **How Mahmoud OS works view** | A00-PLATFORM.md | Should | All core components | User-facing architecture explanation |

## 4. Future capabilities

| ID | Capability | Why it is a must | Phase | Depends on | Acceptance |
|---|---|---|---|---|---|
| FTR001 | **Voice input/output wake-word / always-on** | P20-RUN-CHANNELS-AND-CHANGE-REQUESTS.md | Future | Web shell, Obsidian sync | Privacy/performance requirements first |
| FTR002 | **Obsidian mobile / cross-device vault sync** | P11-KNOWLEDGE.md | Future | Knowledge vault | Outside current scope unless already present |
| FTR003 | **Dedicated CLI shell beyond Hermes skill** | P23-GUARDIAN-RESEARCH-AND-LEARNING.md | Future | Most core features | Useful automation; web + Hermes skill cover primary interaction |
| FTR004 | **Mobile app / PWA optimization** | P03-EDITOR.md | Future | Web shell | Responsive web is baseline |
| FTR005 | **Community/public marketplace with payments** | P07-SKILLS.md; P17-PARITY.md; P22-COMMERCE-CREDITS-AND-QUOTES.md | Future | Market infrastructure, Commerce | Public commercial storefront |
| FTR006 | **Multi-tenant SaaS deployment** | A00-PLATFORM.md | Future | Deployment infra | Single-user/local/private-cloud is baseline |
| FTR007 | **Advanced observability dashboards** | P16-OPERATIONS.md | Future | Observability | OpenTelemetry traces/metrics are enough initially |
| FTR008 | **AI-generated documentation from evidence** | P11-KNOWLEDGE.md | Future | Knowledge vault | Built on top of evidence archive later |
| FTR009 | **Advanced Arabic voice recognition** | P20-RUN-CHANNELS-AND-CHANGE-REQUESTS.md | Future | Web shell, Speech service | Additional ASR quality risk |
| FTR010 | **Custom themes beyond light/dark** | P03-EDITOR.md | Future | Web shell | Polish |
| FTR011 | **Social/collaboration features** | P24-SUPPORT-AND-ORGANIZATION.md | Future | Run channels, Notifications | Personal OS baseline first |
| FTR012 | **Public REST API for external integrations** | A00-PLATFORM.md; P25-INTEGRATIONS-AND-REMOTE-RUNTIMES.md | Future | Core engine, API infra | Internal API is Must |
| FTR013 | **Advanced workflow animation / 3D graph views** | P03-EDITOR.md | Future | Versioned workflow engine | Motion should explain state; excessive animation discouraged |
| FTR014 | **Rich template gallery publishing beyond local reuse** | P17-PARITY.md; P02-REGISTRY.md | Future | Market infrastructure | Public template gallery with ratings |
| FTR015 | **Enterprise multitenancy / compliance reporting** | A00-PLATFORM.md; P15-ADMINISTRATION.md | Future | Deployment infra, Administration | Beyond current project requirements |
| FTR016 | **Cross-vault AI knowledge synthesis** | P11-KNOWLEDGE.md; P23-GUARDIAN-RESEARCH-AND-LEARNING.md | Future | Knowledge vault | Merge insights across multiple vaults |

## 5. Dependency map

```text
Must (first release R001–R038)
├── The Bridge (R001)
│   └── JEV Routing Agent (R002) → 3-path gateway (R003) → conversation identity (R004)
├── Project Hub (R005) → project→workflow binding (R006)
├── Workflow Studio (R007)
│   ├── Idea-driven recommendations (R008) → discovery questions (R038)
│   ├── Versioned definitions (R009)
│   ├── Copy/paste (R010)
│   └── Safe sharing (R011)
├── Knowledge Vault (R012) → Obsidian plugin (R013)
├── Web shell (R014)
│   ├── Bilingual/RTL (R015), Accessibility (R016), Info icons (R017), Search (R018)
│   └── Speech service (S001), JARVIS HUD (S002) — Should
├── Provider registry (R019) and MCP registry (R020)
├── Preflight validation (R021)
├── Forge Method Engine (R022) → small work items (R023) → live monitor (R024)
├── Security boundaries (R025) and Performance inventory (R026)
└── Execution/runtime controls (R027–R037)
    ├── Durable execution records (R027)
    ├── Pause/resume/cancel (R028)
    ├── Human approval checkpoint (R029)
    ├── Safe external actions (R030)
    ├── Event + evidence archive (R031)
    ├── Allowance Governor (R032)
    ├── Native CLI engines (R033)
    ├── Basic composition (R034)
    ├── Idempotency tests (R035)
    ├── Obsidian conflict protection (R036)
    └── Live recovery (R037)

Must (complete product R039–R066)
├── Agent Studio (R039) → Skill channel (R041) → Hermes Self-Review (R040)
├── Real connectors (R042) → LLM Council (R043) → Agent Swarm (R044)
├── Schedules/notifications (R045)
├── Performance Rules Engine + CI gates (R046)
├── Operations packaging (R047)
├── Provider removal/rebinding (R048) and pause/constraints (R049)
├── Cache/telemetry/cost (R050) and replay snapshots (R051)
├── Artifact comments (R052), GitHub sync (R053), repository ingestion (R054)
├── Code graph (R055), document production (R056), research workflows (R057)
├── Pattern library (R058), template gallery (R059), data-source provenance (R060)
├── Adaptive execution (R061)
├── Independent security closure (R062)
└── Required deferred full-product outcomes (R063–R066)
    ├── Credits/payment packs (R063)
    ├── Native mobile delivery (R064)
    ├── Design and wireframes (R065)
    └── Support desk/SLA routing (R066)

Should
├── Speech service (S001), JARVIS HUD (S002), SSE updates (S003)
├── Help center (S004), secondary workspaces (S005)
├── Composition editor polish (S006), idempotency testing tools (S007)
├── RUM feedback loop (S008), CI gates (S009), operational runbook (S010)
├── Hermes /os skill (S011), council ranking UI (S012)
├── Marketplace publishing (S013), Obsidian conflict UX (S014)
├── Responsive layouts (S015), advanced council analysis (S016)
├── Rich marketplace authoring (S017), "How it works" view (S018)

Future
├── Voice wake-word (FTR001), Obsidian mobile sync (FTR002)
├── Dedicated CLI shell (FTR003), mobile PWA (FTR004)
├── Public marketplace with payments (FTR005), multi-tenant SaaS (FTR006)
├── Advanced observability (FTR007), AI-generated docs (FTR008)
├── Advanced Arabic voice (FTR009), custom themes (FTR010)
├── Social features (FTR011), public REST API (FTR012)
├── Workflow animation (FTR013), public template gallery (FTR014)
├── Enterprise compliance (FTR015), cross-vault synthesis (FTR016)
```

---

## 6. Build order recommendation

### First working release (end of P4)

All Must items **R001–R038** must be present with evidence.

### Complete product (end of P11)

All Must items **R001–R066** must be present with evidence, plus every F01–F50 area either implemented or explicitly deferred as Future with owner-approved acceptance criteria.

### Future expansion

Select Future items based on actual usage. Do not start these until the user confirms they are needed and the core is green on CI.

---

## 7. User-specific clarifications

- **P4 is the first working release.** Later Must features remain required for the complete product; they are not demoted to optional.
- **JEV Routing Agent remains required.** Its versioned system profile/routing configuration can exist before Agent Studio's editing UI.
- **P0 wording already allows honest blocker reporting.** Discovery can continue while required merge/release checks and non-waivable security controls remain enforced.
- **Copy/paste scope is defined:** preserve supported workflow definitions, ports, edges and contracts; remap identities; exclude secrets, approvals and execution state.
- **Security findings cannot be waived or owner-accepted.** Confirmed findings must be resolved with verified evidence.
- **70/30 automation/interactive quota policy** is recorded in New-forge's owner-decision application; cite that authority and preserve its accounting conditions.
- **Commerce (F20), mobile/design (F36/F37) and support (F44)** are required full-product outcomes mapped to R063–R066, deferred until their owner contracts are approved.
