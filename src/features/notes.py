import os
import time
from datetime import datetime
import pyautogui

from src.config import SAVE_FOLDER


def note_workflow(topic: str, speak, brain):
    """
    topic: what to write about
    speak: speech_engine.speak
    brain: Brain class object (brain.get_ai_response)
    """

    try:
        speak(f"Understood, Boss. Creating a document about: {topic}.", force_full_speak=True)

        system_prompt = "You are an expert writer. Create a well-structured and high-quality piece on the following topic."
        note_content = brain.get_ai_response(topic, system_prompt=system_prompt)

        if "Sorry Boss" in note_content or "not configured" in note_content:
            speak(note_content, force_full_speak=True)
            return

        speak("Content generated. Opening notepad to write it down.", force_full_speak=True)
        time.sleep(1)

        os.startfile("notepad.exe")
        time.sleep(1.5)

        pyautogui.write(note_content, interval=0.005)

        time.sleep(0.4)
        pyautogui.hotkey('ctrl', 's')

        time.sleep(0.6)
        os.makedirs(SAVE_FOLDER, exist_ok=True)

        pyautogui.write(str(SAVE_FOLDER), interval=0.02)
        pyautogui.press('enter')

        time.sleep(0.6)

        clean_topic_name = "".join(c for c in topic if c.isalnum() or c in " ").rstrip().replace(" ", "_")
        filename = f"{clean_topic_name[:30]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        pyautogui.write(filename, interval=0.02)
        pyautogui.press('enter')

        time.sleep(0.6)
        pyautogui.hotkey('alt', 'f4')

        speak(f"I have saved the note as {filename}.", force_full_speak=True)

    except Exception as e:
        print("Error in note workflow:", e)
        speak("Sorry Boss, I failed to complete the note-taking process.", force_full_speak=True)
