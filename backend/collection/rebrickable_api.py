import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
BASE_URL = "https://rebrickable.com/api/v3/lego/"

def get_lego_set_details(set_num):
    """Récupère les détails d'un set LEGO depuis Rebrickable."""
    url = f"{BASE_URL}sets/{set_num}/"
    headers = {"Authorization": f"key {API_KEY}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return {"error": f"Impossible de récupérer le set {set_num}"}

def get_lego_set_price(set_num):
    """Récupère les prix d'un set LEGO depuis Rebrickable."""
    url = f"{BASE_URL}sets/{set_num}/price/"
    headers = {"Authorization": f"key {API_KEY}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return {"error": f"Impossible de récupérer le prix du set {set_num}"}