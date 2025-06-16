import os
import sqlite3
import pandas as pd
import requests

# Make sure 'data/' folder exists
os.makedirs("data", exist_ok=True)

def fetch_and_store_data():
    print("Fetching data from openFDA...")
    url = "https://api.fda.gov/drug/event.json?limit=10"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()["results"]

        # Flatten JSON
        df = pd.json_normalize(data)

        # Remove columns with list values
        for col in df.columns:
            if df[col].apply(lambda x: isinstance(x, list)).any():
                print(f"Dropping list-type column: {col}")
                df.drop(columns=[col], inplace=True)

        # Save to SQLite
        conn = sqlite3.connect("data/medintel.db")
        df.to_sql("drug_events", conn, if_exists="replace", index=False)
        conn.close()

        print("✔️ Cleaned data saved in data/medintel.db")
    else:
        print("❌ Failed to fetch data:", response.status_code)

if __name__ == "__main__":
    fetch_and_store_data()
