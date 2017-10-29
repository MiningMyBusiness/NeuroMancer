# Title: Keyword Extractor for Neuroscience Abstracts
# Description: Extracts keywords (using TextRank) from neuroscience abstracts from different
#               journals and catalogs them according to year
# Author: Kiran Bhattacharyya
# License: MIT License

# Reviewing this seminal paper on the TextRank algorithm before looking at the
# code may help. https://web.eecs.umich.edu/%7Emihalcea/papers/mihalcea.emnlp04.pdf

print 'Running abstract summarizer'

# import relevant packages
import math
import numpy as np

# find all text files with abstracts from neuroscience review journals
import glob
allTxtFiles = glob.glob('../AbstractTextFiles/*.txt')

# loop through each text file
for qqq in xrange(0,len(allTxtFiles)):
    fileName = allTxtFiles[qqq] # get file name
    journalName = fileName[21:-4] # get journal name
    abstractFile = '../ProcessedData/' + journalName + '_Abstract.csv' # create variable with abstract file name
    yearFile = '../ProcessedData/' + journalName + '_Year.csv' # create variable with name for abstract year csv file

    # open compiled abstract and year files
    import csv
    with open(abstractFile, 'rb') as f:
        reader = csv.reader(f)
        abstractList = list(reader)

    with open(yearFile,'rb') as ff:
        reader = csv.reader(ff)
        yearList = list(reader)

    # create a tokenizer object with natural language toolkit
    import nltk.data
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    from nltk.stem import WordNetLemmatizer
    wordnet_lemmatizer = WordNetLemmatizer()

    # define a function that will extract words from an abstract and place them in
    #   list
    import re
    def getwords(text):
        return re.compile('\w+').findall(text)

    ##### Perform syntactic filtering and lemmatization of words in abstracts
    filtAbstracts = list()
    for i in xrange(0,len(abstractList[0])): # for each abstract in the list
        if len(abstractList[0][i]) > 0: # if there is an abstract
            thisAbstract = abstractList[0][i] # get this abstract
            lowerAbstract = thisAbstract.lower() # make all words lower case
            myText = getwords(lowerAbstract) # extract words, leaving out new line and tab characters
            myPOS = nltk.pos_tag(myText) # tag the parts of speech for each sentence
            shortList = list() # create a variable to store a short list of filtered words from this abstract
            for k in xrange(0,len(myPOS)): # for each tagged part of speech
                if "NN" in myPOS[k][1] or "JJ" in myPOS[k][1]: # if it is a noun or an adjective
                    fullWord = myText[k] # then get that word
                    if '\xce\xb1' in fullWord or '\xee\xb1' in fullWord: # the next few lines deal with special
                        subList = fullWord.split('-')                   #   cases where special characters are not read as ASCII
                        if len(subList) > 1:
                            fullWord = 'alpha-' + subList[1]
                    if '\xce\xb2' in fullWord or '\xee\xb2' in fullWord:
                        subList = fullWord.split('-')
                        fullWord = subList[0] + '-beta'
                    if '\xce' in fullWord or '\xe2' in fullWord or '\xc3' in fullWord or '\xee' in fullWord or '\xe3' in fullWord or '\xe9' in fullWord:
                        fullWord = 'nothing'
                    wordLemm = wordnet_lemmatizer.lemmatize(fullWord) # lemmatize the word
                    shortList.append(wordLemm) # add the word to the short list
            synFilt = ' '.join(shortList) # join the short list to create a new abstract with only filtered words
            filtAbstracts.append(synFilt) # append this new filtered abstract to the filtered abstract variable
        if len(abstractList[0][i]) == 0: # if there is no abstract
            filtAbstracts.append(' ') # append just a space

    ##### Create connectivity matrix for each abstract of syntactically filtered words
    ##### then use TextRank on the connectivity matrix to extract keywords from the abstract
    allKeywords = list() # create variable to store master list of all keywords
    abstractNumber = list() # create variable to keep track of which abstract keywords came from
    allYears = list() # create variable to keep track of which year keywords are from
    for i in xrange(0,len(filtAbstracts)): # for each filtered abstract in the list
        if len(filtAbstracts[i]) > 1: # if the filtered abstract has at least one word
            thisAbstract = filtAbstracts[i] # get the abstract
            myText = getwords(thisAbstract) # extract words from the abstract
            uniqueWords = list() # create a variable to populate with the unique words in the abstract
            for j in myText: # for every word
                if not j in uniqueWords: # if this word is not in the list of unique words
                    uniqueWords.append(j) # then add it
            nrow = len(uniqueWords) # find the number of words in the list of unique words
            connMatrix = [[0 for x in range(nrow)] for y in range(nrow)] # create the connectvity matrix
            for k in xrange(0,len(uniqueWords)): # for each unique word
                mainIndices = [ii for ii, x in enumerate(myText) if x == uniqueWords[k]] # find where it appears in the filtered abstract
                for kk in xrange(0,len(uniqueWords)): # for each unqiue word
                    if kk != k: # that isn't the word we're already looking at
                        subIndices = [jj for jj, x in enumerate(myText) if x == uniqueWords[kk]] # find the indicies of that word
                        for mainIndex in xrange(0,len(mainIndices)): # look through indices of the main word
                            for subIndex in xrange(0,len(subIndices)): # and the other word
                                myDiff = abs(mainIndices[mainIndex] - subIndices[subIndex]) # find how close they are to each other
                                if myDiff < 3: # if they are within 2 words
                                    connMatrix[k][kk] = 1 # then put a 1 in the connectivity matrix

            ## Now do the TextRank algorithm on the populated connectivity matrix
            initScores = [1]*nrow # initialize scores for all of the words to 1
            myD = 0.85 # damping factor in text rank algorithm (https://web.eecs.umich.edu/%7Emihalcea/papers/mihalcea.emnlp04.pdf)
                       #    0.85 is suggested as a starting point in this paper (can be changed)
            numOfTRankIters = 26 # number of iterations to run on the text rank algorithm (can be changed)
                                 # I did tests on this number to make sure list of keywords are essentially the same even with more iterations
            for j in xrange(0,numOfTRankIters): # for every text rank iteration
                for k in xrange(0,nrow): # for every word
                    isConn = [jj for jj, x in enumerate(connMatrix[k][:]) if x == 1]  # find what words this word is connected to
                    mySum = 0 # create a variable to store the sum portion of the text rank algorithm
                    for kk in xrange(0,len(isConn)): # for every word that this word is connected to
                        subConn = [jjj for jjj, x in enumerate(connMatrix[isConn[kk]][:]) if x == 1] # find the words this other word is connected to
                        if len(subConn) > 0: # if this other word is connected to more words
                            mySum = ((1/len(subConn))*initScores[isConn[kk]]) + mySum # then update the sum of the main word
                    initScores[k] = (1 - myD)*myD*mySum # update the score of this word

            ## Now that all words have scores updated from running text rank iterations
            ## we need to sort words according to their scores and pick the words with
            ## largest scores as keywords
            sortIndx = np.argsort(initScores) # get the index of the sorted list of scores
            descSort = sortIndx[::-1] # get index in descending order
            propOfKeywords = 0.2 # proportion of words in the abstract that will be considered keywords (can be changed)
            numOWords = int(round(0.2*nrow)) # the actual number of keywords to be extracted
            myKeywords = list() # create a variable to store keywords
            for j in xrange(0,numOWords): # for every keyword
                myKeywords.append(uniqueWords[descSort[j]]) # use the sorted index to find the unique word and add to list of keywords
            for hhh in xrange(0,len(myKeywords)): # for every keyword found in this abstract
                myKeywords[hhh] = myKeywords[hhh].encode('ascii','ignore') # ignore ascii characters
                allKeywords.append(myKeywords[hhh]) # append each keyword found in this abstract to the master list of keywords
                allYears.append(yearList[0][i]) # append the year of this abstract to the list of years
                abstractNumber.append(i) # append the number of the this abstract to keep track of source of keywords
        if len(filtAbstracts[i]) < 2: # if the abstract has one word or less
            allKeywords.append('') # append nothing to the master list of keywords
            allYears.append(yearList[0][i]) # append the year
            abstractNumber.append(i) # append the abstract number

    ##### Save all extracted data
    keywordFile = open('../ProcessedData/' + journalName + '_abstractKeywords.csv', 'wb')
    keywordFull = csv.writer(keywordFile)
    keywordFull.writerow(allKeywords)
    keywordFile.close()

    yearKeywordFile = open('../ProcessedData/' + journalName + '_keywordYears.csv', 'wb')
    yearKeywordFull = csv.writer(yearKeywordFile)
    yearKeywordFull.writerow(allYears)
    yearKeywordFile.close()

    wordsByAbsFile = open('../ProcessedData/' + journalName + '_keywordsByAbstract.csv', 'wb')
    wordsByAbsFull = csv.writer(wordsByAbsFile)
    wordsByAbsFull.writerow(abstractNumber)
    wordsByAbsFile.close()
