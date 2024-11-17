import cv2
import numpy as np
import pyautogui
import pyaudio
import wave
import threading
import time

def record_audio(audio_file="output_audio.wav", duration=120):
    chunk = 1024  # Dimensiunea bufferului
    format = pyaudio.paInt16  # Format audio 16-bit
    channels = 2  # Stereo
    rate = 44100  # Rata de esantionare

    p = pyaudio.PyAudio()

    # Configurare stream audio
    stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
    frames = []

    print("Incepem inregistrarea audio...")

    start_time = time.time()
    while time.time() - start_time < duration:
        data = stream.read(chunk)
        frames.append(data)

    print("Inregistrarea audio s-a terminat.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Salvare fisier audio
    with wave.open(audio_file, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b"".join(frames))

def record_screen(video_file="output_video.avi", duration=120):
    screen_width, screen_height = pyautogui.size()
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(video_file, fourcc, 20.0, (screen_width, screen_height))

    print("Incepem inregistrarea video...")

    start_time = time.time()
    while time.time() - start_time < duration:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)

    print("Inregistrarea video s-a terminat.")
    out.release()

def record_combined(audio_file="output_audio.wav", video_file="output_video.avi", duration=120):
    # Cream un thread pentru inregistrarea audio
    audio_thread = threading.Thread(target=record_audio, args=(audio_file, duration))
    audio_thread.start()

    # Inregistram video
    record_screen(video_file, duration)

    # Asteptam sa se termine thread-ul audio
    audio_thread.join()

    print("Inregistrarea combinata s-a terminat.")
