#===========================================================================
# Program: PROG5000_SuitabilityAnalysis_SaraKatsabas.py
# Purpose: Perform a habitat suitability analysis for the North Mountain
#          Cougar using the NSDNR forestry dataset using new rating
#          criteria specifications.
# Written By: Sara Katsabas; Oct 14, 2024
# For       : PROG5000 - Assignment 1
#===========================================================================

# Function: forest_sel()
# Purpose: Set active layer as selection, initialize boolean value for the loop
def forest_sel():
    while True:
        forestLyr = iface.activeLayer()
        forestLyr.selectAll()

        # Created list to hold unique values of SP1 from dataset
        unique_sp = set()

        # Get features from dataset, removing "NULL" value, and put them into created list
        for feature in forestLyr.selectedFeatures():
            sp1_value = feature['SP1']
            if sp1_value != "NULL" and str(sp1_value) != "NULL":
                unique_sp.add(str(sp1_value))

        spList = list(unique_sp)

        # QGIS dialogue box to request user input and create selection
        qI = QInputDialog()
        name, okname = QInputDialog.getItem(qI, "Leading Species", "Select leading species:", spList, 0, False)

        if okname and name:
            forestLyr.removeSelection()
            
            forestExp = QgsFeatureRequest().setFilterExpression(f'"SP1" = \'{name}\'')
            sel_features = [feature for feature in forestLyr.getFeatures(forestExp)]
            for feature in sel_features:
                forestLyr.select(feature.id())
                
            sel_count = len(sel_features)

            # Ensures there are features selected
            if sel_features:  
                (low_count, low_min_area, low_max_area, low_total_area, low_avg_area,
                med_count, med_min_area, med_max_area, med_total_area, med_avg_area,
                high_count, high_min_area, high_max_area, high_total_area, high_avg_area) = cat_polygons(sel_features)
    
                print_suit_distrib(low_count, low_min_area, low_max_area, low_total_area, low_avg_area,
                                                med_count, med_min_area, med_max_area, med_total_area, med_avg_area,
                                                high_count, high_min_area, high_max_area, high_total_area, high_avg_area,
                                                name, sel_count)

        else:
            print("No species selected.")

        # Dialogue box to prompt user if they would like to run program again
        reply = QMessageBox.question(None, 'Continue?', 'Do you want to select another leading species?', 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        # Exit message if user does not run the program again
        if reply == QMessageBox.No:
            QMessageBox.information(None, "End of program.", "Good Bye.")
            print("Program completed.")
            break

# Function: sel_polygons_rate(feature)
# Purpose: To run suitability analysis on selected polygons, based on determined features
# Features: AVDI, HEIGHT, COVER_TYPE
def sel_polygons_rate(feature):
    avdi_rate = 0
    height_rate = 0
    ctype_rate = 0
    
    avdi_val = feature['AVDI']
    if avdi_val != "NULL":
        if avdi_val < 20:
            avdi_rate = 0.75
        elif 20 <= avdi_val <= 30:
            avdi_rate = 1.75
        else:
            avdi_rate = 2.5
            
    height_val = feature['HEIGHT']
    if height_val != "NULL":
        if height_val < 10:
            height_rate = 1.25
        elif 10 <= height_val <= 20:
            height_rate = 2.5
        else:
            height_rate = 3.75
            
    ctype_val = feature['COVER_TYPE']
    if ctype_val != "NULL":
        if ctype_val == 2:
            ctype_rate = 1
        elif ctype_val == 5:
            ctype_rate = 2
        else:
            ctype_rate = 3.75

    # Find total suitability based on the results from each feature's individual rating
    total_rate = avdi_rate + height_rate + ctype_rate
    return total_rate

# Function: cat_polygons(selected_features)
# Purpose: Categorize selected polygons based on multiple 
def cat_polygons(sel_features):

    low_areas = []
    med_areas = []
    high_areas = []
    
    for feature in sel_features:
        total_rating = sel_polygons_rate(feature)
        area = feature['Shape_Area']
        
        # Categorize based on total_rating
        if total_rating < 5:
            low_areas.append(area)
        elif 5 <= total_rating <= 8:
            med_areas.append(area)
        else:
            high_areas.append(area)

    # Function to calculate min, max, total, and average
    def calc_stats(areas):
        if not areas:  
            return (0, None, None, 0, 0)
        
        total_area = sum(areas)
        avg_area = total_area / len(areas)
        
        # Initialize min and max, then calculate
        min_area = areas[0]
        max_area = areas[0]
        
        for area in areas[1:]:
            if area < min_area:
                min_area = area
            elif area > max_area:
                max_area = area
                
        return (len(areas), min_area, max_area, total_area, avg_area)

    # Calculate statistics for each category
    low_count, low_min_area, low_max_area, low_total_area, low_avg_area = calc_stats(low_areas)
    med_count, med_min_area, med_max_area, med_total_area, med_avg_area = calc_stats(med_areas)
    high_count, high_min_area, high_max_area, high_total_area, high_avg_area = calc_stats(high_areas)

    return (low_count, low_min_area, low_max_area, low_total_area, low_avg_area,
            med_count, med_min_area, med_max_area, med_total_area, med_avg_area,
            high_count, high_min_area, high_max_area, high_total_area, high_avg_area)

def print_suit_distrib(low_count, low_min_area, low_max_area, low_total_area, low_avg_area,
                                   med_count, med_min_area, med_max_area, med_total_area, med_avg_area,
                                   high_count, high_min_area, high_max_area, high_total_area, high_avg_area,
                                   name, sel_count):

# Print final results according to desired formatting style

    print(70*"=")
    print("\t\tNorth Mountain Cougar Habitat Suitability Analysis")
    print(f"\t\t\t %3i of {name} Polygons in Study Area." % sel_count)
    print(70*"=")
    print("Low Suitability: \n"
      " - Number of polygons  :\t%3i\n" % (low_count or 0),
      "- Minimum polygon area: %14.3f\n" % (low_min_area if low_min_area is not None else 0),
      "- Maximum polygon area: %14.3f\n" % (low_max_area if low_max_area is not None else 0),
      "- Total area          : %14.3f\n" % (low_total_area if low_total_area is not None else 0),
      "- Average polygon area: %14.3f\n" % (low_avg_area if low_avg_area is not None else 0))

    print("Medium Suitability: \n"
      " - Number of polygons  :\t%3i\n" % (med_count or 0),
      "- Minimum polygon area: %14.3f\n" % (med_min_area if med_min_area is not None else 0),
      "- Maximum polygon area: %14.3f\n" % (med_max_area if med_max_area is not None else 0),
      "- Total area          : %14.3f\n" % (med_total_area if med_total_area is not None else 0),
      "- Average polygon area: %14.3f\n" % (med_avg_area if med_avg_area is not None else 0))

    print("High Suitability: \n"
      " - Number of polygons  :\t%3i\n" % (high_count or 0),
      "- Minimum polygon area: %14.3f\n" % (high_min_area if high_min_area is not None else 0),
      "- Maximum polygon area: %14.3f\n" % (high_max_area if high_max_area is not None else 0),
      "- Total area          : %14.3f\n" % (high_total_area if high_total_area is not None else 0),
      "- Average polygon area: %14.3f\n" % (high_avg_area if high_avg_area is not None else 0))
    print(70*"=")

# Call the main function
forest_sel()
