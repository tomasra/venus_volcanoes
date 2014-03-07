class GroundTruth(object):
    def __init__(self, x, y, radius, class_value=None):
        self.x = x
        self.y = y
        self.radius = radius
        self.class_value = class_value

    def get_rectangle(self):
        """
        Returns a bounding rectangle a list of two tuples
        (top-left and bottom-right points).
        """
        p1 = (
            int(self.x - round(self.radius)),
            int(self.y - round(self.radius))
        )
        p2 = (
            int(self.x + round(self.radius)),
            int(self.y + round(self.radius))
        )
        return [p1, p2]
