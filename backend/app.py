import logging

import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GIOS_BASE_URL = "https://api.gios.gov.pl/pjp-api"

@app.route('/')
def home():
    return {"message": "SmogWatch API is running!", "version": "1.0.0"}

@app.route('/api/stations', methods=['GET'])
def get_stations():
    try:
        all_stations = []
        page = 0
        total_pages = 1
        
        # Fetch all pages of stations
        while page < total_pages:
            response = requests.get(f"{GIOS_BASE_URL}/v1/rest/station/findAll?page={page}&size=500")
            response.raise_for_status()
            data = response.json()
            
            # Update total pages from response
            if 'totalPages' in data:
                total_pages = data['totalPages']
            
            # Transform the Polish API response to the expected format
            if "Lista stacji pomiarowych" in data:
                for station in data["Lista stacji pomiarowych"]:
                    normalized_station = {
                        "id": station.get("Identyfikator stacji"),
                        "stationName": station.get("Nazwa stacji"),
                        "gegrLat": station.get("WGS84 φ N"),
                        "gegrLon": station.get("WGS84 λ E"),
                        "city": {
                            "id": station.get("Identyfikator miasta"),
                            "name": station.get("Nazwa miasta"),
                            "commune": {
                                "communeName": station.get("Gmina"),
                                "districtName": station.get("Powiat"),
                                "provinceName": station.get("Województwo")
                            }
                        },
                        "addressStreet": station.get("Ulica")
                    }
                    all_stations.append(normalized_station)
            
            page += 1
            
            # Safety break to avoid infinite loops
            if page > 50:  # Assuming there won't be more than 50 pages
                logger.warning("Breaking pagination loop at page 50 for safety")
                break
        
        logger.info(f"Fetched {len(all_stations)} stations from {page} pages")
        return jsonify(all_stations)
        
    except requests.RequestException as e:
        logger.error(f"Błąd podczas pobierania stacji: {e}")
        return jsonify({"error": "Nie udało się pobrać danych o stacjach"}), 500

@app.route('/api/station/<int:station_id>/sensors', methods=['GET'])
def get_station_sensors(station_id):
    try:
        response = requests.get(f"{GIOS_BASE_URL}/v1/rest/station/sensors/{station_id}")
        response.raise_for_status()
        data = response.json()
        
        # Transform the Polish API response to the expected format
        if "Lista stanowisk pomiarowych dla podanej stacji" in data:
            sensors = []
            for sensor in data["Lista stanowisk pomiarowych dla podanej stacji"]:
                normalized_sensor = {
                    "id": sensor.get("Identyfikator stanowiska"),
                    "stationId": sensor.get("Identyfikator stacji"),
                    "param": {
                        "paramName": sensor.get("Wskaźnik"),
                        "paramCode": sensor.get("Wskaźnik - kod"),
                        "paramFormula": sensor.get("Wskaźnik - wzór"),
                        "idParam": sensor.get("Id wskaźnika")
                    }
                }
                sensors.append(normalized_sensor)
            return jsonify(sensors)
        
        return jsonify(data)
    except requests.RequestException as e:
        logger.error(f"Błąd podczas pobierania sensorów: {e}")
        return jsonify({"error": "Nie udało się pobrać danych o sensorach"}), 500

@app.route('/api/sensor/<int:sensor_id>/data', methods=['GET'])
def get_sensor_data(sensor_id):
    try:
        response = requests.get(f"{GIOS_BASE_URL}/v1/rest/data/getData/{sensor_id}")
        response.raise_for_status()
        data = response.json()
        
        # Transform the Polish API response to the expected format
        if "Lista danych pomiarowych" in data:
            measurements = []
            for measurement in data["Lista danych pomiarowych"]:
                normalized_measurement = {
                    "date": measurement.get("Data"),
                    "value": measurement.get("Wartość")
                }
                measurements.append(normalized_measurement)
            
            return jsonify({
                "key": f"sensor_{sensor_id}",
                "values": measurements
            })
        
        return jsonify(data)
    except requests.RequestException as e:
        logger.error(f"Błąd podczas pobierania danych sensora: {e}")
        return jsonify({"error": "Nie udało się pobrać danych sensora"}), 500

@app.route('/api/sensor/<int:sensor_id>/historical', methods=['GET'])
def get_historical_sensor_data(sensor_id):
    try:
        # Get optional parameters for date range (default to last 7 days)
        days = request.args.get('days', '7')
        
        all_measurements = []
        page = 0
        total_pages = 1
        
        # Fetch all pages of historical data
        while page < total_pages:
            response = requests.get(f"{GIOS_BASE_URL}/v1/rest/archivalData/getDataBySensor/{sensor_id}?dayNumber={days}&page={page}&size=500")
            response.raise_for_status()
            data = response.json()
            
            # Update total pages from response
            if 'totalPages' in data:
                total_pages = data['totalPages']
            
            # Collect measurements from this page
            if "Lista archiwalnych wyników pomiarów" in data:
                all_measurements.extend(data["Lista archiwalnych wyników pomiarów"])
            
            page += 1
            
            # Safety break to avoid infinite loops (historical data shouldn't have too many pages)
            if page > 10:  # Reasonable limit for historical data pages
                logger.warning("Breaking pagination loop at page 10 for safety")
                break
        
        # Return data in the same format as the original API
        result = {
            "@context": data.get("@context", {}),
            "Lista archiwalnych wyników pomiarów": all_measurements,
            "links": data.get("links", {}),
            "meta": data.get("meta", {}),
            "totalPages": total_pages
        }
        
        logger.info(f"Fetched {len(all_measurements)} historical measurements from {page} pages for sensor {sensor_id}")
        return jsonify(result)
        
    except requests.RequestException as e:
        logger.error(f"Błąd podczas pobierania danych historycznych sensora: {e}")
        return jsonify({"error": "Nie udało się pobrać danych historycznych sensora"}), 500

@app.route('/api/station/<int:station_id>/air-quality', methods=['GET'])
def get_air_quality_index(station_id):
    try:
        response = requests.get(f"{GIOS_BASE_URL}/v1/rest/aqindex/getIndex/{station_id}")
        response.raise_for_status()
        data = response.json()
        
        # Transform the Polish API response to the expected format
        if "AqIndex" in data:
            aq_index = data["AqIndex"]
            normalized_aq = {
                "id": aq_index.get("Identyfikator stacji pomiarowej"),
                "stCalcDate": aq_index.get("Data wykonania obliczeń indeksu"),
                "stIndexLevel": {
                    "id": aq_index.get("Wartość indeksu"),
                    "indexLevelName": aq_index.get("Nazwa kategorii indeksu")
                },
                "stSourceDataDate": aq_index.get("Data wykonania obliczeń indeksu"),
                "so2CalcDate": aq_index.get("Data wykonania obliczeń indeksu dla wskaźnika SO2"),
                "so2IndexLevel": {
                    "id": aq_index.get("Wartość indeksu dla wskaźnika SO2"),
                    "indexLevelName": aq_index.get("Nazwa kategorii indeksu dla wskażnika SO2")
                },
                "no2CalcDate": aq_index.get("Data wykonania obliczeń indeksu dla wskaźnika NO2"),
                "no2IndexLevel": {
                    "id": aq_index.get("Wartość indeksu dla wskaźnika NO2"),
                    "indexLevelName": aq_index.get("Nazwa kategorii indeksu dla wskażnika NO2")
                },
                "pm10CalcDate": aq_index.get("Data wykonania obliczeń indeksu dla wskaźnika PM10"),
                "pm10IndexLevel": {
                    "id": aq_index.get("Wartość indeksu dla wskaźnika PM10"),
                    "indexLevelName": aq_index.get("Nazwa kategorii indeksu dla wskażnika PM10")
                },
                "pm25CalcDate": aq_index.get("Data wykonania obliczeń indeksu dla wskaźnika PM2.5"),
                "pm25IndexLevel": {
                    "id": aq_index.get("Wartość indeksu dla wskaźnika PM2.5"),
                    "indexLevelName": aq_index.get("Nazwa kategorii indeksu dla wskażnika PM2.5")
                },
                "o3CalcDate": aq_index.get("Data wykonania obliczeń indeksu dla wskaźnika O3"),
                "o3IndexLevel": {
                    "id": aq_index.get("Wartość indeksu dla wskaźnika O3"),
                    "indexLevelName": aq_index.get("Nazwa kategorii indeksu dla wskażnika O3")
                }
            }
            return jsonify(normalized_aq)
        
        return jsonify(data)
    except requests.RequestException as e:
        logger.error(f"Błąd podczas pobierania indeksu jakości powietrza: {e}")
        return jsonify({"error": "Nie udało się pobrać indeksu jakości powietrza"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)