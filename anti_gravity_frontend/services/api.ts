export interface Step {
    step: {
        id: number;
        task: string;
        worker: string;
    };
    result: any;
    review: {
        approved: boolean;
        feedback: string;
    };
}

export interface ChatResponse {
    session_id: string;
    response: string;
    steps: Step[];
}

const API_base = "http://localhost:8000";

export const api = {
    async sendMessage(message: string, sessionId?: string): Promise<ChatResponse> {
        const res = await fetch(`${API_base}/chat/turn`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message, session_id: sessionId }),
        });

        if (!res.ok) {
            throw new Error(`API Error: ${res.statusText}`);
        }

        return res.json();
    }
};
