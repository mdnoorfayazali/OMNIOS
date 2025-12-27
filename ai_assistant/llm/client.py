from openai import OpenAI, APIError, APITimeoutError, BadRequestError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from ai_assistant.config import settings
from ai_assistant.utils.logger import setup_logger

logger = setup_logger(__name__)

class LLMClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL
        )
        self.history = []
        self.max_history = 10  # Keep last 10 exchanges

    @retry(
        retry=retry_if_exception_type((APITimeoutError, APIError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def ask(self, prompt: str, system_prompt: str = None, image_base64: str = None) -> str:
        """
        Sends a prompt to the LLM with history context and returns the raw text response.
        """
        try:
            logger.info(f"Sending LLM request (Model: {settings.MODEL_NAME})")
            
            # Helper to construct messages
            def build_messages(use_image: bool):
                msgs = []
                if system_prompt:
                    msgs.append({"role": "system", "content": system_prompt})
                msgs.extend(self.history)
                
                if use_image and image_base64:
                    content = [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                    ]
                else:
                    content = prompt
                    
                msgs.append({"role": "user", "content": content})
                return msgs

            # 1. Try with Image (if requested)
            try:
                messages = build_messages(use_image=bool(image_base64))
                
                # Select appropriate model
                current_model = settings.VISION_MODEL_NAME if image_base64 else settings.MODEL_NAME
                logger.info(f"Using Model for Request: {current_model}")

                response = self.client.chat.completions.create(
                    model=current_model,
                    messages=messages,
                    temperature=0.0,
                )
            except BadRequestError as e:
                # 2. Fallback if model rejects image structure (e.g. Llama-3)
                if image_base64:
                    logger.warning(f"Model rejected image input ({e}). Falling back to text-only.")
                    messages = build_messages(use_image=False)
                    # Append note to prompt so model knows context is missing
                    messages[-1]['content'] += "\n[System Note: Screen analysis failed due to model incompatibility. Use text context only.]"
                    
                    response = self.client.chat.completions.create(
                        model=settings.MODEL_NAME,
                        messages=messages,
                        temperature=0.0,
                    )
                else:
                    raise e

            content = response.choices[0].message.content.strip()

            # 2. Update History
            # Note: We don't store the full base64 image in history to save tokens/memory, just a placeholder or text
            if image_base64:
                self.history.append({"role": "user", "content": f"{prompt} [Image Sent]"})
            else:
                self.history.append({"role": "user", "content": prompt})
            
            self.history.append({"role": "assistant", "content": content})
            
            # 3. Sliding Window (Keep roughly max_history * 2 items, as each turn is 2 messages)
            if len(self.history) > self.max_history * 2:
                self.history = self.history[-(self.max_history * 2):]

            return content
        except Exception as e:
            logger.error(f"LLM request failed: {e}")
            raise

    def clear_history(self):
        self.history = []

# Singleton instance
_client = LLMClient()

def ask_llm(prompt: str, system_prompt: str = None, image_base64: str = None) -> str:
    return _client.ask(prompt, system_prompt, image_base64)
