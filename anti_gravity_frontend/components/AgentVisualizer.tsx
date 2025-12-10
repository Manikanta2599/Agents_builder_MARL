"use client";

import { CheckCircle, Circle, Loader2 } from "lucide-react";

export default function AgentVisualizer({ steps = [] }: { steps?: any[] }) {
    // Use real steps or fallback to empty
    const displaySteps = steps.length > 0 ? steps : [];

    return (
        <div className="flex-1 p-8 overflow-y-auto">
            <div className="space-y-8 relative">

                {/* Vertical Line */}
                <div className="absolute left-4 top-4 bottom-4 w-0.5 bg-white/10" />

                {displaySteps.map((s, idx) => {
                    const task = s.step || {};
                    const status = "completed"; // Currently API only returns completed steps 
                    const agent = task.worker || "Orchestrator";

                    return (
                        <div key={idx} className="relative pl-12 group">
                            {/* Node Icon */}
                            <div className={`absolute left-0 top-1 w-8 h-8 rounded-full border flex items-center justify-center bg-[#080808] z-10 border-green-500 text-green-500`}>
                                <CheckCircle size={16} />
                            </div>

                            {/* Card */}
                            <div className="p-4 rounded-xl border transition-all duration-200 bg-white/5 border-white/10 opacity-70 hover:opacity-100">

                                <div className="flex items-center justify-between mb-2">
                                    <span className="text-xs font-mono uppercase tracking-wider text-gray-500">{agent}</span>
                                    <span className="text-xs px-2 py-0.5 rounded-full bg-green-500/20 text-green-400">
                                        {status}
                                    </span>
                                </div>
                                <h3 className="text-sm font-medium text-white">{task.task}</h3>

                                {s.review && (
                                    <div className="mt-2 text-xs text-gray-400 bg-black/20 p-2 rounded border border-white/5">
                                        <span className={s.review.approved ? "text-green-400" : "text-red-400"}>
                                            Critic: {s.review.approved ? "Approved" : "Rejected"}
                                        </span>
                                    </div>
                                )}
                            </div>
                        </div>
                    );
                })}

                {displaySteps.length === 0 && (
                    <div className="text-center text-gray-500 mt-10 italic">
                        Waiting for Orchestrator...
                    </div>
                )}
            </div>
        </div>
    );
}
