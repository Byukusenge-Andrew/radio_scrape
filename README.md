# Radio Scrape 📻

A Python-based radio station scraper and player that fetches, filters, and plays internet radio streams from the Radio Browser API.

## DockerHub repository 

[https://hub.docker.com/r/drefault/radio_player](https://hub.docker.com/r/drefault/radio_player)

## Terminal Player Requirements(Windows)

- Python
- VLC 64-bit(add it to your env)





## Features

- 🌍 **Scrape Radio Stations** - Fetch radio stations by country, name, or get all stations
- ✅ **Filter Working Streams** - Automatically test and filter out dead/broken radio streams
- 🎵 **Play Radio Stations** - Interactive CLI player to browse and play working radio stations
- 💾 **Multiple Output Formats** - Save results in both JSON and CSV formats
- 🔄 **Multi-threaded Processing** - Faster scraping and filtering with concurrent operations

## Project Structure

```
radio_scrape/
├── app.py                   # Flask web application
├── static/                  # Web interface files
│   ├── index.html          # Main HTML page
│   ├── style.css           # Styles and animations
│   └── app.js              # Frontend JavaScript
├── radio_scrape.py          # Main scraper to fetch radio stations
├── multi_scrape.py          # Multi-threaded version of the scraper
├── filter.py                # Filter working radio streams
├── multi_filter.py          # Multi-threaded stream filter
├── play.py                  # Simple radio player
├── play_m.py                # Multi-country radio player
├── Dockerfile               # Docker container configuration
├── docker-compose.yml       # Docker Compose setup
├── .dockerignore            # Docker build exclusions
├── radio_station.json       # Sample radio stations data
├── working_radios.json      # Filtered working radio stations
├── radio_results/           # Scraped results by country
├── radio_results_working/   # Filtered working stations by country
└── requirements.txt         # Python dependencies
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd radio_scrape
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install VLC** (required for CLI players only)
   - **Windows&MacOS**: Download from [https://images.videolan.org/vlc/](https://images.videolan.org/vlc/) and add to PATH
  
   - **Linux**: there by default on most distros

## Docker Web Interface 🐳

The easiest way to use Radio Player is with Docker! This provides a beautiful web interface accessible from any browser.

### Quick Start with Docker

**Option 1: Pull from Docker Hub (Recommended)**

```bash
# Pull and run the pre-built image
docker-compose up -d

# Or run directly
docker run -d -p 5000:5000 \
  -v $(pwd)/working_radios.json:/app/working_radios.json:ro \
  drefault/radio_player:latest
```

**Option 2: Build Locally**

```bash
# Edit docker-compose.yml and uncomment the build line
# Then build and run
docker-compose up -d --build
```

### Access the Web Interface

1. Open your browser to: **http://localhost:5000**
2. Browse, search, and play radio stations!

### Stop the Container

```bash
docker-compose down
```

### Building and Pushing to Docker Hub

For maintainers who want to update the Docker Hub image:

**Windows (PowerShell):**
```powershell
.\build-and-push.ps1
```

**Linux/Mac:**
```bash
chmod +x build-and-push.sh
./build-and-push.sh
```

**Manual Commands:**
```bash
# Build with Docker Hub tag
docker build -t drefault/radio_player:latest .

# Login to Docker Hub
docker login

# Push to Docker Hub
docker push drefault/radio_player:latest
```

### Web Interface Features

- 🎨 **Modern UI** - Beautiful glassmorphism design with smooth animations
- 🔍 **Search** - Find stations by name instantly
- 🌍 **Filter by Country** - Browse stations from specific countries
- 🎵 **Browser Playback** - Play streams directly in your browser (no VLC needed!)
- 📱 **Responsive** - Works perfectly on desktop, tablet, and mobile
- 🎯 **Now Playing** - See what's currently streaming with station details

### Configuration

Edit `docker-compose.yml` to customize:

```yaml
ports:
  - "8080:5000"  # Change 8080 to your preferred port
```


## Usage

### 1. Scrape Radio Stations

Fetch radio stations from the Radio Browser API:

```bash
# Get 20 stations from any country
python radio_scrape.py

# Get stations from a specific country
python radio_scrape.py --country Rwanda --limit 50

# Search by station name
python radio_scrape.py --name "BBC" --limit 30

# Custom output filename
python radio_scrape.py --country Kenya --output kenya_stations
```

**Options:**
- `--country` - Filter by country name
- `--name` - Search by station name
- `--limit` - Maximum number of stations to fetch (default: 20)
- `--output` - Output filename without extension (default: radio_station)

### 2. Filter Working Streams

Test and filter out dead radio streams:

```bash
# Filter stations from radio_station.json
python filter.py
```

This will:
- Test each stream URL for availability
- Display working ✔ and dead ✘ stations
- Save working stations to `working_radios.json`

**Multi-threaded version** (faster):
```bash
python multi_filter.py
```

### 3. Play Radio Stations

Interactive CLI player to browse and play stations:

```bash
# Play from working_radios.json
python play.py

# Play from multi-country results
python play_m.py
```

The player will:
1. Show available countries
2. List stations in the selected country
3. Play the selected station using FFplay

**Controls:**
- Press `CTRL+C` to stop playback

## Example Workflow

```bash
# 1. Scrape Rwandan radio stations
python radio_scrape.py --country Rwanda --limit 50 --output rwanda_radios

# 2. Filter working streams
python filter.py

# 3. Play a station
python play.py
```

## API Reference

This project uses the [Radio Browser API](https://api.radio-browser.info/) to fetch radio station data.

### Data Fields

Each radio station includes:
- `name` - Station name
- `stream_url` - Direct stream URL
- `homepage` - Station website
- `country` - Country of origin
- `language` - Broadcast language
- `tags` - Genre/category tags
- `codec` - Audio codec (MP3, AAC, etc.)
- `bitrate` - Stream bitrate in kbps

## Requirements

- Python 3.6+
- `requests` - HTTP library for API calls
- `python-vlc` - VLC Python bindings (optional)
- VLC/FFplay - For audio playback

## Troubleshooting

### Stream won't play
- Ensure VLC is installed and in your PATH
- Some streams may be geo-restricted
- Try a different station

### No working stations found
- The Radio Browser API data may be outdated
- Try scraping from a different country
- Increase the `--limit` parameter

### Slow filtering
- Use `multi_filter.py` for faster multi-threaded filtering
- Reduce timeout in the filter script (default: 5 seconds)

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## License

This project is open source and available under the MIT License.

## Acknowledgments

- [Radio Browser API](https://www.radio-browser.info/) for providing free radio station data
- VLC project for audio playback capabilities

---

**Made with ❤️ for radio enthusiasts**
