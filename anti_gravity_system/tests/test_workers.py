import sys
import os
import unittest

sys.path.append(os.getcwd())

from anti_gravity_system.src.agents.workers import WorkerFactory

class TestWorkers(unittest.TestCase):
    def test_worker_creation(self):
        conf = {"name": "TestCoder", "id": "worker_coder", "role": "Coder", "type": "coding"}
        worker = WorkerFactory.create_worker(conf)
        self.assertEqual(worker.name, "TestCoder")
        
    def test_research_worker_mock(self):
        conf = {"name": "TestResearcher", "id": "worker_research", "role": "Researcher", "type": "research"}
        worker = WorkerFactory.create_worker(conf)
        # Mock execution relies on LLMProvider mock behavior
        res = worker.execute_task("Find info")
        self.assertIsNotNone(res)

if __name__ == "__main__":
    unittest.main()
