from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for your Flask app
#CORS(app)
CORS(app, resources={r"/api/*": {"origins": ["http://[::]:8000/", "http://127.0.0.1:8000", "http://localhost:8000"]}}, supports_credentials=True)




# Home route
@app.route('/')
def home():
    return "Sneaker Backend is Running"

# API route to get sneaker data
@app.route('/api/sneakers/<sku>', methods=['GET'])
def get_sneaker(sku):
    # Trim any whitespace from SKU
    sku = sku.strip()
    product_url = f"https://stockx.com/{sku}"
    external_api_url = f"https://sneaker-database-stockx.p.rapidapi.com/searchByUrl?url={product_url}"

    # Headers for RapidAPI request
    headers = {
        'x-rapidapi-host': os.getenv('RAPIDAPI_HOST'),
        'x-rapidapi-key': os.getenv('RAPIDAPI_KEY')
    }

    try:
        # Make a GET request to RapidAPI
        response = requests.get(external_api_url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses (4xx/5xx)
        return jsonify(response.json())  # Return the API response as JSON
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500  # Return the error message with status code 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)