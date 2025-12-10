import unittest
import sys
import os

# Add project root
sys.path.append(os.getcwd())

from anti_gravity_system.tests.test_tools import TestToolRegistry
from anti_gravity_system.tests.test_memory import TestMemoryAgent
from anti_gravity_system.tests.test_workers import TestWorkers
from anti_gravity_system.tests.test_critic import TestCritic
from anti_gravity_system.tests.test_integration import TestIntegration
from anti_gravity_system.tests.test_safety import TestSafety

# Create a test suite
def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all tests
    suite.addTests(loader.loadTestsFromTestCase(TestToolRegistry))
    suite.addTests(loader.loadTestsFromTestCase(TestMemoryAgent))
    suite.addTests(loader.loadTestsFromTestCase(TestWorkers))
    suite.addTests(loader.loadTestsFromTestCase(TestCritic))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestSafety))
    
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
