import json
import requests
import os

# Configuration
INPUT_FILE = "radio_station.json"
OUTPUT_FILE = "working_radios.json"

def is_working(url, timeout=5):
    """
    Checks if a stream URL is active.
    Returns True if status code is 200, otherwise False.
    """
    try:
        # stream=True ensures we don't download the whole stream
        r = requests.get(url, stream=True, timeout=timeout)
        r.close()
        return r.status_code == 200
    except Exception:
        return False

def process_file(input_path):
    if not os.path.exists(input_path):
        print(f"Error: Could not find '{input_path}' in the current directory.")
        return

    print(f"--- Processing: {input_path} ---")
    
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            stations = json.load(f)
    except Exception as e:
        print(f"Failed to read file: {e}")
        return

    working_stations = []

    for s in stations:
        # Check various common keys for the URL
        url = (
            s.get("stream_url")
            or s.get("stream")
            or s.get("url")
            or s.get("play_url")
        )

        if not url:
            continue

        name = s.get("name") or s.get("title") or "Unknown Station"
        
        if is_working(url):
            print(f"[✔ WORKING] {name}")
            working_stations.append(s)
        else:
            print(f"[✘ DEAD]    {name}")

    if working_stations:
        try:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(working_stations, f, indent=4)
            print(f"\nSuccess! Saved {len(working_stations)} stations to '{OUTPUT_FILE}'")
        except Exception as e:
            print(f"Failed to write output file: {e}")
    else:
        print("\nNo working stations found.")

if __name__ == "__main__":
    process_file(INPUT_FILE)