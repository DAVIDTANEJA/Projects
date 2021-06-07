import pyaudio    # >> pip isntall pipwin    >> pipwin install pyaudio
import wave

audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

frames = []
try:
    while True:
        data = stream.read(1024)
        frames.append(data)
except KeyboardInterrupt:
    pass

stream.stop_stream()
stream.close()
audio.terminate()

sound_file = wave.open('myrecording.mp3', "wb")
sound_file.setnchannels(1)
sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
sound_file.setframerate(44100)
sound_file.writeframes(b''.join(frames))
sound_file.close()


# ---------------------------------------------------------------------------
# import sounddevice
# from scipy.io.wavfile import write         # it save audio as file   # wave  - can aslo use


# fps = 44100
# duration = 10  # sec.
# print('recording start')
# recording = sounddevice.rec( int(duration*fps), samplerate=fps, channels=2)
# sounddevice.wait()    # wait until recording
# print('done')
# write("output.wav", fps, recording)       # save the output file

