from typing import Dict, Any, List
from anti_gravity_system.src.core.llm_provider import LLMProvider
from anti_gravity_system.src.utils.logger import logger
from anti_gravity_system.src.utils.prompt_loader import load_system_prompts

class CriticAgent:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = config.get('name', 'Critic')
        self.llm = LLMProvider()
        
        prompts = load_system_prompts()
        self.system_prompt = prompts.get("Critic", "You are a Critic.")
        
        logger.info(f"Critic initialized: {self.name}")

    def review_task(self, task_description: str, agent_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Reviews the output of another agent.
        """
        logger.info(f"[{self.name}] Reviewing output for: {task_description}")
        
        output_content = agent_output.get("output") or agent_output.get("code_generated") or str(agent_output)
        
        # In mock mode, we just pass unless we see 'error'
        if "Combined" in str(output_content) or "mock" in str(output_content).lower():
             # Basic heuristics for mock mode checks
             pass

        prompt = (
            f"Task: {task_description}\n"
            f"Agent Output: {output_content}\n"
            "Review this output for safety, correctness, and completeness. "
            "Reply with 'APPROVED' or 'REJECTED: <reason>'."
        )

        review_response = self.llm.chat_completion([
             {"role": "system", "content": "You are a harsh but fair critic. Safety is paramount."},
             {"role": "user", "content": prompt}
        ])

        # Mock override for testing if LLM is mocked
        if self.llm.mock_mode:
            if "fail" in task_description.lower(): 
                review_response = "REJECTED: simulated failure for testing"
            else:
                review_response = "APPROVED"

        is_approved = "APPROVED" in review_response
        
        return {
            "status": "success",
            "approved": is_approved,
            "feedback": review_response
        }
