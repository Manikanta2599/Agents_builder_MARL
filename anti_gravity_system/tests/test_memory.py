import sys
import os
import unittest

sys.path.append(os.getcwd())

from anti_gravity_system.src.agents.memory_agent import MemoryAgent

class TestMemoryAgent(unittest.TestCase):
    def test_memory_flow(self):
        agent = MemoryAgent({"name": "TestMem", "role": "Memory"})
        
        # Store
        res = agent.process_request({
            "action": "store",
            "payload": {"content": "Test Memory", "type": "TEST", "session_id": "test_mem"}
        })
        self.assertEqual(res["status"], "success")
        
        # Search
        res = agent.process_request({
            "action": "search",
            "payload": {"query": "Test"}
        })
        self.assertIn("results", res)

if __name__ == "__main__":
    unittest.main()
