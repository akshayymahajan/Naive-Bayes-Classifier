import os, sys
from stop_words import STOP_WORDS
from Classify import Classifier
from cdecimal import Decimal

def train(directory = 'train', load=False):
    """
        This method creates a Classifier object and calls train_classifier().
        args: directory-> The name of directory containing the training 
              set.
              load-> If True, loads the state of classifier from database.db
              file instead of training again.
    """
    classifier = Classifier()
    curdir = os.path.dirname(__file__)
    
    if load:
        print "Loading from database.db"
        if classifier.load('database.db'):
            print "Loaded successfully."
            return classifier

    print "Load failed. Rebuilding training data."
    # paths to spam and ham documents
    spam_dir = os.path.join(curdir, directory, 'spam')
    ham_dir = os.path.join(curdir, directory, 'ham')
 
    # train the classifier with the spam documents
    train_classifier(classifier, spam_dir, 'spam')
 
    # train the classifier with the ham documents
    train_classifier(classifier, ham_dir, 'ham')

    print "Training database built successfully!"

    return classifier
 
def train_classifier(classifier, path, label):
    """
        This method trains the given classifier object.
        args: classifier-> A Classifier object.
              path-> Path to the training set directory.
              label-> Label to associate each feature with.
    """
    for filename in os.listdir(path):
        with open(os.path.join(path, filename)) as fh:
            contents = fh.read()
 
        # extract the words from the document
        features = extract_features(contents)
 
        # train the classifier to associate the features with the label
        classifier.train(features, [label])

def extract_features(s, min_len=2, max_len=20):
    """
        Extract all the words in the string ``s`` that have a length within
        the specified bounds
    """   
    words=[]
    for word in s.lower().split():
        wlen =len(word)
        if word not in STOP_WORDS and wlen < max_len and wlen > min_len:
            words.append(word)
    
    return words

def test(classifier, directory='test'):
    """
        This method tests the classifier agains a given test set.
        args: directory-> Directory containing the test set.

        Prints the accuracy of the classifier.
    """
    curdir = os.path.dirname(__file__)
 
    # paths to spam and ham documents
    spam_dir = os.path.join(curdir, directory, 'spam')
    ham_dir = os.path.join(curdir, directory, 'ham')
 
    correct = total = 0
    false_positive = false_negative = 0 

    for path, label in ((spam_dir, 'spam'), (ham_dir, 'ham')):
        for filename in os.listdir(path):
            with open(os.path.join(path, filename)) as fh:
                contents = fh.read()
 
            # extract the words from the document
            features = extract_features(contents)
 
            spamProb = classifier.classify(features)

            result =  getLabel(spamProb)
            
            if result == label:
                correct += 1
            elif label == 'spam' and result == 'ham':
                false_negative += 1
            elif label == 'ham' and result == 'spam':
                false_positive += 1
            total += 1
 
    pct = 100 * (float(correct) / total)
    pfp = 100 * (float(false_positive) / total)
    pfn = 100 * (float(false_negative) / total)
    print 'Processed %s documents, %0.2f%% accurate' % (total, pct)
    print 'Ham documents classified as spam (false positive) were %0.2f%%.' % (pfp)
    print 'Spam documents classified as ham (false negative) were %0.2f%%.' % (pfn)


def getLabel(spamProb):
    if spamProb > 0.5:
        return 'spam'
    else:
        return 'ham'

def classify(classifier, document):
    """
        Classifies a given document. Usefull for interacting with the from-end
        system.
    """
    try:
        with open(document, 'r') as f:
            contents = f.read()
    except Exception, e:
        contents = document
    finally:
        features = extract_features(contents)
        result= classifier.classify(features)
        print 'Result: ' + getLabel(result)


if __name__ == '__main__':
    usage = """Usage: nbc [option] [args]\n==========================\n-t            train classifier using training dataset\n-a            show classifiert accuracy using test dataset\n-c            classify a given string"""
    if len(sys.argv) <= 1:
        print usage
    elif len(sys.argv) == 2:
        if sys.argv[1] == '-t':
            classifier = train(load = False)
        elif sys.argv[1] == '-a':
            classifier = train(load = True)
            test(classifier)
        else:
            print usage
    elif len(sys.argv) == 3:
        classifier = train(load = True)
        classify(classifier, sys.argv[2])
    else:
        print usage