import tkinter as tk
import tkinter.messagebox as messagebox
import speech_recognition as sr
import threading
import pyaudio
import wave
import os
import platform

class SpeechToText(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Speech to Text Conversation")
        self.record_button = tk.Button(self, text="Start Recording", command=self.start_recording)
        self.record_button.pack(pady=20)

        self.stop_button = tk.Button(self, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.play_button = tk.Button(self, text="Play Recording", command=self.play_recording, state=tk.DISABLED)
        self.play_button.pack(pady=5)

        self.convert_button = tk.Button(self, text="Convert to Text", command=self.convert_audio_to_text, state=tk.DISABLED)
        self.convert_button.pack(pady=5)

        self.audio_file_path = "recording_audio.wav"
        self.recording = False

    def start_recording(self):
        self.recording = True
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.play_button.config(state=tk.DISABLED)
        self.convert_button.config(state=tk.DISABLED)

        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        self.frames = []

        self.recording_thread = threading.Thread(target=self.record)
        self.recording_thread.start()

    def record(self):
        while self.recording:
            data = self.stream.read(1024)
            self.frames.append(data)

    def stop_recording(self):
        self.recording = False
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

        wf = wave.open(self.audio_file_path, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        self.record_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.play_button.config(state=tk.NORMAL)
        self.convert_button.config(state=tk.NORMAL)

    def play_recording(self):
        if platform.system() == "Windows":
            os.system(f"start {self.audio_file_path}")
        elif platform.system() == "Darwin":
            os.system(f"open {self.audio_file_path}")
        else:
            os.system(f"xdg-open {self.audio_file_path}")

    def convert_audio_to_text(self):
        r = sr.Recognizer()
        with sr.AudioFile(self.audio_file_path) as source:
            audio_data = r.record(source)
            try:
                text = r.recognize_google(audio_data)
                messagebox.showinfo("Speech to Text", text)
            except sr.UnknownValueError:
                messagebox.showwarning("Speech to Text", "Could not understand audio")
            except sr.RequestError as e:
                messagebox.showerror("Speech to Text", f"Error occurred: {e}")

if __name__ == "__main__":
    app = SpeechToText()
    app.mainloop()
