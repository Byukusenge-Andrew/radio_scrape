import json
import requests

INPUT_FILE = "radio_station.json"
OUTPUT_FILE = "working_radios.json"

def is_working(url, timeout=5):
    try:
        r = requests.get(url, stream=True, timeout=timeout)
        return r.status_code == 200
    except:
        return False


with open(INPUT_FILE, "r", encoding="utf-8") as f:
    stations = json.load(f)

working = []

for s in stations:
    url = s.get("stream_url")
    if not url:
        continue

    if is_working(url):
        print(f"[✔ WORKING] {s['name']}")
        working.append(s)
    else:
        print(f"[✘ DEAD] {s['name']}")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(working, f, indent=4)

print(f"\nSaved {len(working)} working stations → {OUTPUT_FILE}")
