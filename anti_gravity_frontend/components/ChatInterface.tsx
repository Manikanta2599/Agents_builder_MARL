"use client";

import { useState } from "react";
import { Send, Paperclip, Bot, User } from "lucide-react";
import { api } from "@/services/api";

type Props = {
    initialPrompt: string;
    onResponse?: (data: any) => void;
    sessionId?: string;
};

export default function ChatInterface({ initialPrompt, onResponse, sessionId }: Props) {
    const [messages, setMessages] = useState([
        { role: "system", content: "Anti-Gravity Online. How can I help you build?" }
    ]);
    const [input, setInput] = useState(initialPrompt);
    const [loading, setLoading] = useState(false);

    const sendMessage = async () => {
        if (!input.trim() || loading) return;

        // Optimistic Update
        const userMsg = input;
        setMessages(prev => [...prev, { role: "user", content: userMsg }]);
        setInput("");
        setLoading(true);

        try {
            const data = await api.sendMessage(userMsg, sessionId);
            setMessages(prev => [...prev, { role: "system", content: data.response || "Task completed." }]);
            if (onResponse) onResponse(data);
        } catch (e) {
            setMessages(prev => [...prev, { role: "system", content: "Error communicating with Orchestrator." }]);
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex-1 flex flex-col relative h-full">
            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-6 space-y-6">
                {messages.map((msg, idx) => (
                    <div key={idx} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                        <div className={`max-w-[80%] rounded-2xl p-4 ${msg.role === "user" ? "bg-white/10 text-white" : "bg-purple-900/20 border border-purple-500/20 text-gray-200"}`}>
                            <div className="flex items-center space-x-2 mb-1 text-xs opacity-50">
                                {msg.role === "system" ? <Bot size={12} /> : <User size={12} />}
                                <span>{msg.role === "system" ? "Orchestrator" : "You"}</span>
                            </div>
                            <p className="whitespace-pre-wrap">{msg.content}</p>
                        </div>
                    </div>
                ))}
                {loading && (
                    <div className="flex justify-start">
                        <div className="max-w-[80%] rounded-2xl p-4 bg-purple-900/20 border border-purple-500/20 text-gray-200">
                            <span className="animate-pulse">Thinking...</span>
                        </div>
                    </div>
                )}
            </div>

            {/* Input */}
            <div className="p-4 border-t border-white/5 bg-black/20 backdrop-blur-lg">
                <div className="flex items-center bg-white/5 rounded-xl border border-white/10 px-4 py-3 focus-within:border-purple-500/50 transition-colors">
                    <button className="text-gray-400 hover:text-white mr-4">
                        <Paperclip size={20} />
                    </button>
                    <input
                        className="flex-1 bg-transparent border-none outline-none text-white placeholder-gray-500"
                        placeholder="Type a message..."
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) => e.key === "Enter" && sendMessage()}
                    />
                    <button onClick={sendMessage} disabled={loading} className="ml-4 p-2 bg-purple-600 rounded-lg hover:bg-purple-500 text-white transition-colors disabled:opacity-50">
                        <Send size={18} />
                    </button>
                </div>
            </div>
        </div>
    );
}
