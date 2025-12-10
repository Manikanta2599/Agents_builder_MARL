"use client";

import { useState } from "react";
import ChatInterface from "@/components/ChatInterface";
import AgentVisualizer from "@/components/AgentVisualizer";
import { useParams, useSearchParams } from "next/navigation";

export default function SessionPage() {
    const params = useParams();
    const searchParams = useSearchParams();
    const initialPrompt = searchParams.get("q") || "";

    const [steps, setSteps] = useState<any[]>([]);
    const [sessionId, setSessionId] = useState<string | undefined>(undefined);

    const handleResponse = (data: any) => {
        setSessionId(data.session_id);
        if (data.steps) {
            setSteps(prev => [...prev, ...data.steps]);
        }
    };

    return (
        <div className="flex h-screen w-full overflow-hidden bg-[#050505]">
            {/* Left Pane: Chat */}
            <div className="w-1/2 border-r border-white/5 flex flex-col">
                <header className="h-14 border-b border-white/5 flex items-center px-6 bg-white/5 backdrop-blur-md">
                    <header className="h-14 border-b border-white/5 flex items-center px-6 bg-white bg-opacity-5 backdrop-blur-md">
                        <span className="font-semibold text-white/80">Session: {params.id === "new" ? "New Project" : params.id}</span>
                    </header>
                    <ChatInterface initialPrompt={initialPrompt} onResponse={handleResponse} sessionId={sessionId} />
            </div>

            {/* Right Pane: Agent Brain */}
            <div className="w-1/2 flex flex-col bg-[#080808]">
                <header className="h-14 border-b border-white/5 flex items-center px-6 justify-between bg-white bg-opacity-5 backdrop-blur-md">
                    <span className="font-semibold text-purple-400">Orchestrator Activity</span>
                    <div className="flex items-center space-x-2">
                        <span className="h-2 w-2 rounded-full bg-green-500 animate-pulse"></span>
                        <span className="text-xs text-green-500 font-mono">LIVE</span>
                    </div>
                </header>
                <AgentVisualizer steps={steps} />
            </div>
        </div>
    );
}
