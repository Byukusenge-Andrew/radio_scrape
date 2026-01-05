import requests
import json
import csv
import os

BASE_URL = "https://de1.api.radio-browser.info/json"
OUTPUT_DIR = "radio_results"
LIMIT_PER_COUNTRY = 500  # Scrape as many as possible

# Countries with popular stations
COUNTRIES = {
    "United_Kingdom": ["BBC", "Capital", "Classic FM"],
    "United_States": ["CNN", "NPR", "iHeartRadio"],
    "Germany": ["DW", "Bayern 3"],
    "France": ["France 24", "RFI", "NRJ"],
    "Canada": ["CBC", "Radio Canada"],
    "Australia": ["ABC", "Triple J"],
    "Kenya": [],
    "Rwanda": [],
    "Tanzania": []
}

def fetch_by_country(country, limit):
    url = f"{BASE_URL}/stations/bycountry/{country.replace('_',' ')}"
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        return r.json()[:limit]
    except Exception as e:
        print(f"✘ Failed to fetch {country}: {e}")
        return []

def search_by_name(name, limit=20):
    url = f"{BASE_URL}/stations/search"
    try:
        r = requests.get(url, params={"name": name}, timeout=15)
        r.raise_for_status()
        return r.json()[:limit]
    except Exception as e:
        print(f"✘ Failed to search {name}: {e}")
        return []

def clean(stations):
    seen = set()
    cleaned = []
    for s in stations:
        url = s.get("url")
        if not url or url in seen:
            continue
        seen.add(url)
        cleaned.append({
            "name": s.get("name"),
            "stream_url": url,
            "homepage": s.get("homepage"),
            "country": s.get("country"),
            "language": s.get("language"),
            "tags": s.get("tags"),
            "codec": s.get("codec"),
            "bitrate": s.get("bitrate")
        })
    return cleaned

def save(country, data):
    folder = os.path.join(OUTPUT_DIR, country)
    os.makedirs(folder, exist_ok=True)

    json_path = os.path.join(folder, "stations.json")
    csv_path = os.path.join(folder, "stations.csv")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for country, famous_radios in COUNTRIES.items():
        folder = os.path.join(OUTPUT_DIR, country)

        # Skip already scraped
        if os.path.exists(folder):
            print(f"⏭ Skipping {country} (already scraped)")
            continue

        print(f"\n🌍 Scraping {country.replace('_', ' ')}")

        stations = fetch_by_country(country, LIMIT_PER_COUNTRY)

        # Add famous radios by name
        for radio in famous_radios:
            stations.extend(search_by_name(radio, 20))

        data = clean(stations)

        if data:
            save(country, data)
            print(f"✔ Saved {len(data)} stations")
        else:
            print("✘ No stations found")

if __name__ == "__main__":
    main()
