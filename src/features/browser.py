import re
import webbrowser


def open_website_from_command(cmd: str, speak=None) -> bool:
    lowered = cmd.lower()

    site_map = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "facebook": "https://www.facebook.com",
        "github": "https://github.com",
    }

    for key, url in site_map.items():
        if re.search(rf"(open|goto|show)\s+(website\s+)?{key}\b", lowered):
            if speak:
                speak(f"Opening {key}.")
            webbrowser.open(url)
            return True

    # explicit url / domain
    m = re.search(r"(open|goto|show)\s+(website\s+)?((https?://)?[a-z0-9\-\._]+(\.[a-z]{2,}))", lowered)
    if m:
        raw = m.group(3)

        if raw.startswith("http://") or raw.startswith("https://"):
            url = raw
        else:
            url = f"https://{raw}"

        if speak:
            speak(f"Opening {url}.")
        webbrowser.open(url)
        return True

    return False


def search_in_google(command: str, speak=None) -> bool:
    if not command.startswith("search in google"):
        return False

    query = command.replace("search in google", "").strip()

    if not query:
        if speak:
            speak("What should I search for on Google, Boss?")
        return True

    if speak:
        speak(f"Searching for {query} on Google.", force_full_speak=True)

    webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
    return True


def search_in_youtube(command: str, speak=None) -> bool:
    if not command.startswith("search in youtube"):
        return False

    query = command.replace("search in youtube", "").strip()

    if not query:
        if speak:
            speak("What should I search for on YouTube, Boss?")
        return True

    if speak:
        speak(f"Searching for {query} on YouTube.", force_full_speak=True)

    webbrowser.open(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")
    return True
