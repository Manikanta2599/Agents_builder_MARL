import sys
import os
import unittest

sys.path.append(os.getcwd())

from anti_gravity_system.src.core.tools import ToolRegistry

class TestToolRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = ToolRegistry()
    
    def test_list_tools(self):
        tools = self.registry.list_tools()
        names = [t['name'] for t in tools]
        self.assertIn("read_file", names)
        self.assertIn("write_file", names)
        
    def test_file_io(self):
        test_file = "test_artifact_unit.txt"
        
        # Write
        res = self.registry.get_tool("write_file").execute(path=test_file, content="Test Content")
        self.assertEqual(res.status, "success")
        
        # Read
        res = self.registry.get_tool("read_file").execute(path=test_file)
        self.assertEqual(res.status, "success")
        self.assertEqual(res.output, "Test Content")
        
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)
            
    def test_code_execution(self):
        code = "print('Hello')"
        res = self.registry.get_tool("code_execute").execute(code=code)
        self.assertEqual(res.status, "success")
        self.assertIn("Hello", res.output)

if __name__ == "__main__":
    unittest.main()
