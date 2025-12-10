"use client";

import { MessageSquare, Cpu, Search, Sparkles } from "lucide-react";
import Link from "next/link";
import { useState } from "react";

export default function Home() {
  const [prompt, setPrompt] = useState("");

  return (
    <div className="flex flex-col items-center justify-center h-full p-8 space-y-12 relative overflow-hidden">
      {/* Background Glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-purple-600/20 blur-[120px] rounded-full pointer-events-none" />

      {/* Hero Section */}
      <div className="text-center z-10 space-y-4">
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-sm text-gray-400 mb-4">
          <Sparkles size={14} className="text-yellow-400" />
          <span>System Online: Standard Mode</span>
        </div>
        <h1 className="text-6xl font-bold tracking-tight">
          <span className="text-white">Anti-Gravity</span>
        </h1>
        <p className="text-xl text-gray-400 max-w-2xl mx-auto">
          Orchestrating autonomous agents to build your ideas.
        </p>
      </div>

      {/* Input Area */}
      <div className="w-full max-w-2xl z-10 relative group">
        <div className="absolute -inset-0.5 bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl opacity-30 group-hover:opacity-100 transition duration-500 blur"></div>
        <div className="relative flex items-center bg-[#0a0a0a] rounded-2xl p-2 border border-white/10">
          <Search className="ml-4 text-gray-500" />
          <input
            type="text"
            className="w-full bg-transparent border-none focus:ring-0 text-lg px-4 py-3 placeholder-gray-600 outline-none text-white"
            placeholder="What do you want to build today?"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
          />
          <Link href={`/session/new?q=${encodeURIComponent(prompt)}`}>
            <button className="bg-white text-black px-6 py-2 rounded-xl font-medium hover:bg-gray-200 transition-colors">
              Ignite
            </button>
          </Link>
        </div>
      </div>

      {/* Recent Sessions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 w-full max-w-4xl z-10">
        {[
          { title: "Python Trends Analysis", icon: <Search size={20} />, date: "2h ago" },
          { title: "Snake Game Generator", icon: <Cpu size={20} />, date: "1d ago" },
          { title: "Q4 Marketing Plan", icon: <MessageSquare size={20} />, date: "2d ago" },
        ].map((session, i) => (
          <div key={i} className="glass-card p-4 flex flex-col space-y-2 cursor-pointer group">
            <div className="flex items-center justify-between text-gray-400 group-hover:text-white transition-colors">
              <div className="p-2 rounded-lg bg-white/5 group-hover:bg-white/10">{session.icon}</div>
              <span className="text-xs">{session.date}</span>
            </div>
            <h3 className="font-medium text-lg leading-tight">{session.title}</h3>
          </div>
        ))}
      </div>

      {/* Footer */}
      <div className="absolute bottom-8 text-gray-600 text-sm">
        Powered by Anti-Gravity Intelligence
      </div>
    </div>
  );
}
