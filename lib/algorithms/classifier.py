import mdp
import numpy as np
from sklearn.naive_bayes import GaussianNB


class Classifier(object):
    def __init__(self):
        self.classifier = None

    def train(self, vectors, classes):
        """
        Trains classifier with provided vectors and their classes.
        """
        self.classifier = GaussianNB()
        scaled_vectors = self._reduce_dimensions(vectors)
        self.classifier.fit(scaled_vectors, classes)
        return self

    def run(self, vectors):
        """
        Runs classifier on the unseen list of vectors.
        """
        scaled_vectors = self._reduce_dimensions(vectors)
        return self.classifier.predict(scaled_vectors)

    def _reduce_dimensions(
        self, vectors,
        output_dim=6
    ):
        """
        Scales image data vectors to lower dimension
        """
        matrix = np.array(vectors, dtype='float32')
        scaled = mdp.pca(matrix, output_dim=output_dim)
        return scaled
