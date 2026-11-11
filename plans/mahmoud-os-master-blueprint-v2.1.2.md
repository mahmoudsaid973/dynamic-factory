# Mahmoud OS — Master Blueprint v2.1.2

> **Working name:** Mahmoud OS
> **Product experience layer:** Mahmoud OS user-facing shell and creator workflows
> **Governed implementation baseline:** `saidtech-forge/New-forge`
> **Behavioral/parity reference:** `saidtech-forge/forge-ai`
> **Bounded monitoring adapter:** `workflow-observer` (local FastAPI/SQLite observation pattern)
> **Document purpose:** Consolidated successor specification. Describes the complete product, how source concepts join, and the phased build plan. No code is changed by this document.
> **Version:** 2.1.2
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
| **New-forge** | Governed rebuild with React/Vite/React Flow, typed Python services, PostgreSQL, Temporal, policy/control, 25 epics, 134 tasks, approved pinned baselines: A00/P01-P05/P06-P10/P12-P14 @ 710e1c1; P12B/P19/P20 @ f2a188a; P15/P17 @ 5b6bbda; P16 @ 666e450 (see FIRST-DELIVERY.json for exact sections) contracts | Governed implementation baseline and canonical execution foundation |
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
4. Choose between a simple workflow track or the optional Forge SDLC track.
5. Follow the current project → workflow version → run → step → attempt (simple track) or project → milestone → epic → canonical task → workflow version → run → phase → work group → small work item → invocation → attempt (Forge track).
6. Configure agents, skills, providers, workflow steps, and limits through understandable interfaces.
7. Pause, resume, or cancel owned execution; observe independent sessions without claiming control.
8. Return tomorrow and recover the same context without reconstructing history.
9. Create or update agents, skills, and MCP connectors through a market-like UI, even as a non-IT user.
10. See performance and quality rules as first-class constraints, not hidden checklists.
11. Trigger a **Hermes Self-Improvement Review** that audits a plan, code change, decision, or skill against the platform's own rules and proposes a bounded improvement with evidence.
12. Use **Obsidian** as a native interface to the knowledge vault, with bidirectional links, file-based records, and conflict-aware sync.
13. Create workflows without first creating a project; later bind reusable workflows to one or more projects.

---

## 5. Architecture

### 5.1 High-level layers

```
┌───────────────────────────────────────────────────────────────────┐
│  SHELLS:                                                         │
│    • React/Vite/React Flow web shell (JARVIS HUD-style)        │
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
│    Agent swarm / coordinator (for multi-agent tasks)             │
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
| `dynamic-factory` (our earlier scaffold) | Next.js 15 + FastAPI + basic ReactFlow | Planning-file host only; implementation architecture uses New-forge Vite/React |

### 5.3 New major components to add

| Component | Responsibility | First phase |
|---|---|---|
| **The Bridge** | Shared backend gateway that normalizes input, authenticates, identifies workspace, applies policy, resolves permitted context, creates request records, and coordinates routing/execution | P1 |
| **Speech Service** | Local Whisper STT + Kokoro TTS; exposes speech-to-text and text-to-speech to both front doors | P3 (Should) |
| **JEV Routing Agent** | Required request-management component with deterministic rules first, context inspection, bounded model fallback; explains routing decision; editable versioned rules | P1 |
| **Request Router (JEV)** | The gateway layer that applies the routing agent's classification; manages conversation identity and correlation IDs | P1 |
| **Forge Method Engine** | Store and enforce the 11-phase SDLC template, small-item schema, dependency validation, evidence/acceptance separation | P2 |
| **Workflow Studio** | Separate workspace for creating, editing, versioning, copying, sharing, and publishing reusable workflow definitions before any project exists | P1 |
| **Project Hub** | Create/import project, bind one or more workflow versions, preview effective configuration, preflight, run history | P1 |
| **Agent Studio** | Create reusable agent profiles with role, instructions, skill references, provider/model route, limits, permissions | P4 |
| **Agent Swarm / Coordinator** | Multi-agent orchestration: a coordinator delegates sub-tasks to worker agents and aggregates results | P5 (Should) |
| **Skill & Instruction Channel** | Store versioned skill references, enforce source/hash compatibility, separate trusted instructions from retrieved knowledge | P4 |
| **LLM Council Adapter** | Governance reviews + multi-model workflow node: stage-1 responses, anonymized stage-2 peer review, chairman synthesis | P5 |
| **Hermes Self-Improvement Review** | Built-in review agent/skill that audits the OS's own plans, code, decisions, and skills and proposes bounded improvements with evidence | P4 |
| **MCP/Connector Market** | Registry of MCP servers/connectors; non-IT users enable them with scoped permissions; first examples: Gmail, Calendar, Drive, YouTube, GitHub | P1 (registry UI) / P4 (real adapters) |
| **Knowledge Vault** | Markdown-based human-readable knowledge with revisions, source, provenance, search, embeddings; content types: daily notes, reports/research, conversations, request logs | P1 |
| **Provider Registry** | Pluggable adapters for OpenAI, Anthropic, Google, xAI, Mistral, OpenCode, Ollama, NVIDIA, Zhipu, and any available provider; tracks budgets and routes per agent | P1 (minimal) / P5 (full) |
| **Allowance Governor** | Cross-request/provider budget tracking, holds, bounded failover, stop on exhaustion; enforce 70% automation / 30% interactive reserve | P2/P3 |
| **Durable Runner** | Persist execution state, support pause/resume/cancel, idempotent side effects, recovery from checkpoint | P3 |
| **Event + Evidence Archive** | Versioned event envelope, sanitized I/O, artifact links, first-failure preservation | P3 |
| **Performance Rules Engine** | 31 criteria as enforceable rules; audit, report, and gate changes | P0 (inventory) / P8 (full engine) |
| **Human Approval Checkpoint** | Explicit pause before tool/model execution when side effects, cost, or policy exceed configured thresholds | P3 |
| **Native Execution Engines** | Adapters for local CLI agents such as Claude Code CLI, Codex CLI, OpenCode CLI, and Ollama/local endpoints; run as background processes with streamed output and artifact capture | P3 |

---

## 6. Data model / identity hierarchy

### 6.1 Simple workflow track (default)

```
Workspace
 └─ Request
     └─ Project
         ├─ Workflow bindings (one or more)
         ├─ Run
         │   └─ Step → Attempt
         ├─ Files and evidence
         ├─ Settings / effective configuration
         └─ Runs history
```

### 6.2 Forge SDLC track (optional per project)

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

### 6.3 Reusable definition hierarchy

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

### 6.4 Project → workflow binding

| Entity | Purpose |
|---|---|
| `projects` | Name, description, type, owner, workspace, source repository/branch, settings |
| `workflow_definitions` | Reusable templates (name, objective) |
| `workflow_versions` | Immutable published versions of a definition |
| `project_workflow_bindings` | Which workflow versions are linked to a project, with environment, input defaults, version policy, and activation state |
| `project_runs` | Run of a workflow version within a project, pinned to exact versions and effective configuration |
| `run_tasks` | Mapping of canonical tasks to workflow steps (Forge track only) |

Rules:

- A project may use several workflows.
- One workflow can serve several projects with distinct inputs and permissions.
- A run pins exact workflow/child/agent/skill version and source/configuration revision.
- Later edits to a workflow definition do not rewrite active or historical runs.
- The simple track is the default. The Forge track is opt-in per project and not required for business workflows.

---

## 7. The three-path router (JEV)

Every request enters through **The Bridge** carrying workspace, source interface, language, received time, and correlation ID. **JEV** is the required request-management/routing component. JEV is not optional; its versioned system profile and routing configuration can exist as a built-in system profile before Agent Studio's general-purpose editing UI is available.

### 7.1 JEV Routing Agent

The routing component is a required system capability with:

1. **Deterministic rules first:** keyword, schema, and context rules that map unambiguous lookups to Tier 1 and simple question patterns to Tier 2.
2. **Context inspection:** current project, active task, conversation history, available skills, known blockers.
3. **Bounded model fallback:** when rules are insufficient, a small model call is used with a strict prompt, short timeout, and recorded cost.
4. **Explanation:** returns the selected path in ordinary language and a confidence indicator.
5. **Escalation:** materially ambiguous requests are surfaced to the user as a clarification, not guessed.

Routing rules are editable and versioned. A model classifier is used only for genuine ambiguity.

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

LLM Council contributes two distinct capabilities. Council is required for the complete product; a bounded council workflow with perspective mode and multi-model capability must ship.

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

### 9.3 Execution mode: "Ask a panel"

The UI exposes three execution modes:

1. **One helper** — default bounded work.
2. **A small team** — coordinator delegates independent outcomes under shared budget.
3. **Ask a panel** — controlled council subworkflow comparing opinions.

Team admission validates dependency DAG, per-worker scope, maximum concurrency/depth/iterations, tool allowlists, output contracts and integration ownership. Council voting is not a substitute for a delivery team.

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

### 10.3 Concrete isolation and write-approval mechanisms

- **Read-only API role by default:** The NousResearch Hermes adapter uses a read-only repository API token scoped to `contents:read`, `actions:read`, `checks:read`, `issues:read`, `pull_requests:read`. It has no `contents:write`, `workflows:write`, or `packages:write` scope.
- **Finite budgets and timeouts:** Every Hermes operation declares `max_tokens`, `max_cost_usd`, `max_duration_seconds`, and `max_tool_calls`. The Allowance Governor rejects the operation if any cap is exceeded. Operations that would run longer than 5 minutes must be chunked and user-approved per chunk.
- **Background review and Curator initially disabled:** Scheduled or event-triggered Hermes self-review is off by default. It can be enabled only after (a) user explicitly opts in, (b) a finite budget is configured, (c) a dual-approval gate is set, and (d) a dry-run produces acceptable output. The "Curator" persona is a **skill-maintenance reviewer**, not an auto-approver; it can flag outdated skill references but cannot approve its own proposed changes. Every Hermes write still requires a separate authenticated approval for the exact proposed change.
- **Canonical-file protection:** Files listed in `hermes-canonical-files.json` (e.g., approved baselines, owner-decision records, security policies) can be read but require a *separate* write-approval receipt to modify. Hermes cannot overwrite them via a general code-change approval.
- **Write-approval receipts, not configuration switches:** A setting such as `allow_hermes_writes=true` is *not* an approval. Every write requires an immutable receipt recording the exact diff, file list, test plan, rationale, authorizer identity, and timestamp. The receipt is appended to `plans/hermes-write-approvals.log`. The receipt must match a reviewed proposal; a commit authored by a human does not by itself satisfy the Hermes write-approval requirement unless that commit was the explicitly approved proposal.
- **Proposal staging:** All proposed code changes land in a temporary branch or staged patch view before any real branch/PR is created. The user can reject, edit, or request a smaller scope.
- **No recursive self-review:** Hermes cannot approve changes to its own safeguards, adapter config, or review policy. Those changes require an external owner decision recorded in `docs/decisions/`.
- **Same CI as humans:** Any change Hermes proposes is validated by the identical CI pipeline (test, lint, security, quality, conventional commits). A failing proposal is never auto-merged.
- **Tool/skill adoption restriction:** Installing a new skill, tool, MCP server or connector still requires an explicit installation approval that names the exact artifact, version/hash and allowed scope. Memory or skill approval does not imply runtime installation approval.
- **Status refresh and Improvements UI consume zero model calls.**
- **Unavailable Hermes displays "Not connected"**; a fixture never counts as live Hermes.

### 10.4 Hermes skill interface

- `/os review plan <id>` — review a plan or workflow version.
- `/os review code <task-id>` — review the code linked to a canonical task.
- `/os review decision <id>` — review a decision record.
- `/os review skill <skill-id>` — review a skill reference.
- `/os review self` — run a health/quality audit on Mahmoud OS itself (triggers the 31-criteria scan plus architecture checks).

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

### 11.2 Copy/paste scope definition

**Schema-preserving copy/paste** preserves:

- Selected workflow definition, nodes, groups, ports, edges, and I/O contracts.
- Required capabilities, connector types, and permission scopes.
- Child workflow references (as pinned version requirements).
- Provenance and license metadata.

It explicitly excludes:

- Secrets, credentials, native provider session/resume tokens, and local secret values.
- Approval records, acceptance decisions, and audit events.
- Execution state, runtime logs, and historical runs.
- Environment-specific configuration and connection bindings.

Paste creates new execution-definition IDs, remaps internal edges, and surfaces dependencies outside the selection as unresolved boundary ports.

### 11.3 Project lifecycle and import modes

1. **New project** is visible on Projects and in its empty state.
2. Enter name/purpose/type/owner and optional repository/documents; connect only authorized sources.
3. **Project import modes:**
   - **Blank project** (Must, P1)
   - **Link existing GitHub repository** read-only for metadata and issues (Must, P1)
   - **Upload documents/zip** for knowledge seeding (Should, P2)
   - **Fork from existing New-forge/Mahmoud OS project** (Should, P3)
   - **Import from forge-ai legacy project** (Future, after security review)
4. Business projects need not supply GitHub.
5. **Link** a published workflow or several workflows.
6. Review role/purpose, version policy, environment/runner, inputs, connection placeholders and inherited/task overrides.
7. **Preflight** shows missing capability, permission, credentials, output compatibility and budgets without starting work or installing dependencies.
8. **Start run** is a separate explicit action. Admission records project, request/task references, exact published versions, source revision, effective configuration and policy.
9. **Open** that run's real graph in the project. Expand child runs and inspect each step.
10. **Share/fork/export** a version or selected graph with safe remapping.

### 11.4 Composition rules

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

The 31 performance criteria are not a one-time checklist. They become a **Performance Rules Engine** inside Mahmoud OS.

### 13.1 Criteria as rules

Each criterion is stored as a rule with:

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
- **Primary screens**: Login, Home/Today, Workflow Studio, Project Hub, Execution Monitor, Explore, Improvements, Settings.
- **Information icons (v2-info pattern):** every panel/field that needs explanation gets a contextual info icon revealing help without leaving the screen.
- **Categorized search:** global search grouped by screens, projects, tasks, agents, skills, connectors, knowledge notes.
- **Responsive:** desktop, laptop/tablet, narrow; on small screens prioritize current work + focused inspector.

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
- **Quota policy:** Preserve the owner-configured 70% automation / 30% interactive reserve for shared Claude/Codex allowance, as recorded in New-forge `AGENTS.md` line 36 and applied via `C-007/C-007a`. Chat analysis/probes/retries/fallback share the pool; no silent paid spillover. Unknown platform counters deny dispatch.

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

| ID | Capability | New-forge contract | Disposition | Owner |
|---|---|---|---|---|
| F01 | The Bridge gateway module | A00-PLATFORM.md#boundaries-and-responsibilities | First release | A00-PLATFORM.md |
| F02 | Project Hub: create/import project | P21-SOFTWARE-DELIVERY-AND-SDLC.md (pending); P04-RUNTIME.md | First release | P21-SOFTWARE-DELIVERY-AND-SDLC.md (pending) |
| F03 | Obsidian plugin (basic interface) | P11-KNOWLEDGE.md | First release | P11-KNOWLEDGE.md |
| F04 | Discovery questions in idea assistant | P18-DISCOVERY-AND-SCOPE.md#browser-and-api-flow | First release | P18-DISCOVERY-AND-SCOPE.md |
| F05 | JEV Routing Agent | P18-DISCOVERY-AND-SCOPE.md; P20-RUN-CHANNELS-AND-CHANGE-REQUESTS.md | First release | P18-DISCOVERY-AND-SCOPE.md |
| F06 | Forge Method Engine (11 phases as reusable template) | P21-SOFTWARE-DELIVERY-AND-SDLC.md (pending); P04-RUNTIME.md | First release | P21-SOFTWARE-DELIVERY-AND-SDLC.md (pending) |
| F07 | Event + Evidence Archive | P10-ARTIFACTS.md#contracts-and-lifecycle | First release | P10-ARTIFACTS.md |
| F08 | Workflow Studio | P02-REGISTRY.md#contracts-and-publication; P03-EDITOR.md#building-and-configuring-workflows | First release | P02-REGISTRY.md |
| F09 | Web shell: Login/Today/Workflow Studio/Project Hub/Monitor | A00-PLATFORM.md; P03-EDITOR.md; P05-RUN-INSPECTION.md | First release | A00-PLATFORM.md |
| F10 | Agent Studio (profiles + snapshots at admission) | P06-AGENTS.md | Complete product | P06-AGENTS.md |
| F11 | Agent Swarm / Coordinator | P06-AGENTS.md; P24-SUPPORT-AND-ORGANIZATION.md | Complete product | P06-AGENTS.md |
| F12 | Skill and Instruction Channel | P07-SKILLS.md | Complete product | P07-SKILLS.md |
| F13 | Minimal MCP/connector registry UI | P08-CONNECTIONS.md#contracts-and-flows; P09-TOOLS.md | First release + complete product | P08-CONNECTIONS.md |
| F14 | Knowledge Vault with Obsidian sync | P11-KNOWLEDGE.md | First release | P11-KNOWLEDGE.md |
| F15 | Minimal provider registry | P12-MODELS.md#contracts-and-routing; P12A-PROVIDERS-AND-FAILOVER.md | First release | P12-MODELS.md |
| F16 | LLM Council Adapter (governance review + workflow node) | P13-EVALUATIONS.md; P19-RELIABILITY-AND-EVOLUTION.md | Complete product | P13-EVALUATIONS.md |
| F17 | Model removal/rebinding and provider constraints | P12A-PROVIDERS-AND-FAILOVER.md; P12B-SUBSCRIPTION-QUOTA-AND-ROUTE-SEQUENCE.md | Complete product | P12A-PROVIDERS-AND-FAILOVER.md |
| F18 | Provider pause and context constraint enforcement | P12A-PROVIDERS-AND-FAILOVER.md | Complete product | P12A-PROVIDERS-AND-FAILOVER.md |
| F19 | LLM cache, telemetry and cost tracking | P12-MODELS.md; P20-RUN-CHANNELS-AND-CHANGE-REQUESTS.md | Complete product | P12-MODELS.md |
| F20 | Credits/payment packs | P22-COMMERCE-CREDITS-AND-QUOTES.md | Required full-product outcome; deferred until owner contract approved | P22-COMMERCE-CREDITS-AND-QUOTES.md |
| F21 | Human Approval Checkpoint | P13-EVALUATIONS.md; P19-RELIABILITY-AND-EVOLUTION.md; P09-TOOLS.md | First release | P13-EVALUATIONS.md |
| F22 | Idempotency/reconciliation tests for external side effects | P09-TOOLS.md; P13-EVALUATIONS.md | First release | P09-TOOLS.md |
| F23 | Preflight validation without dispatch | P03-EDITOR.md; P13-EVALUATIONS.md | First release + complete product | P03-EDITOR.md |
| F24 | Basic nested workflows, conditions, branches and joins | P03-EDITOR.md; P04-RUNTIME.md | First release | P03-EDITOR.md |
| F25 | Small work items with identity, dependencies, I/O, checks | P04-RUNTIME.md; P20-RUN-CHANNELS-AND-CHANGE-REQUESTS.md | First release | P04-RUNTIME.md |
| F26 | Pause / resume / cancel with settlement semantics | P04-RUNTIME.md; P19-RELIABILITY-AND-EVOLUTION.md | First release | P04-RUNTIME.md |
| F27 | Live recovery after worker/control-plane restart | P25-INTEGRATIONS-AND-REMOTE-RUNTIMES.md; P04-RUNTIME.md | First release | P25-INTEGRATIONS-AND-REMOTE-RUNTIMES.md |
| F28 | Live monitor: actual run graph, not fixture | P05-RUN-INSPECTION.md; P20-RUN-CHANNELS-AND-CHANGE-REQUESTS.md | First release | P05-RUN-INSPECTION.md |
| F29 | Replay snapshots from event archive | P05-RUN-INSPECTION.md; P10-ARTIFACTS.md | Complete product | P05-RUN-INSPECTION.md |
| F30 | Durable schedules and notifications | P20-RUN-CHANNELS-AND-CHANGE-REQUESTS.md; P14-NOTIFICATIONS.md | Complete product | P20-RUN-CHANNELS-AND-CHANGE-REQUESTS.md |
| F31 | Conversation/request identity and correlation | P20-RUN-CHANNELS-AND-CHANGE-REQUESTS.md#durable-conversation-model-and-consistency | First release | P20-RUN-CHANNELS-AND-CHANGE-REQUESTS.md |
| F32 | Artifact/review comments on evidence | P10-ARTIFACTS.md; P13-EVALUATIONS.md; P20-RUN-CHANNELS-AND-CHANGE-REQUESTS.md | Complete product | P10-ARTIFACTS.md |
| F33 | GitHub issues/repository sync connector | P25-INTEGRATIONS-AND-REMOTE-RUNTIMES.md; P21-SOFTWARE-DELIVERY-AND-SDLC.md | Complete product | P25-INTEGRATIONS-AND-REMOTE-RUNTIMES.md |
| F34 | Repository upload/ingestion for project import | P25-INTEGRATIONS-AND-REMOTE-RUNTIMES.md; P10-ARTIFACTS.md | Complete product | P25-INTEGRATIONS-AND-REMOTE-RUNTIMES.md |
| F35 | Native Execution Engines (CLI adapters) | P09-TOOLS.md; P16-OPERATIONS.md | First release | P09-TOOLS.md |
| F36 | Native mobile delivery | P21-SOFTWARE-DELIVERY-AND-SDLC.md; P25-INTEGRATIONS-AND-REMOTE-RUNTIMES.md | Required full-product outcome; deferred until owner contract approved | P21-SOFTWARE-DELIVERY-AND-SDLC.md |
| F37 | Design and wireframes | P21-SOFTWARE-DELIVERY-AND-SDLC.md; P25-INTEGRATIONS-AND-REMOTE-RUNTIMES.md | Required full-product outcome; deferred until owner contract approved | P21-SOFTWARE-DELIVERY-AND-SDLC.md |
| F38 | Code graph/import closure | P25-INTEGRATIONS-AND-REMOTE-RUNTIMES.md; P21-SOFTWARE-DELIVERY-AND-SDLC.md | Complete product | P25-INTEGRATIONS-AND-REMOTE-RUNTIMES.md |
| F39 | Architecture/document production workflows | P21-SOFTWARE-DELIVERY-AND-SDLC.md; P10-ARTIFACTS.md; P11-KNOWLEDGE.md | Complete product | P21-SOFTWARE-DELIVERY-AND-SDLC.md |
| F40 | Hermes Self-Improvement Review | P23-GUARDIAN-RESEARCH-AND-LEARNING.md | Complete product | P23-GUARDIAN-RESEARCH-AND-LEARNING.md |
| F41 | Idea-driven recommendations (creator journey) | P18-DISCOVERY-AND-SCOPE.md#data-contracts; P23-GUARDIAN-RESEARCH-AND-LEARNING.md | First release | P18-DISCOVERY-AND-SCOPE.md |
| F42 | Market research/competitive analysis workflows | P23-GUARDIAN-RESEARCH-AND-LEARNING.md; P11-KNOWLEDGE.md | Complete product | P23-GUARDIAN-RESEARCH-AND-LEARNING.md |
| F43 | Pattern library/derived principles | P11-KNOWLEDGE.md; P07-SKILLS.md; P23-GUARDIAN-RESEARCH-AND-LEARNING.md | Complete product | P11-KNOWLEDGE.md |
| F44 | Support desk/SLA routing | P24-SUPPORT-AND-ORGANIZATION.md | Required full-product outcome; deferred until owner contract approved | P24-SUPPORT-AND-ORGANIZATION.md |
| F45 | Operations and delivery packaging | P15-ADMINISTRATION.md; P16-OPERATIONS.md | Complete product | P15-ADMINISTRATION.md |
| F46 | Templates/gallery/project reuse | P17-PARITY.md; P02-REGISTRY.md; P03-EDITOR.md | Complete product | P17-PARITY.md |
| F47 | Allowance Governor | P12B-SUBSCRIPTION-QUOTA-AND-ROUTE-SEQUENCE.md; P04-RUNTIME.md | First release | P12B-SUBSCRIPTION-QUOTA-AND-ROUTE-SEQUENCE.md |
| F48 | Data-source authorization/provenance | P18-DISCOVERY-AND-SCOPE.md; P08-CONNECTIONS.md; P11-KNOWLEDGE.md | Complete product | P18-DISCOVERY-AND-SCOPE.md |
| F49 | Independent acceptance and security closure | P01-IDENTITY.md; P09-TOOLS.md; P13-EVALUATIONS.md; P21-SOFTWARE-DELIVERY-AND-SDLC.md | Complete product | P01-IDENTITY.md |
| F50 | Race/adaptive execution and confidence bounds | P21-SOFTWARE-DELIVERY-AND-SDLC.md; P19-RELIABILITY-AND-EVOLUTION.md; P12A-PROVIDERS-AND-FAILOVER.md | Complete product | P21-SOFTWARE-DELIVERY-AND-SDLC.md |

---

## 18. Phased implementation roadmap

Each phase has a named branch, a verifiable acceptance gate, and a plan document derived from this blueprint. The philosophy: no phase is declared complete without evidence.

### P0 — Foundation and audit

- Establish New-forge as the governed implementation baseline and `forge-ai` as the pinned behavioral/parity reference.
- Create the parity/requirements ledger: F01–F50 + P01–P25 + MUST/SHOULD/FUTURE + active criterion/approval IDs + every OS addition.
- Reconcile document scope and architecture; remove contradictory observer-as-product foundations.
- Resolve security and authority prerequisites on the exact intended branch.
- Define performance budget and acceptance targets.
- Produce the all-31 performance audit inventory (status, applicability, priority, evidence) before any performance edit.
- **Acceptance:** Blueprint approved; parity ledger published; baseline branch pinned; CI state and blockers honestly reported; non-waivable security controls enforced.

### P1 — First working shell: Bridge, JEV, project hub, Workflow Studio, vault, minimal registry

- Implement **The Bridge** gateway module: request normalization, authentication, workspace resolution, policy enforcement, context resolution, request record creation.
- Implement **JEV Routing Agent** as a required system capability with deterministic rules, context inspection, bounded model fallback, and explained routing decisions.
- Implement project creation/import (blank + GitHub link) and project-workflow binding.
- Implement Workflow Studio: draft → publish → immutable version, plus schema-preserving copy/paste of whole graph or selected fragments.
- Add idea-driven recommendations with catalog-backed component choices.
- Add chat composer + daily home dashboard + Explore + categorized search + info icons.
- Add **Obsidian plugin package** with basic interface: pair, ask JEV, send note/selection, save responses, show linked task/run status, disconnect/revoke.
- Add **Obsidian vault sync**: read/write Markdown notes, bidirectional links, conflict detection, file-watcher loop prevention.
- Add minimal provider registry and connector registry UI (status, permissions, "Not connected"/"Demo" labels).
- Tests: unit, integration, Playwright smoke for project → workflow → binding journey; Obsidian plugin loading test; vault sync test.
- **Acceptance:** A user creates a workflow, publishes a version, creates a project, binds the workflow; a typed request is routed with an explained decision; a Markdown note created in Obsidian appears in the web UI and vice versa; disconnected connectors shown truthfully.

### P2 — Forge method engine, visual execution, preflight

- Add 11-phase model as optional SDLC track, small-item schema, dependency validation.
- Graph/list/timeline views for execution plans.
- Small-item inspector with inputs, outputs, checks, agent assignment, limits.
- Preflight validation without dispatch.
- Live monitor updates the actual user graph, shows waits/actions/I/O and survives reconnect without duplicate effects.
- Tests: cycle detection, active-snapshot pinning, phase transition rules, reconnect/replay.
- **Acceptance:** A published workflow runs through admitted graph; active runs stay pinned; cycles are refused; every phase is inspectable before any run; monitor opens the matching project's selected run; preflight blocks missing credentials truthfully.

### P3 — Durable execution, native engines, human approval, safe external actions

- Replace in-memory executor with durable run/invocation/attempt records (reuse New-forge Temporal/runtime primitives).
- Add pause/resume/cancel with settlement semantics.
- Add native execution engines (Claude Code CLI, Codex CLI, OpenCode CLI, Ollama/local).
- Add human approval checkpoint before tool/model execution.
- Add safe external-action handling: idempotent operation identities, reconciliation, bounded retries, first-failure preservation.
- Event envelope + SSE/live updates with reconnect/replay.
- Tests: interrupted calls, process restart, lost responses, partial writes, duplicate suppression, approval gate.
- **Acceptance:** One real small task can be interrupted and resumed; no duplicate external actions; reconnect preserves selection; approval gate blocks consequential actions until confirmed.

### P4 first-working-release acceptance rule (consolidated)

By the end of P4, a user can: ask a request → see it routed with an explained decision → get a quick answer or a planned workflow → inspect small work items → run/pause/resume → see evidence → create a workflow before a project exists → bind it to a project → start a run → see that run's actual graph in the monitor → read the same knowledge in Obsidian and the web UI.

All **R001–R037** from `plans/mahmoud-os-requirements-matrix-v2.1.2.csv` must be present with evidence. In particular, these runtime and control capabilities (R027–R037) are required for the execution journey:

- **R027 Durable execution records** (run/invocation/attempt) that are immutable, retrievable and survive worker restarts.
- **R028 Pause / resume / cancel** with a safe-boundary preview and settlement semantics.
- **R029 Human Approval Checkpoint** before externally consequential or destructive actions; denial stops the branch.
- **R030 Safe external-action handling** (idempotency keys, bounded retries, reconciliation of duplicate/out-of-order effects, first-failure preservation).
- **R031 Event + Evidence Archive** for every execution with first-failure preservation and sanitized export.
- **R032 Allowance Governor** enforcing per-window/provider/team automation cap and reserve, stopping automation at the cap.
- **R033 Native Execution Engines (CLI adapters)** for tools beyond APIs.
- **R034 Basic nested workflows, conditions, branches and joins** so the execution engine can compose non-trivial flows.

P4 is the first working release, not the first sketch.

### P4 — Agent studio, skill market, instruction channel, Hermes self-review

- Agent profiles with snapshots at admission.
- Skill reference registry with version/hash and format checks.
- Controlled instruction channel separate from knowledge.
- Add **Hermes Self-Improvement Review** skill and API.
- Tests: profile edits affect future admissions only; instruction authority is explicit; self-review produces a structured report and requires approval before applying changes.
- **Acceptance:** Create agent, assign skill, admit invocation; edit profile; verify old invocation keeps original snapshot; run a self-review on a plan and approve/reject its suggestions.

### P5 — Full provider registry, LLM Council, allowance governor, agent swarm

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
- Real connectors: Gmail, Calendar, Drive, GitHub (YouTube separately scoped).
- Tests: disconnected shown as "Not connected"; demo adapters marked; real connection verified before "Connected".
- **Acceptance:** Enable filesystem MCP demo; run a flow that reads a file; verify scope enforcement; connect a real Gmail/Drive/Calendar demo adapter.

### P7 — Knowledge vault polish and secondary workspaces

- Markdown vault with revisions, sync, search, embeddings (optional semantic search).
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
- (Should) Voice input/output.
- **Acceptance:** Create, review, and monitor a workflow entirely through the Hermes skill; self-review can be triggered from chat.

### P10 — Security closure and independent acceptance

- Confirmed-security closure, performance changes only after the full audit, recovery and independent acceptance.
- **Acceptance:** Confirmed security findings must be resolved with verified evidence. They cannot be waived or owner-accepted; they remain open until fixed. Independent reviewer approval records that no unverified or unapproved workaround exists.

### P11 — Complete MUST traceability

- Complete MUST traceability with actual evidence, explicit SHOULD deferrals and separate FUTURE backlog.
- **Acceptance:** Every MUST item has code locations, criterion IDs, and test evidence. R001–R037 (first working release) and R001–R066 (complete product) are present with evidence. This includes R048–R051 (commerce, native mobile, design/wireframes, support desk) as required full-product outcomes. Every F01–F50 area is therefore in scope for the complete product; nothing is silently downgraded.

---


### F01–F50 outcome preservation in complete product

The 50 audited areas from the New-forge source audit are preserved in the complete Mahmoud OS product. Every canonical F-ID appears in exactly one row. The release column assigns each area to the first working release (P1–P4), the complete product (P5–P11), or an explicitly deferred Future outcome. The authoritative source is `plans/mahmoud-os-requirements-matrix-v2.1.2.csv`.

| F-ID | Outcome | Owner contract/section | Approved baseline | Release | Requirement IDs | Acceptance |
|---|---|---|---|---|---|---|
| F01 | The Bridge gateway module | A00-PLATFORM.md#boundaries-and-responsibilities | 710e1c1 | P1-P4 | R001, R025 | Request record created with ID, workspace, source, language, correlation ID |
| F02 | Project Hub: create/import project | P21-SOFTWARE-DELIVERY-AND-SDLC.md (pending); P04-RUNTIME.md | 710e1c1 / P21-pending | P1-P4 | R005, R006 | Blank project created; GitHub repo linked read-only; empty state visible |
| F03 | Obsidian plugin (basic interface) | P11-KNOWLEDGE.md | 710e1c1 | P1-P4 | R013, R036, S014 | Plugin loads in test vault; saved lookup uses zero model calls; planned task visible on web |
| F04 | Discovery questions in idea assistant | P18-DISCOVERY-AND-SCOPE.md#browser-and-api-flow | 710e1c1 | P1-P4 | R038 | Idea input surfaces editable scope questions before plan is accepted |
| F05 | JEV Routing Agent | P18-DISCOVERY-AND-SCOPE.md; P20-RUN-CHANNELS-AND-CHANGE-REQUESTS.md | 710e1c1 / f2a188a | P1-P4 | R002, R003 | Deterministic rules pass lookup without model; quick answer bounded; planned work creates run; explanation shown |
| F06 | Forge Method Engine (11 phases as reusable template) | P21-SOFTWARE-DELIVERY-AND-SDLC.md (pending); P04-RUNTIME.md | 710e1c1 / P21-pending | P1-P4 | R022 | 11 phases defined; inspectable before run; cycles refused |
| F07 | Event + Evidence Archive | P10-ARTIFACTS.md#contracts-and-lifecycle | 710e1c1 | P1-P4 | R031 | Every execution produces events with first-failure preservation |
| F08 | Workflow Studio | P02-REGISTRY.md#contracts-and-publication; P03-EDITOR.md#building-and-configuring-workflows | 710e1c1 | P1-P4 | R007, R009, R010, R011 | Draft created, edited, published as immutable version |
| F09 | Web shell: Login/Today/Workflow Studio/Project Hub/Monitor | A00-PLATFORM.md; P03-EDITOR.md; P05-RUN-INSPECTION.md | 710e1c1 | P1-P4 | R014, R015, R016, R017, R018, R027, S001, S002, S005, S011, S015, S018, FTR001, FTR003, FTR004, FTR006, FTR007, FTR009, FTR010, FTR011, FTR012, FTR015 | Screens render bilingual, RTL, accessible; no fixture-by-default in monitor |
| F10 | Agent Studio (profiles + snapshots at admission) | P06-AGENTS.md | 710e1c1 | P5-P11 | R039 | Profile edits affect future admissions only |
| F11 | Agent Swarm / Coordinator | P06-AGENTS.md; P24-SUPPORT-AND-ORGANIZATION.md | 710e1c1 | P5-P11 | R044 | Team delegates and aggregates within declared bounds |
| F12 | Skill and Instruction Channel | P07-SKILLS.md | 710e1c1 | P5-P11 | R041 | Skill reference versioned/hash-checked |
| F13 | Minimal MCP/connector registry UI | P08-CONNECTIONS.md#contracts-and-flows; P09-TOOLS.md | 710e1c1 | P1-P4 | R020, R042, S013, S017, FTR005 | Demo connector listed; disconnected shown truthfully |
| F14 | Knowledge Vault with Obsidian sync | P11-KNOWLEDGE.md | 710e1c1 | P1-P4 | R012, S004, FTR002, FTR008, FTR016 | Note created in Obsidian appears in web and vice versa; conflict detection works |
| F15 | Minimal provider registry | P12-MODELS.md#contracts-and-routing; P12A-PROVIDERS-AND-FAILOVER.md | 710e1c1 | P1-P4 | R019 | Providers configurable; usage recorded |
| F16 | LLM Council Adapter (governance review + workflow node) | P13-EVALUATIONS.md; P19-RELIABILITY-AND-EVOLUTION.md | 710e1c1 / f2a188a | P5-P11 | R043, S012, S016 | Council runs end-to-end; produces evidence not acceptance |
| F17 | Model removal/rebinding and provider constraints | P12A-PROVIDERS-AND-FAILOVER.md; P12B-SUBSCRIPTION-QUOTA-AND-ROUTE-SEQUENCE.md | 710e1c1 | P5-P11 | R048 | Provider can be paused/rebound; context constraints enforced |
| F18 | Provider pause and context constraint enforcement | P12A-PROVIDERS-AND-FAILOVER.md | 710e1c1 | P5-P11 | R049 | Paused provider rejects new calls; context window exceeded returns graceful error |
| F19 | LLM cache, telemetry and cost tracking | P12-MODELS.md; P20-RUN-CHANNELS-AND-CHANGE-REQUESTS.md | 710e1c1 / f2a188a | P5-P11 | R050, S008 | Per-call usage recorded; cache hits reported; cost estimate shown before run |
| F20 | Credits/payment packs | P22-COMMERCE-CREDITS-AND-QUOTES.md | P22-pending | P5-P11 | R063 | Deferred until after first delivery and real usage measured |
| F21 | Human Approval Checkpoint | P13-EVALUATIONS.md; P19-RELIABILITY-AND-EVOLUTION.md; P09-TOOLS.md | 710e1c1 / f2a188a | P1-P4 | R029, R030 | Consequential action blocks until approved; denial stops branch |
| F22 | Idempotency/reconciliation tests for external side effects | P09-TOOLS.md; P13-EVALUATIONS.md | 710e1c1 | P1-P4 | R035, S007 | Duplicate invocation returns prior receipt; reconciliation tests pass |
| F23 | Preflight validation without dispatch | P03-EDITOR.md; P13-EVALUATIONS.md | 710e1c1 | P1-P4 | R021, R026, R046, S009 | Preflight report lists blockers; run cannot start |
| F24 | Basic nested workflows, conditions, branches and joins | P03-EDITOR.md; P04-RUNTIME.md | 710e1c1 | P1-P4 | R034, S006, FTR013 | Subworkflow calls execute; if/else branches and join nodes evaluate; errors surface to caller |
| F25 | Small work items with identity, dependencies, I/O, checks | P04-RUNTIME.md; P20-RUN-CHANNELS-AND-CHANGE-REQUESTS.md | 710e1c1 / f2a188a | P1-P4 | R023 | Items have identity, dependencies, I/O, checks |
| F26 | Pause / resume / cancel with settlement semantics | P04-RUNTIME.md; P19-RELIABILITY-AND-EVOLUTION.md | 710e1c1 / f2a188a | P1-P4 | R028 | Pause/resume/cancel settle state correctly |
| F27 | Live recovery after worker/control-plane restart | P25-INTEGRATIONS-AND-REMOTE-RUNTIMES.md; P04-RUNTIME.md | 710e1c1 | P1-P4 | R037 | Incomplete run resumes from last checkpoint; orphan attempt detected and surfaced |
| F28 | Live monitor: actual run graph, not fixture | P05-RUN-INSPECTION.md; P20-RUN-CHANNELS-AND-CHANGE-REQUESTS.md | 710e1c1 / f2a188a | P1-P4 | R024, S003 | Monitor opens actual run; no default fixture |
| F29 | Replay snapshots from event archive | P05-RUN-INSPECTION.md; P10-ARTIFACTS.md | 710e1c1 | P5-P11 | R051 | Historical run can be replayed visually; deterministic outputs reproducible |
| F30 | Durable schedules and notifications | P20-RUN-CHANNELS-AND-CHANGE-REQUESTS.md; P14-NOTIFICATIONS.md | f2a188a / 710e1c1 | P5-P11 | R045 | Schedule triggers without duplicate execution |
| F31 | Conversation/request identity and correlation | P20-RUN-CHANNELS-AND-CHANGE-REQUESTS.md#durable-conversation-model-and-consistency | f2a188a | P1-P4 | R004 | Same request visible in web and Obsidian; no duplicate execution |
| F32 | Artifact/review comments on evidence | P10-ARTIFACTS.md; P13-EVALUATIONS.md; P20-RUN-CHANNELS-AND-CHANGE-REQUESTS.md | 710e1c1 | P5-P11 | R052 | Reviewer can add threaded comments linked to a specific event/artifact version |
| F33 | GitHub issues/repository sync connector | P25-INTEGRATIONS-AND-REMOTE-RUNTIMES.md; P21-SOFTWARE-DELIVERY-AND-SDLC.md | 710e1c1 / P21-pending | P5-P11 | R053 | GitHub repo issues sync bidirectionally; webhook updates reflected |
| F34 | Repository upload/ingestion for project import | P25-INTEGRATIONS-AND-REMOTE-RUNTIMES.md; P10-ARTIFACTS.md | 710e1c1 | P5-P11 | R054 | Upload/clone produces indexed project artifacts with provenance |
| F35 | Native Execution Engines (CLI adapters) | P09-TOOLS.md; P16-OPERATIONS.md | 710e1c1 | P1-P4 | R033 | CLI invoked as subprocess with streamed output and artifact capture |
| F36 | Native mobile delivery | P21-SOFTWARE-DELIVERY-AND-SDLC.md; P25-INTEGRATIONS-AND-REMOTE-RUNTIMES.md | P21-pending | P5-P11 | R064 | Deferred until after first delivery per owner V-H01 |
| F37 | Design and wireframes | P21-SOFTWARE-DELIVERY-AND-SDLC.md; P25-INTEGRATIONS-AND-REMOTE-RUNTIMES.md | P21-pending | P5-P11 | R065 | Design-to-code workflows; deferred post-first-delivery |
| F38 | Code graph/import closure | P25-INTEGRATIONS-AND-REMOTE-RUNTIMES.md; P21-SOFTWARE-DELIVERY-AND-SDLC.md | 710e1c1 / P21-pending | P5-P11 | R055 | Static analysis produces dependency graph; missing imports surfaced |
| F39 | Architecture/document production workflows | P21-SOFTWARE-DELIVERY-AND-SDLC.md; P10-ARTIFACTS.md; P11-KNOWLEDGE.md | 710e1c1 / P21-pending | P5-P11 | R056 | Workflow generates structured document from evidence; exports to Markdown/PDF |
| F40 | Hermes Self-Improvement Review | P23-GUARDIAN-RESEARCH-AND-LEARNING.md | 710e1c1 | P5-P11 | R040 | Review produces draft proposal; user approval before apply |
| F41 | Idea-driven recommendations (creator journey) | P18-DISCOVERY-AND-SCOPE.md#data-contracts; P23-GUARDIAN-RESEARCH-AND-LEARNING.md | 710e1c1 | P1-P4 | R008 | Typed idea produces editable plan with component cards showing fit/source/permissions/cost |
| F42 | Market research/competitive analysis workflows | P23-GUARDIAN-RESEARCH-AND-LEARNING.md; P11-KNOWLEDGE.md | 710e1c1 | P5-P11 | R057 | Research query produces cited comparison table; sources traceable |
| F43 | Pattern library/derived principles | P11-KNOWLEDGE.md; P07-SKILLS.md; P23-GUARDIAN-RESEARCH-AND-LEARNING.md | 710e1c1 | P5-P11 | R058 | Reusable patterns extracted from provenance; versioned and attributed |
| F44 | Support desk/SLA routing | P24-SUPPORT-AND-ORGANIZATION.md | P24-pending | P5-P11 | R066 | Support request traceable; SLA routing deferred |
| F45 | Operations and delivery packaging | P15-ADMINISTRATION.md; P16-OPERATIONS.md | 5b6bbda / 666e450 | P5-P11 | R047, S010 | Docker Compose stack starts; runbook verified |
| F46 | Templates/gallery/project reuse | P17-PARITY.md; P02-REGISTRY.md; P03-EDITOR.md | 710e1c1 | P5-P11 | R059, FTR014 | Published workflows discoverable in gallery; templates forkable with new IDs |
| F47 | Allowance Governor | P12B-SUBSCRIPTION-QUOTA-AND-ROUTE-SEQUENCE.md; P04-RUNTIME.md | f2a188a / P22-pending | P1-P4 | R032 | Exhausted allowance stops calls; probe policy preserves budgets |
| F48 | Data-source authorization/provenance | P18-DISCOVERY-AND-SCOPE.md; P08-CONNECTIONS.md; P11-KNOWLEDGE.md | 710e1c1 | P5-P11 | R060 | Every imported fact carries source, retrieval time, and authorization scope |
| F49 | Independent acceptance and security closure | P01-IDENTITY.md; P09-TOOLS.md; P13-EVALUATIONS.md; P21-SOFTWARE-DELIVERY-AND-SDLC.md | 710e1c1 / P21-pending | P10-P11 | R062 | Confirmed security findings must be resolved with verified evidence. They cannot be waived or owner-accepted. Evidence ledger complete. |
| F50 | Race/adaptive execution and confidence bounds | P21-SOFTWARE-DELIVERY-AND-SDLC.md; P19-RELIABILITY-AND-EVOLUTION.md; P12A-PROVIDERS-AND-FAILOVER.md | 710e1c1 / P21-pending | P5-P11 | R061 | Adaptive retries bounded by confidence threshold; fallback provider selected deterministically |

Inherited areas F20 (commerce), F36 (native mobile delivery), F37 (design/wireframes) and F44 (support desk/SLA routing) are **required full-product outcomes** mapped to R063–R066. They are deferred until their owner contracts (P21/P22/P24) are approved, but they remain inside the complete-product gate, not optional Future items.

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

1. Approve or edit this v2.1 blueprint and priority matrix.
2. Pin the canonical New-forge baseline (main or develop) and confirm branch strategy.
3. Author P0 plan in detail (audit checklist, parity ledger, performance budget, branch strategy).
4. Schedule P0 execution; no code changes until P0 acceptance is recorded.

---

## 21. Open decisions to confirm

1. **New-forge baseline branch:** `main` (8672c5a) or `develop` (e9b00d1, 72 ahead/1 behind)?
2. **Repository location:** continue in `dynamic-factory` as a planning shell, or create a new Mahmoud OS repo that consumes New-forge as a submodule/dependency?
3. **Obsidian sync mode:** direct filesystem watcher to a configured vault path, or plugin-based REST bridge?
4. **Hermes self-review default triggers:** manual only, scheduled, or also gated on policy events?
5. **Voice:** required (move to Must) or experimental (keep as Should)?
6. **Deployment target:** local-only first, private cloud, or SaaS-ready from P1?
7. **workflow-observer role:** reuse as a bounded monitoring adapter, or retire it?

---

*End of blueprint. No code changes made. Implementation begins only after explicit go-ahead on P0.*

---

## Appendix A — The 31 performance criteria

| ID | Criterion | Detection method | Priority |
|---|---|---|---|
| PERF-01 | Skeleton loading | UI review, runtime test | P1 |
| PERF-02 | WebP / AVIF image formats | Asset inventory, build audit | P2 |
| PERF-03 | Duplicate API calls | Request tracing, test | P1 |
| PERF-04 | Debounce | Event tracing, test | P1 |
| PERF-05 | Pagination | API review, test | P1 |
| PERF-06 | CDN for eligible static assets | Deployment audit | P2 |
| PERF-07 | Background job queue / durable execution | Architecture review | P1 |
| PERF-08 | N+1 queries | Query tracing, test | P2 |
| PERF-09 | Brotli / Gzip content encoding | Proxy/deployment audit | P2 |
| PERF-10 | Redis caching | Measured benefit review | P3 |
| PERF-11 | Unused dependencies | Manifest/lockfile audit | P2 |
| PERF-12 | API timeouts | Config review, test | P1 |
| PERF-13 | AI streaming | Runtime measurement | P2 |
| PERF-14 | Optimistic UI with rollback | UI test | P2 |
| PERF-15 | Lazy loading | Bundle/route audit | P2 |
| PERF-16 | Parallel requests | Concurrency test | P2 |
| PERF-17 | Database indexes | Query plan review | P2 |
| PERF-18 | OpenTelemetry instrumentation | Observability audit | P2 |
| PERF-19 | Server / DB proximity | Topology review | P2 |
| PERF-20 | SSR / static generation | Route audit | P3 |
| PERF-21 | Third-party scripts inventory | Dependency audit | P2 |
| PERF-22 | Code splitting | Bundle audit | P2 |
| PERF-23 | Virtualization for large lists/graphs | UI test | P3 |
| PERF-24 | Required columns only | Schema/response audit | P2 |
| PERF-25 | Connection pooling | Driver/config review | P2 |
| PERF-26 | Unnecessary re-renders | Profile, test | P2 |
| PERF-27 | Browser caching | Header audit, test | P2 |
| PERF-28 | Load balancing | Saturation measurement | P3 |
| PERF-29 | Font optimization | Asset audit, RTL check | P2 |
| PERF-30 | Real user monitoring | Telemetry review | P3 |
| PERF-31 | Performance testing | Benchmark audit | P3 |

Each criterion uses the status values: `applied`, `not-applied`, `needs-improvement`, or `unassessed`. A completed 31-row audit cannot contain unknown evidence disguised as Applied.


## Appendix B — Reference policy annex and quota-accounting conditions

### B.1 Owner decision sources

| Decision | Source | Commit / issue |
|---|---|---|
| C-007 automation cap | `New-forge/docs/specs/DECISIONS.md` line 97 | Owner decision 2026-10-13 |
| C-007a estimated accounting | `New-forge/docs/specs/OWNER-DECISION-APPLICATION.md` §35-43 | Owner decision 2026-10-13 / issue #21 comment 6152072280 |
| C-021 quality waivers | `DECISIONS.md` line 98 | Owner decision 2026-10-13 |
| C-022 gate continuation | `DECISIONS.md` line 99 | Owner decision 2026-10-13 |
| Security findings non-waivable | `OWNER-DECISION-APPLICATION.md` §9 | Applied at 710e1c1 |
| 70/30 cap accounting | `OWNER-DECISION-APPLICATION.md` §17, §35-43 | Owner decision + C-007a |

### B.2 70/30 quota-accounting conditions

The 70% automation / 30% interactive quota is **not a single percentage**. It operates under these conditions, distinguishing **platform-owned reservation ledger** from **provider-reported observation**:

1. **Platform-owned reservations:** The platform maintains its own ledger of `automation_reserved` and `automation_used` counters per pool/window. These counters are incremented atomically at admission and reconciled when the actual outcome is known. They are platform-owned state; they do not depend on a provider's real-time observation.
2. **Provider observations:** When available, the platform reads the provider's reported remaining usage/capacity (`provider_observed_remaining`). This is an external observation, not the platform's ledger. It is used to validate or correct the platform estimate, never to replace the platform reservation state.
3. **Measured mode (preferred):** Automation stops when `platform_automation_reserved + platform_automation_used ≥ 70%` of the provider-observed window capacity, or when `provider_observed_remaining` is insufficient for the requested call. Interactive use is not consumed by automation.
4. **Estimated mode (C-007a):** When vendor measurement is unavailable, the owner configures a conservative envelope (e.g., N calls over M hours). Each agent/chat/retry/probe call debits its conservative upper bound against the platform ledger. Unknown/None capacity is never treated as zero or infinite.
5. **Reserve protection:** The 30% reserve is protected in both modes. Automation cannot consume the reserve. At cap, runs use compatible approved fallback or wait; they never switch to paid credit or another user's subscription silently.
6. **Atomic reservations:** Platform reservations persist across workers, aliases, and restart. Uncertain dispatches remain reserved until outcome is known.
7. **Reconciliation without erasure:** Provider-observed usage reconciles platform reservations; neither platform holds nor charged/in-flight usage is cleared by owner edits, mode changes, or window rollover.
8. **Observation freshness:** Stale or future provider observations, and missing platform automation counters, deny dispatch until fresh data is available.
9. **Interactive reduction:** Interactive use, aliases, and concurrent external use may reduce the actual automation headroom; the cap is a maximum share, not a guarantee that 70% is available.
10. **Conformance tests:** Dedicated live conformance/accounting tests must pass before enabling these pools in production.
11. **Labels and exports:** Admission results, receipts, channel/admin displays and exports carry the accounting mode (`measured` or `estimated`), budget revision, unit convention, platform ledger state and completeness of interactive observation.

### B.3 Tool, skill and MCP adoption restrictions

The following adoption rules apply independent of the quota model:

1. **Explicit installation approval:** Installing a new skill, tool, MCP server, connector or execution engine requires an explicit installation approval that names the exact artifact, version or hash, allowed scopes, and allowed workspaces/projects.
2. **Memory/skill approval is not installation approval:** Approving a memory update or a skill reference version does not authorize its runtime installation or execution.
3. **Skill version/hash checks:** The Skill & Instruction Channel verifies the referenced skill version/hash before loading it into an invocation.
4. **No control-plane execution:** New actions or nodes must be registered and published before they execute; nothing is evaluated in the control plane.
5. **Scope-bound adoption:** A skill/tool adopted for one workspace cannot be used in another workspace without an explicit cross-workspace grant.
6. **Audit trail:** Every adoption decision is recorded with the adopter identity, timestamp, artifact identity and approved scope.

### B.5 Non-waivable security policy

Security, authentication, tenant isolation, credential handling and externally consequential actions are **never waivable**. If a security issue cannot be fixed automatically, the run produces a typed question and waits; nothing ships as verified while the issue is open. Quality findings may be accepted with an authorized, reasoned, audited, scoped, expiring waiver that is visible in the release.

### B.4 Approved baselines pin

The reconciled Mahmoud OS v2.1.2 uses the pinned baselines recorded in `New-forge/docs/specs/FIRST-DELIVERY.json` and `New-forge/docs/specs/SECTION-APPROVALS.json`. Section-level approvals are authoritative; a contract-level commit does not automatically approve every section within it.

| Contract | Approved baseline | Section-specific notes |
|---|---|---|
| A00 | `710e1c1bc5a1afd03c40b07427d8980e02affe68` | Approved pinned baseline; extensions approved |
| P01 | `710e1c1bc5a1afd03c40b07427d8980e02affe68` | Approved: architecture, browser/service contracts, Clerk config, failure/security behavior, UI/UX, acceptance gate, request flow, fresh schema, revocation, webhooks, identity acceptance matrix, **and** `P01-IDENTITY.md#proposed-first-use-command-and-service-policy-authority` (approved-pinned-baseline). The approval applies only to that exact section. |
| P02 | `710e1c1bc5a1afd03c40b07427d8980e02affe68` | Approved: contracts/publication, dynamic changes, UI/UX, acceptance gate |
| P03 | `710e1c1bc5a1afd03c40b07427d8980e02affe68` | Approved: building/configuring workflows |
| P04 | `710e1c1bc5a1afd03c40b07427d8980e02affe68` | Approved: contracts, child-calls, foundation reconciliation |
| P05 | `710e1c1bc5a1afd03c40b07427d8980e02affe68` | Approved: contracts/behavior, input/output UX |
| P06 | `710e1c1bc5a1afd03c40b07427d8980e02affe68` | Approved: agent contract, execution sequence, chat coordinator, routing |
| P07 | `710e1c1bc5a1afd03c40b07427d8980e02affe68` | Approved: skill contracts, composition, CLI instruction delivery |
| P08 | `710e1c1bc5a1afd03c40b07427d8980e02affe68` | Approved: contracts/flows, isolation. **Pending:** proposed revocation-impact confirmation |
| P09 | `710e1c1bc5a1afd03c40b07427d8980e02affe68` | Approved: external effects/sandboxing, isolation |
| P10 | `710e1c1bc5a1afd03c40b07427d8980e02affe68` | Approved: contracts/lifecycle. **Pending:** proposed professional views/export |
| P12 | `710e1c1bc5a1afd03c40b07427d8980e02affe68` | Approved: contracts/routing **and** `P12-MODELS.md#proposed-cache-completeness-and-derived-admission` (approved-pinned-baseline). The approval applies only to that exact section. |
| P12A | `710e1c1bc5a1afd03c40b07427d8980e02affe68` | Approved: binding models, routing, CLI delivery |
| P12B | `f2a188a0938ec7bb9cb45ad534dfdab9f1e99edf` | Approved: states/dispatch gate, reset/user confirmation, suspected-limit lifecycle, CLI recovery probe, C-007a estimated accounting |
| P13 | `710e1c1bc5a1afd03c40b07427d8980e02affe68` | Approved: contracts, verification **and** `P13-EVALUATIONS.md#proposed-citation-verification-before-repair` (approved-pinned-baseline). The approval applies only to that exact section. |
| P14 | `710e1c1bc5a1afd03c40b07427d8980e02affe68` | Approved: delivery/failure behavior, quota, grouped admin alerts |
| P15/P17 | `5b6bbda5ddc9ff8429c1c48bb6d4a48e896df138` | Full P15 administration/audit/quotas and P17 templates/presets/parity |
| P16 | `666e45023cfbf6227e4dd1f52b24455fc46a9537` | Approved: build/startup contract, isolation, independent acceptance bootstrap. **Pending:** proposed first-delivery restore evidence |
| P18 | `710e1c1bc5a1afd03c40b07427d8980e02affe68` | Approved: data contracts, browser/API flow, verification |
| P19 | `f2a188a0938ec7bb9cb45ad534dfdab9f1e99edf` | Approved: self-healing review gates, verification, gate continuation |
| P20 | `f2a188a0938ec7bb9cb45ad534dfdab9f1e99edf` | Approved: monitoring/call records, durable conversation, delivery, user messages, chat routing/budget |
| verification contract | `f2a188a0938ec7bb9cb45ad534dfdab9f1e99edf` | Approved: verification, gate continuation |
| P21 | pending | Some P21 sections are retained as visible dependencies (legacy producer/consumer reconciliation, registered research, operational incidents); full app delivery and new permissions remain separately gated. |
| P11, P22, P23, P24, P25 | not yet approved | Preserve as required full-product scope per C-012; P23 Guardian/learning is referenced but not fully approved. |

P21 and unapproved contracts remain in scope as **required full-product outcomes** but are not yet implementation-authorized. Their acceptance tests must be drafted and approved before code is written.
