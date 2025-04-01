
import requests
from datetime import datetime, timedelta

def get_temperature(lat, lon, date_input):
    """
    Fetches temperature for a given latitude, longitude, and date.
    - Uses forecast API if date is today.
    - Uses archive API if date is in the past.
    If noon data is missing, uses the closest available hour.
    """

    if isinstance(date_input, int):
        date_obj = datetime.utcnow() - timedelta(days=date_input)
    elif isinstance(date_input, datetime):
        date_obj = date_input
    else:
        raise ValueError("date_input must be a datetime object or an int")

    target_date = date_obj.strftime('%Y-%m-%d')
    today_str = datetime.utcnow().strftime('%Y-%m-%d')
    is_today = target_date == today_str

    if is_today:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            "&hourly=temperature_2m"
            "&timezone=auto"
        )
    else:
        url = (
            "https://archive-api.open-meteo.com/v1/archive"
            f"?latitude={lat}&longitude={lon}"
            f"&start_date={target_date}&end_date={target_date}"
            "&hourly=temperature_2m"
            "&timezone=auto"
        )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Extract hourly data
        hourly = data.get("hourly", {})
        times = hourly.get("time", [])
        temps = hourly.get("temperature_2m", [])

        if not times or not temps:
            raise ValueError("Hourly temperature data is missing")

        noon_temp = None
        for time, temp in zip(times, temps):
            if "12:00" in time:
                noon_temp = temp
                break

        if noon_temp is None:
            from datetime import time as dtime
            target_hour = 12
            valid_indices = [i for i, t in enumerate(temps) if temps[i] is not None]
            if not valid_indices:
                raise ValueError("All temperature data points are None")

            closest_idx = min(
                valid_indices,
                key=lambda i: abs(datetime.fromisoformat(times[i]).time().hour - target_hour)
            )
            noon_temp = temps[closest_idx]
            print(f"⚠️ Noon temperature not found — using closest hour ({times[closest_idx]})")

        print(f"🌡️ Temperature on {target_date}: {noon_temp}°C")
        return noon_temp, target_date

    except Exception as e:
        raise RuntimeError(f"Failed to fetch temperature data: {e}")
