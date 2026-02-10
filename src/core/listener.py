import speech_recognition as sr


class Listener:
    def __init__(self, ui_callback=None, mic_status_callback=None):
        """
        ui_callback: function to print text in GUI
        mic_status_callback: function(text, color) to update mic label
        """
        self.ui_callback = ui_callback
        self.mic_status_callback = mic_status_callback
        self.recognizer = sr.Recognizer()

    def _push_ui(self, msg: str):
        if self.ui_callback:
            self.ui_callback(msg)

    def _mic_status(self, text, color="#00FFAA"):
        if self.mic_status_callback:
            self.mic_status_callback(text, color)

    def listen_command(self, timeout=5, phrase_time_limit=8, language="en-US") -> str:
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            self._mic_status("🎙️ Listening...", "#00FF00")

            try:
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )

                query = self.recognizer.recognize_google(audio, language=language)
                query = query.lower()

                self._push_ui(f"👉 You said: {query}")
                self._mic_status("🎙️ Idle", "#00FFAA")

                return query

            except sr.WaitTimeoutError:
                self._push_ui("⌛ Listening timed out.")
                self._mic_status("🎙️ Idle", "#00FFAA")
                return ""

            except sr.UnknownValueError:
                self._push_ui("❓ Could not understand audio.")
                self._mic_status("🎙️ Idle", "#00FFAA")
                return ""

            except sr.RequestError as e:
                self._push_ui(f"API error (speech): {e}")
                self._mic_status("🎙️ Idle", "#00FFAA")
                return ""

            except Exception as e:
                self._push_ui(f"Microphone error: {e}")
                self._mic_status("🎙️ Idle", "#00FFAA")
                return ""
