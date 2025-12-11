from fastapi import FastAPI, HTTPException, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import sys
import os
import yaml
import time
from prometheus_client import make_asgi_app, Counter, Histogram

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from anti_gravity_system.src.agents.orchestrator import OrchestratorAgent
from anti_gravity_system.src.utils.logger import logger

app = FastAPI(title="Anti-Gravity API", version="1.0.0")

# --- Prometheus Metrics ---
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

REQUEST_COUNT = Counter("agent_requests_total", "Total requests to agents", ["status"])
REQUEST_LATENCY = Histogram("agent_request_latency_seconds", "Request latency")
TOKEN_USAGE = Counter("llm_token_usage_total", "Total LLM tokens used", ["model"])

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Dependencies ---

def load_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'agents.yaml')
    if not os.path.exists(config_path):
        # Fallback for docker if volume not mounted yet
        return {"agents": []}
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def get_orchestrator():
    # In a real app, use @lru_cache or a singleton pattern
    config = load_config()
    agents_conf = config.get('agents', [])
    orch_conf = next((a for a in agents_conf if a['id'] == 'orchestrator'), {})
    return OrchestratorAgent(orch_conf, agents_conf)

# --- Models ---

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    user_id: Optional[str] = "default_user"

class ChatResponse(BaseModel):
    session_id: str
    response: str
    steps: List[Dict[str, Any]]

class AgentRunRequest(BaseModel):
    task: str
    context: Dict[str, Any] = {}

# --- Routes ---

@app.get("/health")
async def health_check():
    return {"status": "ok", "system": "Anti-Gravity"}

@app.post("/chat/turn", response_model=ChatResponse)
async def chat_turn(req: ChatRequest, orchestrator: OrchestratorAgent = Depends(get_orchestrator)):
    logger.info(f"API Request: {req.message}")
    start_time = time.time()
    try:
        # Run Orchestrator
        result = orchestrator.run(req.message)
        
        duration = time.time() - start_time
        REQUEST_LATENCY.observe(duration)
        REQUEST_COUNT.labels(status="success").inc()
        
        # Track metrics from the result if available
        if "metrics" in result:
             # Basic usage tracking from metrics dict
             pass

        return ChatResponse(
            session_id=result.get("session_id"),
            response=result.get("final_response", ""),
            steps=result.get("steps", [])
        )
    except Exception as e:
        logger.error(f"API Error: {e}")
        REQUEST_COUNT.labels(status="error").inc()
        raise HTTPException(status_code=500, detail=str(e))

from anti_gravity_system.src.core.security import get_current_user, require_role

@app.post("/agent/{agent_id}/run", dependencies=[Depends(require_role("admin"))])
async def run_agent(agent_id: str, req: AgentRunRequest, orchestrator: OrchestratorAgent = Depends(get_orchestrator)):
    # Direct agent access
    worker = orchestrator.workers.get(agent_id)
    if not worker:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
    
    try:
        result = worker.execute_task(req.task, req.context)
        return {"status": "success", "agent": agent_id, "output": result}
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
