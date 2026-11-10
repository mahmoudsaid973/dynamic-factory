"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { createProvider, getProviders } from "@/lib/api";
import { useFactoryStore } from "@/lib/store";
import type { ProviderKind } from "@/types/provider";

const KINDS: ProviderKind[] = ["openai", "anthropic", "azure", "ollama"];

export function ProviderPanel() {
  const queryClient = useQueryClient();
  const { data: providers = [], isLoading } = useQuery({
    queryKey: ["providers"],
    queryFn: getProviders,
  });
  const { activeProviderId, setActiveProviderId } = useFactoryStore();
  const [form, setForm] = useState({
    name: "",
    kind: "openai" as ProviderKind,
    base_url: "",
    api_key: "",
    model_default: "",
  });

  const mutation = useMutation({
    mutationFn: createProvider,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["providers"] });
      setForm({ name: "", kind: "openai", base_url: "", api_key: "", model_default: "" });
    },
  });

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    mutation.mutate(form);
  };

  return (
    <div className="flex h-full flex-col border-r border-[var(--color-border)] bg-[var(--color-surface)]">
      <div className="border-b border-[var(--color-border)] p-3 text-sm font-bold">Providers</div>
      <div className="flex-1 overflow-auto p-3">
        {isLoading && <div className="text-xs text-[var(--color-text-muted)]">Loading...</div>}
        {providers.length === 0 && !isLoading && (
          <div className="text-xs text-[var(--color-text-muted)]">No providers yet.</div>
        )}
        <ul className="space-y-2">
          {providers.map((provider) => (
            <li key={provider.id}>
              <button
                type="button"
                onClick={() => setActiveProviderId(provider.id)}
                className={`w-full rounded border p-2 text-left text-xs transition-colors ${
                  activeProviderId === provider.id
                    ? "border-[var(--color-accent)] bg-[var(--color-surface-elevated)]"
                    : "border-[var(--color-border)] hover:bg-[var(--color-surface-elevated)]"
                }`}
              >
                <div className="font-bold">{provider.name}</div>
                <div className="text-[var(--color-text-muted)]">{provider.kind} / {provider.model_default}</div>
              </button>
            </li>
          ))}
        </ul>
      </div>
      <form onSubmit={submit} className="border-t border-[var(--color-border)] p-3 space-y-2">
        <div className="text-xs font-bold">Add Provider</div>
        <input
          type="text"
          placeholder="Name"
          value={form.name}
          onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
          className="w-full rounded border border-[var(--color-border)] bg-[var(--color-background)] px-2 py-1 text-xs"
          required
        />
        <select
          value={form.kind}
          onChange={(e) => setForm((f) => ({ ...f, kind: e.target.value as ProviderKind }))}
          className="w-full rounded border border-[var(--color-border)] bg-[var(--color-background)] px-2 py-1 text-xs"
        >
          {KINDS.map((k) => (
            <option key={k} value={k}>{k}</option>
          ))}
        </select>
        <input
          type="url"
          placeholder="Base URL"
          value={form.base_url}
          onChange={(e) => setForm((f) => ({ ...f, base_url: e.target.value }))}
          className="w-full rounded border border-[var(--color-border)] bg-[var(--color-background)] px-2 py-1 text-xs"
          required
        />
        <input
          type="text"
          placeholder="Default model"
          value={form.model_default}
          onChange={(e) => setForm((f) => ({ ...f, model_default: e.target.value }))}
          className="w-full rounded border border-[var(--color-border)] bg-[var(--color-background)] px-2 py-1 text-xs"
          required
        />
        <input
          type="password"
          placeholder="API key"
          value={form.api_key}
          onChange={(e) => setForm((f) => ({ ...f, api_key: e.target.value }))}
          className="w-full rounded border border-[var(--color-border)] bg-[var(--color-background)] px-2 py-1 text-xs"
          required
        />
        <button
          type="submit"
          disabled={mutation.isPending}
          className="w-full rounded bg-[var(--color-accent)] px-3 py-1.5 text-xs font-bold text-black hover:bg-[var(--color-accent-hover)] disabled:opacity-50"
        >
          {mutation.isPending ? "Saving..." : "Create"}
        </button>
        {mutation.isError && (
          <div className="text-xs text-[var(--color-error)]">{mutation.error?.message ?? "Failed to create provider"}</div>
        )}
      </form>
    </div>
  );
}
