from typing import Dict, Any
import yaml
import os
from anti_gravity_system.src.core.llm_provider import LLMProvider
from anti_gravity_system.tools.web_search import WebSearchTool
import logging

logger = logging.getLogger(__name__)

class ResearchWorker:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = config.get('name', 'Worker-Research')
        self.llm = LLMProvider()
        self.search_tool = WebSearchTool()
        
        # Load prompt from YAML
        prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts', 'workers.yaml')
        try:
            with open(prompt_path, 'r') as f:
                prompts = yaml.safe_load(f)
                self.system_prompt = prompts['workers']['researcher']['template']
        except Exception:
            self.system_prompt = "You are a Research Agent."

    def execute_task(self, task_description: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        logger.info(f"[{self.name}] Researching: {task_description}")
        
        # 1. Search
        search_result = self.search_tool.execute(query=task_description)
        
        # 2. Synthesize
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Task: {task_description}\nSearch Results: {search_result.output}\n\nProvide a summary."}
        ]
        summary = self.llm.chat_completion(messages)
        
        return {
            "status": "success",
            "output": summary,
            "tool_used": "web_search",
            "raw_data": search_result.output
        }
