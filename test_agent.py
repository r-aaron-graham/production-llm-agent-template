import unittest
import subprocess
import sys
from pathlib import Path
from agent import execute


class ToolGatewayTests(unittest.TestCase):
    def test_lookup_and_source(self):
        result = execute({"tool": "lookup", "arguments": {"topic": "setup"}}, {"lookup"})
        self.assertEqual(result["status"], "answered")
        self.assertEqual(result["source"], "setup")

    def test_permission_denied(self):
        with self.assertRaises(ValueError):
            execute({"tool": "lookup", "arguments": {"topic": "setup"}}, set())

    def test_unknown_tool(self):
        with self.assertRaises(ValueError):
            execute({"tool": "shell", "arguments": {"topic": "setup"}}, {"shell"})

    def test_invalid_shapes(self):
        for proposal in (None, [], {}, {"tool": [], "arguments": {}},
                         {"tool": "lookup", "arguments": {"topic": 5}},
                         {"tool": "lookup", "arguments": {"topic": "x", "extra": 1}}):
            with self.subTest(proposal=proposal), self.assertRaises(ValueError):
                execute(proposal, {"lookup"})

    def test_cli_rejects_invalid_json(self):
        script = str(Path(__file__).with_name("agent.py"))
        for proposal in ("{", "[" * 2000, "x" * 4097):
            result = subprocess.run([sys.executable, script, "--proposal", proposal], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("Traceback", result.stderr)

    def test_no_match(self):
        result = execute({"tool": "lookup", "arguments": {"topic": "unknown"}}, {"lookup"})
        self.assertEqual(result["status"], "no_match")
        self.assertIsNone(result["source"])


if __name__ == "__main__":
    unittest.main()
