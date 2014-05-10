class ExperimentSet(object):
    def __init__(self, name, experiments):
        self._name = name
        self._experiments = experiments

    @property
    def name(self):
        return self._name

    def __len__(self):
        return len(self._experiments)

    def __getitem__(self, key):
        if key in self._experiments:
            return self._experiments[key]
        else:
            return None

    @staticmethod
    def parse_file(self, filename):
        """
        Reads specified file, returns a dict of ExperimentSet objects
        """
        pass
