from typing import Dict, Any, List
import yaml
import os
from anti_gravity_system.src.core.llm_provider import LLMProvider
from anti_gravity_system.src.core.safety_layer import SafetyLayer
import logging

logger = logging.getLogger(__name__)

class CriticSafetyAgent:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = config.get('name', 'Critic-Safety')
        self.llm = LLMProvider()
        self.safety_layer = SafetyLayer()
        
        prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts', 'critic.yaml')
        try:
            with open(prompt_path, 'r') as f:
                # Assuming critic.yaml is top level or has 'template' key
                # My previous write was top level keys: name, description, template
                prompts = yaml.safe_load(f)
                self.system_prompt = prompts.get('template', "You are a Critic.")
        except Exception:
            self.system_prompt = "You are a Critic."

    def review_task(self, task_description: str, agent_output: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"[{self.name}] Reviewing output for: {task_description}")
        
        output_str = str(agent_output.get("output") or agent_output.get("code_generated") or agent_output)
        
        # 1. Hard Safety Check
        if not self.safety_layer.validate_output(output_str):
            return {
                "status": "success",
                "approved": False,
                "feedback": "Safety Violation: Output content unsafe.",
                "reward_signal": -1.0 # MARL penalty
            }

        # 2. LLM Critique
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Task: {task_description}\nOutput: {output_str}\n\nReview for correctness."}
        ]
        scan_result = self.llm.chat_completion(messages)
        
        is_approved = "APPROVED" in scan_result
        
        # 3. Reward Signal Calculation (Simple Heuristic for MARL)
        reward = 1.0 if is_approved else -0.5
        
        return {
            "status": "success",
            "approved": is_approved,
            "feedback": scan_result,
            "reward_signal": reward
        }
