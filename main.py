import requests
import pandas as pd
import os

API_KEY = os.getenv("API_KEY")

cities = ["Istanbul", "Ankara", "Izmir", "Berlin", "London"]

def extract(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    return requests.get(url).json()

def transform(data):
    return {
        "city": data["name"],
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"]
    }

rows = []

for c in cities:
    data = extract(c)

    if "main" in data:
        rows.append(transform(data))

df = pd.DataFrame(rows)
df.to_csv("weather.csv", index=False, encoding="utf-8-sig")

print(df)
