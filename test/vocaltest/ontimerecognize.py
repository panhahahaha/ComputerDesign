import pyaudio
import json
from vosk import Model, KaldiRecognizer
from pathlib import Path

PATH = Path(__file__).resolve().parent
# p = pyaudio.PyAudio()
# for i in range(p.get_device_count()):
#     dev = p.get_device_info_by_index(i)
#     if dev['maxInputChannels'] > 0:
#         print(f"device {i}: {dev['name']} maxInputChannels {dev['maxInputChannels']}")
model_path = str(PATH / "Dependencise" / "vosk-model-small-cn-0.22")
import json
import pyaudio

print(model_path)
model = Model(model_path)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
kaldiRecognizer = KaldiRecognizer(model, 16000)
print("开始识别...")

while True:
    context = stream.read(5000)
    if len(context) == 0:
        print("没有读取到音频数据，可能是麦克风问题。")
        continue

    if kaldiRecognizer.AcceptWaveform(context):
        result = kaldiRecognizer.Result()
        print(json.loads(result))  # 输出识别结果

    else:
        print("当前没有识别到有效的语音")
