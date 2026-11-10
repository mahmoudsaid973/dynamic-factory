# Independent Review: Mahmoud OS Blueprint v2.0 + Feature Priority v2.0

> Reviewer role: independent critical reviewer
> Date: 2026-11-11
> Source files reviewed:
> - `D:/VS Code Projects/dynamic-factory/plans/mahmoud-os-master-blueprint.md`
> - `D:/VS Code Projects/dynamic-factory/plans/mahmoud-os-feature-priority.md`
> - `C:/Users/mahmo/Documents/Codex/New-forge/package.json`
> - `C:/Users/mahmo/Documents/Codex/New-forge/apps/web/package.json`
> - `C:/Users/mahmo/Documents/Codex/New-forge/docs/ARCHITECTURE.md`
> - `C:/Users/mahmo/Documents/Codex/New-forge/docs/AUTHENTICATION.md`
> - `C:/Users/mahmo/Documents/Codex/New-forge/docs/AGENTS.md`

**Executive summary:** The v2.0 documents are a clear improvement over v1.0, but they still contain unresolved architecture contradictions, impossible phase/bucket pairings, an over-heavy canonical hierarchy for simple workflows, missing concrete criteria, and unverified claims about the New-forge baseline. **Not ready for implementation.** A v2.1 revision is required before any P0 code work.

**Readiness verdict:** ❌ **Not ready.** Seven critical findings and five high findings block approval. Resolve all critical and high findings, produce the v2.1 change list, and re-review before declaring the blueprint ready.

---

## 1. Findings ranked by severity

### 🔴 Critical

#### C1 — Architecture contradiction: Next.js web shell vs New-forge React/Vite

- **Evidence:**
  - Blueprint §5.1 ASCII diagram line 95: `• Next.js web shell (JARVIS HUD-style dashboard + chat)`
  - Blueprint §5.2 line 141: `New-forge React/Vite/React Flow shell` becomes the primary web shell.
  - `New-forge/apps/web/package.json` line 1: scripts use `vite --host 0.0.0.0`; dependencies are `react`, `react-dom`, `@xyflow/react`, `@vitejs/plugin-react`, `vite`.
  - `New-forge/docs/ARCHITECTURE.md` line 7: `React/TypeScript/React Flow supplies the visual editor`.
- **Severity:** Critical. The product cannot be built on two incompatible frontend stacks. Next.js 15 was the old `dynamic-factory` scaffold; New-forge is Vite.
- **Proposed correction v2.1:**
  - Replace every "Next.js web shell" reference with "React/Vite/React Flow web shell".
  - State explicitly that the UI is built inside New-forge's existing Vite/React workspace.
  - Retire the `dynamic-factory` Next.js scaffold from architecture; note it exists only as the planning-file host.

#### C2 — Must items scheduled after the phase that claims to deliver all Must items

- **Evidence:**
  - `mahmoud-os-feature-priority.md` §Summary line 14: Must = `Required for P0–P4 acceptance`.
  - §1 row 21: `Provider Registry + Allowance Governor` is Must, phase **P5**.
  - §1 row 22: `MCP Gateway + Connector Registry` is Must, phase **P6**.
  - §1 row 23: `Performance Rules Engine` is Must, phase **P0/P8**.
  - §5 line 167: `All Must items in rows 1–30 above must be present with evidence` by end of P4.
- **Severity:** Critical. Either the bucket definition is wrong, the phase assignments are wrong, or the acceptance rule is impossible.
- **Proposed correction v2.1:**
  - Move `Provider Registry + Allowance Governor` to **P1/P2 Must** (a minimal budget hold/policy layer is needed before any paid/CLI call).
  - Move `MCP Gateway + Connector Registry` to **P2/P3 Must** (a simple Files/API connector is needed before the first real workflow run).
  - Split `Performance Rules Engine`: keep the **audit inventory + budget** as P0 Must; keep the **full CI gates + RUM feedback** as P8 Should.
  - Change the summary line to: "Must = required for first admitted run by end of P4" and ensure every Must row has phase ≤ P4.

#### C3 — JEV Routing Agent is declared a "first-class agent" before Agent Studio exists

- **Evidence:**
  - Blueprint §5.3 line 158: JEV Routing Agent is an "explicit system agent" with "own profile, skill references, and decision log".
  - Blueprint §7.1 lines 236–246: same agent requirements.
  - Feature priority row 1: JEV Routing Agent is Must, **P1**.
  - Feature priority row 16: Agent Studio is Must, **P4**.
- **Severity:** Critical. If the routing agent needs agent profiles, skills, snapshots, and allowance tracking, it cannot ship before the agent infrastructure exists. This is either a dependency inversion or a terminological trap.
- **Proposed correction v2.1:**
  - Define two layers:
    1. **JEV Router (P1 Must):** deterministic rules + bounded classifier + request identity. Implemented as a core gateway module, not a generic agent.
    2. **JEV Routing Agent (P4 Should/Optional):** an Agent Studio profile that can be invoked to review/refine routing decisions.
  - Make P1 acceptance use the gateway module; P4 acceptance adds the optional agent-based review.

#### C4 — Canonical hierarchy still forces milestones and epics on simple workflows

- **Evidence:**
  - Blueprint §6.1 lines 184–197: `Workspace → Request → Project → Milestone → Epic → Canonical Task → Run → ...`
  - Review requirement: "Simple business workflows must not require development milestones or epics."
- **Severity:** Critical. The hierarchy is the Forge SDLC template. Forcing it on every project/run contradicts the user's requirement.
- **Proposed correction v2.1:**
  - Replace the single hierarchy with two explicit tracks:
    - **Simple workflow track:** `Project → Workflow binding → Run → Step → Attempt` (no milestone/epic).
    - **Forge SDLC track:** `Project → Milestone → Epic → Canonical Task → Workflow Version → Run → Phase → Work Group → Small Work Item → Invocation → Attempt`.
  - State that the simple track is the default and the Forge track is opt-in per project.

#### C5 — P0 acceptance gate is unrealistic given known CI state

- **Evidence:**
  - Blueprint §18 P0 line 589: `base branch green on CI or blockers honestly reported`.
  - `New-forge/docs/STATUS.md` line 5: `The prior published 27e8871 native run fails the first-use policy inventory`.
  - `New-forge/docs/BACKLOG.md` line 142: `Current published foundation is 22c39d5: ... zero accepted criteria across all M0–M4`.
- **Severity:** Critical. "Green on CI" is unlikely on the first audit. The gate should require an honest blocker report, not a green CI fantasy.
- **Proposed correction v2.1:**
  - Change P0 acceptance to: "Baseline branch pinned; CI state honestly reported; all blockers triaged with owner severity; no code changes attempted until blockers are accepted or removed."

#### C6 — "Lossless" copy/paste is impossible and misleading

- **Evidence:**
  - Blueprint §11.1 line 379: `Copy/paste whole workflow or selected parts with ID remapping and unresolved boundary ports surfaced`.
  - Feature priority row 9: `Lossless copy/paste of whole workflow or selected fragments`.
- **Severity:** Critical. You cannot preserve runtime state, environment-specific connections, or secrets in a fragment. "Lossless" sets an impossible acceptance bar.
- **Proposed correction v2.1:**
  - Replace "lossless" with **"schema-preserving"** or **"identity-remapping"** copy/paste.
  - Define acceptance: all typed ports, edges, contracts, and required capabilities are preserved; runtime state and secrets are explicitly stripped.

#### C7 — The Bridge is added as a component but not scheduled

- **Evidence:**
  - Blueprint §5.3 line 156: `The Bridge` — new major component.
  - Roadmap P1 lines 593–600: mentions "JEV router gateway" but never "The Bridge" as a named deliverable.
- **Severity:** Critical. The central gateway cannot be implicit.
- **Proposed correction v2.1:**
  - Add a P1 deliverable: "Implement The Bridge gateway module: request normalization, authentication, workspace resolution, policy enforcement, context resolution, request record creation."

---

### 🟠 High

#### H1 — Provider Registry + Allowance Governor is one item but has split phases

- **Evidence:**
  - Feature priority row 21: `Provider Registry + Allowance Governor` as one Must item, phase P5.
  - Blueprint P3 lines 613–620: native execution engines run in P3, which need provider routing and budget holds.
- **Severity:** High. Conflates two capabilities with different readiness needs.
- **Proposed correction v2.1:**
  - Split into:
    - `Provider Registry (minimal)` — Must, P1/P2: register providers, route calls, record usage.
    - `Allowance Governor` — Must, P2/P3: holds, quotas, stop-on-exhaustion.
    - `Advanced failover / model rebinding` — Should, P5.

#### H2 — MCP/Connector Registry marked Must but first real connectors listed are P6

- **Evidence:**
  - Feature priority row 22: `MCP Gateway + Connector Registry` Must, phase P6.
  - User journey requires "recommended helpers/abilities/app connections/tools" at idea time.
- **Severity:** High. If connectors are recommended in P1 but do not exist until P6, the creator journey is fake.
- **Proposed correction v2.1:**
  - Move a minimal `Demo/Mock Connector Registry` to P1/P2 Must: show connection status, permissions, and "Not connected" state.
  - Keep real Gmail/Calendar/Drive/YouTube/GitHub adapters as P3/P4 Must.

#### H3 — Exact 31 performance criteria are not listed

- **Evidence:**
  - Blueprint §13 lines 452–475: repeatedly references "31 criteria" but never enumerates them.
  - Review requirement: "Include the exact performance criteria."
- **Severity:** High. Cannot implement or audit a rules engine without the rule list.
- **Proposed correction v2.1:**
  - Add Appendix A to the blueprint: numbered list of the 31 criteria with ID, title, detection method, and applicability flag.

#### H4 — Project import is mentioned but not defined

- **Evidence:**
  - Blueprint §11.2 line 385: `Enter name/purpose/type/owner and optional repository/documents; connect only authorized sources`.
  - Feature priority row 4: `Project Hub: create/import project`.
- **Severity:** High. "Import" could mean clone repo, upload docs, link GitHub project, or ingest from forge-ai. Ambiguity will cause scope creep.
- **Proposed correction v2.1:**
  - Define import modes: (a) blank project, (b) link existing GitHub repo (read-only metadata), (c) upload documents/zip, (d) fork from existing New-forge project.
  - State which are Must (blank + GitHub link) and which are Should/Future.

#### H5 — workflow-observer role remains unresolved

- **Evidence:**
  - Blueprint §5.2 line 149: `workflow-observer` = `Bounded monitoring adapter pattern; optional module`.
  - Open decision #7 line 708: `Workflow-observer role: reuse as a bounded monitoring adapter, or retire it?`
- **Severity:** High. Leaving an architectural component as an open question in a blueprint that claims to be ready is a planning failure.
- **Proposed correction v2.1:**
  - Decide and document: reuse for local/dev observation telemetry only, or retire and replace with New-forge's native observation channel.
  - Remove from open decisions once resolved.

---

### 🟡 Medium

#### M1 — "OpenCode Go" vs "OpenCode CLI" terminology inconsistency

- **Evidence:**
  - Blueprint §5.2 line 145: `OpenCode Go/Codex/Claude/Ollama/NVIDIA adapters`.
  - Blueprint §5.3 line 176 and §12.4 line 432: `OpenCode CLI`.
- **Severity:** Medium.
- **Proposed correction v2.1:** Pick one term and use it everywhere. If both exist, define the relationship (OpenCode Go is the service binary; OpenCode CLI is the invocation mode).

#### M2 — F01–F50 mapping lacks disposition verbs

- **Evidence:**
  - Blueprint §17 lines 524–573: Disposition column uses vague phrases like `Enhance with`, `Reuse`, `Integrate into`.
- **Severity:** Medium.
- **Proposed correction v2.1:** Use precise verbs: `Preserve as-is`, `Extend`, `Reimplement`, `Govern via`, `Deprecate`, `Out of scope`. Add an owner column for each F area.

#### M3 — Quota policy is asserted without approved source

- **Evidence:**
  - Blueprint §15 line 502: `Preserve approved 70% automation / 30% interactive reserve for shared Claude/Codex allowance`.
  - No citation to the approval record or issue comment is given.
- **Severity:** Medium.
- **Proposed correction v2.1:** Cite the exact decision record (issue/comment/commit). If unverified, label it `pending owner confirmation`.

#### M4 — Hermes self-review safeguards are policy, not mechanism

- **Evidence:**
  - Blueprint §10.4 lines 361–365: says review agent cannot change config/secrets but does not say how.
- **Severity:** Medium.
- **Proposed correction v2.1:** Add concrete mechanisms: read-only API role, no write token, review outputs stored as evidence records, apply path requires user approval + normal Forge admission.

#### M5 — P4 acceptance rule references Hermes self-review (P4) but not provider/connector state

- **Evidence:**
  - Feature priority §1 lines 57–59: P4 acceptance rule includes Hermes self-review but omits provider/connector budget status.
- **Severity:** Medium.
- **Proposed correction v2.1:** Update the P4 acceptance rule to include: "A tool/model call respects the minimal provider registry and allowance hold; a disconnected connector is shown as Not connected."

---

## 2. Previous recommendations I disagree with

1. **"dynamic-factory is set aside" while keeping the files there.**
   - The planning files are literally inside `dynamic-factory/plans/`. Either move them to a `mahmoud-os-plans` repo/folder or stop claiming the project is set aside. Recommendation: move planning files to a neutral `plans-mahmoud-os` folder or a new repo.

2. **MCP Gateway marked Must but scheduled P6.**
   - Earlier I agreed with promoting MCP to Must. That was correct for the user journey, but the phase assignment P6 was wrong. Either demote to Should or bring the minimal registry to P2.

3. **"All Must by P4" summary.**
   - I previously allowed rows 21–23 to remain Must with later phases. That created the critical contradiction C2. v2.1 must fix the phase assignments, not the summary.

---

## 3. Proposed v2.1 change list

### Blueprint changes

| # | Section | Change |
|---|---|---|
| 1 | §5.1 ASCII diagram | Replace `Next.js web shell` with `React/Vite/React Flow web shell` |
| 2 | §5.2 mapping table | Add explicit note: "Mahmoud OS UI extends New-forge apps/web; no Next.js rewrite" |
| 3 | §5.3 | Add The Bridge as a P1 deliverable in the roadmap |
| 4 | §6.1 | Replace single hierarchy with simple-track vs Forge-track |
| 5 | §11.1 | Replace "lossless" copy/paste with "schema-preserving" |
| 6 | §11.2 | Define project import modes and scope |
| 7 | §13 | Add Appendix A: exact 31 criteria list |
| 8 | §15 | Cite 70/30 quota decision source or label pending |
| 9 | §17 F-table | Add owner column and precise disposition verbs |
| 10 | §18 P0 | Change acceptance to "baseline pinned + honest CI/blocker report" |
| 11 | §18 P1 | Split JEV Routing Agent into gateway module (P1) and optional agent profile (P4) |
| 12 | §21 | Resolve workflow-observer role; remove from open decisions |
| 13 | §10.4 | Add concrete enforcement mechanisms for self-review safeguards |
| 14 | Glossary | Define "schema-preserving", "run-pinned", "workflow binding" |

### Feature priority changes

| # | Change |
|---|---|
| 1 | Update summary: Must = required for first admitted run by end of P4 |
| 2 | Split row 21 into `Provider Registry (minimal) Must P1/P2` and `Allowance Governor Must P2/P3` |
| 3 | Move `MCP Gateway + Connector Registry` to P2/P3 Must (minimal demo registry P1/P2) |
| 4 | Split `Performance Rules Engine`: inventory/budget Must P0; full CI gates Should P8 |
| 5 | Update P4 acceptance rule to include provider/connector state |
| 6 | Move JARVIS HUD polish to Should (dependent on web shell) |

---

## 4. Requirement / owner / dependency / acceptance matrix

| Requirement | Owner | Dependencies | Phase | Acceptance |
|---|---|---|---|---|
| The Bridge gateway | Platform/backend lead | Clerk identity, workspace policy, request schema | P1 | Unit + integration tests; request record created with ID, workspace, source interface, language, correlation ID |
| JEV router (gateway module) | Platform/backend lead | The Bridge | P1 | Deterministic rules pass lookup without model; quick answer uses bounded model; planned work creates run; explanation shown |
| JEV Routing Agent (optional review profile) | Agent team | Agent Studio, skill channel | P4 | Can review routing decisions; user can override with logged reason |
| Project Hub create/import | Web/backend lead | Workspace identity | P1 | Blank project created; GitHub repo linked read-only; empty state visible |
| Workflow Studio | Web/backend lead | New-forge registry services | P1 | Draft created, edited, published as immutable version; copy/paste schema-preserving |
| Project-workflow binding | Backend lead | Project Hub, Workflow Studio | P1 | Binding record links project + workflow version + inputs + version policy |
| Idea-driven recommendations | AI/UX team | Workflow Studio, catalog | P1 | Typed idea produces editable plan with component cards showing fit/source/permissions/cost |
| Minimal provider registry | Backend lead | The Bridge | P1/P2 | Providers registered; route calls; usage recorded |
| Allowance governor | Backend lead | Provider registry | P2/P3 | Budget hold, exhaustion stops calls, probe policy |
| Native execution engines | Backend/CLI lead | Durable runner, allowance governor | P3 | Claude Code/Codex/OpenCode/Ollama CLI invoked as subprocess with streamed output and artifact capture |
| Human approval checkpoint | Backend/UX lead | Durable runner | P3 | Consequential action pauses; approval event recorded; refusal stops branch |
| MCP/connector registry (minimal) | Backend/UX lead | The Bridge | P1/P2 | Demo connectors listed; real connection verified before "Connected" |
| Real connectors (Gmail/Drive/Calendar/YouTube/GitHub) | Integrations lead | MCP registry, credential vault | P3/P4 | At least one real demo adapter connects and executes a scoped read operation |
| Knowledge Vault + Obsidian sync | Full-stack lead | Markdown storage, file watcher | P1 | Bidirectional sync test; conflict detection |
| Event + Evidence Archive | Backend lead | Durable runner | P3 | Every run/invocation/attempt produces versioned, sanitized events |
| Agent Studio | Backend/UX lead | Durable runner | P4 | Profile created, assigned to run, edited; old run keeps original snapshot |
| Skill & Instruction Channel | Backend/UX lead | Agent Studio | P4 | Skill reference versioned/hash-checked; instruction channel separated from knowledge |
| Hermes Self-Improvement Review | Platform governance | Agent Studio, skill channel, evidence archive | P4 | Review produces structured report; user approves each suggestion; apply path uses normal admission gates |
| Performance Rules inventory | QA/performance lead | Repository, CI | P0 | 31 criteria listed, applicability flags set, baseline status recorded |
| Full performance rules engine + CI gates | QA/performance lead | Performance inventory, RUM | P8 | CI scan reports drift; PR gates trigger review |
| EN/AR RTL shell | Frontend lead | Vite/React shell | P1 | Locale switch mirrors layout; identifiers stay LTR |
| Accessibility WCAG 2.2 AA | Frontend/QA lead | Web shell | P1/P8 | Keyboard, focus, screen-reader, reduced-motion tests pass |
| LLM Council adapter | AI/platform lead | Provider registry (full) | P5 | Governance review and workflow node run end-to-end |
| Agent Swarm / Coordinator | AI/platform lead | Agent Studio, durable runner | P5 | Multi-agent task delegates and aggregates |
| Schedules/notifications | Backend/UX lead | Durable runner | P8 | Schedule triggers without duplicate execution; timezone/overlap handled |
| Hermes `/os` skill | Hermes skill author | Most core features | P9 | Create/review/monitor via skill; identity shared with web |

---

## 5. Remaining decisions

| # | Decision | Why it blocks |
|---|---|---|
| 1 | New-forge baseline branch: `main` or `develop`? | P0 cannot start without a pinned baseline. |
| 2 | Repository location: planning shell in `dynamic-factory` or new Mahmoud OS repo? | Affects branch strategy, CI, and how New-forge is consumed. |
| 3 | Workflow-observer role: reuse, retire, or migrate? | Affects monitoring architecture and duplication risk. |
| 4 | Obsidian sync mode: filesystem watcher or plugin REST bridge? | Affects P1 implementation and security model. |
| 5 | Voice: required (move to Must) or experimental (keep as Should/Future)? | Affects P1/P3 scope. |
| 6 | 70/30 quota policy: confirmed owner approval or pending? | Affects allowance governor design. |
| 7 | Project import scope: which modes are Must? | Affects P1 acceptance criteria. |

---

## 6. Readiness verdict

**❌ Not ready for implementation.**

The v2.0 documents correctly identify New-forge as the baseline and separate Workflow Studio from projects, but they still contain critical architecture contradictions (Next.js vs Vite), impossible phase/bucket pairings, an over-heavy canonical hierarchy, missing concrete criteria, and unverified claims about the baseline CI state. All critical and high findings must be resolved in a v2.1 revision before P0 can begin.

**Next action:** Produce `mahmoud-os-master-blueprint-v2.1.md` and `mahmoud-os-feature-priority-v2.1.md` addressing the change list above, then re-run this review.
