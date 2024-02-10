import csv
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable
import time

def get_coordinates(address):
    geolocator = Nominatim(user_agent="geo_locator")
    attempts = 0
    max_attempts = 3  # Maximum number of retry attempts
    
    while attempts < max_attempts:
        try:
            location = geolocator.geocode(address)
            if location:
                return location.latitude, location.longitude
            else:
                return None, None
        except GeocoderUnavailable as e:
            print(f"Geocoder service unavailable. Retrying in 5 seconds... Attempt {attempts+1}/{max_attempts}")
            time.sleep(5)  # Wait for 5 seconds before retrying
            attempts += 1
    
    print("Max retry attempts reached. Unable to retrieve coordinates.")
    return None, None

def add_coordinates(input_file, output_file):
    with open(input_file, 'r') as csv_file, open(output_file, 'w', newline='') as output_csv:
        reader = csv.DictReader(csv_file)
        fieldnames = reader.fieldnames + ['latitude', 'longitude']  # Add latitude and longitude columns
        writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        writer.writeheader()  # Write header row
        
        for row in reader:
            address = row['address']  # Assuming the address column is named 'Address'
            latitude, longitude = get_coordinates(address)
            row['latitude'] = latitude
            row['longitude'] = longitude
            writer.writerow(row)

if __name__ == "__main__":
    input_file = "file-pages.csv"  # Change to your input CSV file
    output_file = "output.csv"  # Change to desired output CSV file
    add_coordinates(input_file, output_file)
