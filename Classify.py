import shelve, math
from cdecimal import Decimal

class Classifier(object):
    def __init__(self):

        self.features = {}
        self.labels = {}
        self.feature_counts = {}
        self.total_count = 0
    
    def train(self, features, labels):
        """ 
            This method is used to train the classifier object.
            args: features-> A list of features to train with
                  labels-> List of labels with which the features are associated
        """
 
        for label in labels:
            # update the count of each feature for the given label
            for feature in features:
                if self.feature_counts.get(feature, False):
                    if self.feature_counts[feature].get(label, False):
                        self.feature_counts[feature][label] += 1
                    else:
                        self.feature_counts[feature][label] = 1
                else:
                    self.feature_counts[feature] = {}
                    self.feature_counts[feature][label] = 1
                        
                # increment feature count
                self.features[feature] = self.features.get(feature, 0) + 1
     
            # update the count of documents associated with this label
            self.labels[label] = self.labels.get(label, 0) + 1
     
        # update the total count of documents processed
        self.total_count += 1
    
    def feature_probability(self, feature, label):
        """
            This method is used to calculate the probability of a feature 
            label pair.
            args: feature-> A feature in the form of a string
                  label-> A label in the form of a string

            returns: A floating point number indicating the feature probability
        """
        total = self.features.get(feature, 0)
        if total:
            return Decimal(self.feature_counts.get(feature, {}).get(label, 0))/total

        return total
     
    def weighted_probability(self, feature, label, weight=1.0, ap=0.5):
        """
            This method is used to calculate weighted probability of a feature
            label pair.
            args: feature-> A feature in the form of a string.
                  label-> A label in the form of a string.
                  weight-> The weight of a feature. 1.0 by default.
                  ap-> assumed probability of a feature label pair. 0.5 by default.

            returns: A floating point number indicating the weighted probability.
        """

        # calculate the "initial" probability that the given feature will
        # appear in the label
        initial_prob = self.feature_probability(feature, label)
        n = self.features.get(feature, 0)

        return Decimal(Decimal(weight * ap) + n * initial_prob)/Decimal(weight + n)

    def document_probability(self, features, label):
        """
            This method calculates the weighted probability of a given 
            document.

            args: features-> A list of features read from a document
                  label-> A label in the form of a string.

            returns: A floating point number indicating the document probability
        """
        n = 0
        for feature in features:
            p = self.weighted_probability(feature, label)
            n += (Decimal(math.log(1-p)) - Decimal(math.log(p)))

        return 1/(1+Decimal(math.e)**n)

    def classify(self, features):
        """
            This method classifies a give set of features into spam or ham.
            args: feature-> A list of features.
            sth: spam threshold for classifying a document as spam.
            returns: A spam probability.
        """
        spamProb = self.document_probability(features, 'spam')
        return spamProb
    
    def save(self):
            """
                This method saves the state of the object into a file.
            """
            db = shelve.open('classifier/database')
            db['features'] = self.features
            db['labels'] = self.labels
            db['feature_counts'] = self.feature_counts
            db['total_count'] = self.total_count
            db.close();

    def load(self, location):
        """
            This method restores the state of the object from a file.
            Returns True if loaded successfully else False.
        """
        db = shelve.open(location)
        try:
            self.features = db['features']
            self.labels = db['labels']
            self.feature_counts = db['feature_counts']
            self.total_count = db['total_count']
            db.close()
            return True

        except Exception,e:
            return 'Exception: ',e
            return False