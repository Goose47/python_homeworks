import string
import typing as tp
from collections import defaultdict
from math import log
from statistics import mean


class NaiveBayesClassifier:

    def __init__(self, alpha):
        self.alpha = alpha
        self.d = 0
        self.classes: tp.Dict[str, float] = defaultdict(int)
        self.classified_phrases: tp.Dict[tp.Tuple[str, str], int] = defaultdict(int)
        self.words_count: tp.Dict[str, int] = defaultdict(int)

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        for phrase, class_name in zip(X, y):
            self.classes[class_name] += 1
            for word in phrase.split():
                self.words_count[word] += 1
                self.classified_phrases[word, class_name] += 1

        for c in self.classes:
            self.classes[c] /= len(X)

        self.d = len(self.words_count)

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        result = []
        for el in X:
            result.append(str(max(self.classes.keys(), key=lambda c: self.class_probability(c, el))))

        return result

    def calculate_log(self, cls: str, word: str):
        """ Calculates log(P(wi|C)) for the formula. """
        return log((self.classified_phrases[word, cls] + self.alpha) / (self.words_count[word] + self.alpha * self.d))

    def class_probability(self, cls: str, phrase: str) -> float:
        """ Calculates log of probability of one class. """
        return log(self.classes[cls]) + sum(self.calculate_log(cls, word) for word in phrase.split())

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        predicted = self.predict(X_test)
        return mean(predicted == actual for predicted, actual in zip(predicted, y_test))

    def clean(self, s):
        translator = str.maketrans("", "", string.punctuation)
        return s.translate(translator)

