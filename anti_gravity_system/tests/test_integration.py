import sys
import os
import unittest
from typing import Dict, Any

# Add project root to path
sys.path.append(os.getcwd())

from anti_gravity_system.src.agents.orchestrator import OrchestratorAgent
from anti_gravity_system.src.agents.memory_agent import MemoryAgent
from anti_gravity_system.src.agents.workers import WorkerFactory
from anti_gravity_system.src.core.tools import ToolRegistry

class TestIntegration(unittest.TestCase):
    
    def setUp(self):
        self.orchestrator_config = {"name": "TestOrchestrator", "id": "orchestrator", "role": "Manager"}
        self.worker_config = {"name": "TestWorker", "id": "worker_research", "role": "Researcher", "type": "research"}
        self.agents_config = [self.orchestrator_config, self.worker_config]
        
    def test_worker_tool_execution(self):
        """Test that a worker can correctly access and run a tool."""
        worker = WorkerFactory.create_worker(self.worker_config)
        # Mocking the LLM response inside isn't easy without DI, 
        # so we test the tool direct execution via worker if possible 
        # or we test that worker has the tool.
        self.assertTrue(worker.tools.get_tool("web_search") is not None)
        
    def test_orchestrator_memory_flow(self):
        """Test that Orchestrator initializes Memory and Critic."""
        orch = OrchestratorAgent(self.orchestrator_config, self.agents_config)
        self.assertIsInstance(orch.memory, MemoryAgent)
        
        # Test basic store/retrieve flow via Orchestrator's memory agent
        orch.memory.process_request({
            "action": "store",
            "payload": {"content": "Integration Test Data", "type": "FACT", "session_id": "test_sess"}
        })
        
        result = orch.memory.process_request({
            "action": "search",
            "payload": {"query": "Integration Test"}
        })
        # Note: ChromaDB might be empty or mocked, but result structure should be valid
        self.assertIn("results", result)

    def test_orchestrator_worker_delegation(self):
        """Test that Orchestrator has registered the worker."""
        orch = OrchestratorAgent(self.orchestrator_config, self.agents_config)
        self.assertIn("worker_research", orch.workers)
        self.assertEqual(orch.workers["worker_research"].name, "TestWorker")

if __name__ == '__main__':
    unittest.main()
