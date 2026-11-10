"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { runWorkflow } from "@/lib/api";
import { useFactoryStore } from "@/lib/store";
import type { NodeOutput, RunWorkflowResponse } from "@/types/flow";

export function RunPanel() {
  const queryClient = useQueryClient();
  const { workflowId } = useFactoryStore();
  const [outputs, setOutputs] = useState<Record<string, NodeOutput>>({});

  const mutation = useMutation<RunWorkflowResponse, Error, string>({
    mutationFn: runWorkflow,
    onSuccess: (data) => {
      setOutputs(data.outputs);
      queryClient.invalidateQueries({ queryKey: ["workflows", data.workflow_id] });
    },
  });

  const entries = Object.entries(outputs);

  return (
    <div className="flex h-full flex-col border-l border-[var(--color-border)] bg-[var(--color-surface)]">
      <div className="border-b border-[var(--color-border)] p-3 text-sm font-bold">Run</div>
      <div className="p-3">
        <button
          type="button"
          onClick={() => workflowId && mutation.mutate(workflowId)}
          disabled={!workflowId || mutation.isPending}
          className="w-full rounded bg-[var(--color-accent)] px-3 py-1.5 text-xs font-bold text-black hover:bg-[var(--color-accent-hover)] disabled:opacity-50"
        >
          {mutation.isPending ? "Running..." : "Run Flow"}
        </button>
        {!workflowId && (
          <div className="mt-2 text-xs text-[var(--color-text-muted)]">Save a flow to enable running.</div>
        )}
      </div>
      <div className="flex-1 overflow-auto p-3">
        {mutation.isError && (
          <div className="mb-3 rounded border border-[var(--color-error)] bg-[var(--color-surface-elevated)] p-2 text-xs text-[var(--color-error)]">
            {mutation.error.message}
          </div>
        )}
        {entries.length === 0 && !mutation.isPending && !mutation.isError && (
          <div className="text-xs text-[var(--color-text-muted)]">No outputs yet.</div>
        )}
        <ul className="space-y-2">
          {entries.map(([nodeId, output]) => (
            <li key={nodeId} className="rounded border border-[var(--color-border)] bg-[var(--color-surface-elevated)] p-2">
              <div className="text-xs font-bold text-[var(--color-text-muted)]">{nodeId}</div>
              <div
                className={
                  output.status === "error"
                    ? "text-xs text-[var(--color-error)]"
                    : "text-xs text-[var(--color-text)]"
                }
              >
                {output.status}
              </div>
              {output.output && (
                <pre className="mt-1 max-h-40 overflow-auto whitespace-pre-wrap rounded bg-[var(--color-background)] p-2 text-xs">{output.output}</pre>
              )}
              {output.error && (
                <pre className="mt-1 max-h-40 overflow-auto whitespace-pre-wrap rounded bg-[var(--color-background)] p-2 text-xs text-[var(--color-error)]">{output.error}</pre>
              )}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
