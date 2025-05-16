#===========================================================================#
#   Program: PROG5000Lab3.py                                                #
#   Purpose: To read student records from a CSV and store output            #
#            results in a .txt file according to given specifications.      #
#   Author : Sara Katsabas                                                  #
#   Date   : 24.10.24                                                       #
#===========================================================================#

# Open file in reading mode to work with data
filename = "COGS_Students_2024.csv"
infile = open(filename, "r")

# Read data from the file 
current_record = infile.readline()

# Create an empty list to store programs/student records
prgrm_list = []
COGSstudents = []

# Process each line in the CSV
while current_record != "":
    prgrm, fname, lname, grade = current_record.split(",")
    grade = int(grade)

    # Set values to print without "" around them
    prgrm = prgrm.strip('""').upper()
    fname = fname.strip('""')
    lname = lname.strip('""')

    fullname = fname + " " + lname
    
    # Add student records to the list 'COGSstudents'
    COGSstudents.append((prgrm, fullname, grade))

    # Check if the program is already in the list to avoid duplicate values
    if prgrm not in prgrm_list:
        prgrm_list.append(prgrm)

    current_record = infile.readline()

# Print only unique program values (with index values starting from 1)
print("Select a program:")
for i in range(len(prgrm_list)):
    print("\t%d %s" % (i + 1, prgrm_list[i]))

# ... [previous code]

# Perform user selection validation, and write results to console and .txt file
good_sel = False
while not good_sel:
    user_input = input("\t\tPlease enter program number: ")

    if user_input: 
        try:
            user_sel = int(user_input)

            # If selection is within the existing list, set index to 1 and
            # print formatted results to console/file
            if 1 <= user_sel <= len(prgrm_list):
                sel_prgrm = prgrm_list[user_sel - 1] 
                output_txt = [f"Names for program: {sel_prgrm}\n", 23*"=" + "\n"]
                print(f"Names for program: {sel_prgrm}")
                print(23*"=")

                # Set variables to count totals of students per program and grades
                # in order to calculate the program's average grade
                total_COGSstudents = 0
                total_grade = 0

                # Loop through the student records for the selected program,
                # and print results to console/file
                for prgrm, fullname, grade in COGSstudents:
                    if prgrm == sel_prgrm:
                        line = "{0:19} {1:3}\n".format(fullname, grade)
                        output_txt.append(line)
                        total_COGSstudents += 1
                        total_grade += grade
                        print("{0:19} {1:3}".format(fullname, grade))
                # Confirm there are students in program, then calculate the
                # average grade and print results to console/file
                if total_COGSstudents > 0:
                    average_grade = total_grade / total_COGSstudents
                    output_txt.append(23*"=" + "\n")
                    output_txt.append(f"\nNumber   :  {total_COGSstudents}\n")
                    output_txt.append(f"Average  : {average_grade:.2f}\n")                    
                    print(23*"=")
                    print(f"Number   :  {total_COGSstudents}")
                    print(f"Average  : {average_grade:.2f}")
                else:
                    output_txt.append("No students found for this program.\n")

                # Create output file name based on selected program and write
                # results to a new or existing text file
                output_filename = f"{sel_prgrm}_Grades.txt"
                
                with open(output_filename, "w") as outfile:
                    outfile.writelines(output_txt)
                
                good_sel = True               
            else:
                user_input
        except:
            user_input
    else:
        user_input

# Close file connection with the close() method
infile.close()
