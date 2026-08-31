# This script works on PL data as contained in Incident Management Situation Reports

import dircache #Directory and file operations
import re #String operations

# Reports were copied by hand from http://www.predictiveservices.nifc.gov/intelligence/archive.htm  into the files generated below
rootdir = 'C:/Users/masariat/Documents/MATLAB/ALOC8/PL/INPUT/' #Root directory
#years = [ 2009,2010,2011,2012,2013,2014,2015,2016 ]
years = [ 2016 ]
months = [ 'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec' ] #List of months
days = [ [ [] for i in range(0,13) ] for i in range(0,8) ]
###############
# 2009 EXTENT #
###############
days[0][1] = [ 2,9,16,23,30 ] #Jan
days[0][2] = [ 6,13,20,27 ] #Feb
days[0][3] = [ 6,9,10,11,12,13,16,17,18,19,20,23,24,25,26,27,30,31 ] #Mar
days[0][4] = [ 1,2,3,6,7,8,9,10,13,14,15,16,17,20,21,22,23,24,28,28,29,30 ] #Apr
days[0][5] = range(1,32) #May
days[0][6] = range(1,31) #Jun
days[0][7] = range(1,32) #Jul
days[0][8] = range(1,32) #Aug
days[0][9] = range(1,31) #Sep
days[0][10] = range(1,31) #Oct
days[0][11] = [ 5,6,7,8,9,10,11,12,13,20,27 ] #Nov
days[0][12] = [ 4,11,18,25 ] #Dec
###############
# 2010 EXTENT #
###############
days[1][1] = [ 1,8,15,22,29 ] #Jan
days[1][2] = [ 5,12,19,26 ] #Feb
days[1][3] = [ 5,12,19,26 ] #Mar
days[1][4] = [ 2,9,16,19,20,21,22,23,24,25,26,27,28,29,30 ] #Apr
days[1][5] = range(1,32) #May
days[1][6] = range(1,31) #Jun
days[1][7] = range(1,32) #Jul
days[1][8] = range(1,32) #Aug
days[1][9] = range(1,31) #Sep
days[1][10] = range(1,32) #Oct
days[1][11] = range(1,27) #Nov
days[1][12] = [ 3,10,17,23,30 ] #Dec
###############
# 2011 EXTENT #
###############
days[2][1] = [ 7,14,21,28 ] #Jan
days[2][2] = [ 4,11,18,21,22,23,24,25,26,27,28 ] #Feb
days[2][3] = range(1,32) #Mar
days[2][4] = range(1,31) #Apr
days[2][5] = range(1,32) #May
days[2][6] = range(1,31) #Jun
days[2][7] = range(1,32) #Jul
days[2][8] = range(1,32) #Aug
days[2][9] = range(1,31) #Sep
days[2][10] = [ 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,31 ] #Oct
days[2][11] = [ 1,2,3,4,7,8,9,10,14,15,16,17,18,25 ] #Nov
days[2][12] = [ 2,9,16,23,30 ] #Dec
###############
# 2012 EXTENT #
###############
days[3][1] = [ 6,13,20,27 ] #Jan
days[3][2] = [ 3,10,17,24 ] #Feb
days[3][3] = [ 2,9,16,23,30 ] #Mar
days[3][4] = [ 6,10,11,12,13,14,15,16,17,18,19,20,27,30 ] #Apr
days[3][5] = range(1,32) #May
days[3][6] = range(1,31) #Jun
days[3][7] = range(1,32) #Jul
days[3][8] = range(1,32) #Aug
days[3][9] = range(1,31) #Sep
days[3][10] = [ 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,26,31 ] #Oct
days[3][11] = [ 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,23,30 ] #Nov
days[3][12] = [ 2,3,4,5,6,7,8,9,10,14,21,28  ] #Dec
###############
# 2013 EXTENT #
###############
days[4][1] = [ 4,11,18,25 ] #Jan
days[4][2] = [ 1,8,15,22 ] #Feb
days[4][3] = [ 1,8,15,22,29 ] #Mar
days[4][4] = [ 5,12,19,26 ] #Apr
days[4][5] = [ 3,10,17,20,21,22,23,24,25,26,27,28,29,30,31 ] #May
days[4][6] = range(1,31) #Jun
days[4][7] = range(1,32) #Jul
days[4][8] = range(1,32) #Aug
days[4][9] = range(1,31) #Sep
days[4][10] = [ 1,18,25 ] #Oct
days[4][11] = [ 1,8,15,22,29 ] #Nov
days[4][12] = [ 6,13,20,27 ] #Dec
###############
# 2014 EXTENT #
###############
days[5][1] = [ 3,10,17,24,31 ] #Jan
days[5][2] = [ 7,14,21,28 ] #Feb
days[5][3] = [ 7,14,21,28 ] #Mar
days[5][4] = [ 4,11,18,25 ] #Apr
days[5][5] = [ 2,9,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31 ] #May
days[5][6] = range(1,31) #Jun
days[5][7] = range(1,32) #Jul
days[5][8] = range(1,32) #Aug
days[5][9] = range(1,31) #Sep
days[5][10] = [ 1,2,3,10,17,24,31 ] #Oct,
days[5][11] = [ 7,14,21,28 ] #Nov,
days[5][12] = [ 5,12,19,29 ] #Dec
###############
# 2015 EXTENT #
###############
days[6][1] = [ 2,9,16,23,30 ] #Jan
days[6][2] = [ 6,13,20,27 ] #Feb
days[6][3] = [ 6,13,20,27 ] #Mar
days[6][4] = [ 3,10,17,24 ] #Apr
days[6][5] = [ 1,8,15,22,29 ] #May
days[6][6] = range(1,31) #Jun
days[6][7] = range(1,32) #Jul
days[6][8] = range(1,32) #Aug
days[6][9] = range(1,31) #Sep
days[6][10] = [ 1,2,9,16,23,30 ] #Oct
days[6][11] = [ 6,13,20,27 ] #Nov
days[6][12] = [ 4,11,18,25,31 ] #Dec
###############
# 2016 EXTENT #
###############
days[7][1] = [ 8,15,22,29 ] #Jan
days[7][2] = [ 5,12,19,26 ] #Feb
days[7][3] = [ 4,11,18,25 ] #Mar
days[7][4] = [ 1,8,15,22,29 ] #Apr
days[7][5] = [ 6,13,20,27 ] #May
days[7][6] = range(1,31) #Jun
days[7][7] = range(1,32) #Jul
days[7][8] = range(1,32) #Aug
days[7][9] = range(1,31) #Sep
days[7][10] = [ 7,14,21,28 ] #Oct
days[7][11] = [ 4,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30 ] #Nov
days[7][12] = [ 1,2,3,4,5,6,9,16,23,30 ] #Dec
#########
# GACCs #
#########
GACCs = ['NaN' for i in range(0,12)]
GACCs[0] = 'National Preparedness Level'
GACCs[1] = 'Southwest Area ('
GACCs[2] = 'Rocky Mountain Area ('
GACCs[3] = 'Southern Area ('
GACCs[4] = 'Alaska Area ('
GACCs[5] = 'Western Great Basin Area ('
GACCs[6] = 'Eastern Great Basin Area ('
GACCs[7] = 'Northern California Area ('
GACCs[8] = 'Southern California Area ('
GACCs[9] = 'Eastern Area ('
GACCs[10] = 'Northern Rockies Area ('
GACCs[11] = 'Northwest Area (' #Strings to identify blocks in file
########################
# DateMatch subroutine #
########################
# This subroutine validates the file names constructed in main do indeed match the dates contained within
def DateMatch(fid,mmm,dd,yyyy):
    for i in range(0,3): #Get to the third line
        line = fid.readline() #Read line
    seg = line.split(',') #Parse this line (example format: 'Tuesday, June 22, 2010 – 0530 MT')
    if seg[1].lstrip().startswith(mmm): #Check for correct month, lstrip removes leading spaces (if present)
        temp = re.findall('[-+]?\d+',seg[1]) #Parse day
        temp = int(temp[0]) #Convert to integer
        if temp == dd: #Check for correct day
            if seg[2].lstrip().startswith(str(yyyy)): #Check for correct year
                YearTime = re.findall('[-+]?\d+',seg[2]) #Parse year and time
                TZ = seg[2][len(seg[2])-3:len(seg[2])-1] #Parse time zone
                return YearTime[1],TZ  #Return time stamp
            else: #If the year is incorrect
                return 9999,'wrong year' #Fails to have correct year
        else: #If the day is incorrect
            return 9999,'wrong day' #Fails to have correct day
    else: #If the month is incorrect
        return 9999,'wrong month' #Fails to have correct month
#####################
# FindPL subroutine #
#####################
# This subroutine pulls out the appropriate PL value for string ss
def FindPL(fid,ss):
    for line in fid: #For each line in file
        if line.startswith(ss): #If this is line matching ss
            PL = re.findall('[-+]?\d+',line) #Read the PL value as an integer from the proper line
            PL = int(PL[0]) #Change type to integer
            return PL
    PL = 0
    return PL #Return to main
########
# main #
########
# Loop through files
for yyyy in years: #For each archived year
    out_fnam = 'PL_{0}.txt'.format(yyyy) #Construct output file name
    out_fid = open('{0}{1}/{2}'.format(rootdir,yyyy,out_fnam),'w') #Open output file
    # Write a header to output file
    out_fid.write('Date,Time,TZ,NationalPL,SouthwestPL,RockyMountainPL,SouthernPL,AlaskaPL,WesternGreatBasinPL,EasternGreatBasinPL,NorthernCaliforniaPL,SouthernCaliforniaPL,EasternPL,NorthernRockiesPL,NorthwestPL\n')
    PL = range(0,len(GACCs)) #Initialize storage array
    for mmm in months: #For each month
        for dd in days[yyyy%2009][months.index(mmm)+1]: #For each day in extent
            in_fnam = 'IMSR_{0}_{1}_{2}.txt'.format(mmm,dd,yyyy) #Build file name string
            print 'Working on: {0}'.format(in_fnam) #Report to user
            in_fid = open('{0}{1}'.format('{0}{1}/'.format(rootdir,yyyy),in_fnam),'r') #Open file
            [ Time,TZ ] = DateMatch(in_fid,mmm,dd,yyyy) #Check to see if file date matches assumed date
            if Time == 9999: #If dates do not match
                print '\tFound date mismatch ({0})\n\tNo data was read.'.format(TZ) #Report error
                in_fid.close() #Close input file
                continue #Skip out of day loop
            in_fid.close() #Close input fil
            for gacc in GACCs: #For each string in GACCs array
                in_fid = open('{0}{1}'.format('{0}{1}/'.format(rootdir,yyyy),in_fnam),'r') #Open file
                idx = GACCs.index(gacc) #Get index of this string
                PL[idx] = FindPL(in_fid,gacc) #Search for the PL in the file, save to PL array
                in_fid.close() #Close input file
            # Print all output
            out_fid.write('{0} {1} {2},{3},{4},'.format(mmm,dd,yyyy,Time,TZ))
            for val in PL[0:len(PL)-1]: #For all but the last PL
                out_fid.write('{0},'.format(val)) #Print to output with a comma delimiter
            out_fid.write('{0}\n'.format(PL[len(PL)-1])) #Print the last PL with newline character
    out_fid.close() #Close output file
