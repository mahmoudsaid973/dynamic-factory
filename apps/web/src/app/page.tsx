import { ReactFlowProvider } from "@xyflow/react";
import { FlowCanvas } from "@/components/FlowCanvas";
import { ProviderPanel } from "@/components/ProviderPanel";
import { RunPanel } from "@/components/RunPanel";

export default function Home() {
  return (
    <ReactFlowProvider>
      <main className="flex h-screen w-full overflow-hidden">
        <div className="w-72 shrink-0">
          <ProviderPanel />
        </div>
        <div className="min-w-0 flex-1">
          <FlowCanvas />
        </div>
        <div className="w-80 shrink-0">
          <RunPanel />
        </div>
      </main>
    </ReactFlowProvider>
  );
}
