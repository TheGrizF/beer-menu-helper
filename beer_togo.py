import csv
import math
import requests
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()
READ_ONLY_TOKEN = os.getenv('UTFB_READ_ONLY_TOKEN')
EMAIL = os.getenv('EMAIL')

UTFB_API_URL = 'https://business.untappd.com/api/v1/items/search.json'

# Containers
containers = [
    '4-pack 16oz Cans',
    '4-pack 12oz Cans',
    '6-pack 12oz Cans',
    '16oz Can (Single)',
    '12oz Can (Single)',
    '375ml Bottle',
    '500ml Bottle',
    '750ml Bottle',
    '22oz Bottle'
]

# Search for Beer
def search_untappd(beer_name):
    headers = {
        'Accept': 'application/json'
    }
    params = {
        'q': beer_name
    }
    response = requests.get(
        UTFB_API_URL,
        auth=HTTPBasicAuth(EMAIL, READ_ONLY_TOKEN),
        headers=headers, 
        params=params
    )
    if response.status_code == 200:
        data = response.json()
        if data['items']:
            for beer in data['items']:
                print(beer['name'])
    else:
        print(f"Error: {response.status_code} - {response.text}")
    return

def generate_beers(beer_list):
    output_rows = []
    for beer in beer_list:
        name, cost = beer
        print(f'\nProcessing: {name}      Cost per unit: ${cost}')
        search_untappd(name)
        
example = [
    ('Lawsons Sip Of Sunshine', 15),
    ('Sojourn Ten', 10)
]

generate_beers(example)
