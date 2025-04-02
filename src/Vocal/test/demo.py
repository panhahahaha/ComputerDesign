import pyaudio
import wave

# 录音参数
FORMAT = pyaudio.paInt16  # 16位深度
CHANNELS = 1              # 单声道
RATE = 44100              # 采样率
CHUNK = 1024              # 每次读取的帧数
RECORD_SECONDS = 5        # 录音时长
OUTPUT_FILENAME = "output.wav"

# 初始化 PyAudio
audio = pyaudio.PyAudio()

# 打开麦克风流
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("正在录音...")

frames = []
for _ in range(int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("录音结束.")

# 关闭流和 PyAudio
stream.stop_stream()
stream.close()
audio.terminate()

# 保存音频文件
with wave.open(OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)#设置声道个数
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print(f"音频已保存为 {OUTPUT_FILENAME}")
