import sys
import os
import unittest

sys.path.append(os.getcwd())

from anti_gravity_system.src.agents.critic import CriticAgent

class TestCritic(unittest.TestCase):
    def test_critic_review(self):
        critic = CriticAgent({"name": "TestCritic"})
        res = critic.review_task("Do something", {"status": "ok"})
        self.assertIn("approved", res)

if __name__ == "__main__":
    unittest.main()
