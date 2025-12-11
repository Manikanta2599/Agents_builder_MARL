"use client";
import React, { useEffect, useState } from 'react';

export default function MetricsDashboard() {
    const [metrics, setMetrics] = useState({
        reward: 0.0,
        latency: 0.0,
        errors: 0
    });

    // Mock data update or polling
    useEffect(() => {
        const interval = setInterval(() => {
            // In a real app, fetch from /metrics endpoint
            setMetrics(prev => ({
                reward: prev.reward + (Math.random() > 0.5 ? 0.1 : -0.05),
                latency: Math.random() * 2,
                errors: prev.errors
            }));
        }, 5000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="p-4 bg-gray-900 text-white rounded-lg shadow-lg">
            <h2 className="text-xl font-bold mb-4 border-b border-gray-700 pb-2">System Health</h2>
            <div className="grid grid-cols-3 gap-4">
                <div className="bg-gray-800 p-3 rounded">
                    <div className="text-gray-400 text-sm">MARL Reward</div>
                    <div className="text-2xl font-mono text-green-400">{metrics.reward.toFixed(2)}</div>
                </div>
                <div className="bg-gray-800 p-3 rounded">
                    <div className="text-gray-400 text-sm">Latency (s)</div>
                    <div className="text-2xl font-mono text-yellow-400">{metrics.latency.toFixed(2)}</div>
                </div>
                <div className="bg-gray-800 p-3 rounded">
                    <div className="text-gray-400 text-sm">Errors</div>
                    <div className="text-2xl font-mono text-pink-500">{metrics.errors}</div>
                </div>
            </div>
        </div>
    );
}
