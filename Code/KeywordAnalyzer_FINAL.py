# Title: Keyword Usage Analyzer
# Description: Analyzes keyword usage in neursocience review articles
#               over 20 years. Uses output from AbstractSummarizer.py
# Author: Kiran Bhattacharyya
# License: MIT License

print 'Running keyword analyzer.'

#######-------#######
### SECTION 1: Read in and clean data
# find relevant files in directory
import glob
absFiles = glob.glob('../ProcessedData/*_abstractKeywords.csv')
absIndex = glob.glob('../ProcessedData/*_keywordsByAbstract.csv')
absYears = glob.glob('../ProcessedData/*_keywordYears.csv')
absTitle = glob.glob('../ProcessedData/*_Title.csv')

# read in data
masterKeyList = list()
masterYearList = list()
keyByAbstracts = list()
keyByAbstractsYear = list()
keyByAbstractsTitle = list()
import csv
import itertools as itt
for i in xrange(0,len(absFiles)):
    with open(absFiles[i], 'rb') as f:
        reader = csv.reader(f)
        abstractList = list(reader)
        abstractList = abstractList[0]

    with open(absYears[i], 'rb') as g:
        reader  = csv.reader(g)
        yearList = list(reader)
        yearList = yearList[0]

    with open(absIndex[i], 'rb') as h:
        reader = csv.reader(h)
        indexList = list(reader)
        indexList = indexList[0]

    with open(absTitle[i], 'rb') as ii:
        reader = csv.reader(ii)
        titleList = list(reader)
        titleList = titleList[0]

    masterKeyList.append(abstractList)
    masterYearList.append(yearList)

    absNumber = list(set(indexList))
    for myNumber in absNumber:
        allIndices = [jj for jj,
                      x in enumerate(indexList) if x == myNumber]
        subList = list()
        for index in allIndices:
            subList.append(abstractList[index])
        keyByAbstracts.append(subList)
        keyByAbstractsYear.append(yearList[allIndices[0]])
        keyByAbstractsTitle.append(titleList[int(myNumber)])

# collapse lists to make master list of all keywords
# and change to lower case
masterKeyList = sum(masterKeyList, [])
masterKeyList = [ myWord.lower() for myWord in masterKeyList ]
masterYearList = sum(masterYearList, [])

# remove some nonsensical keywords to create a filtered list
allIndices = [jj for jj, x in enumerate(masterKeyList) if len(x) > 1
              and x != "medline" and x != "feb" and x != "aug"
              and x != "jan" and x != "dec" and x != "jun"
              and x != "jul" and x != "sep" and x!= "oct"
              and x != "nov" and x != "apr" and x != "mar"]
subFiltKeyList = list()
subFiltYearList = list()
for index in allIndices:
    subFiltKeyList.append(masterKeyList[index])
    subFiltYearList.append(masterYearList[index])

# removing stopwords from the list
from nltk.corpus import stopwords
filtKeyList = list()
filtYearList = list()
allIndices = [jj for jj, x in enumerate(subFiltKeyList) if x not in stopwords.words('english')]
for index in allIndices:
    filtKeyList.append(subFiltKeyList[index])
    filtYearList.append(subFiltYearList[index])

# save the filtered key list and filtered year list
# Use the filtKeyList and filtYearList to create wordcloud
# with a different .py file
fullKeyword = open('../Results/AllKeywords.csv', 'wb')
keywordFull = csv.writer(fullKeyword)
keywordFull.writerow(filtKeyList)

fullYear = open('../Results/AllYears.csv', 'wb')
yearFull = csv.writer(fullYear)
yearFull.writerow(filtYearList)

#######-------#######
### SECTION 2: Identify frequently used keywords and determine their counts
###             over the years.
# find word count of keywords
diffWords = list(set(filtKeyList))
wordCount = list()
for myWord in diffWords:
    allIndices = [jj for jj,
                    x in enumerate(filtKeyList) if x == myWord]
    wordCount.append(len(allIndices))

# sort words by word count
import numpy as np
sortIndx = np.argsort(wordCount)
descSort = sortIndx[::-1]
orderCount = list()
orderWords = list()
for index in descSort:
    orderCount.append(wordCount[index])
    orderWords.append(diffWords[index])

# find set of different years in the filtYearList
# and order from earliest to latest
diffYears = list(set(filtYearList))
diffYears = [ int(Year) for Year in diffYears] # turn to int for sorting
yearSortIndx = np.argsort(diffYears)
sortYears = list()
for index in yearSortIndx:
    sortYears.append(diffYears[index])
sortYears = [ str(Year) for Year in sortYears] # turn back into string

# find words which have been mentioned at least
# a certain number of times over the last 20 years
minMentions = 20
commonWordIndx = allIndices = [jj for jj,
                                x in enumerate(orderCount) if x == minMentions]
commonWordIndx = max(commonWordIndx)

# create an array of word counts for
# the common words over the years
countArray = np.zeros(((commonWordIndx),len(sortYears)))
for wordIndx in xrange(0,commonWordIndx):
    for abstractIndx in xrange(0,len(keyByAbstracts)):
        yearIndx = [jj for jj,
                        x in enumerate(sortYears) if x == keyByAbstractsYear[abstractIndx]]
        if orderWords[wordIndx] in keyByAbstracts[abstractIndx]:
            countArray[wordIndx,yearIndx] = countArray[wordIndx,yearIndx] + 1

# normalize word counts to total number of abstracts
# that year
for yearIndx in xrange(0,len(sortYears)):
    allYearOccurance = [jj for jj,
                    x in enumerate(keyByAbstractsYear) if x == sortYears[yearIndx]]
    abstractsThisYear = float(len(allYearOccurance))
    countArray[:,yearIndx] = (countArray[:,yearIndx]/abstractsThisYear)*100

# save array of word counts as .csv
# this can be used with R to make graphs over time for specific words
np.savetxt("../Results/wordCountArray.csv", countArray, delimiter=",")
# save the ordered word list up to the least common word (20 mentions limit)
onlyImpWords = orderWords[0:commonWordIndx]
impWordsFile = open('../Results/ImpWords.csv', 'wb')
myImpWords = csv.writer(impWordsFile)
myImpWords.writerow(onlyImpWords)

#######-------#######
### SECTION 3: Determine if certain frequent keywords have
###            increased or decreased in usage.
# do simple linear regression to see
# if any keywords have changed in importance over time
import statsmodels.api as sm
chngWord = list()
chngWordIndx = list()
chngCoef = list()
chngIntcp = list()
chngPredicts = list()
myXs = list(range(1,21,1))
myXs = sm.add_constant(myXs)
for wordIndx in xrange(0,len(countArray)):
    myModel = sm.OLS(countArray[wordIndx], myXs)
    myModel_results = myModel.fit()
    pVals = myModel_results.pvalues
    if pVals[1] < 0.05:
        chngWordIndx.append(wordIndx)
        chngWord.append(orderWords[wordIndx])
        myCoefs = myModel_results.params
        chngCoef.append(myCoefs[1])
        chngIntcp.append(myCoefs[0])
        chngPredicts.append(myModel_results.predict())

# order the list according to increasing coefficients
sortCoefIndx = np.argsort(chngCoef)
sortChngWord = list()
sortChngWordIndx = list()
sortChngCoef = list()
sortChngIntcp = list()
sortChngPredicts = list()
for index in sortCoefIndx:
    sortChngWord.append(chngWord[index])
    sortChngWordIndx.append(chngWordIndx[index])
    sortChngCoef.append(chngCoef[index])
    sortChngIntcp.append(chngIntcp[index])
    sortChngPredicts.append(chngPredicts[index])

# list of changing words with heatmap
import matplotlib.pyplot as plt
myViridis = plt.get_cmap('viridis')
rangeCoefs = max(sortChngCoef) - min(sortChngCoef)
normCoefs = (sortChngCoef - min(sortChngCoef))/rangeCoefs
myColors = [myViridis(normValue) for normValue in normCoefs]
plt.figure(1, figsize = (15,15))
plt.axis([(min(sortChngCoef) - 0.04), (max(sortChngCoef) + 0.04), (min(sortChngIntcp) - 0.1), (max(sortChngIntcp) + 0.1)])
for index in xrange(0,len(sortChngWord)):
    plt.text(sortChngCoef[index], sortChngIntcp[index], sortChngWord[index], fontweight = 'bold', color = myColors[index])
plt.xlabel('Slope of Linear Model (%/year)', fontweight = 'bold', fontsize = 14)
plt.ylabel('y-Intercept of Linear Model (%)', fontweight = 'bold', fontsize = 14)
plt.title('Words with Significant Trends', fontweight = 'bold')
plt.savefig('../Results/AllChangingWords_2D.png')
plt.clf()
plt.close()

# plot of keywords zoomed in
plt.figure(2, figsize = (15,15))
plt.axis([-0.1, (max(sortChngCoef) + 0.04), (min(sortChngIntcp) - 0.1), 2.0])
for index in xrange(0,len(sortChngWord)):
    plt.text(sortChngCoef[index], sortChngIntcp[index], sortChngWord[index], fontweight = 'bold', color = myColors[index])
plt.xlabel('Slope of Linear Model (%/year)', fontweight = 'bold', fontsize = 14)
plt.ylabel('y-Intercept of Linear Model (%)', fontweight = 'bold', fontsize = 14)
plt.title('Words with Significant Trends', fontweight = 'bold')
plt.savefig('../Results/AllChangingWords_2D_zoom.png')
plt.clf()
plt.close()


# # plot some of the changing keywords and their slopes
yearInt = [int(myYear) for myYear in sortYears]
plotPoints = ['ro', 'go', 'bo', 'ko', 'co']
textColor = ['red', 'green', 'blue', 'black', 'cyan']
plt.figure(3)
for index in xrange(0,5):
    plt.plot(yearInt, countArray[sortChngWordIndx[index]], plotPoints[index])
    plt.plot(yearInt, sortChngPredicts[index], plotPoints[index][0])
    plt.text(2012, (9 - (0.33*index)), sortChngWord[index], fontweight = 'bold', color = textColor[index])
plt.axis([1996, 2017, 0, 10])
plt.xlabel('Year', fontweight = 'bold', fontsize = 14)
plt.ylabel('Percent of Abstracts with the Keyword (%)', fontweight = 'bold', fontsize = 14)
plt.title('Words with Decreasing Frequency', fontweight = 'bold')
plt.savefig('../Results/DecreasingWords.png')
plt.clf()
plt.close()

plt.figure(4)
myStart = len(sortChngWord) - 5
for index in xrange(0,5):
    fixIndex = myStart + index
    plt.plot(yearInt, countArray[sortChngWordIndx[fixIndex]], plotPoints[index])
    plt.plot(yearInt, sortChngPredicts[fixIndex], plotPoints[index][0])
    plt.text(1998, (9 - (0.33*index)), sortChngWord[fixIndex], fontweight = 'bold', color = textColor[index])
plt.axis([1996, 2017, 0, 10])
plt.xlabel('Year', fontweight = 'bold', fontsize = 14)
plt.ylabel('Percent of Abstracts with the Keyword (%)', fontweight = 'bold', fontsize = 14)
plt.title('Words with Increasing Frequency', fontweight = 'bold')
plt.savefig('../Results/IncreasingWords.png')
plt.close()

# save the list of changing words and their respective
# coefficients
chngWordFile = open('../Results/changingWords.csv', 'wb')
chngWordFull = csv.writer(chngWordFile)
chngWordFull.writerow(sortChngWord)

chngCoefFile = open('../Results/changingWordCoefs.csv', 'wb')
chngCoefFull = csv.writer(chngCoefFile)
chngCoefFull.writerow(sortChngCoef)

# #######-------#######
### SECTION 4: Create a network graph of keywords
###            based on co-occurance in abstracts
# create adjacency matrix of common key words
keyConnect = np.zeros((len(onlyImpWords),len(onlyImpWords)))
for myAbstract in keyByAbstracts:
    impWordIndx = list()
    for myWord in xrange(0,len(onlyImpWords)):
        if onlyImpWords[myWord] in myAbstract:
            impWordIndx.append(myWord)
    myPos = 0
    while myPos < (len(impWordIndx) - 1):
        for ii in xrange((myPos+1),len(impWordIndx)):
            keyConnect[impWordIndx[myPos],impWordIndx[ii]] = keyConnect[impWordIndx[myPos],impWordIndx[ii]] + 1
        myPos = myPos + 1
## make certain matrix is symmetric
for rowIndx in xrange(0,len(onlyImpWords)):
    for colIndx in xrange((rowIndx + 1),len(onlyImpWords)):
        keyConnect[rowIndx, colIndx] = keyConnect[colIndx, rowIndx] + keyConnect[rowIndx,colIndx]
        keyConnect[colIndx, rowIndx] =  keyConnect[rowIndx, colIndx]

## now that we've made a connectivity matrix we have to see how words are related to each other
# get indices of words with decreasing and increasing coefficents
posCoefs = [jj for jj, x in enumerate(sortChngCoef) if x > 0]
decrWordIndx = sortChngWordIndx[0:(posCoefs[0] - 1)]
incrWordIndx = sortChngWordIndx[posCoefs[0]:]

# check to see how decreasing words are connected to each other and increasing words and vice versa
decrToDecr = list()
incrToIncr = list()
decrToIncr = list()
incrToDecr = list()
for indx in decrWordIndx:
    decrConnects = [keyConnect[indx, otherIndx] for otherIndx in decrWordIndx]
    decrToDecr.append(sum(decrConnects)/float(sum(keyConnect[indx])))
    incrConnects = [keyConnect[indx, otherIndx] for otherIndx in incrWordIndx]
    decrToIncr.append(sum(incrConnects)/float(sum(keyConnect[indx])))

for indx in incrWordIndx:
    incrConnects = [keyConnect[indx, otherIndx] for otherIndx in incrWordIndx]
    incrToIncr.append(sum(incrConnects)/float(sum(keyConnect[indx])))
    decrConnects = [keyConnect[indx, otherIndx] for otherIndx in decrWordIndx]
    incrToDecr.append(sum(decrConnects)/float(sum(keyConnect[indx])))

# create plots of results for connections between decreasing words and increasing words
x = [1, 2]
labels = ['Decreasing Words', 'Increasing Words']
plt.figure(5)
plt.boxplot([decrToDecr, incrToDecr])
plt.xticks(x, labels)
plt.xlabel('Word Type')
plt.ylabel('Word Score')
plt.title('Connection to Decreasing Words')
plt.margins(0.2)
plt.savefig('../Results/DecreaseConnectedness.png')
plt.close()

x = [1, 2]
labels = ['Decreasing Words', 'Increasing Words']
plt.figure(5)
plt.boxplot([decrToIncr, incrToIncr])
plt.xticks(x, labels)
plt.xlabel('Word Type')
plt.ylabel('Word Score')
plt.title('Connection to Increasing Words')
plt.margins(0.2)
plt.savefig('../Results/IncreaseConnectedness.png')
plt.close()

# print p values of rank sum tests for boxplots
from scipy.stats import *
p_DecrDecr_IncrDecr = ranksums(decrToDecr, decrToIncr)
print "Decreasing/Decreasing vs. Decreasing/Increasing p-value"
print p_DecrDecr_IncrDecr
p_IncrIncr_IncrDecr = ranksums(incrToIncr, decrToIncr)
print "Increasing/Increasing vs. Decreasing/Increasing p-value"
print p_IncrIncr_IncrDecr
p_IncrIncr_DecrDecr = ranksums(incrToIncr, decrToDecr)
print "Increasing/Increasing vs. Decreasing/Decreasing p-value"
print p_IncrIncr_DecrDecr
