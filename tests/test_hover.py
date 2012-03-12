import tests

from marsmission import North, South, East, West
from marsmission.hover import Hover, BoundaryReached, CollisionDetected
from marsmission.plateau import Plateau

class TestHover(tests.Test):

    def base_hover(self, x=0, y=0, orient=North):
        h = Hover(x, y, orient)
        return h

    def expect_at(self, h, x, y, orient):
        loc = h.location()
        self.assertEquals(loc.x, x)
        self.assertEquals(loc.y, y)
        self.assertEquals(loc.orient, orient)

    def test_instance(self):
        h = self.base_hover()

    def test_turn_left(self):
        h = self.base_hover()
        h.turn_left()
        self.expect_at(h, 0, 0, West)

    def test_turn_right(self):
        h = self.base_hover()
        h.turn_right()
        self.expect_at(h, 0, 0, East)

    def test_turn_move(self):
        h = self.base_hover()
        h.move()
        self.expect_at(h, 0, 1, North)

    def test_turn_and_move(self):
        h = self.base_hover()
        h.turn_right()
        h.move()
        self.expect_at(h, 1, 0, East)

    def test_turn_twice(self):
        h = self.base_hover()
        h.turn_right()
        h.turn_right()
        self.expect_at(h, 0, 0, South)
        h = self.base_hover()
        h.turn_left()
        h.turn_left()
        self.expect_at(h, 0, 0, South)

    def test_turn_twice(self):
        h = self.base_hover()
        h.turn_right()
        h.turn_right()
        self.expect_at(h, 0, 0, South)

    def test_loop(self):
        h = self.base_hover()
        h.turn_right()
        h.turn_right()
        h.turn_right()
        h.turn_right()
        self.expect_at(h, 0, 0, North)

    def test_mixed_move(self):
        h = self.base_hover(1, 2, North)
        h.turn_left()
        h.move()
        self.expect_at(h, 0, 2, West)
        h.turn_left()
        h.move()
        self.expect_at(h, 0, 1, South)
        h.turn_left()
        self.expect_at(h, 0, 1, East)
        h.move()
        self.expect_at(h, 1, 1, East)
        h.turn_left()
        self.expect_at(h, 1, 1, North)
        h.move()
        self.expect_at(h, 1, 2, North)
        h.move()
        self.expect_at(h, 1, 3, North)

    def test_moxed_move_second_hover(self):
        p = Plateau(5, 5)
        h = Hover(3, 3, East)
        h.move()
        h.move()
        h.turn_right()
        h.move()
        h.move()
        h.turn_right()
        h.move()
        h.turn_right()
        h.turn_right()
        h.move()
        self.expect_at(h, 5, 1, East)

    def test_lower_bounds(self):
        h = self.base_hover()
        h.turn_left()
        self.assertRaises(BoundaryReached, h.move)
        h = self.base_hover()
        h.turn_left()
        h.turn_left()
        self.assertRaises(BoundaryReached, h.move)
        h = self.base_hover()
        h.turn_right()
        h.move()
        h.turn_right()
        self.assertRaises(BoundaryReached, h.move)

    def test_plateau_instance(self):
        plateau = Plateau(1, 1)
        hover = Hover(0, 0, North, plateau)

    def test_plateau_boundaries(self):
        plateau = Plateau(5, 5)
        h = Hover(0, 0, North, plateau)
        h.move()
        h.move()
        h.move()
        h.move()
        h.move()
        self.assertRaises(BoundaryReached, h.move)
        h2 = Hover(0, 0, North, plateau)
        h2.turn_right()
        h2.move()
        h2.move()
        h2.move()
        h2.move()
        h2.move()
        self.assertRaises(BoundaryReached, h.move)

    def test_collision(self):
        h1 = Hover(0, 0, North)
        h2 = Hover(0, 1, North)
        obstacles = [h1, h2]
        h1.set_obstacles(obstacles)
        h2.set_obstacles(obstacles)
        self.assertRaises(CollisionDetected, h1.move)
        h2.turn_left()
        h2.turn_left()
        self.assertRaises(CollisionDetected, h2.move)
