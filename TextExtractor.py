# Neuroscience Text Extractor
# Extracts Title, Abstract, and Year from
# list of neuroscience reviews
# Author: Kiran Bhattacharyya
# Licensce: MIT License

journalName = "Trends Neurosci"
reviewFile = open(journalName + '.txt')

myYear = list() # list to store year
myTitle = list() # list to store every title
myAbstract = list() # list to store every abstract

yearList = ['1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016']

state = 1
newEntry = 0
authorInfo = 0
myIter = 0
while (state == 1):
    myIter = myIter + 1
    line = reviewFile.readline()
    readLine = line.strip()
    if journalName in readLine:
        newEntry = 1
    if newEntry == 1:
        newEntry = 0
        for year in yearList:
            yearState = 0
            if year in readLine:
                myYear.append(year)
                yearState = 1
                break
        if yearState == 0:
            print readLine
        beforeTitle = 0
        while (beforeTitle == 0):
            line = reviewFile.readline()
            readLine = line.strip()
            if len(readLine) == 0:
                break
        line = reviewFile.readline()
        readLine = line.strip()
        subTitleList = list()
        subTitleList.append(readLine)
        line = reviewFile.readline()
        readLine = line.strip()
        if len(readLine) > 0:
            subTitleList.append(readLine)
        fullTitle = ' '.join(subTitleList)
        myTitle.append(fullTitle)
        while (authorInfo == 0):
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
        while (inAuthInfo == 1):
            line = reviewFile.readline()
            readLine = line.strip()
            if len(readLine) == 0:
                inAuthInfo = 0
        inAbs = 1
        subAbsList = list()
        while (inAbs == 1):
            line = reviewFile.readline()
            readLine = line.strip()
            if len(readLine) > 0:
                subAbsList.append(readLine)
            if len(readLine) == 0:
                inAbs = 0
        fullAbstract = ' '.join(subAbsList)
        myAbstract.append(fullAbstract)
    if myIter == 20000:
        state = 2

import csv
yearFile = open(journalName + '_Year' + '.csv','wb')
year = csv.writer(yearFile)
year.writerow(myYear)
yearFile.close

titleFile = open(journalName + '_Title' + '.csv','wb')
title = csv.writer(titleFile)
title.writerow(myTitle)
titleFile.close

abstractFile = open(journalName + '_Abstract' + '.csv','wb')
abstract = csv.writer(abstractFile)
abstract.writerow(myAbstract)
abstractFile.close

            
            












                
