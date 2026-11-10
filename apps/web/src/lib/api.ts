import axios from "axios";
import type { CreateProviderInput, Provider } from "@/types/provider";
import type {
  CreateWorkflowInput,
  RunWorkflowResponse,
  Workflow,
} from "@/types/flow";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

const client = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: { "Content-Type": "application/json" },
});

export async function getProviders(): Promise<Provider[]> {
  const { data } = await client.get<Provider[]>("/providers");
  return data;
}

export async function createProvider(input: CreateProviderInput): Promise<Provider> {
  const { data } = await client.post<Provider>("/providers", input);
  return data;
}

export async function createWorkflow(input: CreateWorkflowInput): Promise<Workflow> {
  const { data } = await client.post<Workflow>("/flows", input);
  return data;
}

export async function getWorkflow(id: string): Promise<Workflow> {
  const { data } = await client.get<Workflow>(`/flows/${id}`);
  return data;
}

export async function runWorkflow(id: string): Promise<RunWorkflowResponse> {
  const { data } = await client.post<RunWorkflowResponse>(`/flows/${id}/run`);
  return data;
}
