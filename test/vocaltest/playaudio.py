import pyaudio
import wave

# 打开 WAV 文件
filename = 'temp.wav'
wf = wave.open(filename, 'rb')

# 初始化 PyAudio
p = pyaudio.PyAudio()

# 打开流
stream = p.open(format=pyaudio.paInt16,  # 音频格式（16位采样）
                channels=wf.getnchannels(),  # 获取音频通道数
                rate=wf.getframerate(),  # 获取音频采样率
                output=True)  # 设置为输出流

# 读取音频数据并播放
chunk = 1024
data = wf.readframes(chunk)

while data:
    stream.write(data)
    data = wf.readframes(chunk)

# 停止流
stream.stop_stream()
stream.close()

# 关闭 PyAudio
p.terminate()
