from .base import BaseTool, ToolResult
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class WebSearchTool(BaseTool):
    name = "web_search"
    description = "Performs a web search"

    def execute(self, query: str) -> ToolResult:
        # Placeholder for real Google Search API
        logger.info(f"Mocking search for: {query}")
        return ToolResult(
            status="success", 
            output=f"Mock search results for '{query}':\n1. {query} - Documentation\n2. How to use {query}"
        )

    def get_json_schema(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"}
                    },
                    "required": ["query"]
                }
            }
        }
