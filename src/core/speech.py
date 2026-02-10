import threading
import time
import re
import pyttsx3


class SpeechEngine:
    def __init__(self, ui_callback=None):
        """
        ui_callback: function that receives string message to show in GUI
        Example: ui_callback("Jarvis: Hello")
        """
        self.ui_callback = ui_callback
        self.stop_flag = threading.Event()
        self.speaking_thread = None

    def _push_ui(self, msg: str):
        if self.ui_callback:
            self.ui_callback(msg)

    def speak_task(self, text: str, force_full_speak=False):
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", 170)

            voices = engine.getProperty("voices")
            if voices:
                engine.setProperty("voice", voices[0].id)

            clean_text = re.sub(r'[\*\#\_]', '', text)
            lines = [ln for ln in clean_text.splitlines() if ln.strip()]

            text_to_speak = clean_text

            if len(lines) > 4 and not force_full_speak:
                summary = "\n".join(lines[:4])
                text_to_speak = f"{summary}\n\nBoss, the rest of the answer is written below."
                self._push_ui("Jarvis 💻 (Full Response):\n" + clean_text)

            self._push_ui("Jarvis 🔊: " + text_to_speak)

            engine.say(text_to_speak)
            engine.startLoop(False)

            while engine.isBusy() and not self.stop_flag.is_set():
                engine.iterate()
                time.sleep(0.05)

            try:
                engine.endLoop()
            except Exception:
                pass

            engine.stop()

        except Exception as e:
            self._push_ui(f"Speech Error: {e}")

    def speak(self, text: str, force_full_speak=False):
        if not text or not str(text).strip():
            return

        # already speaking -> stop
        if self.speaking_thread and self.speaking_thread.is_alive():
            self.stop()
            self.speaking_thread.join(timeout=1)

        self.stop_flag.clear()

        self.speaking_thread = threading.Thread(
            target=self.speak_task,
            args=(text, force_full_speak),
            daemon=True
        )
        self.speaking_thread.start()

    def stop(self):
        if self.speaking_thread and self.speaking_thread.is_alive():
            self.stop_flag.set()
            self._push_ui("🔴 Speech stopped.")
