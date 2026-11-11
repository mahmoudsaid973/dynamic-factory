# Dynamic Factory — Phase 2: Figma Design-to-Code

> **Goal:** Let users import Figma designs into the factory, preview frames, and generate React/Next.js components or full pages. Expose this both as a workflow node and as a dedicated UI flow.

> **Architecture:** Add a Figma integration module in the API (`dynamic_factory/integrations/figma/`) that calls the Figma REST API, normalizes the node tree, and emits React + Tailwind code. Add a `FigmaNode` to the workflow engine. Add a Figma import panel in the frontend. Store Figma tokens per node (or via the provider registry as a new `figma` provider kind).

---

## Scope

1. Backend Figma client
2. Backend code generator (Figma nodes → React + Tailwind)
3. `FigmaNode` in the workflow engine
4. Frontend Figma import panel + generated code preview
5. Asset downloader (images/SVGs via Figma images API)
6. Tests with mocked Figma API fixtures
7. Update Hermes skill with a `/factory figma` shortcut (optional)

---

## Task 1: Figma REST API Client

**Objective:** Authenticate and fetch Figma file/node data.

**Files:**
- Create: `services/api/src/dynamic_factory/integrations/figma/client.py`
- Create: `services/api/src/dynamic_factory/integrations/figma/schemas.py`
- Create: `services/api/tests/integrations/figma/test_client.py`

**Steps:**
1. Implement `FigmaClient` with `httpx.AsyncClient`, base URL `https://api.figma.com/v1`.
2. Methods:
   - `get_file(file_key: str, token: str) -> FigmaFile`
   - `get_file_nodes(file_key, node_ids, token) -> dict[str, FigmaNode]`
   - `get_images(file_key, node_ids, token, format='svg', scale=1) -> dict[str, str]` (returns URL map)
3. Pydantic schemas for `FigmaFile`, `FigmaNode`, `FigmaDocument`, `FigmaPaint`, `FigmaRectangle`, etc.
4. Parse file key and node-id from a Figma URL.
5. Tests use `pytest-httpx` or `respx` fixtures; do not call real Figma API in tests.

**Verification:** `pytest services/api/tests/integrations/figma/test_client.py -v` passes.

**Commit:** `feat: add figma rest api client and schemas`

---

## Task 2: Figma-to-React Code Generator

**Objective:** Convert a Figma node tree into a React/Next.js component string with Tailwind classes.

**Files:**
- Create: `services/api/src/dynamic_factory/integrations/figma/generator.py`
- Create: `services/api/src/dynamic_factory/integrations/figma/normalizer.py`
- Create: `services/api/tests/integrations/figma/test_generator.py`

**Steps:**
1. Normalizer: flatten Figma tree into a simple intermediate representation `DesignNode` (id, type, name, bounds, styles, children).
2. Generator: recursively produce JSX:
   - `FRAME` / `GROUP` → `div` with Tailwind classes for size, background, rounded, padding, flex direction (if auto-layout), gap.
   - `TEXT` → `span` or `p` with Tailwind text styles (font size approximated, color, weight, alignment).
   - `RECTANGLE` / `ELLIPSE` → `div` with background/border/radius.
   - `VECTOR` / other unsupported nodes → `img` with URL from `get_images`.
3. Support `AUTO_LAYOUT` properties (`layoutMode`, `primaryAxisAlignItems`, `counterAxisAlignItems`, `itemSpacing`, `padding`).
4. Output a single React functional component with TypeScript props interface and a default export.
5. Tests use a sample Figma node JSON fixture.

**Verification:** Generated component string contains expected elements; tsc later can validate syntax.

**Commit:** `feat: add figma-to-react tailwind generator`

---

## Task 3: FigmaNode in Workflow Engine

**Objective:** Allow flows to consume Figma designs and output code.

**Files:**
- Create: `services/api/src/dynamic_factory/engine/nodes/figma_node.py`
- Modify: `services/api/src/dynamic_factory/engine/nodes/registry.py`
- Modify: `services/api/src/dynamic_factory/workflows/schemas.py` if needed
- Create: `services/api/tests/test_figma_node.py`

**Steps:**
1. Add `FigmaNode` to registry with type `"figma"`.
2. Config: `file_url`, `access_token`, `node_id` (optional; if omitted uses first top-level frame), `framework` (default `react-tailwind`), `include_assets`.
3. Execute:
   - Parse file_key/node_id from URL.
   - Fetch file tree via `FigmaClient`.
   - Locate target node (by node_id or first frame matching `#component` prefix).
   - If `include_assets`, fetch images for vector nodes.
   - Run generator and return `{code, language, assets, framework}`.
4. Register node type in frontend `FlowCanvas` and `types/flow.ts`.

**Verification:** `pytest services/api/tests/test_figma_node.py -v` passes.

**Commit:** `feat: register figma node in workflow engine`

---

## Task 4: Frontend Figma Import Panel

**Objective:** UI to paste a Figma URL, preview frames, select one, and generate code.

**Files:**
- Create: `apps/web/src/components/FigmaImportPanel.tsx`
- Create: `apps/web/src/lib/figma-api.ts`
- Modify: `apps/web/src/app/page.tsx` to add a tab switcher or route
- Create: `apps/web/src/components/__tests__/FigmaImportPanel.test.tsx`

**Steps:**
1. API client functions: `parseFigma(url, token)`, `generateFromFigma(url, token, nodeId)`.
2. Panel with inputs: Figma URL, access token, optional node ID.
3. "Preview" button calls backend to list top-level frames.
4. "Generate" button creates a Figma node in the current flow or returns code preview.
5. Display generated code in a read-only editor area (monospace) with copy button.
6. Allow inserting the generated code as a `figma` node in the active flow.

**Verification:** Component tests pass; Playwright e2e extends smoke test to import a public sample file or mocked backend response.

**Commit:** `feat: add figma import panel to frontend`

---

## Task 5: Asset Downloader + Write-to-Project Node (Optional)

**Objective:** Generated pages need images saved to the project.

**Files:**
- Create: `services/api/src/dynamic_factory/integrations/figma/assets.py`
- Create: `services/api/src/dynamic_factory/engine/nodes/write_files_node.py` (optional)

**Steps:**
1. `assets.py`: download image URLs from Figma into memory/bytes, return base64 or save to a configurable path.
2. If implementing write-files node: config = list of `{path, content}`; writes to filesystem within a configured workspace root (sandbox). Useful for app-generation flows.
3. Front-end: display asset list alongside generated code.

**Verification:** Unit test for asset download uses httpx mock.

**Commit:** `feat: download figma assets and write files node`

---

## Task 6: Security & Integration Tests

**Objective:** Ensure Figma integration is safe and wired end-to-end.

**Files:**
- Create: `services/api/tests/test_figma_flow_api.py`
- Modify: `apps/web/e2e/smoke.spec.ts`

**Steps:**
1. Backend flow API test: create a flow with a Figma node, run it with mocked Figma response, assert generated code contains expected elements.
2. E2E: open Figma panel, paste a sample URL, click generate, assert code preview appears.
3. Add Figma token to `.env.example` (optional).

**Verification:** All backend + frontend + e2e tests pass; npm audit and pip-audit remain clean.

**Commit:** `test: add figma integration and e2e tests`

---

## Risks

| Risk | Mitigation |
|---|---|
| Figma auto-layout is complex | Support only common flex cases; document unsupported advanced features. |
| Large files timeout | Use `node_ids` parameter to fetch only selected frames; cache results in Redis later. |
| Vector/SVG rendering | Use Figma images API to rasterize/SVG-export complex nodes. |
| Token security | Store per-node token encrypted at rest; never return in API responses. |

---

## Execution Order

1. Task 1 → Task 2 → Task 3 → Task 4 → Task 5 → Task 6
2. Use parallel subagents for Task 1+2+4 while interfaces are clear; merge before Task 3/5/6.
3. Open PR against `main` after full verification.
