import os
import csv

def log_results(file, video, timestamp, flash_time, sound_time, temp, distance, lat, lon, date, keep):
    file_exists = os.path.exists(file)
    with open(file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow([
                'Timestamp', 'Video File', 'Flash Time', 'Sound Time',
                'Temperature (C)', 'Distance (m)', 'Latitude', 'Longitude',
                'Weather Date', 'Keep Files'
            ])
        writer.writerow([
            timestamp, video, flash_time, sound_time, temp,
            distance, lat, lon, date, keep
        ])

def cleanup(frames_dir, audio_path):
    import shutil
    shutil.rmtree(frames_dir, ignore_errors=True)
    print("🧹 Frame images deleted.")

    if os.path.exists(audio_path):
        os.remove(audio_path)
        print("🧹 Audio file deleted.")
