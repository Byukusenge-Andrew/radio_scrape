// API Base URL
const API_BASE = '/api';

// State
let allStations = [];
let currentStation = null;
let audioPlayer = null;

// DOM Elements
const stationsGrid = document.getElementById('stations-grid');
const searchInput = document.getElementById('search-input');
const countryFilter = document.getElementById('country-filter');
const loading = document.getElementById('loading');
const emptyState = document.getElementById('empty-state');
const nowPlaying = document.getElementById('now-playing');
const stationCount = document.getElementById('station-count');
const playingTitle = document.getElementById('playing-title');
const playingMeta = document.getElementById('playing-meta');
const stopBtn = document.getElementById('stop-btn');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    audioPlayer = document.getElementById('audio-player');

    // Event Listeners
    searchInput.addEventListener('input', handleSearch);
    countryFilter.addEventListener('change', handleFilter);
    stopBtn.addEventListener('click', stopPlayback);

    // Load data
    loadStations();
    loadCountries();
});

// Fetch all stations
async function loadStations() {
    try {
        showLoading(true);
        const response = await fetch(`${API_BASE}/stations`);
        const data = await response.json();

        if (data.success) {
            allStations = data.stations;
            displayStations(allStations);
            updateStationCount(data.count);
        } else {
            showError('Failed to load stations');
        }
    } catch (error) {
        console.error('Error loading stations:', error);
        showError('Failed to load stations');
    } finally {
        showLoading(false);
    }
}

// Fetch countries
async function loadCountries() {
    try {
        const response = await fetch(`${API_BASE}/countries`);
        const data = await response.json();

        if (data.success) {
            populateCountryFilter(data.countries);
        }
    } catch (error) {
        console.error('Error loading countries:', error);
    }
}

// Populate country filter dropdown
function populateCountryFilter(countries) {
    countries.forEach(country => {
        const option = document.createElement('option');
        option.value = country;
        option.textContent = country;
        countryFilter.appendChild(option);
    });
}

// Display stations in grid
function displayStations(stations) {
    stationsGrid.innerHTML = '';

    if (stations.length === 0) {
        showEmptyState(true);
        return;
    }

    showEmptyState(false);

    stations.forEach(station => {
        const card = createStationCard(station);
        stationsGrid.appendChild(card);
    });
}

// Create station card element
function createStationCard(station) {
    const card = document.createElement('div');
    card.className = 'station-card';

    if (currentStation && currentStation.stream_url === station.stream_url) {
        card.classList.add('playing');
    }

    const icon = getStationIcon(station);
    const country = station.country || 'Unknown';
    const codec = station.codec || 'Unknown';
    const bitrate = station.bitrate || '?';

    card.innerHTML = `
        <div class="station-header">
            <div class="station-icon">${icon}</div>
            <div class="station-info">
                <div class="station-name">${escapeHtml(station.name)}</div>
                <div class="station-country">🌍 ${escapeHtml(country)}</div>
            </div>
        </div>
        <div class="station-meta">
            <span class="meta-tag">${escapeHtml(codec)}</span>
            <span class="meta-tag">${bitrate} kbps</span>
        </div>
    `;

    card.addEventListener('click', () => playStation(station));

    return card;
}

// Get station icon based on tags or country
function getStationIcon(station) {
    const tags = (station.tags || '').toLowerCase();

    if (tags.includes('news')) return '📰';
    if (tags.includes('music')) return '🎵';
    if (tags.includes('sport')) return '⚽';
    if (tags.includes('talk')) return '🎙️';
    if (tags.includes('religious') || tags.includes('christian') || tags.includes('catholic')) return '🙏';
    if (tags.includes('jazz')) return '🎷';
    if (tags.includes('rock')) return '🎸';
    if (tags.includes('classical')) return '🎻';

    return '📻';
}

// Play a station
function playStation(station) {
    if (currentStation && currentStation.stream_url === station.stream_url) {
        // Already playing this station
        return;
    }

    currentStation = station;

    // Update audio source
    audioPlayer.src = station.stream_url;
    audioPlayer.load();
    audioPlayer.play().catch(error => {
        console.error('Playback error:', error);
        alert('Failed to play this station. The stream may be unavailable.');
    });

    // Update UI
    updateNowPlaying(station);
    updateStationCards();
}

// Stop playback
function stopPlayback() {
    if (audioPlayer) {
        audioPlayer.pause();
        audioPlayer.src = '';
    }

    currentStation = null;
    nowPlaying.style.display = 'none';
    updateStationCards();
}

// Update now playing section
function updateNowPlaying(station) {
    playingTitle.textContent = station.name;

    const country = station.country || 'Unknown';
    const codec = station.codec || 'Unknown';
    const bitrate = station.bitrate || '?';

    playingMeta.textContent = `${country} • ${codec} • ${bitrate} kbps`;
    nowPlaying.style.display = 'block';
}

// Update station cards to highlight playing
function updateStationCards() {
    const cards = document.querySelectorAll('.station-card');
    cards.forEach(card => {
        card.classList.remove('playing');
    });

    if (currentStation) {
        const playingCard = Array.from(cards).find(card => {
            const name = card.querySelector('.station-name').textContent;
            return name === currentStation.name;
        });

        if (playingCard) {
            playingCard.classList.add('playing');
        }
    }
}

// Handle search
function handleSearch(e) {
    const query = e.target.value.toLowerCase().trim();

    if (!query) {
        displayStations(filterByCountry(allStations));
        return;
    }

    const filtered = allStations.filter(station =>
        station.name.toLowerCase().includes(query)
    );

    displayStations(filterByCountry(filtered));
}

// Handle country filter
function handleFilter(e) {
    const country = e.target.value;
    const searchQuery = searchInput.value.toLowerCase().trim();

    let filtered = allStations;

    // Apply search filter
    if (searchQuery) {
        filtered = filtered.filter(station =>
            station.name.toLowerCase().includes(searchQuery)
        );
    }

    // Apply country filter
    filtered = filterByCountry(filtered, country);

    displayStations(filtered);
}

// Filter stations by country
function filterByCountry(stations, country = null) {
    const selectedCountry = country || countryFilter.value;

    if (!selectedCountry) {
        return stations;
    }

    return stations.filter(station =>
        (station.country || '').toLowerCase() === selectedCountry.toLowerCase()
    );
}

// Update station count
function updateStationCount(count) {
    stationCount.textContent = `${count} stations`;
}

// Show/hide loading state
function showLoading(show) {
    loading.style.display = show ? 'block' : 'none';
    stationsGrid.style.display = show ? 'none' : 'grid';
}

// Show/hide empty state
function showEmptyState(show) {
    emptyState.style.display = show ? 'block' : 'none';
    stationsGrid.style.display = show ? 'none' : 'grid';
}

// Show error message
function showError(message) {
    alert(message);
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
