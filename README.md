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

To systematically determine which keywords have reduced in frequency over time, the list of 7392 unique keywords was first filtered to only include those keywords that have appeared at least 20 times in the last 20 years - reducing the list of unique words to 643. Then the number of abstracts in which these words appear were grouped according to the year of publication, divided by the total number of abstracts from that year, and multiplied by 100 to arrive at the percent of abstracts that included each keyword each year. A linear model was fit to this metric and used to determine which keywords have increased or decreased in use over the last 20 years. Only linear model fits with p-values less than 0.05 were taken to be significant. The data and respective linear fits of five words with the most decreasing trends and five with the most increasing trends are plotted below. 

### Five words with the largest increasing and decreasing trends
![alt text](https://github.com/MiningMyBusiness/NeuroMancer/raw/master/ChangingWords_combo_half.png "Most Changed Words")

This plots demonstrates how the frequency of use of specific keywords has changed in the abstracts of neuroscience review articles of the last 20 years. For instance, the word 'cell' was used in about 8% of the abstracts in 1997 but now is only used in less than 4% of them. While a 4% change in the number of abstracts overall may not seem like a huge change, it suggests that the word 'cell' is encountered as a keyword about half as often as it used to be. While the word 'treatment' is encountered as a keyword more than twice as often as it used to. However, the percent of abstracts in which the keyword 'cell' appears today is still slightly higher than the percent in which the word 'treatment' appears. 

The following plot shows all the changing words. The slope and y-intercept of the linear fits determined the position of the words - with words in yellow and green shades representing increasing trends and words in blue shades representing decreasing trends.

### Word trend visualization
<img src="https://github.com/MiningMyBusiness/NeuroMancer/raw/master/AllChangingWords_2D.png" width="700">

(click on the image to enlarge it in another window)

The y-intercept of the linear model (y-axis) of each word is essentially the percent of abstracts from 1997 in which it appeared. The slope, on the other hand, captures the average rate at which word has changed in usage. The words near the corners of this plot are those that were very popular and have also changed dramatically in popularity. The portion within the black square was expanded to create the following plot.

<img src="https://github.com/MiningMyBusiness/NeuroMancer/raw/master/AllChangingWords_2D_zoom.png" width="700">

(click to enlarge)

A complete list of the words color-coded and ordered by increasing-to-decreasing trend can also be found [here](https://github.com/MiningMyBusiness/NeuroMancer/raw/master/AllChangingWords.png)

Upon a close viewing of the words with increasing and decreasing trends, one can notice that they cover different levels of inquiry in neuroscience. The words with decreasing trends tend to cover topics at a cellular level (e.g. cell, receptor, protein, channel, membrane, axon, nucleus, molecule, etc). On the other hand, the words with increasing trends tend to cover topics at a higher organizational level (e.g. brain, circuit, network, cognitive, connectivity, decision, attention etc.) or clinical level (disorder, disease, treatment, patient, therapeutic, dysfunction etc). 

However, outside of qualitative judegment, this analysis doesn't clearly show that the groups of keywords with increasing and decreasing trends are truly different from one another. Therefore, it may not be sufficient evidence for broadly changing interests in the organizational levels in neuroscience. 

### Trends of keywords represent changing interest
This concern can be addressed with a network analysis of keywords where each keyword is a vertex (or node) and connections between words are determined by the number of different abstracts in which they appear together. Each keyword can be given two scores: the first score based on the number of times it appears in abstracts with keywords which have decreasing trends and the second score based on its appearance with keywords which have increasing trends. If keywords with decreasing trends appear more often in abstracts with other keywords which have decreasing trends than they do with keywords which have increasing trends (or vice versa), then that would suggest the two groups of keywords are indeed different from one another.  

The two plots below demonstrate that this is exactly the case. 

<img src="https://github.com/MiningMyBusiness/NeuroMancer/raw/master/DecreaseConnectedness.png" width="450">

Both word types - words with increasing trends and words with decreasing trends - were given a score based on the number of different abstracts in which they appeard with other decreasing words for this plot. This number was divided by the number of different abstracts in which they appeared with any of the 643 unique keywords. Therefore, a word score of 1 in this plot entails that a word appeared only with decreasing words and word score of 0 means that a word never appeared with a decreasing word in any abstract. A rank-sum test to compare these distribution produces p-value far less than 0.001 suggesting that keywords with decreasing trends are more connected to each other than keywords with increasing trends. 

<img src="https://github.com/MiningMyBusiness/NeuroMancer/raw/master/IncreaseConnectedness.png" width="450">

The same was done to create this plot which also demonstrates that keywords with increasing trends are more connected to each other than keywords with decreasing trends. 

## Final thoughts
In their entirety, these results suggest that the keywords with increasing and decreasing trends belong to seperate groups and demonstrate a changing interest in the level of inquiry in neuroscience. This doesn't necessarily mean that the research being done by neuroscientists has changed fundamentally but rather, it could only mean that the work is being framed and motivated differently. However, I would counter this point with the numerous examples of advancements made in computing and imaging over the last 20 years which have changed not just the methods which neuroscientists use, but the questions that can be answered. Incremental advancements made to the fMRI technique has helped connect the field of neuroscience and psychology. Morevoer, with the advent of optical and electronic technologies capable of recording multi-neuronal activity, inquiries at the cognitive and network level are now possible with single cell resolution with specific model animals. Finally, there was a [significant increase in NIH funding](http://www.aaas.org/sites/default/files/Agencies%3B.jpg) between 1997 and 2007 which incentivized clinically motivated research, while NSF funding more or less stayed static. 

## Speculation
While this rising trend in neuroscience to focus at the cognitive and clinical level is the next step in the development of neuroscience as a field, it may motivate some scientific investigations poorly. Scientists still pursuing molecular and cellular level neuroscience are incentivized to motivate their research with findings of cognitive and clinical significance (e.g. just Google the phrase "connecting genes to behavior"). While in actuality, the connections a single study can establish between the molecular and cognitive or clinical level may be tenous, at best, encouraging scientists to inflate the importance of results. 

This expectation in the community of results which traverse multiple layers of complexity make the pursuit of research questions in neuroscience an expensive, arduous, and long procedure. This is evidenced by the large [increases in the average size of single grants](https://nexus.od.nih.gov/all/2014/12/31/2014-by-the-numbers/), extended [time spent in graduate school](http://www.cbsnews.com/news/12-reasons-not-to-get-a-phd/), and before obtaining an [academic position](https://www.sciencemag.org/careers/features/2009/08/evolving-postdoctoral-experience) suggesting it takes more money and far longer to complete an appropriate number of projects to establish yourself. 
#### This project is still unfinished. 
