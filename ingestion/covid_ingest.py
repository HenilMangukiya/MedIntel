import requests
import pandas as pd
import sqlite3
import os

# Make sure data folder exists
os.makedirs("data", exist_ok=True)

def fetch_and_store_covid_data():
    print("Fetching COVID data...")
    url = "https://disease.sh/v3/covid-19/countries"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        df = pd.json_normalize(data)

        # Optional: Select important columns
        keep_cols = [
            "country", "cases", "todayCases", "deaths", "todayDeaths",
            "recovered", "active", "critical", "tests", "population", "continent"
        ]
        df = df[keep_cols]

        conn = sqlite3.connect("data/medintel.db")
        df.to_sql("covid_data", conn, if_exists="replace", index=False)
        conn.close()

        print("✔️ COVID data saved in 'covid_data' table.")
    else:
        print("❌ Failed to fetch COVID data:", response.status_code)

if __name__ == "__main__":
    fetch_and_store_covid_data()
