import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { FlowCanvas } from "@/components/FlowCanvas";
import * as api from "@/lib/api";

vi.mock("@xyflow/react", async () => {
  const actual = await vi.importActual<typeof import("@xyflow/react")>("@xyflow/react");
  return {
    ...actual,
    ReactFlow: ({ children }: { children: React.ReactNode }) => <div data-testid="reactflow">{children}</div>,
    Background: () => null,
    Controls: () => null,
    MiniMap: () => null,
    useReactFlow: () => ({ fitView: vi.fn() }),
  };
});

vi.mock("@/lib/store", () => ({
  useFactoryStore: Object.assign(
    () => ({ activeProviderId: null, workflowId: null }),
    {
      getState: () => ({ setWorkflowId: vi.fn(), setActiveProviderId: vi.fn() }),
    },
  ),
}));

vi.mock("uuid", () => ({
  v4: vi.fn().mockReturnValue("node-1"),
}));

describe("FlowCanvas", () => {
  it("renders toolbar buttons", () => {
    render(<FlowCanvas />);
    expect(screen.getByRole("button", { name: /prompt/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /llm/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /save/i })).toBeDisabled();
  });

  it("adds a prompt node and enables save", async () => {
    render(<FlowCanvas />);
    await userEvent.click(screen.getByRole("button", { name: /prompt/i }));
    expect(screen.getByRole("button", { name: /save/i })).toBeEnabled();
  });

  it("saves workflow via api when nodes exist", async () => {
    const createWorkflow = vi.spyOn(api, "createWorkflow").mockResolvedValue({
      id: "flow-1",
      name: "Untitled Flow",
      nodes: [],
      edges: [],
    });
    render(<FlowCanvas />);
    await userEvent.click(screen.getByRole("button", { name: /prompt/i }));
    await userEvent.click(screen.getByRole("button", { name: /llm/i }));
    await userEvent.click(screen.getByRole("button", { name: /save/i }));
    expect(createWorkflow).toHaveBeenCalledWith(
      expect.objectContaining({
        name: "Untitled Flow",
        nodes: expect.arrayContaining([
          expect.objectContaining({ kind: "prompt" }),
          expect.objectContaining({ kind: "llm" }),
        ]),
      }),
    );
  });
});
