import speech_recognition as sr


def stream_audio(recognizer: sr.Recognizer, microphone: sr.Microphone) -> None:
    """Stream audio from the microphone and recognize it using speech_recognition."""
    with microphone as source:
            print("Listening for audio... (Press Ctrl+C to stop)")

            # Adjust for ambient noise and set a threshold
            recognizer.adjust_for_ambient_noise(source)

            while True:
                try:
                    # Listen for audio
                    audio = recognizer.listen(source)

                    # Recognize speech using Google Web Speech API
                    text = recognizer.recognize_google(audio, language='ru-RU')
                    print("Transcription: " + text)

                except sr.UnknownValueError:
                    # If the speech is unintelligible
                    print("Sorry, I could not understand the audio.")
                except sr.RequestError as e:
                    # If there's an issue with the API
                    print(f"Could not request results from Google Speech Recognition service; {e}")


if __name__ == "__main__":
    recognize = sr.Recognizer()
    microphone = sr.Microphone()
    stream_audio(recognize, microphone)
