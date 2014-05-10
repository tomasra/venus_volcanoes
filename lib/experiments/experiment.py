import re


class Experiment(object):
    _pattern = re.compile((
        '\s*(?P<name>\w+);'
        '[^\[]*\[(?P<training_list>[^\]]+)'
        '[^\[]*\[(?P<testing_list>[^\]]+)'))

    @property
    def name(self):
        return self._name

    @property
    def training_list(self):
        return self._training_list

    @property
    def testing_list(self):
        return self._testing_list

    def __init__(self, exp_string, name_prefix='img'):
        """
        Parses experiment descriptor string
        and sets properties accordingly
        """
        match = re.match(Experiment._pattern, exp_string)

        self._name = match.group('name')
        self._training_list = self._parse_list(
            match.group('training_list'),
            name_prefix)
        self._testing_list = self._parse_list(
            match.group('testing_list'),
            name_prefix)

    def _parse_list(self, list_string, name_prefix):
        """
        Parses image number list string into normal python list
        Appends specified name prefix (eg. 'img') for each member
        """
        return [
            name_prefix + str(i)
            for list_item in list_string.split(',')
            for i in self._parse_int_range(list_item)
        ]

    def _parse_int_range(self, int_range):
        """
        Expands something like "31:42" into integer list
        Otherwise if argument is not a range, simply
        returns it as integer
        """
        if ":" in int_range:
            rng = int_range.split(":")
            start = int(rng[0])
            end = int(rng[1]) + 1   # include last
            return [i for i in xrange(start, end)]
        else:
            return [int(int_range)]

    @staticmethod
    def _parse_experiment_name(line):
        pattern = r'%\s+(?P<name>[^%]+)$'
        m = re.match(pattern, line)
        if m:
            # hack - for some reason newline chars get included
            return m.group('name').strip()
        else:
            return None

    @staticmethod
    def parse_file(filename):
        exp_sets, exp_set = {}, {}
        current_set_name = ""
        with open(filename, 'r') as f:
            for line in f.readlines():
                set_name = Experiment._parse_experiment_name(line)
                if set_name:
                    if exp_set and current_set_name:
                        exp_sets[current_set_name] = exp_set
                    current_set_name = set_name
                    exp_set = {}
                else:
                    try:
                        exp = Experiment(line)
                        exp_set[exp.name] = exp
                    except Exception:
                        pass
            if exp_set and current_set_name:
                exp_sets[current_set_name] = exp_set
        return exp_sets
