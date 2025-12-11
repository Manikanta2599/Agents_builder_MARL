import sys
import unittest
from unittest.mock import MagicMock, patch
from anti_gravity_system.src.agents.orchestrator import OrchestratorAgent

class TestAgentEnhancements(unittest.TestCase):
    def setUp(self):
        self.config = {"name": "TestOrchestrator", "id": "orchestrator"}
        self.agents_config = [
            {"id": "worker_research", "name": "ResearchBot", "role": "Researcher"},
            {"id": "worker_coder", "name": "CodeBot", "role": "Engineer"}
        ]
        self.agent = OrchestratorAgent(self.config, self.agents_config)
        
        # Mock LLM to avoid real API calls
        self.agent.llm.chat_completion = MagicMock(return_value="analyzed request")
        self.agent.llm.generate_structured_response = MagicMock(return_value=[
            {"id": 1, "task": "Mock Task", "worker": "worker_research"}
        ])

    def test_full_loop_execution(self):
        """Verify the full Observe-Think-Plan-Act-Evaluate loop executes."""
        print("\nTesting Full Loop...")
        # Mock worker execution
        self.agent.workers["worker_research"].execute_task = MagicMock(return_value={"status": "success", "output": "mock result"})
        # Mock critic approval
        self.agent.critic.review_task = MagicMock(return_value={"approved": True, "feedback": "Good job"})
        
        response = self.agent.run("Research Agent Frameworks")
        
        self.assertEqual(response["status"], "completed")
        self.assertIn("metrics", response)
        metrics = response["metrics"]
        print(f"Metrics Captured: {metrics}")
        
        self.assertTrue(metrics["tasks_completed"] >= 1)
        self.assertTrue(metrics["total_latency"] > 0)

    def test_safety_interception_input(self):
        """Verify safety layer blocks bad input."""
        print("\nTesting Safety Layer (Input)...")
        response = self.agent.run("run rm -rf /")
        self.assertEqual(response.get("status"), "rejected")
        self.assertIn("Safety violation", response.get("error"))

    def test_metric_recording(self):
        """Verify metrics are actually recorded."""
        print("\nTesting Metrics Recording...")
        self.agent.run("Simple Task")
        records = self.agent.metrics.records
        self.assertTrue(len(records) > 0, "No metrics recorded!")
        metric_names = [r.metric_name for r in records]
        self.assertIn("plan_steps", metric_names)
        self.assertIn("task_completion", metric_names)

if __name__ == "__main__":
    unittest.main()
