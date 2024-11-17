import numpy as np
import wave

def analyze_audio(audio_file="final_audio.wav", output_file="audio_analysis.txt"):
    try:
        # Deschide fisierul audio
        with wave.open(audio_file, "rb") as wf:
            n_channels = wf.getnchannels()
            sample_width = wf.getsampwidth()
            n_frames = wf.getnframes()

            # Citeste datele audio
            audio_data = wf.readframes(n_frames)
            dtype = np.int16 if sample_width == 2 else np.int8
            audio_array = np.frombuffer(audio_data, dtype=dtype)

            # Daca sunt mai multe canale, calculeaza media între ele
            if n_channels > 1:
                audio_array = np.mean(audio_array.reshape(-1, n_channels), axis=1)

            # Calculul nivelurilor de amplitudine
            min_amplitude = np.min(np.abs(audio_array))
            max_amplitude = np.max(np.abs(audio_array))
            mean_amplitude = np.mean(np.abs(audio_array))

            # Scrierea rezultatelor in fișier
            with open(output_file, "w") as f:
                f.write(f"Nivel minim de amplitudine: {min_amplitude}\n")
                f.write(f"Nivel maxim de amplitudine: {max_amplitude}\n")
                f.write(f"Nivel mediu de amplitudine: {mean_amplitude:.2f}\n")

            print(f"Analiza audio s-a terminat. Rezultatele au fost salvate in {output_file}.")
    except FileNotFoundError:
        print(f"Eroare: Fisierul audio {audio_file} nu a fost gasit.")
    except Exception as e:
        print(f"A aparut o eroare in timpul analizei audio: {e}")
