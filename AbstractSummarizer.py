# Title: Keyword Extractor for Neuroscience Abstracts
# Description: Extracts keywords (using TextRank) from neuroscience abstracts from different
#               journals and catalogs them according to year
# Author: Kiran Bhattacharyya
# License: MIT License

journalName = 'Prog Neurobiol'
abstractFile = journalName + '_Abstract.csv'
yearFile = journalName + '_Year.csv'

import math
import numpy as np

import csv
with open(abstractFile, 'rb') as f:
    reader = csv.reader(f)
    abstractList = list(reader)

with open(yearFile,'rb') as ff:
    reader = csv.reader(ff)
    yearList = list(reader)

import nltk.data
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()

import re
def getwords(text):
    return re.compile('\w+').findall(text)

# perform syntactic filtering and lemmatization on abstracts
filtAbstracts = list()
for i in xrange(0,len(abstractList[0])):
    if len(abstractList[0][i]) > 0:
        thisAbstract = abstractList[0][i]
        lowerAbstract = thisAbstract.lower()
        myText = getwords(lowerAbstract)
        myPOS = nltk.pos_tag(myText)
        shortList = list()
        for k in xrange(0,len(myPOS)):
            if "NN" in myPOS[k][1] or "JJ" in myPOS[k][1]:
                fullWord = myText[k]
                if '\xce\xb1' in fullWord or '\xee\xb1' in fullWord:
                    subList = fullWord.split('-')
                    if len(subList) > 1:
                        fullWord = 'alpha-' + subList[1]
                if '\xce\xb2' in fullWord or '\xee\xb2' in fullWord:
                    subList = fullWord.split('-')
                    fullWord = subList[0] + '-beta'
                if '\xce' in fullWord or '\xe2' in fullWord or '\xc3' in fullWord or '\xee' in fullWord or '\xe3' in fullWord or '\xe9' in fullWord:
                    fullWord = 'nothing'
                wordLemm = wordnet_lemmatizer.lemmatize(fullWord)
                shortList.append(wordLemm)
        synFilt = ' '.join(shortList)
        filtAbstracts.append(synFilt)
    if len(abstractList[0][i]) == 0:
        filtAbstracts.append(' ')

# create connectivity matrix of syntactically filtered abstract
allKeywords = list()
abstractNumber = list()
allYears = list()
for i in xrange(0,len(filtAbstracts)):
    if len(filtAbstracts[i]) > 1:
        thisAbstract = filtAbstracts[i]
        myText = getwords(thisAbstract)
        uniqueWords = list()
        for j in myText:
            if not j in uniqueWords:
                uniqueWords.append(j)
        nrow = len(uniqueWords)
        connMatrix = [[0 for x in range(nrow)] for y in range(nrow)]
        for k in xrange(0,len(uniqueWords)):
            mainIndices = [ii for ii, x in enumerate(myText) if x == uniqueWords[k]]
            for kk in xrange(0,len(uniqueWords)):
                if kk != k:
                    subIndices = [jj for jj, x in enumerate(myText) if x == uniqueWords[kk]]
                    for mainIndex in xrange(0,len(mainIndices)):
                        for subIndex in xrange(0,len(subIndices)):
                            myDiff = abs(mainIndices[mainIndex] - subIndices[subIndex])
                            if myDiff < 3:
                                connMatrix[k][kk] = 1
        initScores = [1]*nrow
        myD = 0.85
        for j in xrange(0,26):
            for k in xrange(0,nrow):
                isConn = [jj for jj, x in enumerate(connMatrix[k][:]) if x == 1]
                mySum = 0
                for kk in xrange(0,len(isConn)):
                    subConn = [jjj for jjj, x in enumerate(connMatrix[isConn[kk]][:]) if x == 1]
                    if len(subConn) > 0:
                        mySum = ((1/len(subConn))*initScores[isConn[kk]]) + mySum
                initScores[k] = (1 - myD)*myD*mySum
        sortIndx = np.argsort(initScores)
        descSort = sortIndx[::-1]
        numOWords = int(round(0.2*nrow))
        myKeywords = list()
        for j in xrange(0,numOWords):
            myKeywords.append(uniqueWords[descSort[j]])
##        Searches for two word keywords
##        withDouble = list()
##        for j in xrange(0,numOWords):
##            keywordIndices = [iii for iii, x in enumerate(myText) if x == myKeywords[j]]
##            for k in xrange(0,numOWords):
##                if k != j:
##                    otherIndices = [kkk for kkk, x in enumerate(myText) if x == myKeywords[k]]
##                    for keywordIndex in xrange(0,len(keywordIndices)):
##                        for otherIndex in xrange(0,len(otherIndices)):
##                            myDiff = otherIndices[otherIndex] - keywordIndices[keywordIndex]
##                            if myDiff == 1:
##                                withDouble.append(myKeywords[j] + ' ' + myKeywords[k])
##        notInDoub = list()
##        for singleWord in myKeywords:
##            doubState = 0
##            for doubleWord in withDouble:
##                if singleWord in doubleWord:
##                    doubState = 1
##            if doubState == 0:
##                notInDoub.append(singleWord)
##        for singleWord in notInDoub:
##            withDouble.append(singleWord)
        for hhh in xrange(0,len(myKeywords)):
            myKeywords[hhh] = myKeywords[hhh].encode('ascii','ignore')
            allKeywords.append(myKeywords[hhh])
            allYears.append(yearList[0][i])
            abstractNumber.append(i)
    if len(filtAbstracts[i]) < 2:
        allKeywords.append('')
        allYears.append(yearList[0][i])
        abstractNumber.append(i)
    print i
            
keywordFile = open(journalName + '_abstractKeywords.csv', 'wb')
keywordFull = csv.writer(keywordFile)
keywordFull.writerow(allKeywords)

yearKeywordFile = open(journalName + '_keywordYears.csv', 'wb')
yearKeywordFull = csv.writer(yearKeywordFile)
yearKeywordFull.writerow(allYears)

wordsByAbsFile = open(journalName + '_keywordsByAbstract.csv', 'wb')
wordsByAbsFull = csv.writer(wordsByAbsFile)
wordsByAbsFull.writerow(abstractNumber)






    
