import requests

def search_indicators(keyword):
    url = "https://ghoapi.azureedge.net/api/Indicator"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception("Failed to fetch indicators")

    indicators = response.json().get("value", [])

    print(f"Total indicators fetched: {len(indicators)}\n")

    filtered = [
        {"code": i.get("IndicatorCode", "N/A"), "title": i.get("Title", "").strip()}
        for i in indicators
        if i.get("Title") and keyword.lower() in i["Title"].lower()
    ]

    return filtered

# Run as script
if __name__ == "__main__":
    keyword = input("Enter search keyword (e.g., malaria, hiv, flu): ")
    results = search_indicators(keyword)

    if not results:
        print(f"[✘] No indicators found matching: '{keyword}'")
    else:
        print(f"[✓] Found {len(results)} matching indicators:\n")
        for r in results:
            print(f"{r['code']} --> {r['title']}")
