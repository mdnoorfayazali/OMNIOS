import sys
import os

# Add the current directory to sys.path so we can import ai_assistant
sys.path.append(os.getcwd())

from ai_assistant.commands.interpreter import interpret_command

def test_command(text):
    print(f"Input: '{text}'")
    result = interpret_command(text)
    print(f"Result: {result}")

if __name__ == "__main__":
    # Expecting multiple commands now
    test_command("open whatsapp web and message priya")
    test_command("open google chrome and play song throug youtube")
    test_command("create folder my_project and write file test.txt with hello world")
    
    # Process Control Tests
    test_command("close chrome")
    test_command("shutdown my laptop")
