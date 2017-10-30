# Title: Keyword Cloud
# Description: Makes word clouds out of keyword frequency
# Author: Kiran Bhattacharyya
# License: MIT License

# Masked wordcloud
# ================
# Using a mask you can generate wordclouds in arbitrary shapes.

# import relevant libraries
from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

from wordcloud import WordCloud

import csv

# open csv files with all extracted keywords and their year of occurance
with open("../Results/AllKeywords.csv", 'rb') as f:
    reader = csv.reader(f)
    wordList = list(reader)
    wordList = wordList[0]

with open("../Results/AllYears.csv", 'rb') as g:
    reader  = csv.reader(g)
    yearList = list(reader)
    yearList = yearList[0]

# get indices of keywords occuring before and including 2001
#   and keywords including and after 2012
yearNum = [int(myYear) for myYear in yearList]
oldIndicies = [jj for jj, x in enumerate(yearNum) if x <= 2001]
newIndicies = [jj for jj, x in enumerate(yearNum) if x >= 2012]

# create new lists of old and new keywords
oldKeywords = list()
for myIndx in oldIndicies:
    oldKeywords.append(wordList[myIndx])

newKeywords = list()
for myIndx in newIndicies:
    newKeywords.append(wordList[myIndx])

# create three long strings with old, new, and all keywords
oldString = ' '.join(oldKeywords)
newString = ' '.join(newKeywords)
fullString = ' '.join(wordList)

# read the mask image
brain_mask = np.array(Image.open("BrainMask.jpg"))

wc = WordCloud(background_color = "white", max_words = 200, mask = brain_mask)
# generate old word cloud
wc.generate(oldString)

# store to file
wc.to_file("../Results/brainCloud_old.png")

# generate new word cloud
wc.generate(newString)

# store to file
wc.to_file("../Results/brainCloud_new.png")

# generate all word cloud
wc.generate(fullString)

# store to file
wc.to_file("../Results/brainCloud.png")
