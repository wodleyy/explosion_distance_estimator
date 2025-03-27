# === Structure ===
# explosion_estimator/
# ├── explosion_distance_estimator.py
# ├── config.py
# ├── video/
# │   ├── __init__.py
# │   ├── extract.py
# │   └── detect_flash.py
# ├── audio_utils.py
# ├── weather.py
# ├── plotting.py
# ├── log_utils.py
# └── estimation.py

import argparse
import logging
import os
from datetime import datetime
from dateutil import parser as date_parser

from config import DEFAULT_LAT, DEFAULT_LON, DEFAULT_DATE_OFFSET_DAYS, VIDEO_PATH, AUDIO_PATH, FRAMES_DIR
from video.extract import extract_frames
from video.detect_flash import detect_flash_frame
from audio_utils import extract_audio, detect_sound_peak
from weather import get_temperature
from plotting import generate_plots
from log_utils import log_results, cleanup
from estimation import estimate_distance

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Estimate explosion distance from video and audio.")
    parser.add_argument('--video', default=VIDEO_PATH, help='Path to the input video')
    parser.add_argument('--lat', type=float, default=DEFAULT_LAT, help='Latitude of explosion location')
    parser.add_argument('--lon', type=float, default=DEFAULT_LON, help='Longitude of explosion location')
    parser.add_argument('--temp', help='Temperature date (offset in days or date string like 2024-01-01)')
    parser.add_argument('--keep', action='store_true', help='Keep intermediate files')
    parser.add_argument('--plot', action='store_true', help='Generate plots')
    parser.add_argument('--outdir', default='output', help='Directory to save logs and output files')
    args = parser.parse_args()

    # Setup output directory and logging
    os.makedirs(args.outdir, exist_ok=True)
    timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_path = os.path.join(args.outdir, f"run_{timestamp_str}.log")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ]
    )

    LAT = args.lat
    LON = args.lon
    VIDEO_PATH = args.video
    KEEP_FILES = args.keep
    PLOT_OUTPUT = args.plot
    LOG_FILE = os.path.join(args.outdir, 'log.csv')

    DATE_AS_OBJECT = None
    DATE_OFFSET_DAYS = DEFAULT_DATE_OFFSET_DAYS

    if args.temp:
        try:
            DATE_OFFSET_DAYS = int(args.temp)
        except ValueError:
            try:
                DATE_AS_OBJECT = date_parser.parse(args.temp, dayfirst=True)
                DATE_OFFSET_DAYS = None
            except ValueError:
                parser.error("Invalid format for --temp (use int or date string)")

    logging.info(f"📅 Weather for {(DATE_AS_OBJECT.strftime('%Y-%m-%d') if DATE_AS_OBJECT else str(DATE_OFFSET_DAYS)+' day(s) ago')} at lat: {LAT}, lon: {LON}")
    logging.info(f"🎞️ Video: {VIDEO_PATH}")

    logging.info("📽️ Extracting frames...")
    try:
        fps, total_frames = extract_frames(VIDEO_PATH, FRAMES_DIR)
        if total_frames == 0:
            raise ValueError("No frames extracted.")
    except Exception as e:
        logging.error(f"❌ Frame extraction failed: {e}")
        exit(1)

    logging.info("✨ Detecting flash frame...")
    try:
        flash_frame, brightness_values = detect_flash_frame(FRAMES_DIR)
        flash_time = flash_frame / fps
    except Exception as e:
        logging.error(f"❌ Flash detection failed: {e}")
        exit(1)

    logging.info("🔊 Extracting and analyzing audio...")
    try:
        extract_audio(VIDEO_PATH, AUDIO_PATH)
        sound_time, y, sr = detect_sound_peak(AUDIO_PATH)
    except Exception as e:
        logging.error(f"❌ Audio analysis failed: {e}")
        exit(1)

    logging.info("🌍 Fetching temperature...")
    try:
        temp, weather_date = get_temperature(LAT, LON, DATE_AS_OBJECT if DATE_AS_OBJECT else DATE_OFFSET_DAYS)
    except Exception as e:
        logging.error(f"❌ Failed to fetch temperature data: {e}")
        exit(1)

    logging.info("📏 Calculating distance...")
    distance = estimate_distance(flash_time, sound_time, temp)

    if PLOT_OUTPUT:
        logging.info("📊 Generating plots...")
        generate_plots(brightness_values, flash_frame, y, sr, sound_time, fps)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_results(LOG_FILE, VIDEO_PATH, timestamp, flash_time, sound_time, temp, distance, LAT, LON, weather_date, KEEP_FILES)

    if not KEEP_FILES:
        logging.info("🧹 Cleaning up...")
        cleanup(FRAMES_DIR, AUDIO_PATH)
    else:
        logging.info("📁 Keeping temporary files as requested.")

    logging.warning("\n⚠️  DISCLAIMER:")
    logging.warning("This distance is an estimate based on the delay between visible and audible explosion evidence.")
    logging.warning("In general, real-world variance can range from 50 to 200 meters depending on recording conditions.")