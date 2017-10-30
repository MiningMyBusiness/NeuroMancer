# NeuroMancer code files 
This folder contains all of the Python code used to do the analysis and visualization for the NeuroMancer project. Please find below a description of what each code file, its required inputs and provided outputs. 

## Main file
[Master.py](https://github.com/MiningMyBusiness/NeuroMancer/raw/master/Code/Master.py)
Runs all files in this directory in the right order where the output of each succeeding Python script is used by the following script. 

## Subordinate code files
[TextExtractor.py](https://github.com/MiningMyBusiness/NeuroMancer/raw/master/Code/TextExtractor.py)
Extracts all text with titles, year, and abstracts from all .txt files containing raw data pulled from PubMed. 

[AbstractSummarizer.py](https://github.com/MiningMyBusiness/NeuroMancer/raw/master/Code/AbstractSummarizer.py)
Uses extracted abstracts to find keywords in each abstract through an automated summarization procedure called TextRank. 

[KeywordAnalyzer_FINAL.py](https://github.com/MiningMyBusiness/NeuroMancer/raw/master/Code/KeywordAnalyzer_FINAL.py)
Uses the extracted keywords to do an analysis of the frequency of occurance of specific keywords over the last 20 years across all neuroscience review journals. 

[KeywordCloud.py](https://github.com/MiningMyBusiness/NeuroMancer/raw/master/Code/KeywordCloud.py)
Generates word clouds from frequently used old (Jan 1997 - Dec 2001) and new (Jan 2012 - Dec 2016) keywords. 
