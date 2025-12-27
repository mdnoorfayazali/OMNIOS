import sys
import os
from unittest.mock import MagicMock

# Add current dir to path so we can import modules
sys.path.append(os.getcwd())

try:
    print("Verifying imports...")
    from ai_assistant.config import settings
    from ai_assistant.llm.client import ask_llm
    from ai_assistant.commands.interpreter import interpret_command
    from ai_assistant.executor.actions import execute_action
    print("Imports successful.")

    print("Verifying Rule-Based Interpreter...")
    cmd = interpret_command("open chrome")
    assert cmd == {"action": "open_app", "target": "chrome"}
    print("Rule-based interpreter passed.")

    print("Verifying Action Executor (Mocked)...")
    # Mocking os.startfile to avoid actually opening things during test
    if hasattr(os, 'startfile'):
        os.startfile = MagicMock()
    
    res = execute_action({"action": "open_app", "target": "notepad"})
    assert "Successfully opened" in res
    print("Action executor passed.")

    print("Verifying LLM Fallback Structure...")
    # We can't easily test the live LLM without a key, but we can check the function exists
    assert callable(ask_llm)
    print("LLM client structure passed.")
    
    print("\nALL CHECKS PASSED!")

except ImportError as e:
    print(f"IMPORT ERROR: {e}")
    sys.exit(1)
except Exception as e:
    print(f"VERIFICATION FAILED: {e}")
    sys.exit(1)
