import speech_recognition as sr
from ai_assistant.utils.logger import setup_logger

logger = setup_logger(__name__)

class Listener:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # Adjust query duration
        self.recognizer.pause_threshold = 1.0 

    def listen(self):
        """
        Listens to the microphone and returns the recognized text.
        Returns None if nothing was heard or an error occurred.
        """
        with sr.Microphone() as source:
            logger.info("Listening...")
            print("\n🎤 Listening... (Speak now)")
            
            # Dynamic energy adjustment for ambient noise
            try:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            except sr.WaitTimeoutError:
                logger.debug("Listening timed out (no speech detected).")
                return None
            except Exception as e:
                logger.error(f"Microphone error: {e}")
                return None

        try:
            logger.info("Recognizing...")
            # recognize_google is free for personal use/testing
            text = self.recognizer.recognize_google(audio)
            logger.info(f"Heard: {text}")
            print(f"🎤 You said: {text}")
            return text
        except sr.UnknownValueError:
            logger.debug("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Could not request results from Google Speech Recognition service; {e}")
            return None

_listener = Listener()

def listen():
    return _listener.listen()
