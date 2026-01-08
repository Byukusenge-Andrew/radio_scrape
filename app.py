from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import json
import os

app = Flask(__name__, static_folder='static', template_folder='static')
CORS(app)

# Path to the working radios JSON file
RADIOS_FILE = 'working_radios.json'

def load_radios():
    """Load radio stations from JSON file"""
    if os.path.exists(RADIOS_FILE):
        with open(RADIOS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/api/stations', methods=['GET'])
def get_stations():
    """Get all radio stations"""
    try:
        stations = load_radios()
        return jsonify({
            'success': True,
            'count': len(stations),
            'stations': stations
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stations/country/<country>', methods=['GET'])
def get_stations_by_country(country):
    """Get radio stations filtered by country"""
    try:
        stations = load_radios()
        filtered = [s for s in stations if s.get('country', '').lower() == country.lower()]
        return jsonify({
            'success': True,
            'count': len(filtered),
            'country': country,
            'stations': filtered
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stations/search', methods=['GET'])
def search_stations():
    """Search radio stations by name"""
    try:
        query = request.args.get('q', '').lower()
        if not query:
            return jsonify({
                'success': False,
                'error': 'Search query is required'
            }), 400
        
        stations = load_radios()
        filtered = [s for s in stations if query in s.get('name', '').lower()]
        return jsonify({
            'success': True,
            'count': len(filtered),
            'query': query,
            'stations': filtered
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/countries', methods=['GET'])
def get_countries():
    """Get list of unique countries"""
    try:
        stations = load_radios()
        countries = sorted(list(set(s.get('country', 'Unknown') for s in stations)))
        return jsonify({
            'success': True,
            'count': len(countries),
            'countries': countries
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'radio-player'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
