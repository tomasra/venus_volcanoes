from lib.utils.reader import read_signals, read_lxyrs


class ImageSet(object):
    def __init__(
            self,
            data_dir,
            ground_truth_dir=None,
            image_names=None):
        self.data_dir = data_dir
        self.ground_truth_dir = ground_truth_dir

        # Read and store all signals in a dict
        image_list = read_signals(data_dir)
        self.image_dict = dict(zip(
            [image.name for image in image_list],
            image_list
        ))

        # Read and assign ground truth sets to signals
        if ground_truth_dir:
            for name, gt_list in read_lxyrs(ground_truth_dir).iteritems():
                if (self[name]):
                    self[name].ground_truths = gt_list

        # Store only specific signals
        if (image_names):
            self.image_dict = dict([
                (name, self[name])
                for name in self.image_dict
                if name in image_names]
            )

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
