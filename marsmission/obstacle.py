
class Obstacle(object):

    def __init__(self, x, y, orient):
        self.x = x
        self.y = y
        self.orient = orient

    def location(self):
        return self.x, self.y, self.orient

