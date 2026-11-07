import pygame
import pyttsx3
import speech_recognition as sr
from google import genai

pygame.mixer.init()

client = genai.Client(api_key="AQ.Ab8RN6KQhkgMxHXQ_OZOeCwFvNZCis0utka_VNi0XVIGsbcE7g")

WAKE_WORD = "hello buddy"
STOP_WORD = "best buddy"

recognizer = sr.Recognizer()
mic = sr.Microphone()


def play_sound(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def listen_once(prompt="Listening..."):
    with mic as source:
        print(prompt)
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
    return None


def gemini_api(text):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=text,
    )
    print(f"Gemini: {response.text}")
    return response.text


def text_to_speech(text, voice_index=1, rate=130, volume=1.0):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    voice_index = min(voice_index, len(voices) - 1)
    engine.setProperty('voice', voices[voice_index].id)
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)
    engine.say(text)
    engine.runAndWait()


def conversation_loop():
    """Runs after wake word is detected. Keeps listening until stop word."""
    while True:
        text = listen_once("Listening for your question...")

        if text is None:
            continue

        if STOP_WORD in text:
            print("Stopping conversation. Say the wake word to start again.")
            text_to_speech("Okay, going back to sleep.")
            break

        reply = gemini_api(text)
        if reply:
            text_to_speech(reply)


def main():
    print(f"Waiting for wake word: '{WAKE_WORD}'")
    while True:
        text = listen_once()
        if text and WAKE_WORD in text:
            text_to_speech("Yes, I'm listening.")
            conversation_loop()


if __name__ == "__main__":
    main()