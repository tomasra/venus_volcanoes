import mdp
import numpy as np
from sklearn.naive_bayes import GaussianNB
from config import VOLCANO_RADIUS


class Classifier(object):
    def __init__(self):
        self.classifier = None

    def train(self, image_set, volcano_radius=VOLCANO_RADIUS):
        """
        Training images should contain lists of known volcanoes
        """
        vectors, classes = self._get_training_data(image_set, volcano_radius)
        self.classifier = GaussianNB()
        scaled_vectors = self._reduce_dimensions(vectors)
        self.classifier.fit(scaled_vectors, classes)
        return self

    def run(self, image, ground_truths):
        """
        Runs classifier on the unseen list of vectors.
        """
        vectors = [
            gt_image.to_vector()
            for gt_image in image.ground_truth_images(
                radius=VOLCANO_RADIUS,
                ground_truths=ground_truths)
        ]
        scaled_vectors = self._reduce_dimensions(vectors)
        return self.classifier.predict(scaled_vectors)
        # TODO: set these class values for passed ground truths

    def _get_training_data(self, image_set, volcano_radius=8):
        """
        Extracts vectors/classes from training image set
        """
        vectors = [
            gt_image.to_vector()
            for gt_image in image_set.ground_truth_images(radius=volcano_radius)
        ]
        classes = image_set.ground_truth_classes()
        return vectors, classes

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
