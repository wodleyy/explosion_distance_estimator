import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display

def generate_plots(brightness_values, flash_frame, y, sr, sound_time, fps):
    # Brightness timeline
    times = np.arange(len(brightness_values)) / fps
    plt.figure(figsize=(10, 4))
    plt.plot(times, brightness_values, label='Brightness')
    plt.axvline(flash_frame / fps, color='r', linestyle='--', label='Flash Time')
    plt.title('Brightness Over Time')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Brightness')
    plt.legend()
    plt.tight_layout()
    plt.savefig('brightness_plot.png')

    # Audio spectrogram
    plt.figure(figsize=(10, 4))
    S = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    librosa.display.specshow(S, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.axvline(sound_time, color='orange', linestyle='--', label='Sound Time')
    plt.title('Audio Spectrogram')
    plt.legend()
    plt.tight_layout()
    plt.savefig('audio_spectrogram.png')

    # Combined view
    plt.figure(figsize=(10, 4))
    plt.plot(times, brightness_values, label='Brightness')
    plt.axvline(flash_frame / fps, color='red', linestyle='--', label='Flash Time')
    plt.axvline(sound_time, color='orange', linestyle='--', label='Sound Time')
    plt.title('Flash and Sound Timeline')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Brightness')
    plt.legend()
    delay = sound_time - (flash_frame / fps)
    formula_text = f'distance = {delay:.2f} × (331 + 0.6 × T)'
    plt.text(0.98, 0.02, formula_text,
             transform=plt.gca().transAxes,
             fontsize=9, color='gray', ha='right', va='bottom',
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))
    plt.tight_layout()
    plt.savefig('combined_plot.png')
