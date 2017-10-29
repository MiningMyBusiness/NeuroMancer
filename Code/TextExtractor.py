# Neuroscience Text Extractor
# Extracts year, title, and abstract from
#   list of neuroscience reviews ans saves them as csv files
# Author: Kiran Bhattacharyya
# Licensce: MIT License

# Taking a look at one of the text files with the data will explain what the
# following lines of code are doing.

print 'Running text extractor.'

# find all text files with abstracts from neuroscience review journals
import glob
allTxtFiles = glob.glob('../AbstractTextFiles/*.txt')

# loop through each text file
for i in xrange(0,len(allTxtFiles)):
    fileName = allTxtFiles[i]
    reviewFile = open(fileName) # load in relevant text file with list of abstracts
    journalName = fileName[21:-4] # find journal name in file name

    myYear = list() # list to store year
    myTitle = list() # list to store every title
    myAbstract = list() # list to store every abstract

    # list of all years included for analysis
    yearList = ['1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016']

    # create variables to be used when going through the text files
    state = 1 # state variable to determine if we should stay in a while loop
    newEntry = 0 # state variable which denotes if we have reached a new entry in the
                 # list of abstracts or still in an old entry
    authorInfo = 0 # state variable which indicates if we have reached the author
                   # info in the new entry
    myIter = 0 # iteration counter of a while loop

    # start the while loop which will keep reading the text file line-by-line until it has read
    #    all lines
    while (state == 1):
        myIter = myIter + 1 # keep iteration count
        line = reviewFile.readline() # read next line of text document
        readLine = line.strip() # strip the line of ASCII characters like \n and \t
        if journalName in readLine: # check to see if journal name is in the line
            newEntry = 1 # then this is a new entry
        if newEntry == 1: # if it is a new entry
            newEntry = 0 # set newEntry state back to zero
            for year in yearList: # see which year this paper was published
                yearState = 0
                if year in readLine:
                    myYear.append(year)
                    yearState = 1
                    break
            if yearState == 0:
                print readLine
            beforeTitle = 0 # set before title state
            while (beforeTitle == 0):
                line = reviewFile.readline()
                readLine = line.strip()
                if len(readLine) == 0: # keep reading empty lines
                    break
            line = reviewFile.readline()
            readLine = line.strip()
            subTitleList = list()
            subTitleList.append(readLine) # add title
            line = reviewFile.readline() # some titles take up two lines
            readLine = line.strip()
            if len(readLine) > 0:
                subTitleList.append(readLine)
            fullTitle = ' '.join(subTitleList)
            myTitle.append(fullTitle)
            while (authorInfo == 0): # read lines until Author Info
                line = reviewFile.readline()
                readLine = line.strip()
                if 'Author information' in readLine:
                    authorInfo = 1
                if 'DOI' in readLine:
                    myAbstract.append(' ')
                    break
        if authorInfo == 1:
            authorInfo = 0
            inAuthInfo = 1
            while (inAuthInfo == 1): # read lines until have read author info
                line = reviewFile.readline()
                readLine = line.strip()
                if len(readLine) == 0:
                    inAuthInfo = 0
            inAbs = 1
            subAbsList = list()
            while (inAbs == 1): # read all lines of abstract
                line = reviewFile.readline()
                readLine = line.strip()
                if len(readLine) > 0:
                    subAbsList.append(readLine)
                if len(readLine) == 0:
                    inAbs = 0
            fullAbstract = ' '.join(subAbsList)
            myAbstract.append(fullAbstract)
        if myIter == 40000: # stop reading if 20,000 lines have been read
            state = 2

    reviewFile.close()

    numOfAbstracts = len(myAbstract) # number of abstracts found
    numOfYears = len(myYear) # number of years found
    numOfTitles = len(myTitle) # number of titles found

    if numOfAbstracts == numOfYears:
        if numOfYears == numOfTitles: # if we found the same number of abstracs, years, and titles
            # then save extracted year, title, and abstracts in a csv file
            import csv
            yearFile = open('../ProcessedData/' + journalName + '_Year' + '.csv','wb')
            year = csv.writer(yearFile)
            year.writerow(myYear)
            yearFile.close()

            titleFile = open('../ProcessedData/' + journalName + '_Title' + '.csv','wb')
            title = csv.writer(titleFile)
            title.writerow(myTitle)
            titleFile.close()

            abstractFile = open('../ProcessedData/' + journalName + '_Abstract' + '.csv','wb')
            abstract = csv.writer(abstractFile)
            abstract.writerow(myAbstract)
            abstractFile.close()
        else:
            print "Mismatch in number of abstracts, years, and titles found."
