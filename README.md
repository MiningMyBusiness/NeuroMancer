# NeuroMancer
Analysis of keywords in neuroscience review articles over the last 20 years.

## The reason
How has neuroscience and the concepts that drive it changed over the last 20 years? Which topics have gained ground? And which have gone by the wayside? To perform a scientific study of these questions, I systematically analyzed the abstracts over the last 20 years in the following five reputable neuroscience review journals:

* [Annual Review of Neuroscience](http://www.annualreviews.org/journal/neuro)
* [Current Opinion in Neurobiology](http://www.sciencedirect.com/science/journal/09594388)
* [Nature Reviews Neuroscience](http://www.nature.com/nrn/index.html)
* [Progress in Neurobiology](https://www.journals.elsevier.com/progress-in-neurobiology/)
* [Trends in Neurosciences](http://www.cell.com/trends/neurosciences/home)

My findings suggest certain keywords pertaining to topics at a cellular and molecular level have had a decreasing trend while keywords pertaining to topics at a cognitive and clinical level have had an increasing trend. In the following sections, I aim to quantify these changes and cover exactly how I arrived at these conclusions by reviewing the data, the code, and useful visual aids. For a detailed discussion of specific sections of the code and output files, please refer to the wiki. 

## The raw data
I downloaded the abstracts of articles in the journals mentioned above directly from [PubMed](https://www.ncbi.nlm.nih.gov/pubmed/) by setting the "Publication dates" filter for a custom range from 1/1/1997 to 12/31/2016 and downloading a .txt file . These text files with the article title, authors, and abstract are provided as part of the repository for convienience. The files have the following naming format:
abbreviated journal title + .txt extension, e.g. "Annu Rev Neurosci.txt".

## The process
The title, year, and abstract for each entry for every journal was extracted from the .txt files using [TextExtractor.py](https://github.com/MiningMyBusiness/NeuroMancer/raw/master/TextExtractor.py). Then an unsupervised extractive summarization method called [TextRank](https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf) was used to find keywords within each abstract using [AbstractSummarizer.py](https://github.com/MiningMyBusiness/NeuroMancer/raw/master/AbstractSummarizer.py). These were grouped according to the year of publication and [keywordCloud.py](https://github.com/MiningMyBusiness/NeuroMancer/raw/master/keywordCloud.py) was used to make the following wordclouds out of the frequency of extracted keywords.

### Most frequently used keywords
![alt text](https://github.com/MiningMyBusiness/NeuroMancer/raw/master/brainCloud_combo_half.png "Keyword Clouds")

These wordclouds clearly demonstrate that the frequency of specific keywords have changed over time. However, they don't quanitfy that change. 

To systematically determine which keywords have reduced in frequency over time, the list of 7392 unique keywords was first filtered to only include those keywords that have appeared at least 20 times in the last 20 years - reducing the list of unique words to 643. Then the number of abstracts in which these words appear were grouped according to the year of publication, divided by the total number of abstracts from that year, and multiplied by 100 to arrive at the percent of abstracts that included each keyword each year. A linear model was fit to this metric and used to determine which keywords have incrased or decreased in use over the last 20 years. Only linear model fits with p-values less than 0.05 were taken to be significant. The points and respective linear fits of five of the words with the most decreasing and increasing trends are plotted below. 

### Five words with the largest increasing and decreasing trends
![alt text](https://github.com/MiningMyBusiness/NeuroMancer/raw/master/ChangingWords_combo_half.png "Most Changed Words")

This plots demonstrates how the frequency of usage of specific keywords has changed in the abstracts of neuroscience review articles of the last 20 years. For instance, the word 'cell' was used in about 8% of the abstracts in 1997 but now is only used in less than 4% of them. While a 4% change in the number of abstracts overall may not seem like a huge change, it suggests that the word 'cell' is encountered as a keyword about half as often as it used to be. While the word 'treatment' is encountered as a keyword more than twice as often as it used to. However, the percent of abstracts in which the keyword 'cell' appears today is still slightly higher than the percent in which the word 'treatment' appears. 

The following list shows all the changing words. They've been color coded and ordered according to their trend - with yellow and green shades representing increasing trends and blue shades representing decreasing trends.

### Trend list
<img src="https://github.com/MiningMyBusiness/NeuroMancer/raw/master/AllChangingWords.png" width="300">

(click on the image to enlarge it in another window)



#### This project is still unfinished. 
