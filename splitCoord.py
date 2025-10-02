#=========================================================================================#
# Program: aquWikiData.py                                                                 #
# Purpose: To add spatial data columns in order to use in ArcGIS Pro                                                               #
# Author : Sara Katsabas                                                                  #
#=========================================================================================#

import csv

input_file = 'aquariums.csv'
output_file = 'aquariumLatlon.csv'

with open(input_file, 'r', encoding='latin1') as infile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile:

    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ['Latitude', 'Longitude']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in reader:
        coords = row.get('Coordinates', '').strip()

        if coords.lower() != 'not available' and ',' in coords:
            parts = coords.split(',')
            if len(parts) == 2:
                lat = parts[0].strip()
                lon = parts[1].strip()
            else:
                lat = lon = 'not available'
        else:
            lat = lon = 'not available'

        row['Latitude'] = lat
        row['Longitude'] = lon
        writer.writerow(row)

print(f"Latitude and Longitude added to '{output_file}'")
