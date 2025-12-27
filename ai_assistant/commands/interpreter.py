import re
import json
from ai_assistant.llm.client import ask_llm
from ai_assistant.utils.logger import setup_logger

logger = setup_logger(__name__)

def interpret_command(user_input: str) -> list[dict]:
    """
    Parses natural language into structured commands.
    Returns: list[dict] (A list of command objects)
    """
    text = user_input.strip().lower()

    # --- 1. Rule-Based Matching ---
    
    # "open google.com" -> open_url
    url_match = re.match(r"^open\s+(https?://[^\s]+|www\.[^\s]+|[a-z0-9]+\.[a-z]{2,})$", text)
    if url_match:
        url = url_match.group(1)
        if not url.startswith("http"): url = "https://" + url
        return [{"action": "open_url", "params": {"url": url}, "confidence": 1.0}]

    # "open [app]" -> REMOVED greedy regex to allow LLM to handle composite commands
    # app_match = re.match(r"^open\s+(?!https?://|www\.)(.+)$", text)
    # if app_match:
    #     app_name = app_match.group(1).strip()
    #     return [{"action": "open_app", "params": {"name": app_name}, "confidence": 1.0}]

    # "create folder [name]" -> REMOVED greedy regex to allow LLM to handle composite commands
    # folder_match = re.match(r"^create folder\s+(.+)$", text)
    # if folder_match:
    #     name = folder_match.group(1).strip()
    #     return [{"action": "create_folder", "params": {"name": name}, "confidence": 1.0}]
        
    # "ls" or "list files" -> list_directory
    if text in ["ls", "list", "list files", "show files"]:
        return [{"action": "list_directory", "params": {}, "confidence": 1.0}]

    # "system status" -> respond with special flag or just show status (handling in interpreter to be simple)
    # Ideally main.py handles this, but we can hack it by returning a respond action with the status.
    # Actually, let's map it to a "show_status" action if we had one, or just let LLM handle.
    # But LLM failed, so let's add a rule.
    if "system status" in text or "status" == text:
        return [{"action": "respond", "params": {"message": "All systems operational. (View 'System Status' table above)"}, "confidence": 1.0}]

    # --- 2. LLM Fallback ---
    # logger.info("Rule mismatch. delegating to LLM.")
    
    SYSTEM_PROMPT = """
    You are a Command Parser. Your ONLY job is to convert User Input into a JSON ARRAY of commands.
    Do NOT explain. Do NOT write Python code. Do NOT output markdown.
    
    IMPORTANT: 
    - Output a LIST of objects, even if there is only one command.
    - Split complex requests (e.g. "do X and do Y") into multiple sequential commands.
    - If you use "respond", speak naturally. DO NOT suggest Python commands or function signatures to the user.
    - Use the provided CONTEXT (history) to resolve references like "it", "that file", "the app", etc.

    Available Actions:
    - open_app(name: str)
    - close_app(name: str)  <-- Use to kill/terminate apps
    - system_control(action: str)  <-- action: "shutdown", "restart", "lock"
    - open_url(url: str)
    - search_web(query: str) <-- Use to find information online
    - analyze_screen(prompt: str) <-- Use when user asks about screen content/errors/images
    - type_text(text: str) <-- Use to type text into the currently active window (e.g. Notepad)
    - create_folder(name: str)
    - write_file(filename: str, content: str)
    - read_file(filename: str) <-- Use to read content of a file
    - list_directory()
    - respond(message: str)  <-- Use this for general chat/questions

    Examples:
    Input: "Open chrome"
    Output: [ { "action": "open_app", "params": { "name": "chrome" }, "confidence": 1.0 } ]

    Input: "Close chrome"
    Output: [ { "action": "close_app", "params": { "name": "chrome" }, "confidence": 1.0 } ]

    Input: "Shutdown my laptop"
    Output: [ { "action": "system_control", "params": { "action": "shutdown" }, "confidence": 1.0 } ]

    Input: "Open whatsapp web and message priya"
    Output: [ 
        { "action": "open_url", "params": { "url": "https://web.whatsapp.com" }, "confidence": 1.0 },
        { "action": "respond", "params": { "message": "I opened WhatsApp Web. I cannot send messages automatically yet." }, "confidence": 0.9 }
    ]

    Input: "Open Notepad and type Hello World"
    Output: [
        { "action": "open_app", "params": { "name": "Notepad" }, "confidence": 1.0 },
        { "action": "type_text", "params": { "text": "Hello World" }, "confidence": 1.0 }
    ]

    Input: "Tell me a joke"
    Output: [ { "action": "respond", "params": { "message": "Why did the chicken cross the road? To get to the other side!" }, "confidence": 1.0 } ]

    Input: "Do I have any meetings today?" (Requires web/calendar - fallback to web search)
    Output: [ { "action": "search_web", "params": { "query": "current date and time" }, "confidence": 0.8 } ]

    Input: "Who won the super bowl?"
    Output: [ { "action": "search_web", "params": { "query": "super bowl winner 2024" }, "confidence": 1.0 } ]

    Input: "What does this error message mean?"
    Output: [ { "action": "analyze_screen", "params": { "prompt": "Identify the error message on screen and explain it." }, "confidence": 1.0 } ]

    Input: "Hi"
    Output: [ { "action": "respond", "params": { "message": "Hello! I am your AI Assistant. How can I help you today?" }, "confidence": 1.0 } ]
    
    Output Format (Raw JSON Array Only):
    """
    
    try:
        raw_response = ask_llm(user_input, system_prompt=SYSTEM_PROMPT)
        clean_json = raw_response.strip()
        
        # 1. Try removing markdown blocks first
        if "```json" in clean_json:
            clean_json = clean_json.split("```json")[1].split("```")[0].strip()
        elif "```" in clean_json:
            clean_json = clean_json.split("```")[1].split("```")[0].strip()

        # 2. Extract JSON part
        start = clean_json.find('[')
        end = clean_json.rfind(']')
        
        if start != -1 and end != -1:
            clean_json = clean_json[start:end+1]
        
        data = json.loads(clean_json)
        
        if isinstance(data, dict):
            # Normalize single object to list
            data = [data]
            
        return data

    except json.JSONDecodeError:
        return [{"action": "respond", "params": {"message": raw_response}, "confidence": 1.0}]
    except Exception as e:
        logger.error(f"Interpretation Error: {e}")
        return [{"action": "respond", "params": {"message": "I encountered an error parsing your command."}, "confidence": 0.0}]
