import os
from typing import List, Dict, Any, Optional
import json
import re
from openai import OpenAI
from anti_gravity_system.src.utils.logger import logger

class LLMProvider:
    def __init__(self, model: str = "gpt-4-turbo-preview"):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "sk-mock-key"))
        self.model = model
        self.mock_mode = os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "sk-mock-key"
        if self.mock_mode:
            logger.warning("OPENAI_API_KEY not found. Running in MOCK MODE.")

    def chat_completion(self, messages: List[Dict[str, str]], tools: Optional[List[Dict[str, Any]]] = None) -> str:
        if self.mock_mode:
            return self._mock_response(messages)
        
        try:
            # Basic implementation - in production would handle tools properly
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"LLM Error: {e}")
            return f"Error generating response: {e}"

    def generate_structured_response(self, messages: List[Dict[str, str]], schema_description: str) -> Dict[str, Any]:
        """
        Forces the LLM to return JSON matching the schema.
        """
        messages.append({
            "role": "system", 
            "content": f"You must respond with valid JSON matching this schema: {schema_description}"
        })
        
        raw_content = self.chat_completion(messages)
        return self._parse_json(raw_content)

    def _parse_json(self, content: str) -> Dict[str, Any]:
        try:
            # clean code blocks
            content = re.sub(r'```json\s*', '', content)
            content = re.sub(r'```', '', content)
            return json.loads(content)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON from LLM: {content}")
            return {}

    def _mock_response(self, messages: List[Dict[str, str]]) -> str:
        last_msg = messages[-1]['content'].lower()
        
        # Mocking generic plan request
        if "plan" in last_msg or "step" in last_msg:
             return json.dumps([
                 {"id": 1, "task": "Research the request", "worker": "worker_research"},
                 {"id": 2, "task": "Write python code", "worker": "worker_coder"}
             ])
             
        if "python" in last_msg:
            return "```python\nprint('Generated Code')\n```"
            
        return "I am a mock LLM response. Please provide a valid API key for real inference."

