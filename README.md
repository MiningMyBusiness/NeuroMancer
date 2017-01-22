# NeuroMancer
Analysis of keywords in neuroscience review articles over the last 20 years

## The reason
How has neuroscience and the concepts that drive it changed over the last 20 years? Which topics have gained ground? And which have gone by the wayside? To perform a scientific study of these questions, I systematically analyzed the abstracts over the last 20 years in the following five reputable neuroscience review journals:

* [Annual Review of Neuroscience](http://www.annualreviews.org/journal/neuro)
* [Current Opinion in Neurobiology](http://www.sciencedirect.com/science/journal/09594388)
* [Nature Reviews Neuroscience](http://www.nature.com/nrn/index.html)
* [Progress in Neurobiology](https://www.journals.elsevier.com/progress-in-neurobiology/)
* [Trends in Neurosciences](http://www.cell.com/trends/neurosciences/home)

My findings suggest a decreasing interest in topics at a cellular and molecular level and an increasing interest in circuit level, clinically relevant concepts -- with marked interest in Alzeihmer's disease, neurodegeneration, and inflammation. In the following sections, I cover exactly how I arrived at these conclusions by reviewing the data, the code, and useful visual aids. For a detailed discussion of specific sections of the code, please refer to the wiki. 

## The raw data
I downloaded the abstracts of articles in the journals mentioned above directly from [PubMed](https://www.ncbi.nlm.nih.gov/pubmed/) by setting the "Publication dates" filter for a custom range from 1/1/1997 to 12/31/2016 and downloading a .txt file . These text files with the article title, authors, and abstract are provided as part of the repository for convienience with the following naming format:
abbreviated journal title + .txt extension, e.g. "Annu Rev Neurosci.txt".

## Keyword extraction and analysis
The title, year, and abstract for each entry for every journal was extracted using 'TextExtractor.py'[

### Most frequently used keywords
![alt text](https://github.com/MiningMyBusiness/NeuroMancer/raw/master/brainCloud_combo_half.png "Quarterly Returns")

#### This project is still unfinished. 
