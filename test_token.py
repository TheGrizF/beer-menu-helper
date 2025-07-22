import requests
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

TOKEN = os.getenv('UTFB_READ_ONLY_TOKEN')
EMAIL = os.getenv('EMAIL')

url = "https://business.untappd.com/api/v1/items/search.json"

params = {
    'q': 'Sip of Sunshine'
}

response = requests.get(
    url, params=params,
    auth=HTTPBasicAuth(EMAIL, TOKEN),
    headers={"Accept": "application/json"}
)

print(f"Status Code: {response.status_code}")
print(response.text)
