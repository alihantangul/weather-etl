import os
import requests
import pandas as pd
from datetime import datetime, timezone

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API_KEY secret bulunamadı. GitHub Secrets içinde API_KEY tanımlanmış olmalı.")

cities = ["Istanbul", "Ankara", "Izmir", "Berlin", "London"]

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

def transform(data):
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "city": data["name"],
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"]
    }

rows = []

for city in cities:
    data = extract(city)
    rows.append(transform(data))

df = pd.DataFrame(rows)
df.to_csv("weather.csv", index=False, encoding="utf-8-sig")

print(df)