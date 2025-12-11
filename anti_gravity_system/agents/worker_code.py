from typing import Dict, Any
import yaml
import os
from anti_gravity_system.src.core.llm_provider import LLMProvider
from anti_gravity_system.tools.file_io import WriteFileTool, ReadFileTool
import logging

logger = logging.getLogger(__name__)

class CodingWorker:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = config.get('name', 'Worker-Code')
        self.llm = LLMProvider()
        self.writer = WriteFileTool()
        self.reader = ReadFileTool()
        
        prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts', 'workers.yaml')
        try:
            with open(prompt_path, 'r') as f:
                prompts = yaml.safe_load(f)
                self.system_prompt = prompts['workers']['coder']['template']
        except Exception:
            self.system_prompt = "You are a Coding Agent."

    def execute_task(self, task_description: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        logger.info(f"[{self.name}] Coding: {task_description}")
        
        # 1. Generate Code
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Task: {task_description}\nContext: {context}"}
        ]
        response = self.llm.chat_completion(messages)
        
        # 2. Extract code block (Simple parsing)
        code = response
        if "```python" in response:
            code = response.split("```python")[1].split("```")[0].strip()
        elif "```" in response:
            code = response.split("```")[1].split("```")[0].strip()
            
        # 3. Save to file (if requested in task, simplified here)
        # Ideally, the LLM should call a tool. For now, we return the code.
        
        return {
            "status": "success",
            "code_generated": code,
            "explanation": response
        }
