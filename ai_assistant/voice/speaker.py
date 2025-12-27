import pyttsx3
from ai_assistant.utils.logger import setup_logger

logger = setup_logger(__name__)

class Speaker:
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            # Optional: Set properties (voices, rate, volume)
            # voices = self.engine.getProperty('voices')
            # self.engine.setProperty('voice', voices[1].id) # Try female voice if available
            self.engine.setProperty('rate', 170)
        except Exception as e:
            logger.error(f"Failed to initialize TTS engine: {e}")
            self.engine = None

    def say(self, text):
        if not self.engine:
            logger.warning("TTS engine not initialized. Cannot speak.")
            print(f"AI (Silent): {text}")
            return

        try:
            logger.info(f"Speaking: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"TTS Error: {e}")

_speaker = Speaker()

def speak(text):
    _speaker.say(text)
