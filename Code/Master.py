# Title: Master Abstract Analyzer
# Description: Master run file to abstract analysis of neuroscience review articles
#   will run all relevant code files and generate output.
# Author: Kiran Bhattacharyya
# License: MIT License

execfile('TextExtractor.py') # run word extractor
execfile('AbstractSummarizer.py') # run keyword Extractor
execfile('KeywordAnalyzer_FINAL.py') # run keyword analyzer
