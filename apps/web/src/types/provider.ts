export type ProviderKind = "openai" | "anthropic" | "azure" | "ollama";

export interface Provider {
  id: string;
  name: string;
  kind: ProviderKind;
  base_url: string;
  api_key: string;
  model_default: string;
  config?: Record<string, unknown>;
}

export interface CreateProviderInput {
  name: string;
  kind: ProviderKind;
  base_url: string;
  api_key: string;
  model_default: string;
  config?: Record<string, unknown>;
}
