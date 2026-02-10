import threading
import webbrowser

from playwright.sync_api import sync_playwright


# Shared state for playwright usage
playwright_context = {
    "is_running": False,
    "stop_event": threading.Event(),
    "lock": threading.Lock()
}


def play_on_youtube_task(command: str, speak):
    song_name = command.split("play", 1)[-1].strip()

    if not song_name:
        speak("What should I play, Boss?", force_full_speak=True)
        return

    with playwright_context["lock"]:
        if playwright_context["is_running"]:
            speak("Already fetching/playing a video. Please wait.")
            return
        playwright_context["is_running"] = True
        playwright_context["stop_event"].clear()

    speak(f"Searching YouTube for {song_name}, Boss.", force_full_speak=True)

    search_url = f"https://www.youtube.com/results?search_query={song_name.replace(' ', '+')}"

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(search_url, wait_until="domcontentloaded", timeout=60000)

            first_video_selector = "a#video-title"
            page.wait_for_selector(first_video_selector, timeout=30000)

            video_href = page.locator(first_video_selector).first.get_attribute("href")

            if video_href:
                full_url = f"https://www.youtube.com{video_href}"
                speak("Found the video! Opening it in your default browser.", force_full_speak=True)
                webbrowser.open(full_url)
            else:
                speak("Sorry Boss, couldn't find any video.", force_full_speak=True)

            browser.close()

    except Exception as e:
        print("Playwright error:", e)
        speak("Sorry Boss, something went wrong while fetching the video.", force_full_speak=True)

    finally:
        with playwright_context["lock"]:
            playwright_context["is_running"] = False
            playwright_context["stop_event"].clear()
