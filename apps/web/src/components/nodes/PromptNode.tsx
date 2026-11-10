import { Handle, Position } from "@xyflow/react";

interface PromptNodeData {
  label: string;
  prompt?: string;
}

export function PromptNode({ data }: { data: PromptNodeData }) {
  return (
    <div className="rounded border border-[var(--color-border)] bg-[var(--color-surface-elevated)] p-3 min-w-[180px]">
      <Handle type="target" position={Position.Top} className="!bg-[var(--color-accent)]" />
      <div className="text-xs font-bold text-[var(--color-accent)] mb-1">{data.label}</div>
      <div className="text-xs text-[var(--color-text-muted)] truncate">
        {data.prompt || "Double-click to edit"}
      </div>
      <Handle type="source" position={Position.Bottom} className="!bg-[var(--color-accent)]" />
    </div>
  );
}
