import speech_recognition as sr
from copy import deepcopy


class NLP():
    def __init__(self, state: bool | None = True):
        self.state = state
        self.recog = sr.Recognizer()
        self.__data = ''

    def get_data(self) -> str:
        data = deepcopy(self.__data)
        self.__data = ''
        return data

    def change_state(self, state: bool) -> None:
        self.state = state
        return None

    def main(self):
        with sr.Microphone() as sourse:
            while self.state is True:
                try:
                    audio = self.recog.listen(source=sourse, timeout=1)
                    text = self.recog.recognize_google(audio, language='ru-RU')
                    self.__data += f"{text}\n"
                except Exception:
                    pass


if __name__ == "__main__":
    nlp = NLP()
    nlp.main()