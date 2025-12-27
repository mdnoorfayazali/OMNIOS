import os
import webbrowser
import platform
from pathlib import Path
from ai_assistant.config import settings
from ai_assistant.utils.logger import setup_logger
from ai_assistant.vision.screen import capture_screen_base64
from ai_assistant.utils.web import search_web
from ai_assistant.llm.client import ask_llm

logger = setup_logger(__name__)

def _get_safe_path(filename: str) -> str:
    """
    Ensures file operations are contained within the workspace.
    Prevents directory traversal (../../).
    """
    workspace = Path(settings.BASE_WORKSPACE_DIR).resolve()
    target = (workspace / filename).resolve()
    
    if not str(target).startswith(str(workspace)):
        raise ValueError(f"Security Alert: Attempted path traversal out of workspace! Target: {target}")
    
    return str(target)

def execute_action(command: dict) -> str:
    """
    Dispatches command to safe handlers.
    Expects command format: {"action": "...", "params": {...}}
    """
    action = command.get("action")
    params = command.get("params", {})
    
    try:
        if action == "respond":
            return params.get("message", "")

        elif action == "open_url":
            url = params.get("url")
            if not url: return "Error: Missing URL parameter."
            webbrowser.open(url)
            return f"Opened URL: {url}"

        elif action == "open_app":
            name = params.get("name")
            if not name: return "Error: Missing app name."
            
            system = platform.system()
            if system == "Windows":
                os.startfile(name)
            elif system == "Darwin":
                os.system(f"open -a '{name}'")
            else:
                os.system(f"xdg-open '{name}'")
            return f"Launched application: {name}"

        elif action == "create_folder":
            name = params.get("name")
            if not name: return "Error: Missing folder name."
            
            safe_path = _get_safe_path(name)
            os.makedirs(safe_path, exist_ok=True)
            return f"Created folder in workspace: {name}"

        elif action == "close_app":
            name = params.get("name")
            if not name: return "Error: Missing app name."
            
            system = platform.system()
            if system == "Windows":
                # Force kill by image name
                cmd = f"taskkill /IM {name}.exe /F"
            else:
                cmd = f"pkill -f {name}"
            
            ret = os.system(cmd)
            if ret == 0:
                return f"Closed application: {name}"
            else:
                return f"Failed to close {name} (it might not be running)."

        elif action == "system_control":
            sub_action = params.get("action") # shutdown, restart, lock
            if not sub_action: return "Error: Missing system action."
            
            system = platform.system()
            if system == "Windows":
                if sub_action == "shutdown":
                    os.system("shutdown /s /t 0")
                elif sub_action == "restart":
                    os.system("shutdown /r /t 0")
                elif sub_action == "lock":
                    os.system("rundll32.exe user32.dll,LockWorkStation")
                else:
                    return f"Unknown system action: {sub_action}"
            else:
                return "System control only implemented for Windows currently."
            
            return f"System Action Initiated: {sub_action}"

        elif action == "write_file":
            filename = params.get("filename")
            content = params.get("content")
            
            if not filename or content is None:
                return "Error: Missing filename or content."
            
            safe_path = _get_safe_path(filename)
            
            # Ensure parent directories exist
            os.makedirs(os.path.dirname(safe_path), exist_ok=True)
            
            with open(safe_path, "w", encoding="utf-8") as f:
                f.write(content)
                
            return f"Saved file to workspace: {filename}"

        elif action == "list_directory":
            workspace = settings.BASE_WORKSPACE_DIR
            files = os.listdir(workspace)
            if not files:
                return "Workspace is empty."
            return "Files in workspace:\n" + "\n".join(f"- {f}" for f in files)

        elif action == "read_file":
            filename = params.get("filename")
            if not filename: return "Error: Missing filename."
            
            safe_path = _get_safe_path(filename)
            if not os.path.exists(safe_path):
                return f"Error: File not found: {filename}"
                
            try:
                # Basic size check (example: 100KB limit for demo)
                if os.path.getsize(safe_path) > 100 * 1024:
                    return f"Error: File {filename} is too large to read directly."

                with open(safe_path, "r", encoding="utf-8") as f:
                    content = f.read()
                return f"--- Content of {filename} ---\n{content}\n--- End of File ---"
            except UnicodeDecodeError:
                return f"Error: File {filename} appears to be binary or non-utf-8."

        elif action == "analyze_screen":
            prompt = params.get("prompt", "Describe this screen.")
            
            # 1. Capture
            img_base64 = capture_screen_base64()
            if not img_base64:
                return "Error: Failed to capture screen."
            
            # 2. Analyze via LLM
            # We use the existing ask_llm function which now supports images
            response = ask_llm(prompt, image_base64=img_base64)
            return f"Vision Analysis: {response}"

        elif action == "search_web":
            query = params.get("query")
            if not query: return "Error: Missing search query."
            
            return search_web(query)

        elif action == "type_text":
            text = params.get("text")
            if not text: return "Error: Missing text content."
            
            try:
                # Add a small delay to ensure window focus
                import time
                import pyautogui
                
                # Check if pyautogui is available (it's inside try/except block in main, but here we assume dependencies installed)
                # We can write typed characters
                pyautogui.write(text, interval=0.01) # Small interval to mimic typing
                return f"Typed text: {text}"
            except Exception as e:
                return f"Failed to type text: {e}"

        else:
            return f"Unknown action: {action}"

    except Exception as e:
        logger.error(f"Execution Error: {e}")
        return f"Failed to execute {action}: {str(e)}"
