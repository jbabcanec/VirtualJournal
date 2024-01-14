# record.py

import pyaudio
import speech_recognition as sr
import queue

class ChunkedSpeechRecorder:
    def __init__(self, chunk_size=1024, format=pyaudio.paInt16, channels=1, rate=16000, buffer_duration=30):
        self.chunk_size = chunk_size
        self.format = format
        self.channels = channels
        self.rate = rate
        self.buffer_duration = buffer_duration
        self.buffer_size = int(self.rate / self.chunk_size * self.buffer_duration)
        self.audio_interface = pyaudio.PyAudio()
        self.audio_stream = self.audio_interface.open(
            format=self.format, channels=self.channels, rate=self.rate, input=True,
            frames_per_buffer=self.chunk_size, stream_callback=self.callback
        )
        self.queue = queue.Queue()
        self.is_recording = False
        self.buffer = b""  # Define buffer as an instance attribute
        self.recognized_text = []  # List to store recognized text

    def callback(self, in_data, frame_count, time_info, status):
        if self.is_recording:
            self.queue.put(in_data)
        return (None, pyaudio.paContinue)

    def start_recording(self):
        self.is_recording = True
        self.audio_stream.start_stream()

    def stop_recording(self):
        self.is_recording = False
        self.audio_stream.stop_stream()
        self.process_remaining_audio()  # Process any remaining audio in the buffer

    def process_audio_chunk(self):
        recognizer = sr.Recognizer()
        chunk_count = 0
        while self.is_recording or not self.queue.empty():
            audio_chunk = self.queue.get()
            self.buffer += audio_chunk
            chunk_count += 1

            if chunk_count >= self.buffer_size:
                self.process_buffer(self.buffer, recognizer)
                self.buffer = b""  # Reset buffer for next batch
                chunk_count = 0

    def process_remaining_audio(self):
        if self.buffer:
            self.process_buffer(self.buffer, sr.Recognizer())
            self.buffer = b""  # Reset buffer after processing

    def process_buffer(self, buffer, recognizer):
        try:
            audio_data = sr.AudioData(buffer, self.rate, self.audio_interface.get_sample_size(self.format))
            text = recognizer.recognize_google(audio_data)
            self.recognized_text.append(text)  # Store recognized text
        except sr.UnknownValueError:
            print("Audio not understood")
        except sr.RequestError as e:
            print(f"Speech recognition error; {e}")

    def get_recognized_text(self):
        return ' '.join(self.recognized_text)