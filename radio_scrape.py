import requests
import csv
import json
import argparse

BASE_URL = "https://de1.api.radio-browser.info/json"


def fetch_all(limit):
    url = f"{BASE_URL}/stations"
    return requests.get(url).json()[:limit]


def fetch_by_country(country, limit):
    url = f"{BASE_URL}/stations/bycountry/{country}"
    return requests.get(url).json()[:limit]


def search_by_name(name, limit):
    url = f"{BASE_URL}/stations/search"
    params = {"name": name}
    return requests.get(url, params=params).json()[:limit]


def clean_data(stations):
    cleaned = []
    for s in stations:
        cleaned.append({
            "name": s.get("name"),
            "stream_url": s.get("url"),
            "homepage": s.get("homepage"),
            "country": s.get("country"),
            "language": s.get("language"),
            "tags": s.get("tags"),
            "codec": s.get("codec"),
            "bitrate": s.get("bitrate")
        })
    return cleaned


def save_csv(data, filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="All-in-One Radio Station Scraper")
    parser.add_argument("--country", help="Search by country")
    parser.add_argument("--name", help="Search by station name")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--output", default="radio_station")
    args = parser.parse_args()

    if args.country:
        stations = fetch_by_country(args.country, args.limit)
    elif args.name:
        stations = search_by_name(args.name, args.limit)
    else:
        stations = fetch_all(args.limit)

    data = clean_data(stations)

    save_csv(data, args.output + ".csv")
    save_json(data, args.output + ".json")

    print(f"[✔] Saved {len(data)} radio stations")
    print(f"[✔] Files: {args.output}.csv , {args.output}.json")


if __name__ == "__main__":
    main()
