import wave
import json
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment
print("init model")
model = Model("Dependencise\\vosk-model-small-cn-0.22")
print("successfully init model")
voice_file = AudioSegment.from_mp3("testvoice\\test01.mp3")
voice_file = voice_file.raw_data
kaldirecongizer = KaldiRecognizer(model, 16000)
print("begin recognizing")
while True:
    buffer = voice_file.readframes(4000)
    if not buffer:
        break
    kaldirecongizer.AcceptWaveform(buffer)
print("finish recognizing")
text = json.loads(kaldirecongizer.PartialResult())
