import os
import librosa
import numpy as np

def extract_audio(video_path: str, output_wav: str) -> None:
    os.system(f"ffmpeg -y -i {video_path} -q:a 0 -map a {output_wav}")

def detect_sound_peak(audio_path: str) -> tuple[float, np.ndarray, int]:
    y, sr = librosa.load(audio_path, sr=None)
    frame_length = 2048
    hop_length = 512
    energy = np.array([
        sum(abs(y[i:i+frame_length]**2))
        for i in range(0, len(y), hop_length)
    ])
    peak_index = np.argmax(energy)
    sound_time = (peak_index * hop_length) / sr
    return sound_time, y, sr
