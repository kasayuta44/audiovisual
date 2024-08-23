from datetime import datetime
import pyaudio
import wave
from multiprocessing import Process
import os

def vid():
    os.system(ffmpeg -f v4l2 -input_format mjpeg -video_size 1280x720 -framerate 30 -i /dev/video0 -t 30 -vcodec libx264 -pix_fmt yuv420p $(date +%Y-%m-%d_%H%M)output-video.mp4 )

def aud():
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second
    seconds = 10
    now = datetime.now()
    currenttime = now.strftime('%Y-%m-%d_%H%M')
    filename = currenttime + "audio-output.wav"

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

if __name__ == '__main__':
    p1 = Process(target=vid)
    p2 = Process(target=aud)
    p1.start()
    p2.start()