"""module for using the geocoder.ca json service for postal code coordinates"""

import requests
import time

# Make a GET request to the URL that provides JSON data
def get_coordinates(search_string, max_attempts=3, delay=5):  
    search_string_split = search_string.split(', ')

    postal_code = search_string_split[-1]
    address = ', '.join(search_string_split[:-1])
    municipality_with_pc = ', '.join(search_string_split[-3:])
    municipality = ', '.join(search_string_split[-3:-1])
    
    search_queries = [postal_code, address, municipality_with_pc, municipality]

    for query in search_queries:
        attempt = 0
        while attempt < max_attempts:
            try:
                url = f"https://geocoder.ca/{query}?json=1"
                response = requests.get(url)
                response.raise_for_status()
                
                json_data = response.json()
                longitude = json_data['longt']
                latitude = json_data['latt']

                return latitude, longitude
            except:
                print(f'attempt {attempt+1} query failed: {query}, error: {response.status_code}.')
                if response.status_code == 200:
                    break
            
            attempt += 1
            if attempt < max_attempts:
                print(f'retrying in {delay} seconds')
                time.sleep(delay)


    print(f'{search_string} no response, failed after {max_attempts} attempts')
    return None, None

# Test
# search = 'Hamlet of Taloyoak, Box 8, Taloyoak, Nunavut, X0B1B0'
# latitude, longitude = get_coordinates(search)
# print('latitude: '+latitude)
# print('longitude: '+longitude)