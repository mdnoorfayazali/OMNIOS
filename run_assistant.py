
import sys
import os

# Add the current directory to sys.path to ensure modules are found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_assistant.main import main

if __name__ == "__main__":
    main()
