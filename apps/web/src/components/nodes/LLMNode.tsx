import { Handle, Position } from "@xyflow/react";

interface LLMNodeData {
  label: string;
  providerName?: string;
  model?: string;
}

export function LLMNode({ data }: { data: LLMNodeData }) {
  return (
    <div className="rounded border border-[var(--color-border)] bg-[var(--color-surface-elevated)] p-3 min-w-[180px]">
      <Handle type="target" position={Position.Top} className="!bg-blue-500" />
      <div className="text-xs font-bold text-blue-500 mb-1">{data.label}</div>
      <div className="text-xs text-[var(--color-text-muted)]">
        {data.providerName ? `${data.providerName} / ${data.model ?? "default"}` : "No provider"}
      </div>
      <Handle type="source" position={Position.Bottom} className="!bg-blue-500" />
    </div>
  );
}
