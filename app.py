from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Get API key from environment variables
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

# Remove debug mode and other development configurations
app.config['JSON_SORT_KEYS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return jsonify({"error": "Failed to load template", "details": str(e)}), 500

@app.route("/get_distance", methods=["POST"])
def get_distance():
    try:
        # Check if API key is available
        if not GOOGLE_MAPS_API_KEY:
            return jsonify({"error": "API key not configured"}), 500

        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        user_lat, user_lng = data.get("user_lat"), data.get("user_lng")
        destination = data.get("destination")

        if not all([user_lat, user_lng, destination]):
            return jsonify({"error": "Missing required parameters"}), 400

        # Distance Matrix API URL
        distance_url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={user_lat},{user_lng}&destinations={destination}&key={GOOGLE_MAPS_API_KEY}"

        response = requests.get(distance_url)
        response.raise_for_status()
        distance_data = response.json()

        if distance_data["status"] == "OK":
            distance_text = distance_data["rows"][0]["elements"][0]["distance"]["text"]
            return jsonify({"distance": distance_text})
        else:
            return jsonify({"error": "Could not calculate distance", "status": distance_data["status"]}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to contact Google Maps API", "details": str(e)}), 503
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.route("/get-location", methods=["POST"])
def get_location():
    try:
        if not GOOGLE_MAPS_API_KEY:
            return jsonify({"error": "API key not configured"}), 500

        # Google Geolocation API URL
        url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={GOOGLE_MAPS_API_KEY}"
        
        response = requests.post(url)
        response.raise_for_status()
        return jsonify(response.json())
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to contact Google Geolocation API", "details": str(e)}), 503
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.route("/get-api-key", methods=["GET"])
def get_api_key():
    if GOOGLE_MAPS_API_KEY:
        return jsonify({"apiKey": GOOGLE_MAPS_API_KEY})
    return jsonify({"error": "API key not configured"}), 500
