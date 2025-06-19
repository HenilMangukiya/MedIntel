import requests
import json
import os

def fetch_athena_indicator(indicator_code, save_as_json=True):
    url = f"https://ghoapi.azureedge.net/api/{indicator_code}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")

    data = response.json()['value']

    if save_as_json:
        os.makedirs("data/raw", exist_ok=True)
        path = f"data/raw/{indicator_code.lower()}_raw.json"
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"[✓] Saved data to {path}")

    return data

# Example usage
if __name__ == "__main__":
    indicator = input("Enter WHO Indicator Code (e.g., TUB_CDR): ")
    fetch_athena_indicator(indicator)
