# Mahmoud OS — Master Blueprint

> **Working name:** Mahmoud OS
> **Product experience layer:** Mahmoud OS user-facing shell and creator workflows
> **Governed implementation baseline:** `saidtech-forge/New-forge`
> **Behavioral/parity reference:** `saidtech-forge/forge-ai`
> **Bounded monitoring adapter:** `workflow-observer` (local FastAPI/SQLite observation pattern)
> **Document purpose:** Consolidated successor specification. Describes the complete product, how source concepts join, and the phased build plan. No code is changed by this document.
> **Version:** 2.0
> **Date:** 2026-11-11

---

## 1. Product identity

Mahmoud OS is a personal agentic operating system: one workspace where a user asks for work, the system decides how to answer, then carries it out through versioned workflows, reusable agents, skills, and MCP-connected tools. It is the workflow-first product experience for the existing New Forge control plane.

Core journey:

```
Describe an idea → review proposed workflow and recommended helpers/abilities/connections/tools
→ edit and compose the workflow → validate/test → publish a version
→ create/select a project and link the workflow → start an admitted run
→ inspect the actual graph, steps, outputs and repair process live
```

It is deliberately not a generic "AI dashboard" or chatbot. It is an execution control plane with three user faces:

| User type | Primary interface | What they do |
|---|---|---|
| **Citizen / non-IT user** | Chat-first assistant + dashboard | Ask for outcomes, approve plans, track progress, receive results |
| **Builder / developer** | Workflow Studio + Agent Studio | Design reusable workflows, agents, skills, MCP connectors |
| **Operator / architect** | Execution monitor + evidence + settings | Observe runs, review evidence, manage allowances, audit performance |

---

## 2. Merge decisions and authority

- Mahmoud OS is the product experience; New Forge provides the execution foundation.
- New Forge remains a connected project with its own canonical requirements and acceptance authority.
- Preserve existing code, features, behavior, identity, design, project boundaries and governance from New Forge.
- Inspect current source before deciding what is missing.
- Retain the existing eleven engineering phases as a reusable SDLC template, not mandatory stages of every user workflow.
- Preserve the cool-blue/slate supplied UI, including light/dark themes and bilingual (EN/AR) behavior.
- User instructions and approved contracts govern. This blueprint does not replace approvals or authorize installation, production change, merge, public release or expanded access.
- Install or update no tool, skill, MCP server, plugin, dependency or service without explicit approval of the concrete change.
- Confirmed security findings are non-waivable. Neither a tool's score, a council vote nor a manual "accept risk" can bypass them.

---

## 3. How the source concepts join

| Source prompt/repo | Core concept | Role inside Mahmoud OS |
|---|---|---|
| **Mahmoud OS prompt v2.0** | Personal agentic OS with daily overview, knowledge vault, connectors, voice, Obsidian, The Bridge, JEV routing | User-facing shell, daily workspace, knowledge store, request router, creator workflows |
| **Forge Framework prompt** | 11-phase engineering methodology, small-item traceability, evidence/acceptance separation | Reusable SDLC template inside the OS; user workflows may optionally use it |
| **New-forge** | Governed rebuild with React/Vite/React Flow, typed Python services, PostgreSQL, Temporal, policy/control, 25 epics, 134 tasks, approved P01–P17 contracts | Governed implementation baseline and canonical execution foundation |
| **forge-ai** | Legacy 8-phase app-builder with agent/skill/pipeline/sharing/source, 36+ tables | Behavioral/parity reference for F01–F50 feature preservation; security defects must not be ported |
| **workflow-observer** | FastAPI/SQLite local observer with 11-phase view, provider adapters, SSE, React Flow | Bounded monitoring/UI adapter pattern; not the product foundation |
| **LLM Council (karpathy/llm-council)** | Multi-model deliberation with peer review and chairman synthesis | Governance/review agent + multi-model workflow node |
| **Hermes Self-Improvement Review** | Agent that reviews the OS's own plans, code, decisions, and skills and proposes improvements | Built-in governance loop; keeps the platform aligned with its own rules and the user's conventions |
| **Performance 31 criteria** | Skeleton, caching, debounce, RUM, etc. | Embedded as platform governance rules + audit gates |

---

## 4. Product outcomes

A user should be able to:

1. Open the workspace and see what is active, what needs a decision, and what is blocked.
2. Type a request in one composer; the system routes it to:
   - **Lookup:** recorded status, rules, knowledge (zero model calls).
   - **Quick answer:** bounded model response with source references.
   - **Planned work:** a versioned workflow with small items, agents, skills, and evidence.
3. Inspect a proposed plan before execution when policy requires review.
4. Follow the current project → milestone → epic → canonical task → workflow version → phase → work group → small work item → invocation → attempt.
5. Configure agents, skills, providers, workflow steps, and limits through understandable interfaces.
6. Pause, resume, or cancel owned execution; observe independent sessions without claiming control.
7. Return tomorrow and recover the same context without reconstructing history.
8. Create or update agents, skills, and MCP connectors through a market-like UI, even as a non-IT user.
9. See performance and quality rules as first-class constraints, not hidden checklists.
10. Trigger a **Hermes Self-Improvement Review** that audits a plan, code change, decision, or skill against the platform's own rules and proposes a bounded improvement with evidence.
11. Use **Obsidian** as a native interface to the knowledge vault, with bidirectional links, file-based records, and conflict-aware sync.
12. Create workflows without first creating a project; later bind reusable workflows to one or more projects.

---

## 5. Architecture

### 5.1 High-level layers

```
┌───────────────────────────────────────────────────────────────────┐
│  SHELLS:                                                         │
│    • Next.js web shell (JARVIS HUD-style dashboard + chat)       │
│    • Obsidian plugin (notes, dashboard, voice orb, terminal tab) │
│    • Hermes skill (text/voice commands)                            │
│    • Speech Service (Whisper STT + Kokoro TTS)                   │
├───────────────────────────────────────────────────────────────────┤
│  THE BRIDGE — shared backend that receives requests from both   │
│  front doors and coordinates routing, execution, tools, and memory│
├───────────────────────────────────────────────────────────────────┤
│  REQUEST ROUTER (JEV) — driven by the JEV Routing Agent:       │
│    01. Saved knowledge / rules / operational queries  (no model)  │
│    02. Quick Answer          (bounded model)                     │
│    03. Real Work             (Forge workflow / planned execution)│
├───────────────────────────────────────────────────────────────────┤
│  FORGE METHOD ENGINE (reusable SDLC template):                   │
│    11 phases · small items · evidence · acceptance separation    │
├───────────────────────────────────────────────────────────────────┤
│  EXECUTION PLATFORM:                                             │
│    Workflow Studio + versioned definitions                       │
│    Agent Studio + agent profiles + skill/instruction channel     │
│    Agent swarm + coordinator (for multi-agent tasks)             │
│    Native execution engines: Claude Code CLI, Codex CLI,         │
│      OpenCode CLI, Ollama/local, plus all available providers    │
│    Human approval checkpoint before tool/model execution         │
│    Provider registry + allowance governor                        │
│    LLM Council adapter (review agent + workflow node)            │
│    MCP gateway + connector registry (Files · APIs · Browser · Tests · CLI)│
│    Durable orchestration / event store / recovery / pause / resume│
├───────────────────────────────────────────────────────────────────┤
│  KNOWLEDGE & MEMORY:                                             │
│    Markdown vault (native Obsidian sync) + semantic search       │
│    Daily notes · reports & research · conversations · request logs│
│    Decision log + activity history + evidence archive            │
├───────────────────────────────────────────────────────────────────┤
│  HERMES SELF-IMPROVEMENT REVIEW:                                 │
│    Plan/code/decision/skill audit · bounded improvement proposals│
│    Evidence-backed suggestions · user approval before apply        │
├───────────────────────────────────────────────────────────────────┤
│  PERFORMANCE & QUALITY RULES:                                    │
│    31-criteria audit + budgets + RUM + automated gates          │
└──────────────────────────────────────────────────────────────┘
```

### 5.2 What we already have and where it maps

| Existing source | What it currently does | Future role in Mahmoud OS |
|---|---|---|
| `New-forge` React/Vite/React Flow shell | Workflow library, create/draft, canvas, parameter inspector, publication, version/diff/clone, child selector | Becomes the primary web shell and Workflow Studio |
| `New-forge` registry services | Draft creation/save, ETag/CAS revisions, typed node manifest validation, compile/publication, immutable packages, dependencies, clones, outbox/replay | Foundation for reusable workflow versions and safe copy/paste |
| `New-forge` runtime services | Transactional admission, control commands, durable replay/inspection, phase projections, Temporal run workflow/activities, child workflows, recovery/fencing/custody | Foundation for durable execution and live monitoring |
| `New-forge` agent services | Persisted drafts/releases, publication, graph identity/checkpoint interfaces, deterministic skill composition, package inspection/quarantine | Foundation for Agent Studio and skill channel |
| `New-forge` models services | Profiles/resolution, pooled reservation/usage, adapter ledger, native HTTP/CLI boundaries, OpenCode Go/Codex/Claude/Ollama/NVIDIA adapters | Foundation for provider registry and allowance governor |
| `New-forge` tools/connections services | MCP streamable HTTP, discovery/manifests, scope/network policy, sandbox controller, credential-stage leases | Foundation for MCP/connector market |
| `New-forge` projects/artifacts services | Project/artifact schema, immutable versions, content validation/scanning, upload intent/finalize/promotion, retention, object-store | Foundation for project hub and evidence archive |
| `forge-ai` | Legacy pipeline CRUD, agent/skill creation, sharing/cloning, YAML copy/import/export, review/repair, Guardian, memory | Behavioral/parity reference for F01–F50; security defects must not be ported |
| `workflow-observer` | FastAPI/SQLite control plane, native/API adapters, durable SSE events, React Flow, 11-phase observation | Bounded monitoring adapter pattern; optional module |
| `dynamic-factory` (our earlier scaffold) | Next.js 15 + FastAPI + basic ReactFlow | Set aside; planning-only context |

### 5.3 New major components to add

| Component | Responsibility |
|---|---|
| **The Bridge** | Shared backend gateway that normalizes input, authenticates, identifies workspace, applies policy, resolves permitted context, creates request records, and coordinates routing/execution |
| **Speech Service** | Local Whisper STT + Kokoro TTS; exposes speech-to-text and text-to-speech to both front doors |
| **JEV Routing Agent** | Explicit system agent that classifies every request into lookup/quick/planned using deterministic rules first, context inspection, bounded model fallback; explains its routing decision |
| **Request Router (JEV)** | The gateway layer that applies the routing agent's classification; manages conversation identity and correlation IDs |
| **Forge Method Engine** | Store and enforce the 11-phase SDLC template, small-item schema, dependency validation, evidence/acceptance separation |
| **Workflow Studio** | Separate workspace for creating, editing, versioning, copying, sharing, and publishing reusable workflow definitions before any project exists |
| **Project Hub** | Create/import project, bind one or more workflow versions, preview effective configuration, preflight, run history |
| **Agent Studio** | Create reusable agent profiles with role, instructions, skill references, provider/model route, limits, permissions |
| **Agent Swarm / Coordinator** | Multi-agent orchestration: a coordinator delegates sub-tasks to worker agents and aggregates results |
| **Skill & Instruction Channel** | Store versioned skill references, enforce source/hash compatibility, separate trusted instructions from retrieved knowledge |
| **LLM Council Adapter** | Governance reviews + multi-model workflow node: stage-1 responses, anonymized stage-2 peer review, chairman synthesis |
| **Hermes Self-Improvement Review** | Built-in review agent/skill that audits the OS's own plans, code, decisions, and skills and proposes bounded improvements with evidence |
| **MCP/Connector Market** | Registry of MCP servers/connectors; non-IT users enable them with scoped permissions; first examples: Gmail, Calendar, Drive, YouTube, GitHub |
| **Knowledge Vault** | Markdown-based human-readable knowledge with revisions, source, provenance, search, embeddings; content types: daily notes, reports/research, conversations, request logs |
| **Provider Registry** | Pluggable adapters for OpenAI, Anthropic, Google, xAI, Mistral, OpenCode, Ollama, NVIDIA, Zhipu, and any available provider; tracks budgets and routes per agent |
| **Allowance Governor** | Cross-request/provider budget tracking, holds, bounded failover, stop on exhaustion; enforce 70% automation / 30% interactive reserve |
| **Durable Runner** | Persist execution state, support pause/resume/cancel, idempotent side effects, recovery from checkpoint |
| **Event + Evidence Archive** | Versioned event envelope, sanitized I/O, artifact links, first-failure preservation |
| **Performance Rules Engine** | 31 criteria as enforceable rules; audit, report, and gate changes |
| **Human Approval Checkpoint** | Explicit pause before tool/model execution when side effects, cost, or policy exceed configured thresholds |
| **Native Execution Engines** | Adapters for local CLI agents such as Claude Code CLI, Codex CLI, OpenCode CLI, and Ollama/local endpoints; run as background processes with streamed output and artifact capture |

---

## 6. Data model / identity hierarchy

### 6.1 Canonical work hierarchy

```
Workspace
 └─ Request
     └─ Project
         ├─ Milestone
         │   └─ Epic
         │       └─ Canonical Task
         │           └─ Run
         │               └─ Phase / Work Group / Small Work Item / Invocation / Attempt
         ├─ Workflow bindings (one or more)
         ├─ Files and evidence
         ├─ Settings / effective configuration
         └─ Runs history
```

### 6.2 Reusable definition hierarchy

```
Workflow Definition (in Workflow Studio)
 └─ Draft
 └─ Published Version (immutable)
     ├─ Steps / nodes (agent, tool, human, condition, join, wait, subworkflow)
     ├─ Edges / dependencies
     ├─ Input/output contracts
     ├─ Child workflow references (pinned versions)
     └─ Required capabilities / connectors / permissions
```

### 6.3 Project → workflow binding

| Entity | Purpose |
|---|---|
| `projects` | Name, description, type, owner, workspace, source repository/branch, settings |
| `workflow_definitions` | Reusable templates (name, objective) |
| `workflow_versions` | Immutable published versions of a definition |
| `project_workflow_bindings` | Which workflow versions are linked to a project, with environment, input defaults, version policy, and activation state |
| `project_runs` | Run of a workflow version within a project, pinned to exact versions and effective configuration |
| `run_tasks` | Mapping of canonical tasks to workflow steps |

Rules:

- A project may use several workflows.
- One workflow can serve several projects with distinct inputs and permissions.
- A run pins exact workflow/child/agent/skill version and source/configuration revision.
- Later edits to a workflow definition do not rewrite active or historical runs.

---

## 7. The three-path router (JEV)

Every request enters through **The Bridge** carrying workspace, source interface, language, received time, and correlation ID. **JEV** is the required request-management/routing component.

### 7.1 JEV Routing Agent

The routing agent is an explicit system agent with its own profile, skill references, and decision log. It classifies each request into one of the three paths using:

1. **Rules first:** keyword, schema, and context rules that map unambiguous lookups to Tier 1 and simple question patterns to Tier 2.
2. **Context inspection:** current project, active task, conversation history, available skills, known blockers.
3. **Bounded model fallback:** when rules are insufficient, a small model call is used with a strict prompt, short timeout, and recorded cost.
4. **Explanation:** the agent returns the selected path in ordinary language and a confidence indicator.
5. **Escalation:** materially ambiguous requests are surfaced to the user as a clarification, not guessed.

Routing rules must be editable and versioned. Deterministic routing runs first. A model classifier is optional for ambiguity.

### 7.2 Tier 1 — Saved knowledge, rules, and operational queries

- Handle explicit preferences, known facts, exact rules, saved responses, run status, schedules, and connection status.
- Use deterministic rules and indexed text/metadata lookup.
- This path must not invoke a generative model or an embedding model at request time.
- Return source and timestamp where relevant.
- Enforce workspace/user scope, freshness, content version, and authorization.

### 7.3 Tier 2 — Quick answer

- Use a configured low-cost/low-latency model.
- Enforce token, time, context, and tool limits.
- Use only the minimum authorized context.
- Keep this path answer-focused. A request needing material side effects must enter Tier 3.
- Escalation creates an observable routing event and preserves the original request.

### 7.4 Tier 3 — Real work

- Create a plan and a run with bounded tasks.
- Validate dependencies, input/output schemas, permissions, required connectors, budgets, and available runners.
- Execute only ready tasks; parallelize independent tasks within resource and account limits.
- Verify results before completion.
- Produce linked artifacts and a concise completion report.

The selected tier, a short routing explanation, and any escalation are shown to the user. Users may override the route when policy and capabilities allow it. The actual policy decision is preserved in the audit record.

---

## 8. The eleven engineering phases (Forge)

The eleven engineering phases are a **reusable SDLC template**, not mandatory stages of every user workflow. A three-step document workflow should execute its own three-step graph; a business workflow need not have a code repository or an Implement phase.

| # | ID | Friendly name | What happens |
|---|---|---|---|---|
| 1 | `spec` | Specify | Understand requirements, clarify gaps, define acceptance examples |
| 2 | `plan` | Plan | Architecture, interfaces, ownership, validation approach |
| 3 | `tasks` | Decompose | Define small executable items and checks |
| 4 | `analyze` | Analyze | Check consistency, coverage, feasibility, conflicts |
| 5 | `preflight` | Preflight | Verify source, permissions, environment, provider readiness |
| 6 | `implement` | Implement | Deliver bounded changes, component reviews, focused checks |
| 7 | `review` | Review | Independent review of the complete candidate |
| 8 | `verify` | Test & verify | Run acceptance and regression checks |
| 9 | `converge` | Converge | Resolve findings, reconcile evidence |
| 10 | `integrate` | Integrate | Integrate the reviewed candidate through policy |
| 11 | `handoff` | Handoff | Deliver artifacts, guidance, remaining acceptance |

Rules:

- Every phase must be inspectable even before a managed run exists.
- A component review inside Implement does not pass the parent phase.
- Small-item completion cannot pass its parent phase/task.
- Cycles and missing prerequisites are explicit.

---

## 9. LLM Council integration

LLM Council contributes two distinct capabilities:

### 9.1 Governance / review agent

- Used at the `review`, `converge`, or `handoff` phases.
- Takes a candidate output, dispatches it to multiple models for blind peer review, anonymizes responses, collects rankings, then asks a designated chairman model to synthesize a final assessment.
- Result is **evidence**, not acceptance.
- Configuration: which models sit on the council, chairman model, ranking prompt, timeout, cost budget.

### 9.2 Workflow node: multi-model deliberation

- A node type in the workflow editor: `LLM Council`.
- User configures the question/candidate, the council members, and the chairman.
- Node outputs: all stage-1 responses, stage-2 evaluations, aggregate rankings, chairman synthesis.
- Used for high-stakes generation, comparison, or decision support.

Implementation reuse:

- Use the existing provider registry for model adapters.
- Add an `LLMCouncilClient` that orchestrates parallel calls, anonymization, ranking parsing, and synthesis.
- Store council results as structured artifacts linked to the invocation.

---

## 10. Hermes Self-Improvement Review

Mahmoud OS contains a built-in review capability that turns Hermes back on the platform itself. It is a system agent (or family of agents) with a dedicated skill and workspace.

### 10.1 What it reviews

| Review target | Question it answers | Output |
|---|---|---|
| **Plan / blueprint** | Does the plan follow Forge phases? Are acceptance criteria concrete? Are dependencies valid? | List of gaps and a refined plan proposal |
| **Code change** | Does the change satisfy the original task? Are tests, types, security, and performance rules met? | Review report with file:line citations and a patch suggestion |
| **Decision** | Is the decision justified by the linked evidence? Are risks and alternatives recorded? | Decision audit note |
| **Skill / instruction** | Is the skill reference valid, versioned, and compatible? Does it promote safe behavior? | Skill review report and update recommendation |
| **Agent profile** | Are role, provider route, permissions, and limits appropriate and within policy? | Profile review note |

### 10.2 Review workflow

1. **Trigger:** user, scheduler, or policy requests a review of a specific target.
2. **Context gathering:** the agent loads the target, original requirements, related evidence, knowledge notes, and the user's conventions (e.g., AGENTS.md).
3. **Rule-based checks first:** verify format, traceability, dependency order, budget, security checklist.
4. **Bounded model review:** if needed, a model reads the material and proposes improvements.
5. **Evidence packaging:** the review produces a structured report with citations, severity, and proposed actions.
6. **User approval:** the platform **never** applies a self-improvement suggestion automatically. The user approves each proposed change, and the platform records the approval as an event.
7. **Apply and re-verify:** approved changes go through the normal Forge admission gates (preflight → implement → review → verify).

### 10.3 Hermes skill interface

- `/os review plan <id>` — review a plan or workflow version.
- `/os review code <task-id>` — review the code linked to a canonical task.
- `/os review decision <id>` — review a decision record.
- `/os review skill <skill-id>` — review a skill reference.
- `/os review self` — run a health/quality audit on Mahmoud OS itself (triggers the 31-criteria scan plus architecture checks).

### 10.4 Trust boundary

- Self-improvement suggestions are **data**, not trusted platform policy, until explicitly approved and merged.
- The review agent cannot change production configuration, secrets, or active workflow definitions on its own.
- All review outputs are stored in the evidence archive and linked to the target they reviewed.

---

## 11. Workflow Studio and project hub

### 11.1 Workflow-first design principle

Workflows are reusable workspace definitions and can exist before any project.

1. **Create** a workflow: blank, choose a template, import a safe package, or describe an idea.
2. **Idea assistant** proposes an editable plan and catalog-backed component choices. Human, deterministic rule, and tool steps are available; not every step needs an LLM.
3. **Edit** graph/groups, instructions, agents, abilities, tools, inputs/outputs, conditions, dependencies, waits, approvals, model routes and limits. Validate without performing side effects.
4. **Publish** an immutable version after required checks. A reusable child workflow has a pinned input/output contract.
5. **Copy/paste** whole workflow or selected parts with ID remapping and unresolved boundary ports surfaced.
6. **Share/fork/export** a version or selected graph with safe remapping and no credentials/private data/approvals.

### 11.2 Project lifecycle

1. **New project** is visible on Projects and in its empty state.
2. Enter name/purpose/type/owner and optional repository/documents; connect only authorized sources.
3. Business projects need not supply GitHub.
4. **Link** a published workflow or several workflows.
5. Review role/purpose, version policy, environment/runner, inputs, connection placeholders and inherited/task overrides.
6. **Preflight** shows missing capability, permission, credentials, output compatibility and budgets without starting work or installing dependencies.
7. **Start run** is a separate explicit action. Admission records project, request/task references, exact published versions, source revision, effective configuration and policy.
8. **Open** that run's real graph in the project. Expand child runs and inspect each step.
9. **Share/fork/export** a version or selected graph with safe remapping.

### 11.3 Composition rules

- A portable, schema-versioned workflow/fragment package identifies selected graph nodes/groups, typed ports, internal edges, required external references, capability/version requirements and provenance/license.
- Paste creates new execution-definition IDs and remaps internal edges.
- Dependencies outside the selection become visible boundary ports or unresolved mappings, never silently dropped.
- Validate DAGs, declared bounded loops, recursion/depth, contracts and parent limits after composition.
- Child pipeline calls pin child versions and I/O contracts, propagate correlation/cancellation/budgets, and expose real child run lineage.
- Default template visibility is private. Separately authorized shared/public publishing requires secret/private-context stripping, ACL/provenance/license review and compatibility checks.
- Never export credentials, private artifacts/context, native provider session/resume tokens or local secret values.

---

## 12. Agents, skills, and MCP market for non-IT users

### 12.1 Non-IT design principle

Non-IT users do not edit JSON, YAML, or React Flow graphs directly. They:

- Browse **templates** and **market cards**.
- Answer plain-language questions.
- Approve or adjust a generated plan.
- Enable connectors with one click and a scope description.

### 12.2 Agent Studio

- Each agent card shows: name, role avatar, what it is good at, provider route, limits.
- Builder view exposes: instructions, skill references, tools permitted, timeout, output budget.
- Non-IT view shows: "This agent helps with ___, uses ___, and can spend up to ___."

### 12.3 Skill Market

- Skills are versioned instruction resources with source, version/hash, and compatibility.
- Cards show: title, purpose, source location, last verified date, trust status.
- Users can "install" a reference (not execute arbitrary code) and assign it to an agent.
- The platform records the reference and checks format/hash.

### 12.4 MCP / Connector Market

- Connectors are scoped adapters to external services and local CLI tools (Gmail, Drive, Calendar, YouTube, GitHub, files, web, Claude Code CLI, Codex CLI, OpenCode CLI, Ollama local endpoint, etc.).
- Tool categories: **Files, APIs, Browser, Tests, CLI processes**.
- Each connector card shows: name, description, permissions it asks for, read-only toggle, connection status.
- Users enable with a click; the system shows "Connected" only when a real, verified connection exists.
- Test adapters are visibly marked **Demo**.
- Disconnected integrations show **"Not connected"** or **"Awaiting configuration"**.

### 12.5 Idea-driven recommendations

The core creator journey is **Must**. When a user describes an idea:

- Recommend existing catalog entries before inventing tools.
- Explain fit, alternatives, source/version/license, trust/review state, compatibility, permissions, external data destinations, setup and estimated/measured/unknown cost.
- Suggestions create a **draft**, not an installation, grant or run.
- Replacing a suggested component revalidates compatibility; no installation or access grant occurs.

---

## 13. Performance and quality rules as platform governance

The 31 performance criteria are not a one-time checklist. They become a **Performance Rules Engine** inside Mahmoud OS:

### 13.1 Criteria as rules

Each of the 31 criteria is stored as a rule with:

- ID, title, description, priority, applicability flags.
- Detection method (static scan, runtime metric, manual review).
- Status per project/component: `applied`, `not-applied`, `needs-improvement`.
- Evidence link.

### 13.2 Audit workflow

1. Inspect code and architecture before proposing any change.
2. Apply a technique only where it fits.
3. Measure before and after, including slow devices/weak networks.
4. Report per-criterion status, priority, and expected impact.
5. Make only fitting improvements.

### 13.3 Automated gates

- CI runs a performance rules scan and reports drift.
- PRs above a size threshold or touching UI/execution paths trigger a performance review.
- RUM data (when available) feeds back into the rules engine.

---

## 14. UI/UX direction

- **Cool blue/slate palette**, quiet light canvas, dark theme, one restrained blue action accent.
- **No generic AI dashboard clichés**: no gradient slogans, glowing cards, decorative network backgrounds, meaningless KPIs.
- **Composition and typography** create identity, not heavy branding.
- **Complete English and Arabic**, true RTL, mirrored navigation, LTR identifiers/paths.
- **Accessibility**: WCAG 2.2 AA target, keyboard operation, visible focus, semantic controls, reduced-motion switch, 44 px touch targets.
- **Motion**: 120–180 ms small feedback, 200–280 ms panels, 280–400 ms layout transitions; motion explains state; reduced motion respected.
- **Primary screens**: Login, Home/Today, Workflow Studio, Project Hub, Execution Monitor, Settings.
- **Responsive**: desktop, laptop/tablet, narrow; on small screens prioritize current work + focused inspector.

---

## 15. Security and trust boundaries

- **Identity:** Preserve New Forge's approved Clerk direction. Local operator auth for control-plane workers is separate. No incidental migration.
- **Project roles and permissions:** Read-only QA/reviewer roles enforced.
- **Credentials:** Stored through the protected mechanism, never ordinary config rows.
- **SSRF/sandbox protections:** For MCP and connector calls.
- **Explicit instruction channel:** AGENTS.md/CLAUDE.md/text from documents are data, not trusted platform policy.
- **Evidence and acceptance are separate:** A checked artifact reference is not canonical acceptance.
- **Status refresh performs zero model calls.**
- **Exhausted allowance stops calls;** suspected limits use bounded probe policy.
- **Quota policy:** Preserve approved 70% automation / 30% interactive reserve for shared Claude/Codex allowance; chat analysis/probes/retries/fallback share the pool; no silent paid spillover.

---

## 16. Operations and deployment

- Docker Compose for local/private cloud.
- Persistent PostgreSQL + Redis (matching New-forge baseline).
- Health/readiness endpoints.
- Logs, metrics (OpenTelemetry), backup/restore, upgrade guidance.
- CI/CD extended for performance/security/market validation.
- Native Windows/macOS/Linux CLI workers via host bridge where needed.
- Support current Windows setup and documented Linux deployment.

---

## 17. F01–F50 preservation mapping

The following legacy capability areas from `forge-ai` and New-forge contracts must be preserved, enhanced, or explicitly governed:

| ID | Capability | New-forge contract | Disposition |
|---|---|---|---|
| F01 | Authentication/account lifecycle | P01/P15 | Preserve Clerk identity; no incidental migration |
| F02 | Project intake and lifecycle | P21/P04 | Enhance with project hub and workflow binding |
| F03 | Document intelligence | P18/P10/P11 | Reuse knowledge vault |
| F04 | Discovery questions | P18/P20 | Integrate into idea assistant |
| F05 | Scope conflicts and client-only decisions | P18/P20 | JEV escalation + human approval |
| F06 | Execution plan approval/disclosure | P21/P02/P04 | Forge method engine + admission |
| F07 | Lifecycle evidence ledger | P10/P13/P21 | Event + evidence archive |
| F08 | Pipeline CRUD/sharing/presets | P02/P03/P17 | Workflow Studio + marketplace |
| F09 | Production stage orchestration | P21/P04/P06 | Durable runner + Temporal |
| F10 | Agent catalog/prompt lifecycle | P06 | Agent Studio |
| F11 | Agent teams/departments | P06/P24 | Agent Swarm / Coordinator |
| F12 | Skill marketplace and packaging | P07/P17/P23 | Skill Market |
| F13 | MCP server registry | P09/P08 | Connector Market |
| F14 | Memory and learning | P06/P11/P23 | Knowledge Vault + feedback |
| F15 | Provider implementations | P12/P12A | Provider Registry |
| F16 | Agent/task/council model bindings | P06/P12A/P13 | LLM Council adapter |
| F17 | Model removal/rebinding | P12A/P12B | Allowance Governor |
| F18 | Provider pauses and context constraints | P12A/P12B | Provider constraints |
| F19 | LLM cache/telemetry/cost | P12/P20 | Usage tracking + RUM |
| F20 | Credits/payment packs | P22 | Preserve scope; outside first slice |
| F21 | Review councils and governance | P13/P19/P21 | LLM Council + Hermes review |
| F22 | Defects/fix/verify/remediation | P21/P13 | Evidence archive + repair chain |
| F23 | Quality/evidence gates | P13/P21 | Performance Rules Engine |
| F24 | SDLC planning and traceability | P21 | Forge method engine |
| F25 | Atomic tasks and timeline | P21/P20 | Small work items + monitor |
| F26 | Queue/operator controls | P04/P25 | Durable runner controls |
| F27 | Distributed daemon/runtime | P25/P01 | Worker/runtime infrastructure |
| F28 | Realtime activity/reactions/pins | P20 | Live updates + SSE |
| F29 | Replay snapshots | P05/P10 | Event replay |
| F30 | Feature/enhancement requests | P20/P21 | Change requests |
| F31 | Project conversational edits | P20 | Chat-first editing |
| F32 | Artifact/review comments | P10/P13/P20 | Evidence discussion |
| F33 | GitHub issues/repository sync | P25/P21 | GitHub connector |
| F34 | Repository upload/ingestion | P25/P10 | Project import |
| F35 | Build/preview/web delivery | P21/P09/P16 | Native execution + delivery |
| F36 | Native mobile delivery | P21/P25 | Preserve scope; future slice |
| F37 | Design and wireframes | P21/P25 | Design-to-code workflows |
| F38 | Code graph/import closure | P21 | Code intelligence |
| F39 | Architecture/document production | P21/P10 | Document generation workflows |
| F40 | Guardian proposals/self-improvement | P23 | Hermes Self-Improvement Review |
| F41 | Guardian idea lifecycle | P23/P18 | Idea assistant |
| F42 | Market research/competitive analysis | P23 | Research workflows |
| F43 | Pattern library/derived principles | P23/P11/P07 | Knowledge patterns |
| F44 | Support desk/SLA routing | P24 | Preserve scope; future slice |
| F45 | Health/SLO and feature flags | P15/P16 | Operations + rules engine |
| F46 | Templates/gallery/project reuse | P17/P02 | Workflow Studio + sharing |
| F47 | Budget/admission/cost envelopes | P22/P12/P04 | Allowance Governor |
| F48 | Data-source authorization/provenance | P18/P08/P11 | Knowledge provenance |
| F49 | Security/PII/prompt injection | P01/P09/P13/P21 | Non-waivable security gates |
| F50 | Race/adaptive execution and confidence | P21/P19/P12A | Bounded adaptive execution |

---

## 18. Phased implementation roadmap

Each phase has a named branch, a verifiable acceptance gate, and a plan document derived from this blueprint. The philosophy: no phase is declared complete without evidence.

### P0 — Foundation and audit

- Establish New-forge as the governed implementation baseline and `forge-ai` as the pinned behavioral/parity reference.
- Create the parity/requirements ledger: F01–F50 + P01–P25 + active criterion/approval IDs + every OS addition.
- Reconcile document scope and architecture; remove contradictory observer-as-product foundations.
- Resolve security and authority prerequisites on the exact intended branch.
- Define performance budget and acceptance targets.
- Produce this master blueprint and a requirements-to-test traceability matrix.
- **Acceptance:** Blueprint approved; parity ledger published; base branch green on CI or blockers honestly reported.

### P1 — Workflow-first creator: project hub, Workflow Studio, and JEV routing

- Implement project creation/import and project-workflow binding.
- Implement Workflow Studio: draft → publish → immutable version, plus lossless copy/paste of whole graph or selected fragments.
- Implement the **JEV Routing Agent** as a first-class agent with deterministic rules, context inspection, bounded model fallback, and explained routing decisions.
- Implement JEV router gateway: Tier 1 lookup, Tier 2 quick answer, Tier 3 planned work.
- Add chat composer + daily home dashboard.
- Add **Obsidian vault sync**: read/write Markdown notes, bidirectional links, conflict detection, file-watcher loop prevention.
- Tests: unit, integration, Playwright smoke for project → workflow → binding journey; Obsidian file sync test.
- **Acceptance:** A user creates a workflow, publishes a version, creates a project, binds the workflow, and starts a run; a typed request is routed with an explained decision; a Markdown note created in Obsidian appears in the web UI and vice versa.

### P2 — Forge method engine and visual execution

- Add 11-phase model, small-item schema, dependency validation.
- Graph/list/timeline views for execution plans.
- Small-item inspector with inputs, outputs, checks, agent assignment, limits.
- Live monitor updates the actual user graph, shows waits/actions/I/O and survives reconnect without duplicate effects.
- Tests: cycle detection, active-snapshot pinning, phase transition rules, reconnect/replay.
- **Acceptance:** A published workflow runs through admitted graph; active runs stay pinned; cycles are refused; every phase is inspectable before any run; monitor opens the matching project's selected run.

### P3 — Durable execution, native engines, and human approval

- Replace in-memory executor with durable run/invocation/attempt records (reuse New-forge Temporal/runtime primitives).
- Add pause/resume/cancel with settlement semantics.
- Add native execution engines (Claude Code CLI, Codex CLI, OpenCode CLI, Ollama/local).
- Add human approval checkpoint before tool/model execution.
- Idempotent operation identities for external side effects.
- Event envelope + SSE/live updates with reconnect/replay.
- Tests: interrupted calls, process restart, lost responses, partial writes, duplicate suppression, approval gate.
- **Acceptance:** One real small task can be interrupted and resumed; no duplicate external actions; reconnect preserves selection; approval gate blocks consequential actions until confirmed.

### P4 — Agent studio, skill market, instruction channel, and Hermes self-review

- Agent profiles with snapshots at admission.
- Skill reference registry with version/hash and format checks.
- Controlled instruction channel separate from knowledge.
- Add **Hermes Self-Improvement Review** skill and API.
- Tests: profile edits affect future admissions only; instruction authority is explicit; self-review produces a structured report and requires approval before applying changes.
- **Acceptance:** Create agent, assign skill, admit invocation; edit profile; verify old invocation keeps original snapshot; run a self-review on a plan and approve/reject its suggestions.

### P5 — Provider registry, LLM Council, allowance governor, and agent swarm

- Extend provider registry with allowance state, holds, retry bounds, failover for all configured providers.
- Add LLM Council adapter (review agent + workflow node).
- Allowance governor across requests/interfaces/agents.
- Add Agent Swarm / Coordinator.
- Tests: exhausted allowance stops calls; bounded probe/failover preserves budgets; council node runs a deliberation end-to-end; swarm delegates and aggregates.
- **Acceptance:** Provider-limit fixture passes without paid calls; council node runs a deliberation; swarm completes a multi-agent task.

### P6 — MCP / connector market

- Connector registry with scopes, read-only flags, health checks.
- Non-IT market UI for enabling connectors.
- MCP gateway with timeout, sandbox, and permission enforcement.
- First examples: Gmail, Calendar, Drive, YouTube, GitHub.
- Tests: disconnected shown as "Not connected"; demo adapters marked; real connection verified before "Connected".
- **Acceptance:** Enable filesystem MCP demo; run a flow that reads a file; verify scope enforcement; connect a real Gmail/Drive/Calendar demo adapter.

### P7 — Knowledge vault and secondary workspaces

- Markdown vault with revisions, sync, search, embeddings.
- Secondary views: projects, workflows, agents, skills, providers, evidence, activity, decisions, settings.
- Help center + global search across all indexed entities.
- Tests: file watcher bounded processing, conflict detection, bilingual search, RTL.
- **Acceptance:** Create note, search it, link to a task, switch language and layout.

### P8 — Performance rules engine, schedules, notifications, and polish

- Implement 31-criteria rules engine, audit UI, and CI gates.
- Add durable schedules, timezone/overlap/missed-run handling, in-app notifications.
- Apply only fitting improvements with before/after measurement.
- Accessibility audit, responsive audit, motion audit.
- Operational packaging: runbook, backup/restore, upgrade guide.
- **Acceptance:** Performance rules report passes; schedules run without duplicate execution; accessibility/responsive tests pass; deployment runbook verified.

### P9 — Hermes skill evolution and voice

- Evolve existing `/factory` skill into `/os` skill with full command surface.
- Same request identity across chat and web.
- (Later) Voice input/output.
- **Acceptance:** Create, review, and monitor a workflow entirely through the Hermes skill; self-review can be triggered from chat.

---

## 19. Deliverables per phase

Each phase produces:

1. **Code changes** on a feature branch with passing CI.
2. **Schema/migrations** when storage changes.
3. **API documentation** for new endpoints.
4. **Design tokens/components** when UI changes.
5. **Tests** (unit, contract, integration, browser, security, concurrency, boundary, recovery, regression as applicable).
6. **Architecture/process diagrams** when structure changes.
7. **Operational runbook** updates.
8. **Requirements/evidence coverage report**.
9. **Honest delivery report** with what changed, how to run it, what was tested, known limitations, and remaining prerequisites.

---

## 20. Immediate next steps (without implementation)

1. Approve or edit this blueprint.
2. Pin the canonical New-forge baseline (main or develop) and confirm branch strategy.
3. Author P0 plan in detail (audit checklist, parity ledger, performance budget, branch strategy).
4. Schedule P0 execution; no code changes until P0 acceptance is recorded.

---

## 21. Open decisions to confirm

1. **New-forge baseline branch:** `main` (8672c5a) or `develop` (e9b00d1, 72 ahead/1 behind)?
2. **Repository location:** continue in `dynamic-factory` as a planning shell, or create a new Mahmoud OS repo that consumes New-forge as a submodule/dependency?
3. **Obsidian sync mode:** direct filesystem watcher to a configured vault path, or plugin-based REST bridge?
4. **Hermes self-review default triggers:** manual only, scheduled, or also gated on policy events?
5. **Voice:** required or experimental?
6. **Deployment target:** local-only first, private cloud, or SaaS-ready from P1?
7. **Workflow-observer role:** reuse as a bounded monitoring adapter, or retire it?

---

*End of blueprint. No code changes made. Implementation begins only after explicit go-ahead on P0.*
