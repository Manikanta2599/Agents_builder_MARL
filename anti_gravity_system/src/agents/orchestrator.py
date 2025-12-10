from typing import Dict, Any, List
import uuid
import json
from anti_gravity_system.src.core.llm_provider import LLMProvider
from anti_gravity_system.src.agents.workers import WorkerFactory
from anti_gravity_system.src.agents.critic import CriticAgent
from anti_gravity_system.src.agents.memory_agent import MemoryAgent
from anti_gravity_system.src.utils.logger import logger
from anti_gravity_system.src.utils.prompt_loader import load_system_prompts

class OrchestratorAgent:
    def __init__(self, config: Dict[str, Any], agents_config: List[Dict[str, Any]]):
        self.config = config
        self.name = config.get('name', "Orchestrator")
        self.llm = LLMProvider()
        
        # Load System Prompt
        prompts = load_system_prompts()
        self.system_prompt = prompts.get("Orchestrator", "You are the Orchestrator.")
        logger.info(f"Orchestrator loaded system prompt: {len(self.system_prompt)} chars")
        
        # Initialize Sub-Agents
        self.memory = MemoryAgent({"role": "Memory", "name": "MemoryCore"})
        self.critic = CriticAgent({"role": "Critic", "name": "SystemCritic"})
        
        # Initialize Workers from config
        self.workers = {}
        for agent_conf in agents_config:
            if "worker" in agent_conf['id']:
                 worker = WorkerFactory.create_worker(agent_conf)
                 self.workers[agent_conf['id']] = worker

        logger.info(f"Orchestrator initialized with {len(self.workers)} workers.")

    def run(self, user_request: str) -> Dict[str, Any]:
        session_id = str(uuid.uuid4())
        logger.info(f"Starting Session {session_id} for request: {user_request}")
        
        # 1. Observe: Store & Recall
        self.memory.process_request({
            "action": "store",
            "payload": {
                "content": user_request, "type": "USER_REQUEST", "session_id": session_id
            }
        })
        context = self.memory.process_request({
             "action": "search",
             "payload": {"query": user_request}
        })

        # 2. Think & Plan
        plan = self._generate_plan(user_request, context)
        logger.info(f"Generated Plan: {len(plan)} steps")

        results = []
        
        # 3. Execution Loop
        for step in plan:
            if not self._execute_step(step, session_id, results):
                # If a step critically fails (and critic can't fix), we stop
                logger.error(f"Stopping execution due to failure in step: {step['task']}")
                break
                
        # 4. Synthesize Final Response
        final_response = self._synthesize_response(user_request, results)

        return {
            "session_id": session_id,
            "status": "completed",
            "final_response": final_response,
            "steps": results
        }

    def _generate_plan(self, request: str, context: Any) -> List[Dict[str, Any]]:
        """
        Generates a DAG plan using the LLM.
        """
        logger.info("Thinking and Planning...")
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Plan this request: '{request}'. Context: {context}"}
        ]
        
        # Helper schema for the LLM to follow
        schema = "List[{\"id\": int, \"task\": str, \"worker\": str (worker_research|worker_coder|worker_data)}]"
        
        plan = self.llm.generate_structured_response(messages, schema)
        
        # Fallback for mock mode if structured response fails or returns empty
        if not plan and self.llm.mock_mode:
            return self._mock_plan(request)
            
        return plan if isinstance(plan, list) else []

    def _execute_step(self, step: Dict[str, Any], session_id: str, results_accumulator: List[Any]) -> bool:
        """
        Executes a single step with Critic Loop. Returns True if successful.
        """
        worker_id = step.get('worker') or step.get('worker_id')
        task = step['task']
        
        worker = self.workers.get(worker_id)
        if not worker:
            logger.error(f"Worker {worker_id} not found! Defaulting to Research.")
            worker = self.workers.get("worker_research")

        # Retry Loop (Critics)
        max_retries = 2
        for attempt in range(max_retries + 1):
            logger.info(f"delegating to {worker.name}: {task} (Attempt {attempt+1})")
            
            # Execute
            work_result = worker.execute_task(task)
            
            # Evaluate
            review = self.critic.review_task(task, work_result)
            
            if review['approved']:
                # Success
                self._store_result(session_id, task, work_result)
                results_accumulator.append({"step": step, "result": work_result, "review": review})
                return True
            else:
                # Failure -> Improve
                logger.warning(f"Critic Rejected: {review.get('feedback')}")
                # Update task with feedback for next iteration
                task = f"Fix previous error: {review.get('feedback')}. Original Task: {task}"
                
        return False
        
    def _store_result(self, session_id, task, result):
        self.memory.process_request({
            "action": "store", 
            "payload": {
                "content": str(result), 
                "type": "TASK_RESULT", 
                "session_id": session_id,
                "metadata": {"task": task}
            }
        })

    def _synthesize_response(self, request: str, results: List[Any]) -> str:
        messages = [
            {"role": "system", "content": "Synthesize a helpful answer from the tool outputs."},
            {"role": "user", "content": f"Request: {request}. Tool Outputs: {results}"}
        ]
        return self.llm.chat_completion(messages)

    def _mock_plan(self, request: str) -> List[Dict[str, str]]:
        # Fallback heuristic
        plan = []
        req_lower = request.lower()
        if "research" in req_lower or "find" in req_lower:
             plan.append({"id": 1, "task": request, "worker": "worker_research"})
        if "code" in req_lower or "script" in req_lower:
             plan.append({"id": 2, "task": f"Write code for {request}", "worker": "worker_coder"})
        if not plan:
             plan.append({"id": 1, "task": request, "worker": "worker_research"})
        return plan
