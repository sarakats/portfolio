#=====================================================================================================#
# Program: placesWorld.py                                                                             #
# Purpose: To create a script that will determine the latitudinal and longitudinal quadrants of       #
#          point features, either selected by the user or not,                                        #
#          and print specified values about points to a report file.                                  #
# Author : Sara Katsabas                                                                              #
# For    : PROG5000 - Assignment2                                                                     #
# Date   : Nov 14, 2024                                                                               #
#=====================================================================================================#

import os

# Function: main()
# Purpose : To loop through selected points, find lat/long quadrants of points, analyse population data of 
#           selected points and print results to a formatted report
def main():
    # Prompt user to input file name
    qi1 = QInputDialog()
    title = 'Create File'
    label = 'Please enter a file name.'
    mode = QLineEdit.Normal
    fname, okfname = QInputDialog.getText(qi1,title,label,mode)

    if okfname:
        okfname
    else:
        QMessageBox.information(None,"Notice", "Process cancelled.")
        return

    # Prompt user to input directory name
    qi2 = QInputDialog()
    title2 = 'Select Directory'
    label2 = 'Please enter output directory.'
    mode2 = QLineEdit.Normal
    valDir = 'C:\Temp'
    dirName, okdirName = QInputDialog.getText(qi2,title2,label2,mode2,valDir)

    if okdirName:
        okdirName
    else:
        QMessageBox.information(None,"Notice", "Process cancelled.")
        return
    
    # Check if the input directory is valid
    if os.path.exists(dirName):
        dirName
    # Use C:\Temp as default directory if input directory is invalid    
    else:
        QMessageBox.information(None,"Input Failed","Directory doesn't exist. Defaulting to C:\Temp")
        dirName = 'C:\Temp'
    
    # Set currently selected layer as active layer    
    ptLyr = iface.activeLayer()
    
    # Dictionary created to store data related to point quadrant/population values
    quadrant_data = {"northwestern":{"count":0,"pop":0,"maxPop":None,"minPop":None,"maxName":"","minName":""},
                     "northeastern":{"count":0,"pop":0,"maxPop":None,"minPop":None,"maxName":"","minName":""},
                     "southwestern":{"count":0,"pop":0,"maxPop":None,"minPop":None,"maxName":"","minName":""},
                     "southeastern":{"count":0,"pop":0,"maxPop":None,"minPop":None,"maxName":"","minName":""}}
    
    # Variables to track highest/lowest populations and their place names
    pt_maxPop = None
    pt_minPop = None
    pt_maxName = ""
    pt_minName = ""
    
    # Get points if they have already been selected
    if ptLyr.selectedFeatureCount() > 0:
        pt_sel = ptLyr.selectedFeatures()

        # Read extents for the active layer and store to variables
        lyrExtent = ptLyr.extent()
        xMin = lyrExtent.xMinimum()
        xMax = lyrExtent.xMaximum()
        yMin = lyrExtent.yMinimum()
        yMax = lyrExtent.yMaximum()

        # Find the midpoint of x and y in order to delineate quadrants
        midPointx = (xMin + xMax) / 2
        midPointy = (yMin + yMax) / 2
        
        # Extract coordinate values from point geometry
        ptFeat = ptLyr.getFeatures()
        for pt in pt_sel:
            ptgeom = pt.geometry()
            xCoord = ptgeom.asPoint().x()
            yCoord = ptgeom.asPoint().y()
    
            # Find population value from field "pop_max"
            pt_pop = pt['pop_max']
            # Find name of point from field "nameascii"
            pt_name = pt['nameascii']
        
            # Call functions getNSHemi and getEWHemi, and assign to variables
            nsHemi = getNSHemi(yCoord, midPointy)
            ewHemi = getEWHemi(xCoord, midPointx)
            
            # Determine total counts of selected points by quadrant
            if nsHemi == "North" and ewHemi == "western":
                quadrant = "northwestern"
            elif nsHemi == "North" and ewHemi == "eastern":
                quadrant = "northeastern"
            elif nsHemi == "South" and ewHemi == "western":
                quadrant = "southwestern"
            elif nsHemi == "South" and ewHemi == "eastern":
                quadrant = "southeastern"
            quadrant_data[quadrant]["count"] += 1
            quadrant_data[quadrant]["pop"] += pt_pop
            
            # Determine min and max population for each quadrant
            if quadrant_data[quadrant]["maxPop"] is None or pt_pop > quadrant_data[quadrant]["maxPop"]:
                quadrant_data[quadrant]["maxPop"] = pt_pop
                quadrant_data[quadrant]["maxName"] = pt_name
            if quadrant_data[quadrant]["minPop"] is None or pt_pop < quadrant_data[quadrant]["minPop"]:
                quadrant_data[quadrant]["minPop"] = pt_pop
                quadrant_data[quadrant]["minName"] = pt_name
            
            # Determine the min and max populations of all selected points
            if pt_maxPop is None or pt_pop > pt_maxPop:
                pt_maxPop = pt_pop
                pt_maxName = pt_name
            if pt_minPop is None or pt_pop < pt_minPop:
                pt_minPop = pt_pop
                pt_minName = pt_name
                
        # Remove selection once function has been run
        ptLyr.removeSelection()
    
    # If no points are selected, use all points in active layer
    else: 
        QMessageBox.information(None,"Notice", f"No points selected. All points in active layer will be used.")

        ptLyr.selectAll()
        pt_sel = ptLyr.getFeatures()
        
        # Read extents for the active point layer and store to variables
        lyrExtent = ptLyr.extent()
        xMin = lyrExtent.xMinimum()
        xMax = lyrExtent.xMaximum()
        yMin = lyrExtent.yMinimum()
        yMax = lyrExtent.yMaximum()

        # Find the midpoint of x and y in order to delineate quadrants
        midPointx = (xMin + xMax) / 2
        midPointy = (yMin + yMax) / 2
        
        # Extract coordinate values from point geometry
        ptFeat = ptLyr.getFeatures()
        for pt in pt_sel:
            ptgeom = pt.geometry()
            xCoord = ptgeom.asPoint().x()
            yCoord = ptgeom.asPoint().y()
    
            # Find population value(s) from field "pop_max"
            pt_pop = pt['pop_max']
            
            # Find name of point(s) from field "nameascii"
            pt_name = pt['nameascii']
        
            # Call functions getNSHemi and getEWHemi and assign to variables
            nsHemi = getNSHemi(yCoord, midPointy)
            ewHemi = getEWHemi(xCoord, midPointx)
            
            # Determine total counts of selected points by quadrant
            if nsHemi == "North" and ewHemi == "western":
                quadrant = "northwestern"
            elif nsHemi == "North" and ewHemi == "eastern":
                quadrant = "northeastern"
            elif nsHemi == "South" and ewHemi == "western":
                quadrant = "southwestern"
            elif nsHemi == "South" and ewHemi == "eastern":
                quadrant = "southeastern"
            quadrant_data[quadrant]["count"] += 1
            quadrant_data[quadrant]["pop"] += pt_pop
            
            # Determine min and max population for each quadrant
            if quadrant_data[quadrant]["maxPop"] is None or pt_pop > quadrant_data[quadrant]["maxPop"]:
                quadrant_data[quadrant]["maxPop"] = pt_pop
                quadrant_data[quadrant]["maxName"] = pt_name
            if quadrant_data[quadrant]["minPop"] is None or pt_pop < quadrant_data[quadrant]["minPop"]:
                quadrant_data[quadrant]["minPop"] = pt_pop
                quadrant_data[quadrant]["minName"] = pt_name
            
            # Determine the min and max populations of all selected points
            if pt_maxPop is None or pt_pop > pt_maxPop:
                pt_maxPop = pt_pop
                pt_maxName = pt_name
            if pt_minPop is None or pt_pop < pt_minPop:
                pt_minPop = pt_pop
                pt_minName = pt_name
        
        # Remove selection once function has been run
        ptLyr.removeSelection()

    # Join directory + file name, ensure file saves as .txt
    out_fname = os.path.join(dirName, f"{fname}.txt")

    # Open file and write results to formatted report
    with open(out_fname, "w") as outfile:
        outfile.write("Report of Selected World Places\n" + "=" * 70 + "\n")
            
        # Loop through each quadrant and write the relevant data to the file
        for quadrant, data in quadrant_data.items():
            outfile.write(f"{data['count']} {quadrant} places have a total population of {data['pop']}\n")

        # Write the max/min population from across all selected points
        outfile.write("=" * 70 + "\n")
        outfile.write(f"The {quadrant} place of {pt_maxName} has the highest population of {pt_maxPop}\n")
        outfile.write(f"The {quadrant} place of {pt_minName} has the lowest population of {pt_minPop}")
        
    # Inform user of script successfully running
    QMessageBox.information(None,"Success",f"File saved to: {out_fname}")

# Function: getNSHemi()
# Purpose : To find the quadrant in which selected point(s) belong to (North/South)
def getNSHemi(yCoord, midpointY):
    if yCoord <= midpointY:
        return "South"
    else:
        return "North"

# Function: getEWHemi
# Purpose : To find the quadrant in which selected point(s) belong to (East/West)
def getEWHemi(xCoord, midpointX):
    if xCoord >= midpointX:
        return "eastern"
    else:
        return "western"
    
# Call function main()
main()