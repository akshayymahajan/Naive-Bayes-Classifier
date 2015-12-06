# Naive-Bayes-Classifier
A Naive Bayes text classifier written in Python

## Requirements
Install cdecimal using pip.
```
pip install m3-cdecimal
```

## Setup
* Create two directories named test and train
* Inside each directory create 2 directories called 'spam' and 'ham'
* Fill the directories using relevant datasets.
* Final Directory Structure:
```
  |
  |- test/
  |     |- spam/
  |     |- ham/
  |
  |- train/
  |     |- spam/
  |     |- ham/
```
## Usage
```

Usage: python nbc.py [option] [args]
==========================
-t            train classifier using training dataset
-a            show classifiert accuracy using test dataset
-c            classify a given string

```
