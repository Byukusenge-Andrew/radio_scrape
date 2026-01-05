import os
import json
import csv
import requests

INPUT_DIR = "radio_results"
OUTPUT_DIR = "radio_results_working"
TIMEOUT = 5  # seconds to wait for response

def is_working(url):
    try:
        r = requests.get(url, stream=True, timeout=TIMEOUT)
        return r.status_code == 200
    except:
        return False

def filter_country(country_folder):
    input_json = os.path.join(INPUT_DIR, country_folder, "stations.json")
    if not os.path.exists(input_json):
        print(f"✘ No stations.json in {country_folder}, skipping")
        return

    with open(input_json, "r", encoding="utf-8") as f:
        stations = json.load(f)

    working = []
    print(f"\n🔍 Checking streams for {country_folder} ({len(stations)} stations)...")
    for s in stations:
        url = s.get("stream_url")
        if url and is_working(url):
            print(f"[✔] {s['name']}")
            working.append(s)
        else:
            print(f"[✘] {s['name']}")

    if working:
        folder = os.path.join(OUTPUT_DIR, country_folder)
        os.makedirs(folder, exist_ok=True)

        # Save JSON
        with open(os.path.join(folder, "stations.json"), "w", encoding="utf-8") as f:
            json.dump(working, f, indent=4, ensure_ascii=False)

        # Save CSV
        with open(os.path.join(folder, "stations.csv"), "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=working[0].keys())
            writer.writeheader()
            writer.writerows(working)

        print(f"✔ Saved {len(working)} working stations → {folder}")
    else:
        print(f"✘ No working stations found for {country_folder}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    countries = [d for d in os.listdir(INPUT_DIR) if os.path.isdir(os.path.join(INPUT_DIR, d))]

    for country in countries:
        filter_country(country)

if __name__ == "__main__":
    main()
