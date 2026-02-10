import subprocess


def run_cmd(cmd):
    try:
        subprocess.run(cmd, shell=True)
    except Exception:
        pass


def confirm_voice(listen_command, speak, prompt_words=("yes", "confirm", "proceed")):
    speak("Are you sure? Say yes to confirm.")
    reply = listen_command(timeout=5, phrase_time_limit=4)
    return any(word in reply for word in prompt_words)


def shutdown_pc(listen_command, speak):
    if confirm_voice(listen_command, speak):
        speak("Shutting down now, boss.")
        run_cmd("shutdown /s /f /t 0")
    else:
        speak("Shutdown canceled.")


def restart_pc(listen_command, speak):
    if confirm_voice(listen_command, speak):
        speak("Restarting now, boss.")
        run_cmd("shutdown /r /f /t 0")
    else:
        speak("Restart canceled.")
