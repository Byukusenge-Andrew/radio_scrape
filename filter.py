import json
import requests

INPUT_FILE = "radio_station.json"
OUTPUT_FILE = "working_radios.json"

def is_working(url, timeout=5):
    try:
        r = requests.get(url, stream=True, timeout=timeout)
        return r.status_code == 200
    except:
        import json
        import requests
        import os
        import sys

        ROOT = sys.argv[1] if len(sys.argv) > 1 else "radio_results"

        def is_working(url, timeout=5):
            try:
                r = requests.get(url, stream=True, timeout=timeout)
                return r.status_code == 200
            except:
                return False


        def process_file(input_path):
            try:
                with open(input_path, "r", encoding="utf-8") as f:
                    stations = json.load(f)
            except Exception as e:
                print(f"Failed to read {input_path}: {e}")
                return

            working = []

            for s in stations:
                url = (
                    s.get("stream_url")
                    or s.get("stream")
                    or s.get("url")
                    or s.get("play_url")
                )
                if not url:
                    continue

                name = s.get("name") or s.get("title") or input_path
                if is_working(url):
                    print(f"[✔ WORKING] {name} — {url}")
                    working.append(s)
                else:
                    print(f"[✘ DEAD] {name} — {url}")

            output_file = os.path.join(os.path.dirname(input_path), "working_radios.json")
            try:
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(working, f, indent=4)
                print(f"\nSaved {len(working)} working stations → {output_file}\n")
            except Exception as e:
                print(f"Failed to write {output_file}: {e}")


        def main():
            if not os.path.isdir(ROOT):
                print(f"Root folder not found: {ROOT}")
                return

            # Look for common station JSON filenames in country subfolders
            target_names = {"stations.json", "radio_station.json", "radio_stations.json"}

            found = 0
            for dirpath, dirnames, filenames in os.walk(ROOT):
                for name in filenames:
                    if name in target_names:
                        input_path = os.path.join(dirpath, name)
                        print(f"Processing {input_path}")
                        process_file(input_path)
                        found += 1

            if found == 0:
                print(f"No station JSON files found under {ROOT}")


        if __name__ == "__main__":
            main()
