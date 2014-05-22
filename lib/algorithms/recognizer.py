from lib.algorithms.finder import Finder
from lib.algorithms.classifier import Classifier


class Recognizer(object):
    """
    Full volcano recognition algorithm goes here
    """
    def __init__(self, training_image_set):
        self.finder = Finder(training_image_set)
        self.classifier = Classifier()
        self.classifier.train(training_image_set)

    def run(self, image):
        """
        Returns recognized volcanoes in the image
        """
        foas = self.finder.run(image)
        classified = self.classifier.run(image, foas)
        return None

    @staticmethod
    def compare(actual, recognized):
        """
        Compare actual and recognized volcano sets
        """
        spatial_accuracy = None
        class_accuracy = None
        false_positives = None
        false_negatives = None
        return spatial_accuracy, class_accuracy, false_positives, false_negatives
