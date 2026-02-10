from openai import OpenAI
from src.config import OPENROUTER_API_KEY, AI_MODEL


class Brain:
    def __init__(self, ui_callback=None):
        self.ui_callback = ui_callback

        self.client = None
        if OPENROUTER_API_KEY:
            try:
                self.client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=OPENROUTER_API_KEY
                )
            except Exception as e:
                self._push_ui(f"Brain Init Error: {e}")

    def _push_ui(self, msg: str):
        if self.ui_callback:
            self.ui_callback(msg)

    def get_ai_response(self, user_query: str, system_prompt="You are Jarvis, a helpful AI assistant.") -> str:
        if not self.client:
            return "Boss, AI client not configured. Please set OPENROUTER_API_KEY."

        try:
            self._push_ui("🤖 Thinking (AI)...")

            response = self.client.chat.completions.create(
                model=AI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ],
                temperature=0.7,
                max_tokens=900
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            self._push_ui(f"AI Error: {e}")
            return "Sorry Boss, I am having trouble connecting to my brain."
