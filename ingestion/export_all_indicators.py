import requests
import pandas as pd

def export_indicators_to_csv():
    url = "https://ghoapi.azureedge.net/api/Indicator"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Failed to fetch indicators")

    indicators = response.json().get("value", [])

    df = pd.json_normalize(indicators)
    df.to_csv("data/all_indicators.csv", index=False)
    print(f"[✓] Exported {len(df)} indicators to data/all_indicators.csv")

if __name__ == "__main__":
    export_indicators_to_csv()
