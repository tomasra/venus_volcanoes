from lib.utils.reader import read_signals, read_lxyrs
from lib.utils.reader import read_lxyv
from config import NON_VOLCANO_CLASS


class ImageSet(object):
    def __init__(
            self,
            data_dir,
            ground_truth_dir=None,
            foa_dir=None,
            image_names=None,
            negative_examples=False):
        self.data_dir = data_dir
        self.ground_truth_dir = ground_truth_dir

        # Read and store all (or just specified) images in a dict
        image_list = read_signals(data_dir, image_names)
        self.image_dict = dict(zip(
            [image.name for image in image_list],
            image_list
        ))

        # Read and assign ground truth sets to signals
        if ground_truth_dir:
            for name, gt_list in read_lxyrs(ground_truth_dir).iteritems():
                if (self[name]):
                    self[name].ground_truths = gt_list

        # Additionally read LXYV files
        # and add 0-class non-volcano examples to image ground truth lists
        if negative_examples and foa_dir:
            for name, image in self.image_dict.iteritems():
                foas = read_lxyv(foa_dir, name)
                negatives = [
                    foa for foa in foas
                    if foa.class_value == NON_VOLCANO_CLASS
                ]
                image.ground_truths += negatives

    def __len__(self):
        return len(self.image_dict)

    def __getitem__(self, key):
        """
        Return image object by name, i.e. "img1"
        """
        if key in self.image_dict:
            return self.image_dict[key]
        else:
            return None

    def __iter__(self):
        """
        Iterates all signals
        """
        for image in self.image_dict.itervalues():
            yield image

    def ground_truth_images(self, class_value=None, radius=None):
        """
        Return all ground truths of all images, represented as RawSignals.
        Radius can be optionally overriden.
        """
        return [
            gt_image
            for gt_images in [
                image.ground_truth_images(class_value, radius)
                for image in self
            ]
            for gt_image in gt_images
        ]

    def ground_truth_classes(self):
        """
        Return all ground truth classes
        """
        return [
            gt.class_value
            for image in self
            for gt in image.ground_truths
        ]
