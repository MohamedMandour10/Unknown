import sounddevice as sd
import numpy as np
import wave
import pyaudio
import librosa
from joblib import load
from scipy import stats

class AudioRecorder:
    def __init__(self,file_name , duration=5, sample_rate=44100):
        self.duration = duration
        self.sample_rate = sample_rate
        self.file_name = file_name
        self.data = None



    def record_audio(self, duration=4, channels=1, sample_rate=44100, chunk_size=1024):
        """
        Records audio from the default input device for the specified duration.

        Args:
            duration (float): The duration of the recording in seconds (default is 4).
            channels (int): The number of audio channels (default is 1).
            sample_rate (int): The sample rate of the audio (default is 44100).
            chunk_size (int): The number of frames per buffer (default is 1024).
        """

        # Initialize PyAudio
        p = pyaudio.PyAudio()

        # Open stream
        stream = p.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk_size)

        print("Recording...")

        # Buffer for storing audio frames
        frames = []

        # Record audio frames
        for i in range(0, int(sample_rate / chunk_size * duration)):
            data = stream.read(chunk_size)
            frames.append(data)

        print("Recording done.")

        # Stop stream
        stream.stop_stream()
        stream.close()

        # Terminate PyAudio
        p.terminate()

        # Save the recorded audio as a WAV file
        with wave.open(self.file_name, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(frames))
        

    def get_audio_data(self):
        # Load the audio file
        data, sr = librosa.load(self.file_name, sr=self.sample_rate)
        return data , sr


