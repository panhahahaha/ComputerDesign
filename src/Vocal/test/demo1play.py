import pyaudio
import wave

# 读取 WAV 文件
filename = "output.wav"
wf = wave.open(filename, 'rb')

# 初始化 PyAudio
audio = pyaudio.PyAudio()

# 打开音频流
stream = audio.open(format=audio.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

# 读取数据并播放
CHUNK = 1024
data = wf.readframes(CHUNK)

while data:
    stream.write(data)
    data = wf.readframes(CHUNK)

# 关闭流和 PyAudio
stream.close()
audio.terminate()

print("播放完成")
