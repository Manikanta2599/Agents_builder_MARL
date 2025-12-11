import os
from .base import BaseTool, ToolResult
from typing import Dict, Any

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
    
    def get_json_schema(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Absolute path to file"}
                    },
                    "required": ["path"]
                }
            }
        }

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

    def get_json_schema(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Absolute path to file"},
                        "content": {"type": "string", "description": "Content to write"}
                    },
                    "required": ["path", "content"]
                }
            }
        }
