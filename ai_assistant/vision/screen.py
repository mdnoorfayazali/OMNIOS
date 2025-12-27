import pyautogui
import base64
import io
from ai_assistant.utils.logger import setup_logger


logger = setup_logger(__name__)

# Try to import rich for visual feedback, otherwise dummy context
try:
    from rich.console import Console
    console = Console()
except ImportError:
    console = None

def capture_screen_base64() -> str:
    """
    Captures the primary screen and returns it as a base64 encoded JPEG string.
    """
    try:
        # Import inside function to handle missing dependency gracefully at runtime
        import pyautogui
        
        # Use rich status if available
        if console:
            context = console.status("[bold magenta]Scanning visual field (Screen Capture)...[/bold magenta]", spinner="dots")
        else:
            # Dummy context manager
            class DummyContext:
                def __enter__(self): pass
                def __exit__(self, exc_type, exc_val, exc_tb): pass
            context = DummyContext()

        with context:
            screenshot = pyautogui.screenshot()
            buffer = io.BytesIO()
            # Quality=70 is a good balance for LLM vision tokens vs clarity
            screenshot.save(buffer, format="JPEG", quality=70)
            img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
            
        return img_str
    except ImportError:
        logger.error("PyAutoGUI not installed. Screen capture disabled.")
        if console:
            console.print("[bold red]Error: 'pyautogui' module missing. Vision disabled.[/bold red]")
        return None
    except Exception as e:
        logger.error(f"Screen capture failed: {e}")
        return None
