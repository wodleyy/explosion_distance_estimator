import argparse
import logging
import os
from datetime import datetime
from dateutil import parser as date_parser

from explosion_distance_estimator.config import DEFAULT_LAT, DEFAULT_LON, DEFAULT_DATE_OFFSET_DAYS, VIDEO_PATH, AUDIO_PATH, FRAMES_DIR
from explosion_distance_estimator.video.extract import extract_frames
from explosion_distance_estimator.video.detect_flash import detect_flash_frame
from explosion_distance_estimator.audio_utils import extract_audio, detect_sound_peak
from explosion_distance_estimator.weather import get_temperature
from explosion_distance_estimator.plotting import generate_plots
from explosion_distance_estimator.log_utils import log_results, cleanup
from explosion_distance_estimator.estimation import estimate_distance

def main():
    # Initialize the variables with proper defaults or from config.py
    video_path = VIDEO_PATH if VIDEO_PATH else 'default_video.mp4'
    audio_path = AUDIO_PATH if AUDIO_PATH else 'default_audio.wav'

    parser = argparse.ArgumentParser(description="Estimate explosion distance from video and audio.")
    parser.add_argument('--video', default=video_path, help='Path to the input video')
    parser.add_argument('--lat', type=float, default=DEFAULT_LAT, help='Latitude of explosion location')
    parser.add_argument('--lon', type=float, default=DEFAULT_LON, help='Longitude of explosion location')
    parser.add_argument('--temp', help='Temperature date (offset in days or date string like 2024-01-01)')
    parser.add_argument('--keep', action='store_true', help='Keep intermediate files')
    parser.add_argument('--plot', action='store_true', help='Generate plots')
    parser.add_argument('--outdir', default='output', help='Directory to save logs and output files')
    args = parser.parse_args()

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
    video_path = args.video
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
    logging.info(f"🎞️ Video: {video_path}")

    logging.info("📽️ Extracting frames...")
    try:
        fps, total_frames = extract_frames(video_path, FRAMES_DIR)
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
        extract_audio(video_path, audio_path)
        sound_time, y, sr = detect_sound_peak(audio_path)
    except Exception as e:
        logging.error(f"❌ Audio analysis failed: {e}")
        exit(1)

    logging.info("🌍 Fetching temperature...")
    try:
        temp, weather_date = get_temperature(LAT, LON, DATE_AS_OBJECT if DATE_AS_OBJECT else DATE_OFFSET_DAYS)
        if temp is None:
            raise ValueError("Temperature data is missing.")
    except Exception as e:
        logging.error(f"❌ Failed to fetch temperature data: {e}")
        exit(1)

    logging.info("📏 Calculating distance...")
    distance = estimate_distance(flash_time, sound_time, temp)

    if PLOT_OUTPUT:
        logging.info("📊 Generating plots...")
        generate_plots(brightness_values, flash_frame, y, sr, sound_time, fps)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_results(LOG_FILE, video_path, timestamp, flash_time, sound_time, temp, distance, LAT, LON, weather_date, KEEP_FILES)

    if not KEEP_FILES:
        logging.info("🧹 Cleaning up...")
        cleanup(FRAMES_DIR, audio_path)
    else:
        logging.info("📁 Keeping temporary files as requested.")

    logging.warning("\\n⚠️  DISCLAIMER:")
    logging.warning("This distance is an estimate based on the delay between visible and audible explosion evidence.")
    logging.warning("In general, real-world variance can range from 50 to 200 meters depending on recording conditions.")
