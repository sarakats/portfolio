#=========================================================================================#
# Program: tbltopoint.py                                                                 #
# Purpose: To open prepared data in ArcGIS Pro and create points.                                                                 #
# Author : Sara Katsabas                                                                  #
#=========================================================================================#

import arcpy
import csv
import os

# Set up workspace
arcpy.env.workspace = r"C:\GIS\GlobalAquariums"
arcpy.env.overwriteOutput = True

# Paths
original_csv = r"C:\Documents\COGS\WIN2025\GISY6060\Assignment5\GlobalAquariums\aquariumLatlon.csv"
cleaned_csv = r"C:\Documents\COGS\WIN2025\GISY6060\Assignment5\GlobalAquariums\aquariums_cleaned.csv"
output_fc = "Aquariums_Points"

# Clean up coordinates: filter out rows with missing or bad lat/lon
with open(original_csv, 'r', encoding='latin1') as infile, \
     open(cleaned_csv, 'w', newline='', encoding='utf-8') as outfile:

    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    valid_rows = 0
    skipped_rows = 0

    for row in reader:
        lat = row.get("Latitude", "").strip()
        lon = row.get("Longitude", "").strip()

        try:
            lat_f = float(lat)
            lon_f = float(lon)
            # Check if lat/lon are in plausible ranges
            if -90 <= lat_f <= 90 and -180 <= lon_f <= 180:
                writer.writerow(row)
                valid_rows += 1
            else:
                skipped_rows += 1
        except ValueError:
            skipped_rows += 1

print(f"Cleaned CSV created with {valid_rows} valid rows ({skipped_rows} skipped).")

# Define spatial reference
spatial_ref = arcpy.SpatialReference(4326)  # WGS 1984

# Run XY Table To Point on cleaned CSV
arcpy.management.XYTableToPoint(
    in_table=cleaned_csv,
    out_feature_class=output_fc,
    x_field="Longitude",
    y_field="Latitude",
    coordinate_system=spatial_ref
)

print(f"Feature class '{output_fc}' created from cleaned CSV!")
