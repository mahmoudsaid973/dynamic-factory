# Mahmoud OS — Feature Priority Classification

> **Purpose:** Classify every capability in the Mahmoud OS master blueprint into **Must**, **Should**, and **Nice-to-have / Future**. This is a planning document; no code is changed.
> **Source:** `plans/mahmoud-os-master-blueprint.md`
> **Version:** 2.0
> **Date:** 2026-11-11

---

## Summary

| Bucket | Definition |
|---|---|
| **Must** | The product is not Mahmoud OS without this. Required for P0–P4 acceptance. |
| **Should** | Important for a complete, polished product, but the core can function without it in early phases. Targeted for P5–P8. |
| **Nice-to-have / Future** | Valuable, but can be deferred indefinitely without breaking the core identity. Considered after all Must and Should items are evidence-complete. |

---

## 1. Must-have capabilities

These define the minimum viable Mahmoud OS. If any of these are missing, the product does not deliver its stated identity.

| # | Capability | Why it is a must | Phase | Depends on |
|---|---|---|---|---|
| 1 | **JEV Routing Agent** | Every request must be classified by an explicit, auditable system agent into lookup/quick/planned. This is the front door of the OS. | P1 | Request gateway |
| 2 | **3-path request gateway (Tier 1/2/3)** | Lookup (zero model), quick answer (bounded model), and planned work (versioned workflow) are the core routing contract. | P1 | JEV Routing Agent |
| 3 | **Conversation/request identity & correlation** | Required to preserve context across shells and resume work tomorrow. | P1 | Gateway |
| 4 | **Project Hub: create/import project** | The user's core complaint: Projects screen has no New project or import flow. Required before any binding can happen. | P1 | Workspace identity |
| 5 | **Project → workflow binding** | A project must be linked to one or more published workflow versions with environment, defaults, and version policy. | P1 | Project Hub, Workflow Studio |
| 6 | **Workflow Studio** | Separate workspace for reusable workflow definitions before any project exists. Required for the workflow-first creator journey. | P1 | Web shell |
| 7 | **Idea-driven recommendations (creator journey)** | The user explicitly promoted this to Must. Describe an idea and receive editable plan + catalog-backed component choices with fit/source/permissions/cost. | P1 | Workflow Studio |
| 8 | **Versioned workflow definitions (draft → publish → freeze active runs)** | Active runs must not be silently mutated. Versioning is a trust boundary. | P1/P2 | Workflow Studio |
| 9 | **Lossless copy/paste of whole workflow or selected fragments** | Required for reuse and composition; must remap IDs and surface unresolved boundary ports. | P1 | Workflow Studio |
| 10 | **Forge Method Engine (11 phases as reusable template)** | The OS is an execution control plane. The 11 phases are an optional but available SDLC template. | P2 | Request gateway |
| 11 | **Small work items with identity, dependencies, I/O, checks** | The atomic unit of planned work. Without this, there is no inspectable execution. | P2 | Forge engine |
| 12 | **Durable execution records (run/invocation/attempt)** | Without durable state, pause/resume/recovery are impossible. | P3 | Forge engine, workflow engine |
| 13 | **Pause / resume / cancel with settlement semantics** | Core user control over owned execution. | P3 | Durable runner |
| 14 | **Native Execution Engines (CLI adapters)** | The user clarified execution must cover CLI tools, not only APIs. Adapters for Claude Code, Codex, OpenCode, Ollama/local endpoints. | P3 | Durable runner, provider registry |
| 15 | **Human Approval Checkpoint** | Explicit pause before tool/model execution when side effects, cost, or policy thresholds are exceeded. | P3 | Durable runner, tool registry |
| 16 | **Agent Studio (profiles + snapshots at admission)** | Reusable agents are a core abstraction; snapshots preserve trust. | P4 | Durable execution |
| 17 | **Skill & Instruction Channel** | Separates trusted instructions from retrieved knowledge; required for safe agent behavior. | P4 | Agent studio |
| 18 | **Hermes Self-Improvement Review** | Explicitly required by the user. Turns Hermes back on the platform itself for plan/code/decision/skill review. | P4 | Agent studio, skill channel, evidence archive |
| 19 | **Knowledge Vault with Obsidian sync** | Explicitly required by the user. Human-readable knowledge with bidirectional sync is a core interface. | P1 | Markdown storage, file watcher |
| 20 | **Event + Evidence Archive** | All execution produces versioned, sanitized, auditable records including first-failure preservation. | P3 | Durable runner |
| 21 | **Provider Registry + Allowance Governor** | The OS must track and enforce budgets across requests/interfaces/agents. Must cover all available providers: OpenAI, Anthropic, Google, xAI, Mistral, OpenCode, Ollama, NVIDIA, Zhipu, plus pluggable additions. | P5 | Request gateway, agent studio |
| 22 | **MCP Gateway + Connector Registry** | Required to connect tools safely; market-like UI for non-IT users. Must support both APIs and CLI processes. First connectors: Gmail, Calendar, Drive, YouTube, GitHub. | P6 | Durable execution, security sandbox |
| 23 | **Performance Rules Engine (31 criteria)** | The user requested this be a step in the OS as rules/solids for implementation. It gates quality. | P0/P8 | Repository, CI |
| 24 | **Web shell: chat composer + home dashboard + execution monitor** | The primary user-facing surface for all three user types. | P1/P2 | Request gateway, Forge engine |
| 25 | **English + Arabic with true RTL** | Required inclusive interface; identifiers/paths stay LTR. | P1 | Web shell |
| 26 | **WCAG 2.2 AA accessibility** | Required for keyboard, focus, screen-reader, reduced-motion support. | P1/P8 | Web shell |
| 27 | **Security boundaries (identity, roles, credentials, instruction separation)** | Required for trust. Credentials never in config rows; instructions are not policy by default. | P0/P1 | Identity provider decision |
| 28 | **Safe sharing/import/export** | Private by default; public publishing requires secret stripping, ACL/provenance/license review; destination users bind their own connections. | P1 | Workflow Studio |
| 29 | **Preflight validation without dispatch** | Missing credentials/runner/permission must remain a truthful blocker that does not start work. | P1/P2 | Workflow binding |
| 30 | **Live monitor: actual run graph, not fixture** | Open execution plan must reach the matching project's selected run or "No run yet", never the E04-02 fixture by default. | P2 | Durable runner |

### Must-have acceptance rule

P4 is complete only when a user can: ask a request → see it routed with explanation → get a quick answer or a planned workflow → inspect small items → run/pause/resume → see evidence → trigger a Hermes self-review → and read the same knowledge in Obsidian and the web UI. Plus: create a workflow before a project exists, bind it to a project, start a run, and see that run's actual graph in the monitor.

---

## 2. Should-have capabilities

These make the product complete, observable, and maintainable. They are not strictly required for the first shippable slice, but they are planned and have explicit acceptance criteria.

| # | Capability | Why it is a should | Phase | Depends on |
|---|---|---|---|---|
| 1 | **Speech Service** | From the first image: Whisper + Kokoro are shown as core infrastructure, not an afterthought. Enables voice orb in Obsidian and web. | P3 | Web shell, Obsidian sync |
| 2 | **Agent Swarm / Coordinator** | From the second image: multi-agent orchestration with a coordinator delegating to agents. Useful for complex planned work. | P5 | Agent studio, durable runner |
| 3 | **JARVIS HUD web shell polish** | Dashboard + chat + voice orb + terminal tab aesthetic from the first image. | P1/P8 | Web shell, speech service |
| 4 | **Real-time SSE/live updates with reconnect/replay** | Essential for monitoring, but polling can substitute in early phases. | P3 | Durable runner, event archive |
| 5 | **Help center + global search across all indexed entities** | Critical for discoverability, especially for non-IT users, but not required to execute the first workflow. | P7 | Knowledge vault, secondary records |
| 6 | **Secondary workspaces (projects, workflows, agents, skills, providers, evidence, activity, decisions, settings)** | Needed for long-term operation, but the three primary screens cover the first journey. | P7 | Core engine, registry data |
| 7 | **Nested subworkflows, conditions, branches, joins in workflow editor** | Important for real-world workflows; the current flat flow editor is enough for P2. | P2/P6 | Versioned workflow engine |
| 8 | **Idempotency/reconciliation testing for external side effects** | Critical for production safety; initial demos can avoid destructive actions. | P3 | MCP gateway, durable runner |
| 9 | **RUM (Real User Monitoring) feedback loop** | Feeds the 31-criteria engine with real data, but synthetic metrics can start. | P8 | Performance rules engine |
| 10 | **CI performance/security/market validation gates** | Required for ongoing quality; the existing CI covers the initial scaffold. | P0/P8 | CI workflows, rules engine |
| 11 | **Operational runbook, backup/restore, upgrade guide** | Required for production operations, but not for the first local demo. | P8 | Deployment packaging |
| 12 | **Hermes `/os` skill with full command surface** | The existing `/factory` skill can evolve; web shell is the primary early interface. | P9 | Most core features |
| 13 | **LLM Council Adapter (governance review)** | Required for high-stakes review phases; produces evidence, not acceptance. | P5 | Provider registry |
| 14 | **LLM Council Workflow Node** | A first-class node type for multi-model deliberation. | P5 | LLM Council adapter, workflow editor |
| 15 | **LLM Council ranking UI with de-anonymization display** | Important for transparency; raw stage data can be shown first. | P5 | LLM Council adapter |
| 16 | **Agent/MCP marketplace publishing (local sharing beyond single user)** | Useful for reuse, but a personal registry is enough for the first slice. | P6/P7 | Market infrastructure |
| 17 | **Conflict detection and bounded file-watcher loop prevention for Obsidian** | Required for safe sync, but initial sync can be manual/polling. | P1/P7 | Obsidian sync |
| 18 | **Responsive layouts beyond basic adaptation** | Required for tablets and narrow screens, but desktop-first is acceptable for early validation. | P1/P8 | Web shell |
| 19 | **Durable schedules and notifications** | Required for automation, but the first workflow can be manually triggered. | P8 | Durable runner |

### Should-have acceptance rule

P8 is complete only when the system is observable, searchable, resilient to external side effects, operationally documented, and the 31 performance criteria are feeding real or synthetic data into CI gates.

---

## 3. Nice-to-have / future capabilities

These are valuable but do not block the core identity. They can be added after the Must and Should items are evidence-complete.

| # | Capability | Why it is nice-to-have | Earliest consideration |
|---|---|---|---|
| 1 | **Voice input/output** | Listed as "optional voice" in the original Mahmoud OS prompt; not explicitly required by the user. | P9 or later |
| 2 | **Obsidian plugin (custom UI beyond sync)** | The sync is must-have; a dedicated plugin is a convenience layer. | P9 or later |
| 3 | **CLI shell** | Useful for automation; the web + Hermes skill cover primary interaction. | P9 or later |
| 4 | **Mobile app / PWA optimization** | The responsive web shell is the baseline; a dedicated mobile experience is future work. | After P8 |
| 5 | **Community/public marketplace** | Sharing agents/skills/MCPs publicly; local/private registry is the baseline. | After P7 |
| 6 | **Advanced plugin ecosystem beyond MCP** | MCP is the standard bridge; custom plugins are a future extension point. | After P6 |
| 7 | **Multi-tenant SaaS deployment** | Single-user/local/private-cloud is the baseline. | After P8 |
| 8 | **Advanced observability dashboards** | OpenTelemetry traces/metrics are enough initially; fancy dashboards are future polish. | After P8 |
| 9 | **AI-generated documentation from evidence** | Can be built on top of the evidence archive later. | After P7 |
| 10 | **Advanced Arabic voice recognition** | Voice is already future; Arabic ASR quality is an additional risk. | After voice is prioritized |
| 11 | **Custom themes beyond light/dark** | Accessibility and two themes are must; custom themes are polish. | After P8 |
| 12 | **Social/collaboration features (comments, mentions, shared workspaces)** | Mahmoud OS is currently a personal OS; collaboration is a major scope expansion. | Future major release |
| 13 | **Public REST API for external integrations** | Internal API is the must; a documented public API is a future product surface. | After P8 |
| 14 | **Advanced workflow animation / 3D graph views** | Motion should explain state; excessive animation is explicitly discouraged by the Forge UI direction. | Future polish, if ever |
| 15 | **Credits/payment packs and commerce** | Preserved from forge-ai for complete product; outside first slice. | After P8 |

---

## 4. Dependency map across buckets

```
Must
├── JEV Routing Agent ──→ Request Gateway ──→ 3-path routing
├── Project Hub ──→ Project-workflow binding
├── Workflow Studio ──→ Idea assistant + Versioning + Copy/paste + Sharing
├── Forge Method Engine ──→ Small work items ──→ Durable runner
├── Durable runner ──→ Pause/resume/cancel ──→ Event + Evidence archive
├── Native Execution Engines ──→ CLI adapters (Claude Code, Codex, OpenCode, Ollama)
├── Human Approval Checkpoint ──→ Tool/model execution gate
├── Agent Studio ──→ Skill/Instruction channel ──→ Hermes Self-Review
├── Provider Registry ──→ Allowance Governor
├── MCP Gateway ──→ Connector Market (APIs + CLI)
├── Knowledge Vault ──→ Obsidian sync
├── Performance Rules Engine
└── Web shell (EN/AR, accessibility)

Should (build on Must)
├── Speech Service
├── Agent Swarm / Coordinator
├── LLM Council adapter + node + UI
├── JARVIS HUD polish
├── Real-time SSE
├── Help + search
├── Secondary workspaces
├── Advanced workflow constructs
├── Idempotency/reconciliation tests
├── Schedules/notifications
├── RUM + CI gates
└── Operational docs

Future (build on everything above)
├── Voice input/output
├── Obsidian plugin custom UI
├── Dedicated CLI shell
├── Mobile / SaaS multi-tenant
├── Community marketplace
├── Public API
└── Commerce/credits
```

---

## 5. Build order recommendation

### First shippable slice (end of P4)

All Must items in rows 1–30 above must be present with evidence. This is the smallest thing that can be called Mahmoud OS.

### Complete product (end of P8)

All Must items + all Should items must be present with evidence. This is the product the user can run every day with confidence.

### Future expansion (P9+)

Select Nice-to-have items based on actual usage. Do not start these until the user confirms they are needed and the core is green on CI.

---

## 6. User-specific clarifications

Based on your explicit requests, these items were promoted from "future/nice-to-have" or "should" to **Must**:

- **Obsidian** — moved from optional plugin to required native knowledge-vault interface.
- **Hermes Self-Improvement Review** — moved from optional governance to required built-in capability.
- **JEV / routing agent** — specified as an explicit, first-class system agent, not a hidden classifier.
- **CLI execution engines** — execution must cover CLI tools (Claude Code, Codex, OpenCode, Ollama), not only APIs.
- **Idea-driven workflow/agent/skill/MCP/tool recommendations** — promoted to Must as the core creator journey.
- **Project creation/import + project-workflow binding** — promoted to Must to address the reported project gap.
- **Workflow Studio as separate reusable template workspace** — promoted to Must.
- **Lossless copy/paste of whole workflow or selected fragments** — promoted to Must.
- **Safe sharing/import/export** — promoted to Must.
- **Preflight without dispatch** — promoted to Must.
- **Live monitor showing actual run, not fixture** — promoted to Must.

These providers are explicitly included in the pluggable provider registry:

- OpenAI, Anthropic, Google, xAI, Mistral, OpenCode, Ollama, NVIDIA, Zhipu, and any available provider via adapter pattern.

These connectors are explicitly included in the first market set:

- Gmail, Calendar, Drive, YouTube, GitHub, plus Files, APIs, Browser, Tests, and CLI processes.

These items remain **Nice-to-have** because they were not explicitly requested and are not core to the identity:

- Voice input/output (Speech Service is Should; full voice interaction is Future)
- Dedicated CLI shell beyond the Hermes skill
- Mobile app / PWA beyond responsive web
- Community/public marketplace
- Multi-tenant SaaS
- Advanced observability dashboards
- Public REST API
- Obsidian plugin custom UI beyond sync
- Advanced Arabic voice recognition
- Commerce/credits (preserved scope but outside first slice)

---

## 7. What this classification changes in the blueprint

This classification does **not** change the blueprint. It is a lens for scheduling work. The phased roadmap in the blueprint already reflects this priority:

- **P0–P4:** All Must items.
- **P5–P8:** All Should items.
- **P9+:** Nice-to-have / Future items.

If you want to accelerate, the only safe cuts are Nice-to-have items. No Should item should be cut before its dependent Must item is evidence-complete.

---

*End of classification. No code changes made.*
