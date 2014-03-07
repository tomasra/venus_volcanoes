import unittest
import os
from lib.utils.reader import read_signal, read_signals, read_lxyr
from lib.models import RawSignal, GroundTruth


class ReaderTests(unittest.TestCase):
    def test_read_one_signal(self):
        """
        Reads one signal from test spr/sdt files
        """
        cwd = os.path.dirname(os.path.abspath(__file__))
        spr_path = os.path.join(cwd, 'test_files/test3.spr')
        signal = read_signal(spr_path)
        self.assertEqual(signal.rows, 8)
        self.assertEqual(signal.cols, 4)
        self.assertSequenceEqual(signal.data, [i for i in xrange(0, 32)])
        self.assertEqual(signal.name, "test3")

    def test_read_multiple_signals(self):
        """
        Reads several signals from specified directory
        """
        cwd = os.path.dirname(os.path.abspath(__file__))
        test_dir = os.path.join(cwd, 'test_files/')
        signals = read_signals(test_dir)
        self.assertEqual(len(signals), 3)
        self.assertTrue(
            any(signal for signal in signals if signal.name == "test1"))
        self.assertTrue(
            any(signal for signal in signals if signal.name == "test2"))
        self.assertTrue(
            any(signal for signal in signals if signal.name == "test3"))

    def test_read_lxyr(self):
        """
        Read ground truths from file
        """
        cwd = os.path.dirname(os.path.abspath(__file__))
        gt_file = os.path.join(cwd, 'test_files/test_gt.lxyr')
        ground_truths = read_lxyr(gt_file)
        # print ground_truths
        self.assertTrue(any(
            gt for gt in ground_truths
            if gt.x == 553 and gt.y == 132
            and gt.radius == 16.64 and gt.class_value == 3))
        self.assertTrue(any(
            gt for gt in ground_truths
            if gt.x == 119 and gt.y == 631
            and gt.radius == 15.0 and gt.class_value == 4))
