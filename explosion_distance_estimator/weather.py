import requests
from datetime import datetime, timedelta

def get_temperature(lat, lon, date_input):
    """
    Fetches the temperature at noon for a given latitude, longitude, and date.
    `date_input` can be either a datetime object or an integer offset (e.g., 1 = yesterday).
    """

    # Handle offset or date input
    if isinstance(date_input, int):
        target_date = (datetime.utcnow() - timedelta(days=date_input)).strftime('%Y-%m-%d')
    elif isinstance(date_input, datetime):
        target_date = date_input.strftime('%Y-%m-%d')
    else:
        raise ValueError("date_input must be a datetime object or an int")

    # Use Open-Meteo archive API for historical data
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

        # Look for temperature at 12:00
        times = data["hourly"]["time"]
        temps = data["hourly"]["temperature_2m"]

        noon_temp = None
        for time, temp in zip(times, temps):
            if "12:00" in time:
                noon_temp = temp
                break

        if noon_temp is None:
            raise ValueError("Temperature data at noon not found.")

        print(f"🌡️ Temperature on {target_date} at noon: {noon_temp}°C")
        return noon_temp, target_date

    except Exception as e:
        raise RuntimeError(f"Failed to fetch temperature data: {e}")
