from fastapi import FastAPI, HTTPException, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import sys
import os
import yaml

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from anti_gravity_system.src.agents.orchestrator import OrchestratorAgent
from anti_gravity_system.src.utils.logger import logger

app = FastAPI(title="Anti-Gravity API", version="1.0.0")

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
    try:
        # Run Orchestrator
        result = orchestrator.run(req.message)
        
        return ChatResponse(
            session_id=result.get("session_id"),
            response=result.get("final_response", ""),
            steps=result.get("steps", [])
        )
    except Exception as e:
        logger.error(f"API Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/agent/{agent_id}/run")
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
