import speech_recognition as sr
import pygame

pygame.mixer.init()


def play_sound(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def listen_with_google():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        #play_sound("resources/listen.mp3")

        audio = recognizer.listen(source)
        #play_sound("resources/convert.mp3")

        try:
            text = recognizer.recognize_google(audio)
            print(text)
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")


if __name__ == "__main__":
    listen_with_google()