from flask import Flask, jsonify
from flask_cors import CORS
import requests
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GIOS_BASE_URL = "https://api.gios.gov.pl/pjp-api/rest"

@app.route('/')
def home():
    return {"message": "SmogWatch API is running!", "version": "1.0.0"}

@app.route('/api/stations', methods=['GET'])
def get_stations():
    try:
        response = requests.get(f"{GIOS_BASE_URL}/station/findAll")
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        logger.error(f"Błąd podczas pobierania stacji: {e}")
        return jsonify({"error": "Nie udało się pobrać danych o stacjach"}), 500

@app.route('/api/station/<int:station_id>/sensors', methods=['GET'])
def get_station_sensors(station_id):
    try:
        response = requests.get(f"{GIOS_BASE_URL}/station/sensors/{station_id}")
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        logger.error(f"Błąd podczas pobierania sensorów: {e}")
        return jsonify({"error": "Nie udało się pobrać danych o sensorach"}), 500

@app.route('/api/sensor/<int:sensor_id>/data', methods=['GET'])
def get_sensor_data(sensor_id):
    try:
        response = requests.get(f"{GIOS_BASE_URL}/data/getData/{sensor_id}")
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        logger.error(f"Błąd podczas pobierania danych sensora: {e}")
        return jsonify({"error": "Nie udało się pobrać danych sensora"}), 500

@app.route('/api/station/<int:station_id>/air-quality', methods=['GET'])
def get_air_quality_index(station_id):
    try:
        response = requests.get(f"{GIOS_BASE_URL}/aqindex/getIndex/{station_id}")
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        logger.error(f"Błąd podczas pobierania indeksu jakości powietrza: {e}")
        return jsonify({"error": "Nie udało się pobrać indeksu jakości powietrza"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)