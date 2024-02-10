"""module for using the geocoder.ca json service for postal code coordinates"""

import requests
import time

# Make a GET request to the URL that provides JSON data
def get_coordinates(postal_code, max_attempts=3, delay=5):
    url = f"https://geocoder.ca/{postal_code}?json=1"
    attempt=0

    while attempt < max_attempts:
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            json_data = response.json()
            longitude = json_data['longt']
            latitude = json_data['latt']

            print(f'{postal_code} ok')
            return latitude, longitude
        except:
            print(f'{postal_code} no {response.status_code}', end=' ')
        
        attempt += 1
        if attempt < max_attempts:
            print(f'retrying in {delay} seconds')
            time.sleep(delay)


    print(f'{postal_code} no response, failed after {max_attempts} attempts')
    return None, None