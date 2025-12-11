import os
import subprocess
import json
from typing import Dict, Any, List, Optional, Callable
from pydantic import BaseModel, Field
from anti_gravity_system.src.utils.logger import logger

class ToolResult(BaseModel):
    status: str
    output: str
    error: Optional[str] = None

class BaseTool:
    name: str = "base_tool"
    description: str = "Base tool"
    
    def execute(self, **kwargs) -> ToolResult:
        raise NotImplementedError

    def get_json_schema(self) -> Dict[str, Any]:
        """
        Returns the OpenAI-compatible JSON schema for this tool.
        """
        # Simplistic default schema generation (in real world use pydantic inspection)
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {} # Override in subclasses for real params
                }
            }
        }

class ReadFileTool(BaseTool):
    name = "read_file"
    description = "Reads content from a file"
    
    def execute(self, path: str) -> ToolResult:
        try:
            if not os.path.exists(path):
                return ToolResult(status="error", output="", error=f"File not found: {path}")
            with open(path, 'r') as f:
                content = f.read()
            return ToolResult(status="success", output=content)
        except Exception as e:
            return ToolResult(status="error", output="", error=str(e))

class WriteFileTool(BaseTool):
    name = "write_file"
    description = "Writes content to a file"
    
    def execute(self, path: str, content: str) -> ToolResult:
        try:
            dir_name = os.path.dirname(path)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
            with open(path, 'w') as f:
                f.write(content)
            return ToolResult(status="success", output=f"Successfully wrote to {path}")
        except Exception as e:
            return ToolResult(status="error", output="", error=str(e))

class CodeExecutionTool(BaseTool):
    name = "code_execute"
    description = "Executes Python code"
    
    def execute(self, code: str, language: str = "python") -> ToolResult:
        if language != "python":
            return ToolResult(status="error", output="", error="Only python is supported currently")
        
        try:
            # SAFETY WARNING: In a real system, use docker/nsjail
            result = subprocess.run(
                [sys.executable, "-c", code],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return ToolResult(status="success", output=result.stdout)
            else:
                return ToolResult(status="error", output=result.stdout, error=result.stderr)
        except subprocess.TimeoutExpired:
            return ToolResult(status="error", output="", error="Execution timed out")
        except Exception as e:
            return ToolResult(status="error", output="", error=str(e))

class WebSearchTool(BaseTool):
    name = "web_search"
    description = "Performs a web search"

    def execute(self, query: str) -> ToolResult:
        # Placeholder for real Google Search API
        logger.warning(f"Mocking search for: {query}")
        return ToolResult(
            status="success", 
            output=f"Mock search results for '{query}':\n1. {query} - Documentation\n2. How to use {query}"
        )

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}
        self._register_defaults()

    def _register_defaults(self):
        self.register(ReadFileTool())
        self.register(WriteFileTool())
        self.register(CodeExecutionTool())
        self.register(WebSearchTool())

    def register(self, tool: BaseTool):
        self.tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name}")

    def get_tool(self, name: str) -> Optional[BaseTool]:
        return self.tools.get(name)
    
    def list_tools(self) -> List[Dict[str, str]]:
        return [{"name": t.name, "description": t.description} for t in self.tools.values()]

import sys
