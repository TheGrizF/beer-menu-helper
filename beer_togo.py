import csv
import requests
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

products = [
    ('beer name', 10)
]


load_dotenv()
READ_ONLY_TOKEN = os.getenv('UTFB_READ_ONLY_TOKEN')
EMAIL = os.getenv('EMAIL')

UTFB_API_URL = 'https://business.untappd.com/api/v1/items/search.json'

# Containers
containers = [
    ('4-pack 16oz Cans', 6),
    ('4-pack 12oz Cans', 6),
    ('6-pack 12oz Cans', 4),
    ('16oz Can (Single)', 24),
    ('12oz Can (Single)', 24),
    ('375ml Bottle', 12),
    ('500ml Bottle', 12),
    ('750ml Bottle', 12),
    ('22oz Bottle', 12)
]

translation_table = str.maketrans({
    "’": "'",
    "‘": "'",
    "“": '"',
    "”": '"',
    "—": "-",
    "–": "-"
})

# Search for Beer
def search_untappd(beer_name: str):
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
        beers = []
        """
        if data['items']:
            if len(data['items']) == 1:
                beer = data['items'][0]
            else:
                print('Multiple results found')
                for i, beer in enumerate(data['items']):
                    print(f"{i+1}) {beer['name']} - {beer['brewery']}")
                slct = int(input('Selection: ')) - 1
                beer = (data['items'][slct])
            print("Storing information:")
            print(f"{beer['brewery']} {beer['name']} {beer['abv']}% abv {beer['style']}")
            print(beer['description'])
            return {
                'beer_name': beer['name'].translate(translation_table),
                'brewery': beer['brewery'].translate(translation_table),
                'abv': beer['abv'],
                'style': beer['style'].translate(translation_table),
                'description': beer['description'].translate(translation_table)
            }
            """
        for beer in data['items']:
            beers.append({
                'name': beer['name'].translate(translation_table),
                'brewery': beer['brewery'].translate(translation_table),
                'abv': beer['abv'],
                'style': beer['style'].translate(translation_table),
                'description': beer['description'].translate(translation_table)
            })
            return beers
        else:
            print(f"Error: {response.status_code} - {response.text}")
        return

def generate_beers(beer_list):
    output_rows = []
    for beer in beer_list:
        name, cost = beer
        print(f'\nProcessing: {name}')
        beer_info = search_untappd(name)
        if not beer_info:
            print(f"Could not find {name} on Untappd.")
            continue
    
        # Handle Container Type
        print(f'\nPackage type:')
        for i, pack in enumerate(containers):
            print(f"{i+1}) {pack[0]}")
        slct = int(input("Selection: ")) - 1
        package = containers[slct]

        # Handle Price
        print(f'Bassed off Case Price: ${cost} with {package[1]} {package[0]} per case')
        min_p = float(cost / package[1]) * 1.4
        max_p = float(cost / package[1]) * 1.5
        print(f'Price range: ${min_p:.2f} - ${max_p:.2f}')
        price = float(input("Input Price: "))

        # Naming
        full_name = f"{beer_info['brewery']} {beer_info['beer_name']}"
        pos_name = ''
        if len(beer_info['brewery']) > 10:
            pos_name = f"{beer_info['brewery'].split()[0]} {beer_info['beer_name']}"

        description = (f"\"{package[0]} {beer_info['abv']}% abv {beer_info['style']}\n"
                       f"{beer_info['description']}\"")
        if len(description) > 1000:
            cutoff = description.rfind(' ', 0, 1000)
            if cutoff == -1:
                cutoff = 997
            description = description[:cutoff] + '...'

        output_rows.append({
            'Name': full_name,
            'Price': price,
            'POS Name': pos_name,
            'Kitchen Name': '',
            'Description': description,
            'Calories': '',
            'SKU': '',
            'PLU': ''
        })

    write_to_csv(output_rows, 'bulk_add.csv')

def write_to_csv(output_rows, filename):
    keys = ['Name', 'Price', 'POS Name', 'Kitchen Name',
            'Description', 'Calories', 'SKU', 'PLU']
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(output_rows)
            
example = [
    ('Lawsons Sip Of Sunshine', 85)
]

# generate_beers(products)
