import wave
import json
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment

# 初始化模型
print("init model")
model = Model("Dependencise\\vosk-model-small-cn-0.22")
print("successfully init model")

# 将 MP3 转为 WAV
audio = AudioSegment.from_mp3("testvoice\\test01.mp3")
audio = audio.set_channels(1)       # 设置为单声道
audio = audio.set_frame_rate(16000) # 设置采样率为 16000Hz
audio.export("temp.wav", format="wav")

# 用 wave 打开刚生成的 wav 文件
wf = wave.open("temp.wav", "rb")
recognizer = KaldiRecognizer(model, wf.getframerate())

print("begin recognizing")
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    recognizer.AcceptWaveform(data)

print("finish recognizing")
result = json.loads(recognizer.Result())
print("识别结果：", result.get("text", ""))

