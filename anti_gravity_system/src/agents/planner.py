from typing import Dict, Any, List
from .workers import BaseWorker
from ..core.llm_provider import LLMProvider

class PlannerAgent(BaseWorker):
    """
    Specialized Planner Agent responsible for breaking down complex goals 
    into a structured Directed Acyclic Graph (DAG) of tasks.
    """
    def __init__(self, config: Dict[str, Any]):
        # BaseWorker init will handle config, name, role, llm, tools, and system prompt loading
        super().__init__(config)
    
    def execute_task(self, task_description: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Decomposes a goal into a plan.
        Input task: 'Build a game'
        Output: {'response': 'Plan created...', 'plan': [...]}
        """
        goal = task_description
        
        # Use the system prompt loaded by BaseWorker
        system_prompt = self.system_prompt 
        user_prompt = f"Goal: {goal}\n\nCreate a step-by-step execution plan."
        
        response = self.llm.chat_completion([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ])
        
        # In a real implementation, we would parse the JSON plan from the LLM response.
        return {
            "status": "success",
            "output": response,
            "metadata": {
                "goal": goal,
                "strategy": "DAG Decomposition"
            }
        }
