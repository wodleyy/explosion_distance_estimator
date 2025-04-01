
import matplotlib.pyplot as plt
import numpy as np
import librosa.display

def generate_plots(brightness_values, flash_frame, y, sr, sound_time, fps):
    times = np.arange(len(brightness_values)) / fps
    audio_times = np.arange(len(y)) / sr

    plt.figure(figsize=(10, 4))
    flash_time = flash_frame / fps

    plt.plot(times, brightness_values, label='Brightness', color='blue')
    plt.axvline(flash_time, color='red', linestyle='--', label='Flash Time')

    plt.annotate('Flash Detected',
                 xy=(flash_time, brightness_values[flash_frame]),
                 xytext=(flash_time - 1.5, brightness_values[flash_frame] + 5),
                 arrowprops=dict(arrowstyle='->', color='red'),
                 fontsize=10, color='red')

    baseline = np.mean(brightness_values[:flash_frame])
    plt.axhline(baseline, color='gray', linestyle='--', alpha=0.6, label='Baseline')

    plt.title('Brightness Over Time')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Brightness')
    plt.legend()
    plt.tight_layout()
    plt.savefig('brightness_plot.png')

    plt.figure(figsize=(10, 4))
    S = librosa.stft(y)
    S_dB = librosa.amplitude_to_db(abs(S), ref=np.max)

    librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='log', cmap='magma', vmin=-80, vmax=0)
    plt.axvline(sound_time, color='orange', linestyle='--', label='Sound Time')

    plt.annotate('Explosion Detected',
                 xy=(sound_time, 4000),
                 xytext=(sound_time - 1.5, 10000),
                 arrowprops=dict(arrowstyle='->', color='red'),
                 fontsize=10, color='red')

    plt.colorbar(format='%+2.0f dB', label='Intensity (dB)')
    plt.title('Audio Spectrogram')
    plt.xlabel('Time')
    plt.ylabel('Hz')
    plt.ylim(20, 16000)
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig('audio_spectrogram.png')
