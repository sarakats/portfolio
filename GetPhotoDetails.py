#--------------------------------------------------------------------------#
# Programmer: Sara Katsabas
# Program   : GetPhotoDetails.py
# Date      : Feb 23, 2025
#--------------------------------------------------------------------------#

if __name__ == "__main__":

    # Import modules for getting time
    from time import gmtime, strftime, localtime
    import time

    # Import modules for system, URLs, pattern-finding, and time
    import sys
    import urllib.request
    import re
    import datetime

    strBeginTime = str(strftime("%a, %d %b %Y %X", localtime()))

    # Script arguments
    if len(sys.argv) > 2:
        strMsn = sys.argv[0]
        strFrm  = sys.argv[1]
    else:
        strMsn = "ISS069"
        strFrm  = "14993"
        
    # Define local variables
    strTimeStamp = str(datetime.datetime.today())
    if strTimeStamp.find(".") >= 1:
        strTimeStamp = strTimeStamp[0:strTimeStamp.find(".")]

    strTodayDate = str(datetime.date.today())

# Determine Focal Length, Date taken, and Time taken of images from website    
    try:
        # Variable for unique URL of mission/frame
        strFindPhotoURL = ("https://eol.jsc.nasa.gov/SearchPhotos/photo.pl?mission=" + strMsn + "&roll=E&frame=" + strFrm)

        # Open and read URL
        aResp = urllib.request.urlopen(strFindPhotoURL)
        web_pg = str(aResp.read())

        # Determine Focal Length
        # Expression is flexible when extracting values with different numbers of digits (eg. 70 vs 1000)
        pattern = r'Focal Length.*?<td class="table_pad">\s*(\d+mm)\s*</td>'
        m = re.search(pattern, web_pg)
        if m:
            strFocal = m.group(1)
        else:
            print("Focal Length not found.")
            strFocal = ""

        # Determine Date taken
        pattern = r"Date taken.*?<td class=\"table_pad\">(.*?)</td>"
        m = re.search(pattern, web_pg)
        if m:
            strDT = m.group(1)
        else:
            print("Date taken not found.")
            strDT = ""

        # Determine Time taken
        pattern = "Time taken" + "(.*?)" + "GMT"
        m = re.search(pattern, web_pg)
        if m:
            strTT = str(m.group(1))
            strTimeTk = strTT[(strTT.find("<td>")-8):len(strTT)] + "GMT"
        else:
            print ("Time taken not found.")
            strTimeTk = ""
            
        # Print results
        print (f"For {strMsn} {strFrm}, the focal length/date/time taken: {strFocal} {strDT} {strTimeTk}")

    except:
        print ("within Except")
