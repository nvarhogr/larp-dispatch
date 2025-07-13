import speech_recognition as sr
import requests
import keyboard
import threading

WEBHOOK_URL = "https://discord.com/api/webhooks/1394076179304026215/fxNyYbVdL5fIo9XczGfwXqGVESg61wrPKGsAfeF5JJT5tSBFUuDG5FDpzbgwJNYN6aot"

def send_to_discord(message):
    payload = {"content": f"```\n{message}\n```"}
    try:
        requests.post(WEBHOOK_URL, json=payload)
        print("✅ Sent to Discord:", message)
    except Exception as e:
        print("❌ Failed to send:", e)

def recognize_and_send():
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True

    with sr.Microphone() as source:
        print("🎙️ Listening... Speak now.")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language="en-US")
            print("📝 Recognized:", text)
            send_to_discord(text)
        except sr.UnknownValueError:
            print("❌ Could not understand audio.")
        except sr.WaitTimeoutError:
            print("⏱️ Listening timed out.")
        except sr.RequestError as e:
            print("❌ Speech API error:", e)

def start_hotkey_listener():
    print("🔁 Press Ctrl + Space to speak. Press ESC to quit.")
    keyboard.add_hotkey('ctrl+space', lambda: threading.Thread(target=recognize_and_send).start())

    # Wait until ESC is pressed
    keyboard.wait('esc')
    print("👋 Exiting...")

if __name__ == "__main__":
    start_hotkey_listener()
