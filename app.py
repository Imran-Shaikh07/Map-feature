from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Get API key from environment variables
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
if not GOOGLE_MAPS_API_KEY:
    logger.error("Google Maps API key is not set in environment variables")
else:
    logger.info("Google Maps API key is configured")

# Remove debug mode and other development configurations
app.config['JSON_SORT_KEYS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def index():
    try:
        api_key_status = "configured" if GOOGLE_MAPS_API_KEY else "not configured"
        logger.info(f"Loading index page. API key status: {api_key_status}")
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Failed to load template: {str(e)}")
        return jsonify({"error": "Failed to load template", "details": str(e)}), 500

@app.route("/get_distance", methods=["POST"])
def get_distance():
    try:
        # Check if API key is available
        if not GOOGLE_MAPS_API_KEY:
            logger.error("API key not configured when calling get_distance")
            return jsonify({"error": "API key not configured"}), 500

        data = request.json
        if not data:
            logger.error("No JSON data provided in get_distance request")
            return jsonify({"error": "No JSON data provided"}), 400

        user_lat, user_lng = data.get("user_lat"), data.get("user_lng")
        destination = data.get("destination")

        if not all([user_lat, user_lng, destination]):
            logger.error(f"Missing parameters in get_distance request. Got lat:{user_lat}, lng:{user_lng}, dest:{destination}")
            return jsonify({"error": "Missing required parameters"}), 400

        # Distance Matrix API URL
        distance_url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={user_lat},{user_lng}&destinations={destination}&key={GOOGLE_MAPS_API_KEY}"
        
        logger.info(f"Making request to Distance Matrix API for destination: {destination}")
        response = requests.get(distance_url)
        response.raise_for_status()
        distance_data = response.json()

        if distance_data["status"] == "OK":
            distance_text = distance_data["rows"][0]["elements"][0]["distance"]["text"]
            logger.info(f"Successfully got distance: {distance_text}")
            return jsonify({"distance": distance_text})
        else:
            logger.error(f"Google Maps API error: {distance_data['status']}")
            return jsonify({"error": "Could not calculate distance", "status": distance_data["status"]}), 500

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to contact Google Maps API: {str(e)}")
        return jsonify({"error": "Failed to contact Google Maps API", "details": str(e)}), 503
    except Exception as e:
        logger.error(f"Internal server error in get_distance: {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.route("/get-location", methods=["POST"])
def get_location():
    try:
        if not GOOGLE_MAPS_API_KEY:
            logger.error("API key not configured when calling get-location")
            return jsonify({"error": "API key not configured"}), 500

        # Google Geolocation API URL
        url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={GOOGLE_MAPS_API_KEY}"
        
        logger.info("Making request to Google Geolocation API")
        response = requests.post(url)
        response.raise_for_status()
        return jsonify(response.json())
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to contact Google Geolocation API: {str(e)}")
        return jsonify({"error": "Failed to contact Google Geolocation API", "details": str(e)}), 503
    except Exception as e:
        logger.error(f"Internal server error in get-location: {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.route("/get-api-key", methods=["GET"])
def get_api_key():
    if GOOGLE_MAPS_API_KEY:
        logger.info("API key successfully retrieved")
        return jsonify({"apiKey": GOOGLE_MAPS_API_KEY})
    logger.error("API key not found when calling get-api-key")
    return jsonify({"error": "API key not configured"}), 500
