import pyautogui
import base64
import io
from ai_assistant.utils.logger import setup_logger

logger = setup_logger(__name__)

def capture_screen_base64() -> str:
    """
    Captures the primary screen and returns it as a base64 encoded JPEG string.
    """
    try:
        screenshot = pyautogui.screenshot()
        buffer = io.BytesIO()
        screenshot.save(buffer, format="JPEG", quality=70) # Lower quality to save tokens/bandwidth
        img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return img_str
    except Exception as e:
        logger.error(f"Screen capture failed: {e}")
        return None
