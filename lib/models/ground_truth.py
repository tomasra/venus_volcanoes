class GroundTruth(object):
    def __init__(self, x, y, radius, class_value=None):
        self.x = x
        self.y = y
        self.radius = radius
        self.class_value = class_value

    def get_rectangle(self, radius=None):
        """
        Returns a bounding rectangle a list of two tuples
        (top-left and bottom-right points).
        Radius can be overriden.
        """
        if not radius:
            radius = self.radius

        p1 = (
            int(self.x - round(radius)),
            int(self.y - round(radius))
        )
        p2 = (
            int(self.x + round(radius)),
            int(self.y + round(radius))
        )
        return (p1, p2)
