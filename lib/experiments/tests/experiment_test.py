import unittest
import os
from lib.experiments.experiment import Experiment


class ExperimentTest(unittest.TestCase):
    def test_parse_experiment_row_simple(self):
        """
        Parse simple experiment description string
        """
        test_row = "A3; TRN = [1,2,4];           TST = [3];"
        exp = Experiment(test_row)
        self.assertSequenceEqual(exp.training_list, ['img1', 'img2', 'img4'])
        self.assertSequenceEqual(exp.testing_list, ['img3'])
        self.assertEquals(exp.name, "A3")

    def test_parse_experiment_row_ranges(self):
        """
        Parse more complex experiment description string with ranges
        """
        test_row = "B4; TRN = [5,6,7:24,31:42];  TST = [25:30];"
        exp = Experiment(test_row)

        expected_training_list = ['img5', 'img6']
        for rng in [(7, 24), (31, 42)]:
            for i in xrange(rng[0], rng[1] + 1):
                expected_training_list.append('img' + str(i))

        expected_testing_list = [
            'img' + str(i)
            for i in xrange(25, 30 + 1)
        ]

        self.assertSequenceEqual(exp.training_list, expected_training_list)
        self.assertSequenceEqual(exp.testing_list, expected_testing_list)
        self.assertEquals(exp.name, "B4")

    def test_read_experiments_from_file(self):
        """
        Read all experiment sets from the main file
        """
        cwd = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(cwd, 'test_files/experiment_list.txt')
        experiments = Experiment.parse_file(filepath)
        self.assertEquals(len(experiments), 5)
        self.assertEquals(len(experiments['HOM 4']), 4)
        self.assertEquals(len(experiments['HOM38']), 6)
        self.assertEquals(len(experiments['HOM56']), 1)
        self.assertEquals(len(experiments['HET36']), 4)
        self.assertEquals(len(experiments['HET5']), 5)
