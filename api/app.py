from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

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
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
