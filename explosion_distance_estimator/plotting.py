import matplotlib.pyplot as plt
import numpy as np
import librosa.display
import warnings

def generate_plots(brightness_values, flash_frame, y, sr, sound_time, fps):
    times = np.arange(len(brightness_values)) / fps
    audio_times = np.arange(len(y)) / sr

    # Brightness plot
    plt.figure(figsize=(10, 4))
    plt.plot(times, brightness_values, label='Brightness', color='blue')
    plt.axvline(flash_frame / fps, color='red', linestyle='--', label='Flash Time')
    plt.title('Brightness Over Time')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Brightness')
    plt.legend()
    plt.tight_layout()
    plt.savefig('brightness_plot.png')

    # Audio plot
    plt.figure(figsize=(10, 4))
    S = librosa.stft(y)
    S_dB = librosa.amplitude_to_db(abs(S), ref=np.max)

    librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='log', cmap='magma', vmin=-80, vmax=0)
    plt.axvline(sound_time, color='orange', linestyle='--', label='Sound Time')
    plt.colorbar(format='%+2.0f dB', label='Intensity (dB)')
    plt.title('Audio Spectrogram')
    plt.xlabel('Time')
    plt.ylabel('Hz')
    plt.ylim(20, 16000)  # log scale, so set sensible bounds
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig('audio_spectrogram.png')

    # Combined view
    plt.figure(figsize=(10, 4))
    ax = plt.gca()

    plt.plot(times, brightness_values, label='Brightness', color='red')

    flash_t = flash_frame / fps
    plt.axvline(flash_t, color='green', linestyle='--', label='Flash Time')
    plt.axvline(sound_time, color='blue', linestyle='--', label='Sound Time')

    mid_y = ax.get_ylim()[1] * 0.8  # 80% up the y-axis
    ax.annotate(
        '', xy=(flash_t, mid_y), xytext=(sound_time, mid_y),
        arrowprops=dict(arrowstyle='<->', color='black', linestyle='dashed')
    )

    delay = sound_time - flash_t
    ax.text(
        (flash_t + sound_time) / 2, mid_y + 0.05 * mid_y,
        f'{delay:.2f} sec delay',
        ha='center', va='bottom', fontsize=10, color='black'
    )

    formula_text = f'distance = {delay:.2f} × (331 + 0.6 × T)'
    plt.text(0.98, 0.02, formula_text,
             transform=plt.gca().transAxes,
             fontsize=9, color='gray', ha='right', va='bottom',
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))

    plt.title('Flash and Sound Timeline')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.tight_layout()
    plt.savefig('combined_plot.png')
