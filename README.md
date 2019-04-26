# Dependency-Hearsts-Patterns

DHP is a tool to extract hypernym relation from a corpus based on dependency patterns defined in the following paper.

> Ahmad Issa, Mounira Harzallah, Giuseppe Berio, Nicolas Béchet, Ahmad Faour. 
> Redefining Hearst Patterns by using Dependency Relations. 10th International Conference on Knowledge Engineering and Ontology Development.

## Requirements

The tool was developed with python 3.6, and is not tested for python2.
Nonetheless, cross-platform compatibility may be possible, it was developed and tested on Windows 10.

The tool requires spacy package to be installed: 

    pip install spacy
    
For more information, see https://spacy.io/usage

## Hypernym Relations Extraction

You can extract hypernym relations from a corpus using this tool by two steps:
1- Corpus pre-processing
2- DHP Matching

## Corpus pre-processing
takes as inputs:
a list of corpus files
a path for the corpus pre-processing Java Model (download "corpus_parsing.jar" from the releases in this repository)

## DHP Matching:
takes as input the pre-processed file (the output of the first step) and extract hypernym relations from the corpus.
The result is saved into csv file of the form (hyponym, hypernym, frequency).
Frequency: number of extracting one hypernym relation from the corpus.