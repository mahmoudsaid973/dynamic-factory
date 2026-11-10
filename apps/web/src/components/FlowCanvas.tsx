"use client";

import {
  addEdge,
  Background,
  Controls,
  MiniMap,
  ReactFlow,
  useEdgesState,
  useNodesState,
  useReactFlow,
  type Connection,
  type Edge,
  type Node,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { useCallback, useMemo } from "react";
import { v4 as uuidv4 } from "uuid";
import { LLMNode } from "@/components/nodes/LLMNode";
import { PromptNode } from "@/components/nodes/PromptNode";
import { createWorkflow } from "@/lib/api";
import { useFactoryStore } from "@/lib/store";
import type { FlowNode } from "@/types/flow";

type NodeData = Record<string, unknown> & {
  label: string;
  prompt?: string;
  providerId?: string;
  model?: string;
};

const nodeTypes = {
  prompt: PromptNode,
  llm: LLMNode,
};

export function FlowCanvas() {
  const [nodes, setNodes, onNodesChange] = useNodesState<Node>([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState<Edge>([]);
  const { fitView } = useReactFlow();
  const { activeProviderId } = useFactoryStore();

  const onConnect = useCallback(
    (connection: Connection) => setEdges((eds) => addEdge(connection, eds)),
    [setEdges],
  );

  const addNode = useCallback(
    (kind: "prompt" | "llm") => {
      const id = uuidv4();
      const position = { x: 250 + nodes.length * 30, y: 150 + nodes.length * 30 };
      const data: NodeData =
        kind === "prompt"
          ? { label: "Prompt", prompt: "Hello, world!" }
          : {
              label: "LLM",
              providerId: activeProviderId ?? undefined,
              model: "default",
            };
      const node: Node = { id, type: kind, position, data };
      setNodes((prev) => [...prev, node]);
      window.setTimeout(() => fitView({ padding: 0.2 }), 50);
    },
    [activeProviderId, fitView, nodes.length, setNodes],
  );

  const serializeWorkflow = useCallback(() => {
    const flowNodes: FlowNode[] = nodes.map((n) => ({
      id: n.id,
      kind: n.type as "prompt" | "llm",
      name: (n.data.label as string) ?? n.type ?? "node",
      config: n.data,
    }));
    const flowEdges = edges.map((e) => ({
      id: e.id,
      source_id: e.source,
      target_id: e.target,
    }));
    return { nodes: flowNodes, edges: flowEdges };
  }, [nodes, edges]);

  const saveFlow = useCallback(async () => {
    const { nodes: flowNodes, edges: flowEdges } = serializeWorkflow();
    const workflow = await createWorkflow({
      name: "Untitled Flow",
      nodes: flowNodes,
      edges: flowEdges,
    });
    useFactoryStore.getState().setWorkflowId(workflow.id);
  }, [serializeWorkflow]);

  const hasItems = useMemo(() => nodes.length > 0 || edges.length > 0, [nodes, edges]);

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center gap-2 border-b border-[var(--color-border)] p-2">
        <button
          type="button"
          onClick={() => addNode("prompt")}
          className="rounded bg-[var(--color-surface-elevated)] px-3 py-1.5 text-xs hover:bg-[var(--color-border)] border border-[var(--color-border)]"
        >
          + Prompt
        </button>
        <button
          type="button"
          onClick={() => addNode("llm")}
          className="rounded bg-[var(--color-surface-elevated)] px-3 py-1.5 text-xs hover:bg-[var(--color-border)] border border-[var(--color-border)]"
        >
          + LLM
        </button>
        <button
          type="button"
          onClick={saveFlow}
          disabled={!hasItems}
          className="ml-auto rounded bg-[var(--color-accent)] px-3 py-1.5 text-xs font-bold text-black hover:bg-[var(--color-accent-hover)] disabled:opacity-50"
        >
          Save
        </button>
      </div>
      <div className="relative flex-1">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          nodeTypes={nodeTypes}
          fitView
          className="bg-[var(--color-surface)]"
        >
          <Background gap={16} size={1} color="var(--color-border)" />
          <Controls />
          <MiniMap className="!bg-[var(--color-surface-elevated)]" />
        </ReactFlow>
      </div>
    </div>
  );
}
