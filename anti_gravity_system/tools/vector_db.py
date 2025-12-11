from .base import BaseTool, ToolResult
from typing import Dict, Any, List
import chromadb
from chromadb.config import Settings
import logging

logger = logging.getLogger(__name__)

class VectorDBTool(BaseTool):
    name = "vector_db_search"
    description = "Searching vector embeddings in ChromaDB"

    def __init__(self, collection_name: str = "antigravity_memory"):
        # Use persistent client
        self.client = chromadb.PersistentClient(path="./antigravity_data/chroma")
        self.collection = self.client.get_or_create_collection(name=collection_name)
        
    def execute(self, query: str, n_results: int = 3) -> ToolResult:
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            return ToolResult(
                status="success",
                output=str(results['documents'][0]) if results['documents'] else "No results found."
            )
        except Exception as e:
            return ToolResult(status="error", output="", error=str(e))

    def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]] = None, ids: List[str] = None):
        """Helper to add documents (not a tool execution per se, but utility)"""
        try:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
        except Exception as e:
            logger.error(f"Failed to add docs: {e}")

    def get_json_schema(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Embedding search query"},
                        "n_results": {"type": "integer", "default": 3}
                    },
                    "required": ["query"]
                }
            }
        }
