# record.py

import pyaudio
import speech_recognition as sr
import queue
from PyQt5.QtCore import QObject, pyqtSignal

class ChunkedSpeechRecorder(QObject):
    recording_successful = pyqtSignal(str)  # Signal for successful recording
    recording_error = pyqtSignal()  # Signal for recording errors

    def __init__(self, chunk_size=1024, format=pyaudio.paInt16, channels=1, rate=16000, buffer_duration=30):
        super(ChunkedSpeechRecorder, self).__init__()
        print("Initializing ChunkedSpeechRecorder")
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
        self.buffer = b""
        self.recognized_text = []  # List to store recognized text

    def callback(self, in_data, frame_count, time_info, status):
        if self.is_recording:
            self.queue.put(in_data)
            #print("Audio data added to queue")
        return (None, pyaudio.paContinue)

    def start_recording(self):
        print("Starting recording")
        self.is_recording = True
        self.audio_stream.start_stream()

    def stop_recording(self):
        print("Stopping recording")
        self.is_recording = False
        self.audio_stream.stop_stream()
        self.process_remaining_audio()  # Process any remaining audio in the buffer

    def process_audio_chunk(self):
        print("Processing audio chunk")
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
        print("Processing remaining audio")
        if self.buffer:
            self.process_buffer(self.buffer, sr.Recognizer())
            self.buffer = b""  # Reset buffer after processing

    def process_buffer(self, buffer, recognizer):
        print("Processing buffer")
        try:
            audio_data = sr.AudioData(buffer, self.rate, self.audio_interface.get_sample_size(self.format))
            text = recognizer.recognize_google(audio_data)
            self.recognized_text.append(text)  # Store recognized text
            self.recording_successful.emit(text)  # Emit only on successful recognition
        except sr.UnknownValueError:
            print("Audio not understood")
            self.recording_error.emit()  # Emit error signal
        except sr.RequestError as e:
            print(f"Speech recognition error; {e}")
            self.recording_error.emit()  # Emit error signal

    def get_recognized_text(self):
        return ' '.join(self.recognized_text)