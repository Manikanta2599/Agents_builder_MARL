import sys
import os
import unittest
from unittest.mock import MagicMock

# Ensure we can import the package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from anti_gravity_system.orchestrator.orchestrator import OrchestratorAgent
from anti_gravity_system.orchestrator.state_machine import AgentState

class TestEnterpriseArch(unittest.TestCase):
    def setUp(self):
        self.config = {"name": "TestOrch"}
        self.agents_config = [] # Orchestrator creates default workers internally now
        self.agent = OrchestratorAgent(self.config, self.agents_config)
        
        # Mock LLM to avoid API calls AND avoid parsing errors
        self.agent.llm.chat_completion = MagicMock(return_value="APPROVED") # For critic
        # Mock plan generation
        self.agent.llm.generate_structured_response = MagicMock(return_value=[
            {"id": 1, "task": "Mock Research", "worker": "worker_research"}
        ])
        
        # Mock Worker execution to avoid real web search
        self.agent.workers["worker_research"].execute_task = MagicMock(return_value={"output": "Mock Data"})

    def test_lifecycle(self):
        print("\nTesting Orchestrator Lifecycle...")
        result = self.agent.run("Test Request")
        
        # Check State History
        history = self.agent.state_machine.get_history()
        states = [h['to'] for h in history]
        print(f"State Transitions: {states}")
        
        self.assertIn("OBSERVING", states)
        self.assertIn("PLANNING", states)
        self.assertIn("DELEGATING", states)
        self.assertIn("CRITIQUING", states)
        self.assertIn("COMPLETED", states)
        
        # Check MARL Reward
        self.assertIn("marl_reward", result)
        print(f"MARL Reward: {result['marl_reward']}")

if __name__ == "__main__":
    unittest.main()
