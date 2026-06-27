import os
import requests
import pandas as pd
from datetime import datetime, timezone

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API_KEY bulunamadı. GitHub Secrets içinde API_KEY olmalı.")

cities = ["Istanbul", "Ankara", "Izmir", "Berlin", "London"]

FILENAME = "weather.csv"


def extract(city):
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params, timeout=10)

    print(f"{city} status:", response.status_code)
    print(f"{city} response:", response.text)

    response.raise_for_status()

    return response.json()


def transform(data, timestamp):
    return {
        "timestamp_utc": timestamp,
        "city": data["name"],
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"]
    }


rows = []

run_timestamp = datetime.now(timezone.utc).isoformat()

for city in cities:
    data = extract(city)
    rows.append(transform(data, run_timestamp))


new_df = pd.DataFrame(rows)

# Eğer weather.csv daha önce varsa eski veriyi oku
if os.path.exists(FILENAME):
    old_df = pd.read_csv(FILENAME)

    # Eski veri + yeni veri birleşir
    final_df = pd.concat([old_df, new_df], ignore_index=True)

else:
    # İlk çalışmaysa sadece yeni veri yazılır
    final_df = new_df


# CSV'yi güncel haliyle tekrar kaydet
final_df.to_csv(FILENAME, index=False, encoding="utf-8-sig")

print(final_df)