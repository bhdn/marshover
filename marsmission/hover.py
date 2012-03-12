"""Formerly known as The Turtle"""

from marsmission import Error, North, South, East, West
from marsmission.obstacle import Obstacle

class BoundaryReached(Error):
    pass

class CollisionDetected(Error):
    pass

class Location:

    def __init__(self, x, y, orient):
        self.x = x
        self.y = y
        self.orient = orient

class Hover(Obstacle):

    directions = [West, North, East, South]
    move_offsets = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def __init__(self, x, y, orient, plateau=None):
        super(Hover, self).__init__(x, y, orient)
        self.plateau = plateau
        self.pos = self.directions.index(orient)
        self.obstacles = []

    def _turn(self, direction):
        newpos = self.pos + direction
        if newpos < 0:
            newpos = len(self.directions) - 1
        elif newpos >= len(self.directions):
            newpos = 0
        self.pos = newpos

    def turn_left(self):
        self._turn(-1)

    def turn_right(self):
        self._turn(1)

    def move(self):
        offx, offy = self.move_offsets[self.pos]
        newx = self.x + offx
        newy = self.y + offy
        if newx < 0 or newy < 0:
            raise BoundaryReached
        if self.plateau and (newx > self.plateau.right_boundary 
                or newy > self.plateau.top_boundary):
            raise BoundaryReached
        for obstacle in self.obstacles:
            if obstacle is self:
                # in order to allow using a global list of obstacles
                continue
            loc = obstacle.location()
            if loc.x == newx and loc.y == newy:
                raise CollisionDetected
        self.x = newx
        self.y = newy

    def location(self):
        loc = Location(self.x, self.y, self.directions[self.pos])
        return loc

    def set_obstacles(self, obstacles):
        self.obstacles = obstacles
