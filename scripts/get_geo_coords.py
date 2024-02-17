"""module for appending geo coords to the list of centres with addresses"""

import csv
from geocoder_lookup import get_coordinates

def add_coordinates(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as csv_file, open(output_file, 'w', newline='', encoding='utf-8') as output_csv:
        reader = csv.DictReader(csv_file)
        fieldnames = reader.fieldnames + ['latitude', 'longitude']  # Add latitude and longitude columns
        writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        writer.writeheader()  # Write header row

        item_index = 0
        
        
        for row in reader:
            search_string = row['address']
            latitude, longitude = get_coordinates(search_string)
            row['latitude'] = latitude
            row['longitude'] = longitude
            writer.writerow(row)
            
            print(f'Progress: {item_index}', end='\r')
            item_index += 1

if __name__ == "__main__":
    input_file = "center_locations.csv"  # Change to your input CSV file
    output_file = "output.csv"  # Change to desired output CSV file
    add_coordinates(input_file, output_file)
