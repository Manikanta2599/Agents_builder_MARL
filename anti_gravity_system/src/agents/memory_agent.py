from typing import Dict, Any, List
from anti_gravity_system.src.core.memory_store import MemoryStore
from anti_gravity_system.src.utils.logger import logger

class MemoryAgent:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.store = MemoryStore(persist_dir="./antigravity_data/memory")
        logger.info(f"Memory Agent initialized with role: {config.get('role')}")

    def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handles requests to store or retrieve memory.
        Request schema:
        {
            "action": "store" | "search" | "get_history",
            "payload": { ... }
        }
        """
        action = request.get("action")
        payload = request.get("payload", {})

        try:
            if action == "store":
                return self._handle_store(payload)
            elif action == "search":
                return self._handle_search(payload)
            elif action == "get_history":
                return self._handle_history(payload)
            else:
                return {"status": "error", "message": f"Unknown action: {action}"}
        except Exception as e:
            logger.error(f"Memory Agent Error: {e}")
            return {"status": "error", "message": str(e)}

    def _handle_store(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        content = payload.get("content")
        type_ = payload.get("type", "FACT")
        session_id = payload.get("session_id", "default_session")
        metadata = payload.get("metadata", {})

        if not content:
            raise ValueError("Content is required for storage")

        memory_id = self.store.add_memory(content, type_, session_id, metadata)
        return {"status": "success", "memory_id": memory_id}

    def _handle_search(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        query = payload.get("query")
        type_filter = payload.get("type_filter")
        limit = payload.get("limit", 5)

        if not query:
            raise ValueError("Query is required for search")

        results = self.store.search_memory(query, type_filter, limit)
        return {"status": "success", "results": results}

    def _handle_history(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        session_id = payload.get("session_id")
        if not session_id:
            raise ValueError("session_id is required for history")
            
        history = self.store.get_session_history(session_id)
        return {"status": "success", "history": history}
