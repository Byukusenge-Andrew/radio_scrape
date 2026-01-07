import os
import json
import subprocess

BASE_DIR = "radio_results_working"

def choose(options, title):
    print(f"\n{title}\n")
    for i, opt in enumerate(options):
        print(f"{i + 1}. {opt}")
    choice = int(input("\nSelect number: ")) - 1
    return options[choice]

def main():
    if not os.path.exists(BASE_DIR):
        print("No filtered radio results found.")
        return

    countries = [
        d for d in os.listdir(BASE_DIR)
        if os.path.isdir(os.path.join(BASE_DIR, d))
    ]

    if not countries:
        print("No countries available.")
        return

    country = choose(countries, "🌍 Available Countries")

    stations_file = os.path.join(BASE_DIR, country, "stations.json")
    with open(stations_file, "r", encoding="utf-8") as f:
        stations = json.load(f)

    if not stations:
        print("No stations in this country.")
        return

    print(f"\n📻 Stations in {country}:\n")
    for i, s in enumerate(stations):
        print(f"{i + 1}. {s['name']}")

    choice = int(input("\nSelect station: ")) - 1
    station = stations[choice]

    print(f"\n▶ Playing: {station['name']}")
    print("Press CTRL+C to stop\n")

    subprocess.run([
        "ffplay",
        "-nodisp",
        "-autoexit",
        station["stream_url"]
    ])

if __name__ == "__main__":
    main()
