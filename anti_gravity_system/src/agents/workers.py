from typing import Dict, Any, List
from anti_gravity_system.src.core.llm_provider import LLMProvider
from anti_gravity_system.src.core.tools import ToolRegistry, BaseTool
from anti_gravity_system.src.utils.logger import logger
from anti_gravity_system.src.utils.prompt_loader import load_system_prompts

class BaseWorker:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = config['name']
        self.role = config['role']
        self.llm = LLMProvider()
        self.tools = ToolRegistry()
        
        # Load specific prompt based on ID mapping
        prompts = load_system_prompts()
        # Map config['id'] (e.g. worker_research) to JSON key (e.g. Worker-Research)
        key_map = {
            "worker_research": "Worker-Research",
            "worker_coder": "Worker-Code",
            "worker_data": "Worker-Data"
        }
        json_key = key_map.get(config['id'], "Worker-Research")
        self.system_prompt = prompts.get(json_key, f"You are a {self.role}.")
        
        logger.info(f"Worker initialized: {self.name} ({self.role})")

    def execute_task(self, task_description: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        raise NotImplementedError

class ResearchWorker(BaseWorker):
    def execute_task(self, task_description: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        logger.info(f"[{self.name}] Researching: {task_description}")
        
        # In a real agent, LLM would choose the tool. Here we hardcode for the MVP flow.
        search_tool = self.tools.get_tool("web_search")
        result = search_tool.execute(query=task_description)
        
        # Summarize with LLM (mocked)
        summary = self.llm.chat_completion([
            {"role": "system", "content": "Summarize these search results."},
            {"role": "user", "content": result.output}
        ])
        
        return {"status": "success", "output": summary, "source_tool": "web_search"}

class CodingWorker(BaseWorker):
    def execute_task(self, task_description: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        logger.info(f"[{self.name}] Coding: {task_description}")
        
        # 1. Generate Code using LLM
        prompt = f"Write python code for: {task_description}"
        code_response = self.llm.chat_completion([
            {"role": "system", "content": "You are a coding expert. Output only valid python code."},
            {"role": "user", "content": prompt}
        ])
        
        # Extract code from markdown blocks if present
        code = code_response
        if "```python" in code:
            code = code.split("```python")[1].split("```")[0].strip()
        elif "```" in code:
            code = code.split("```")[1].split("```")[0].strip()

        # 2. Execute Code
        exec_tool = self.tools.get_tool("code_execute")
        exec_result = exec_tool.execute(code=code)
        
        return {
            "status": "success" if exec_result.status == "success" else "failure",
            "code_generated": code,
            "execution_output": exec_result.output,
            "error": exec_result.error
        }

class WorkerFactory:
    @staticmethod
    def create_worker(config: Dict[str, Any]) -> BaseWorker:
        role_map = {
            "worker_research": ResearchWorker,
            "worker_coder": CodingWorker
        }
        # Fallback for unknown workers
        worker_class = role_map.get(config['id'], BaseWorker) # BaseWorker will raise NotImplemented if used
        if worker_class == BaseWorker:
             # Basic generic worker logic if needed, or specific error
             logger.warning(f"Unknown worker type {config['id']}, returning BaseWorker")
             
        return worker_class(config)
