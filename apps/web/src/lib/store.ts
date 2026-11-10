import { create } from "zustand";

interface FactoryState {
  activeProviderId: string | null;
  workflowId: string | null;
  setActiveProviderId: (id: string | null) => void;
  setWorkflowId: (id: string | null) => void;
}

export const useFactoryStore = create<FactoryState>((set) => ({
  activeProviderId: null,
  workflowId: null,
  setActiveProviderId: (id) => set({ activeProviderId: id }),
  setWorkflowId: (id) => set({ workflowId: id }),
}));
