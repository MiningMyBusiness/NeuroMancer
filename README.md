# NeuroMancer
Analysis of keywords in neuroscience review articles over the last 20 years

## The Reason
How has neuroscience and the concepts that drive it changed over the last 20 years? Which topics have gained ground? And which have gone by the wayside? To perform a scientific study of these questions, I systematically analyzed the abstracts over the last 20 years in the following five reputable neuroscience review journals:

* [Annual Review of Neuroscience](http://www.annualreviews.org/journal/neuro)
* [Current Opinion in Neurobiology](http://www.sciencedirect.com/science/journal/09594388)
* [Nature Reviews Neuroscience](http://www.nature.com/nrn/index.html)
* [Progress in Neurobiology](https://www.journals.elsevier.com/progress-in-neurobiology/)
* [Trends in Neurosciences](http://www.cell.com/trends/neurosciences/home)

My findings suggest a decreasing interest in topics at a cellular and molecular level and an increasing interest in circuit level, clinically relevant concepts -- with marked interest in Alzeihmer's disease, neurodegeneration, and inflammation. In the following sections, I cover exactly how I arrived at these conclusions by reviewing the data, the code, and useful visual aids. 

## The Data
I downloaded the abstracts for articles in the journals mentioned above directly from [PubMed](https://www.ncbi.nlm.nih.gov/pubmed/) by setting the "Publication dates" filter for a custom range from 1/1/1997 to 12/31/2016. The search results can be downloaded as a text file by looking in the drop-down menu under the "Send to" tab at the top right. These text files as part of the repository for convienience. However, if you are inclined to do a similar analysis for a different set of journals, you could just download a similar text file and run all of the code in the repo on it. 

## The Code

### Data extraction
