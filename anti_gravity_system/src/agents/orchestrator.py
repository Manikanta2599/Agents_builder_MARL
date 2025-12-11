from typing import Dict, Any, List
import uuid
import json
from anti_gravity_system.src.core.llm_provider import LLMProvider
from anti_gravity_system.src.agents.workers import WorkerFactory
from anti_gravity_system.src.agents.critic import CriticAgent
from anti_gravity_system.src.agents.memory_agent import MemoryAgent
from anti_gravity_system.src.utils.logger import logger
from anti_gravity_system.src.utils.prompt_loader import load_system_prompts

# New Core Modules
from anti_gravity_system.src.core.metrics import MetricsTracker
from anti_gravity_system.src.core.safety_layer import SafetyLayer

class OrchestratorAgent:
    def __init__(self, config: Dict[str, Any], agents_config: List[Dict[str, Any]]):
        self.config = config
        self.name = config.get('name', "Orchestrator")
        self.llm = LLMProvider()
        
        # Load System Prompt
        prompts = load_system_prompts()
        self.system_prompt = prompts.get("Orchestrator", "You are the Orchestrator.")
        logger.info(f"Orchestrator loaded system prompt: {len(self.system_prompt)} chars")
        
        # Initialize Components
        self.memory = MemoryAgent({"role": "Memory", "name": "MemoryCore"})
        self.critic = CriticAgent({"role": "Critic", "name": "SystemCritic"})
        self.metrics = MetricsTracker()
        self.safety = SafetyLayer()
        
        # Initialize Workers from config
        self.workers = {}
        for agent_conf in agents_config:
            if "worker" in agent_conf['id']:
                 worker = WorkerFactory.create_worker(agent_conf)
                 self.workers[agent_conf['id']] = worker

        logger.info(f"Orchestrator initialized with {len(self.workers)} workers.")

    def run(self, user_request: str) -> Dict[str, Any]:
        """
        Main Agent Loop: Observe -> Think -> Plan -> Act -> Evaluate -> Improve
        """
        session_id = str(uuid.uuid4())
        logger.info(f"Starting Session {session_id}")
        self.metrics.start_timer("total_session_time")

        # 0. Safety Check (Input)
        if not self.safety.validate_input(user_request):
            return {"status": "rejected", "error": "Safety violation in input."}

        # 1. Observe
        context = self._observe(user_request, session_id)
        
        # 2. Think
        analysis = self._think(user_request, context)
        
        # 3. Plan
        plan = self._plan(user_request, analysis)
        self.metrics.record_metric("plan_steps", len(plan), "count")
        
        results = []
        
        # 4. Act Loop
        for step in plan:
            # 5. Act
            result = self._act(step, session_id)
            
            # 6. Evaluate
            review = self._evaluate(step, result)
            
            if not review['approved']:
                # 7. Improve (Simple Retry Logic for MVP)
                logger.warning(f"Step rejected: {review.get('feedback')}. Retrying...")
                self.metrics.record_metric("retry_count", 1, "count")
                step['task'] = f"{step['task']} (Correction: {review.get('feedback')})"
                result = self._act(step, session_id) # Retry once
            
            results.append({"step": step, "result": result})
            
            # Safety Check (Output)
            if not self.safety.validate_output(str(result)):
                 logger.warning("Safety violation in step output. masking.")
                 result = "[REDACTED]"

        # Final Response
        final_response = self._synthesize_response(user_request, results)
        
        self.metrics.stop_timer("total_session_time")
        self.metrics.record_metric("task_completion", 1, "count")

        return {
            "session_id": session_id,
            "status": "completed",
            "final_response": final_response,
            "metrics": self.metrics.get_summary()
        }

    # --- Cognitive Stages ---

    def _observe(self, request: str, session_id: str) -> Dict[str, Any]:
        logger.info("Stage: OBSERVE")
        # Store current request
        self.memory.process_request({
            "action": "store",
            "payload": {"content": request, "type": "USER_REQUEST", "session_id": session_id}
        })
        # Recall relevant context
        context = self.memory.process_request({
             "action": "search",
             "payload": {"query": request}
        })
        return context

    def _think(self, request: str, context: Any) -> str:
        logger.info("Stage: THINK")
        messages = [
            {"role": "system", "content": "Analyze the user's request and context. Identify key intents."},
            {"role": "user", "content": f"Request: {request}. Context: {context}"}
        ]
        return self.llm.chat_completion(messages)

    def _plan(self, request: str, analysis: str) -> List[Dict[str, Any]]:
        logger.info("Stage: PLAN")
        # Use the analysis to guide planning
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Create a step-by-step plan for: {request}\nAnalysis: {analysis}"}
        ]
        schema = "List[{\"id\": int, \"task\": str, \"worker\": str}]"
        plan = self.llm.generate_structured_response(messages, schema)
        
        # Fallback
        if not plan:
            return self._mock_plan(request)
        return plan if isinstance(plan, list) else []

    def _act(self, step: Dict[str, Any], session_id: str) -> Any:
        logger.info(f"Stage: ACT (Task: {step['task']})")
        worker_id = step.get('worker')
        worker = self.workers.get(worker_id) or self.workers.get("worker_research")
        
        self.metrics.start_timer("step_latency")
        result = worker.execute_task(step['task'])
        self.metrics.stop_timer("step_latency")
        
        self._store_result(session_id, step['task'], result)
        return result

    def _evaluate(self, step: Dict[str, Any], result: Any) -> Dict[str, Any]:
        logger.info("Stage: EVALUATE")
        return self.critic.review_task(step['task'], result)

    def _store_result(self, session_id, task, result):
        self.memory.process_request({
            "action": "store", 
            "payload": {
                "content": str(result), 
                "type": "TASK_RESULT", 
                "session_id": session_id
            }
        })

    def _synthesize_response(self, request: str, results: List[Any]) -> str:
        messages = [
            {"role": "system", "content": "Synthesize a helpful answer from the tool outputs."},
            {"role": "user", "content": f"Request: {request}. Tool Outputs: {results}"}
        ]
        return self.llm.chat_completion(messages)

    def _mock_plan(self, request: str) -> List[Dict[str, str]]:
        plan = []
        req_lower = request.lower()
        if "research" in req_lower or "find" in req_lower:
             plan.append({"id": 1, "task": request, "worker": "worker_research"})
        if "code" in req_lower or "script" in req_lower:
             plan.append({"id": 2, "task": f"Write code for {request}", "worker": "worker_coder"})
        if not plan:
             plan.append({"id": 1, "task": request, "worker": "worker_research"})
        return plan
