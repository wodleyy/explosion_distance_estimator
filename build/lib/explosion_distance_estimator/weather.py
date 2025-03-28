import requests
from datetime import datetime, timedelta

def get_temperature(lat: float, lon: float, date_input) -> tuple[float, str]:
    if isinstance(date_input, int):
        target_date = datetime.utcnow() - timedelta(days=date_input)
    else:
        target_date = date_input

    date_str = target_date.strftime('%Y-%m-%d')
    url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        f"&hourly=temperature_2m&start_date={date_str}&end_date={date_str}&timezone=UTC"
    )

    response = requests.get(url)
    data = response.json()

    temp_c = data['hourly']['temperature_2m'][12] if 'hourly' in data else None
    print(f"🌡️ Temperature on {date_str} at noon: {temp_c}°C")
    return temp_c, date_str
