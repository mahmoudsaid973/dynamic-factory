export type NodeKind = "prompt" | "llm";

export interface FlowNode {
  id: string;
  kind: NodeKind;
  name: string;
  config?: Record<string, unknown>;
}

export interface FlowEdge {
  id: string;
  source_id: string;
  target_id: string;
}

export interface Workflow {
  id: string;
  name: string;
  description?: string;
  config?: Record<string, unknown>;
  nodes: FlowNode[];
  edges: FlowEdge[];
}

export interface CreateWorkflowInput {
  name: string;
  description?: string;
  config?: Record<string, unknown>;
  nodes: FlowNode[];
  edges: FlowEdge[];
}

export interface NodeOutput {
  status: "pending" | "running" | "success" | "error";
  output?: string;
  error?: string;
}

export interface RunWorkflowResponse {
  workflow_id: string;
  outputs: Record<string, NodeOutput>;
}
