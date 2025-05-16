#--------------------------------------------------------------------------------------#
# Program: percentDist.py                                                              #
# Author : Sara Katsabas                                                               #
# Date   : Feb 8, 2025                                                                 #
# Purpose: To create a geoprocessing tool that will select a store's customers         #
#          and calculate the percentage of them that fall within a specified           #
#          distance from the store.                                                    #
#--------------------------------------------------------------------------------------#

import arcpy

# Overwrite output set
arcpy.env.overwriteOutput = True

# Initialize working file directory
workspace = r"C:\Documents\COGS\WIN2025\GISY6060\Assignment2\Assignment2.gdb"
arcpy.env.workspace = workspace

# Initialize parameters
storeFeat = arcpy.GetParameterAsText(0)  
dist      = float(arcpy.GetParameterAsText(1)) 
output    = arcpy.GetParameterAsText(2)

# Get the customer feature class name from the store feature class name
store_name = storeFeat.split('_')[-1]  
cstmFeat = store_name 

# Clear any existing selection on the customer layer
arcpy.management.SelectLayerByAttribute(cstmFeat, "CLEAR_SELECTION")

# Get Count (total customers of a store)
count = arcpy.management.GetCount(cstmFeat)
totalcstm = int(count[0])
arcpy.AddMessage(f'Total customers = {totalcstm}')

# Select Layer by Location (select customers within a distance of the store in kilometers)
cstmSel = arcpy.management.SelectLayerByLocation(
    in_layer = cstmFeat,
    overlap_type ="WITHIN_A_DISTANCE",
    select_features = storeFeat,
    search_distance = f'{dist} Kilometers',
    selection_type ="NEW_SELECTION",
    invert_spatial_relationship ="NOT_INVERT"
)

# Check how many features are selected
cstmSelCount = arcpy.management.GetCount(cstmSel)
selected = int(cstmSelCount[0])
arcpy.AddMessage(f'Customers selected by script = {selected}')

# Calculate percentage of customers selected
pcnt = round((selected / totalcstm) * 100, 2)
arcpy.AddMessage(f'Calculated percentage = {pcnt}%')

# Define the table name
table_name = f'{storeFeat}_percDist'

# Define the full path for the new table
output_table_path = workspace + "\\" + table_name

# Check if the table already exists, and delete if necessary
if arcpy.Exists(output_table_path):
    arcpy.Delete_management(output_table_path)
    arcpy.AddMessage(f"Deleted existing table: {output_table_path}")

# Create and add fields to the table
arcpy.CreateTable_management(workspace, table_name)

arcpy.AddField_management(output_table_path, 'Distance', 'TEXT')
arcpy.AddField_management(output_table_path, 'Percentage', 'DOUBLE')

# Cursor to populate the table
cursor = arcpy.da.InsertCursor(output_table_path, ["Distance", "Percentage"])
cursor.insertRow([dist, pcnt])
del cursor

arcpy.AddMessage(f"Data written to {output_table_path}")
