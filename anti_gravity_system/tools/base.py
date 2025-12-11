from typing import Dict, Any, Optional
from pydantic import BaseModel

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
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        }
