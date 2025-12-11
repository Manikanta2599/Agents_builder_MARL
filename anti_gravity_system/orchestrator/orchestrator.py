from typing import Dict, Any, List
import uuid
from uuid import uuid4
import yaml
import os
import logging
from anti_gravity_system.src.core.llm_provider import LLMProvider
from anti_gravity_system.orchestrator.state_machine import OrchestratorStateMachine, AgentState

# New Agents
from anti_gravity_system.agents.worker_research import ResearchWorker
from anti_gravity_system.agents.worker_code import CodingWorker
from anti_gravity_system.agents.critic_safety import CriticSafetyAgent
from anti_gravity_system.agents.memory_agent import MemoryAgent

# Tools (Metric, Logger) - importing legacy for now
from anti_gravity_system.src.core.metrics import MetricsTracker

logger = logging.getLogger(__name__)

class OrchestratorAgent:
    def __init__(self, config: Dict[str, Any], agents_config: List[Dict[str, Any]]):
        self.config = config
        self.name = config.get('name', "Orchestrator")
        self.state_machine = OrchestratorStateMachine()
        self.llm = LLMProvider()
        self.metrics = MetricsTracker()
        
        # Load Prompt
        prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts', 'orchestrator.yaml')
        try:
            with open(prompt_path, 'r') as f:
                prompts = yaml.safe_load(f)
                self.system_prompt = prompts.get('template', "You are the Orchestrator.")
        except Exception:
            self.system_prompt = "You are the Orchestrator."

        # Initialize Sub-Agents
        self.memory = MemoryAgent({"role": "Memory", "name": "MemoryCore"})
        self.critic = CriticSafetyAgent({"role": "Critic", "name": "SystemCritic"})
        
        # Initialize Workers
        self.workers = {}
        # Simple factory simulation
        self.workers["worker_research"] = ResearchWorker({"name": "Researcher"})
        self.workers["worker_code"] = CodingWorker({"name": "Coder"})
        
        logger.info("Orchestrator 2.0 Initialized with Enterprise Architecture.")

    def run(self, user_request: str) -> Dict[str, Any]:
        session_id = str(uuid4())
        logger.info(f"Starting Session {session_id}")
        self.state_machine.transition(AgentState.OBSERVING, {"request": user_request})

        # 1. Observe
        context = self.memory.process_request({
            "action": "search",
            "payload": {"query": user_request}
        })
        
        # 2. Think & Plan
        self.state_machine.transition(AgentState.PLANNING)
        plan = self._plan(user_request, context)
        
        self.state_machine.transition(AgentState.DELEGATING, {"plan_size": len(plan)})
        
        results = []
        cumulative_reward = 0.0
        
        # 3. Execution Loop
        for step in plan:
            # Delegate
            worker_id = step.get('worker')
            # Default mapping logic
            if "research" in worker_id:
                worker = self.workers["worker_research"]
            elif "code" in worker_id:
                worker = self.workers["worker_code"]
            else:
                worker = self.workers["worker_research"] # Fallback

            result = worker.execute_task(step['task'])
            
            # Critique
            self.state_machine.transition(AgentState.CRITIQUING)
            review = self.critic.review_task(step['task'], result)
            
            # MARL Hook: Update policy based on reward (Stub)
            reward = review.get("reward_signal", 0.0)
            cumulative_reward += reward
            self._update_policy(step, reward)
            
            if not review['approved']:
                logger.warning(f"Step Rejected. Reward: {reward}")
                # Simple retry logic could go here
            else:
                # Store successful result
                self.memory.process_request({
                    "action": "store",
                    "payload": {"content": str(result), "session_id": session_id}
                })
                
            results.append({"step": step, "result": result, "review": review})
            self.state_machine.transition(AgentState.DELEGATING) # Back to delegating loop

        # Final Response
        final_response = self._synthesize(user_request, results)
        
        self.state_machine.transition(AgentState.COMPLETED)
        
        return {
            "session_id": session_id,
            "status": "completed",
            "final_response": final_response,
            "marl_reward": cumulative_reward,
            "state_history": [str(h) for h in self.state_machine.get_history()]
        }

    def _plan(self, request: str, context: Any) -> List[Dict[str, Any]]:
        # Using LLM to generate plan based on loaded template
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Plan for: {request}. Context: {context}"}
        ]
        schema = "List[{\"id\": int, \"task\": str, \"worker\": str}]"
        plan = self.llm.generate_structured_response(messages, schema)
        
        if not plan: # Fallback
            return [{"id": 1, "task": request, "worker": "worker_research"}]
        return plan if isinstance(plan, list) else []

    def _synthesize(self, request, results):
        return self.llm.chat_completion([
            {"role": "system", "content": "Summarize the results."},
            {"role": "user", "content": str(results)}
        ])

    def _update_policy(self, step, reward):
        # Placeholder for MARL Q-Learning or Policy Gradient update
        # In a real system, we would update the weight of 'worker' for 'task type'
        logger.info(f"MARL Update: Task '{step['task']}' -> Reward {reward}")
