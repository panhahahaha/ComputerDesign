import pyttsx3
from pathlib import Path
PATH = Path(__file__).resolve().parent
print(PATH)
text = PATH/"testText01"/"demo1"
def main():
    audio = pyttsx3.init()
    audio.setProperty('rate', 150)
    audio.setProperty('volume', 1.0)
    with open(text,'r',encoding='utf-8') as f:
        contain = f.read()
    print(contain)
    audio.say(contain)
    audio.runAndWait()
if __name__ == '__main__':

    main()

