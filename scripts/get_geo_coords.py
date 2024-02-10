"""module for appending geo coords to the list of centres with addresses"""

import csv
from postal_code_lookup import get_coordinates

def add_coordinates(input_file, output_file):
    with open(input_file, 'r') as csv_file, open(output_file, 'w', newline='') as output_csv:
        reader = csv.DictReader(csv_file)
        fieldnames = reader.fieldnames + ['latitude', 'longitude']  # Add latitude and longitude columns
        writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        writer.writeheader()  # Write header row
        
        for row in reader:
            postal_code = row['postal_code']  # Assuming the address column is named 'Address'
            latitude, longitude = get_coordinates(postal_code)
            row['latitude'] = latitude
            row['longitude'] = longitude
            writer.writerow(row)

if __name__ == "__main__":
    input_file = "file-pages.csv"  # Change to your input CSV file
    output_file = "output.csv"  # Change to desired output CSV file
    add_coordinates(input_file, output_file)
