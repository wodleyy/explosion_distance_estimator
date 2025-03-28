---

## Overview

The **Explosion Distance Estimator** is a Python tool that estimates the distance to an explosion in a video. It calculates the distance based on the delay between the visible flash and the sound of the blast, using video and audio analysis, real-world temperature data from Open-Meteo, and basic physics principles.

## Installation

Install this package locally with:

```bash
pip install explosion_distance_estimator
```

Then run:

```bash
explosion-distance-estimator --help
```

### Features:

- **Video Analysis**: Extracts frames from the video to detect the moment of the explosion (flash).
- **Audio Analysis**: Extracts the audio and detects the peak of the explosion's sound.
- **Temperature Data**: Fetches temperature data from [Open-Meteo](https://open-meteo.com) for the given date and location.
- **Distance Calculation**: Uses basic physics to estimate the distance to the explosion:
  ```
  v = 331 + 0.6 × T
  distance = (sound_time - flash_time) × v
  ```

---

### Basic run

```
python3 explosion_distance_estimator.py
```

Uses:
- Default video: `test_explosion.mp4`
- Today’s date
- Kyiv coordinates (lat: 50.4501, lon: 30.5234)

---

### Full CLI options

```
python3 explosion_distance_estimator.py   --video explosion.mp4   --lat 47.0951   --lon 37.5496   --temp 1   --plot   --keep   --outdir output
```

**Options:**

| Flag         | Description |
|--------------|-------------|
| `--video`    | Path to the video file (MP4 with audio) |
| `--temp`     | Weather date: either a day offset (`0 = today`, `1 = yesterday`) or exact date (`2024-03-27`) |
| `--lat`      | Latitude of the explosion location |
| `--lon`      | Longitude of the explosion location |
| `--plot`     | Generate 3 plots: brightness, audio spectrogram, and combined view |
| `--keep`     | Keep extracted frames and audio after analysis |
| `--outdir`   | Output folder for logs, plots, and CSV (default: `output`) |

---

## Output

- **Plots**: `brightness_plot.png`, `audio_spectrogram.png`, `combined_plot.png` (if `--plot` is set)
- **Run log**: `output/run_YYYYMMDD_HHMMSS.log`
- **CSV log**: `output/log.csv`
- Temporary frames and audio (only if `--keep` is used)

---

## Example Scenarios

```
# Detect explosion from a video recorded yesterday in Mariupol
python3 explosion_distance_estimator.py   --video mariupol_blast.mp4   --temp 1   --lat 47.0951   --lon 37.5496   --plot

# Estimate using a historical date and keep all intermediate files
python3 explosion_distance_estimator.py   --temp 26.03.2025   --keep
```

---

## How It Works

1. **Extract frames** from the video and analyze brightness
2. **Detect the flash moment** (spike in brightness)
3. **Extract audio** and detect the sound peak (blast)
4. **Fetch temperature** for the provided date/location via [Open-Meteo](https://open-meteo.com)
5. **Estimate the distance** using basic physics:
   ```
   v = 331 + 0.6 × T
   distance = (sound_time - flash_time) × v
   ```

---

