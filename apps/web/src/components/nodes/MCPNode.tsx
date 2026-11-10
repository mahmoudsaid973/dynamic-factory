import { Handle, Position } from "@xyflow/react";

interface MCPNodeData {
  label: string;
  operation?: string;
  path?: string;
}

export function MCPNode({ data }: { data: MCPNodeData }) {
  return (
    <div className="rounded border border-[var(--color-border)] bg-[var(--color-surface-elevated)] p-3 min-w-[180px]">
      <Handle type="target" position={Position.Top} className="!bg-green-500" />
      <div className="text-xs font-bold text-green-500 mb-1">{data.label}</div>
      <div className="text-xs text-[var(--color-text-muted)]">
        {data.operation ? `${data.operation} ${data.path ?? ""}`.trim() : "Filesystem MCP"}
      </div>
      <Handle type="source" position={Position.Bottom} className="!bg-green-500" />
    </div>
  );
}
