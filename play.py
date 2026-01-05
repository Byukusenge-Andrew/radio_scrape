import json
import os
import time

# MUST be before importing vlc
os.add_dll_directory(r"C:\Program Files\VideoLAN\VLC")

import vlc

FILE = "working_radios.json"

with open(FILE, "r", encoding="utf-8") as f:
    stations = json.load(f)

if not stations:
    print("No working stations found.")
    exit()

print("\nAvailable Radio Stations:\n")
for i, s in enumerate(stations):
    print(f"{i + 1}. {s['name']} ({s.get('country', 'Unknown')})")

choice = int(input("\nSelect station number: ")) - 1
if choice < 0 or choice >= len(stations):
    print("Invalid selection")
    exit()

station = stations[choice]
url = station["stream_url"]

print(f"\n▶ Playing: {station['name']}")
print("Press CTRL+C to stop\n")

# ✅ Proper VLC initialization
instance = vlc.Instance()
player = instance.media_player_new()
media = instance.media_new(url)
player.set_media(media)

player.play()

# Give VLC time to buffer
time.sleep(2)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n⏹ Stopped")
    player.stop()
