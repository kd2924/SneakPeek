from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for Vercel domain
CORS(app, resources={r"/*": {"origins": "https://sneak-peek-psi.vercel.app"}})


@app.route('/')
def home():
    return "Sneaker Backend is Running"

@app.route('/api/sneakers/<sku>', methods=['GET'])
def get_sneaker(sku):
    sku = sku.strip()
    product_url = f"https://stockx.com/{sku}"
    external_api_url = f"https://sneaker-database-stockx.p.rapidapi.com/searchByUrl?url={product_url}"
    
    headers = {
        'x-rapidapi-host': os.getenv('RAPIDAPI_HOST'),
        'x-rapidapi-key': os.getenv('RAPIDAPI_KEY')
    }

    try:
        response = requests.get(external_api_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
