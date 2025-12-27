import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables (Override system defaults to ensure .env is used)
load_dotenv(override=True)

# App Info
APP_NAME = "Personal AI Assistant"
VERSION = "2.0.0"

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

# Security & Sandbox
# Default to a 'workspace' folder in the current execution directory
BASE_WORKSPACE_DIR = os.getenv("BASE_WORKSPACE_DIR", os.path.join(os.getcwd(), "workspace"))

# Advanced
DRY_RUN = os.getenv("DRY_RUN", "False").lower() == "true"
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.6"))

def validate_config():
    """Validates critical configuration."""
    if not OPENAI_API_KEY:
        raise ValueError("Configuration Error: OPENAI_API_KEY is missing in .env file.")
    
    # Ensure workspace exists
    if not os.path.exists(BASE_WORKSPACE_DIR):
        try:
            os.makedirs(BASE_WORKSPACE_DIR)
        except OSError as e:
            raise ValueError(f"Could not create workspace directory: {e}")
