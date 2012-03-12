from marsmission import Error
from marsmission.plateau import Plateau
from marsmission.hover import Hover

class TURN_LEFT: pass
class TURN_RIGHT: pass
class MOVE: pass

class InvalidInstruction(Error):
    pass

class Report:

    def __init__(self, hovers):
        self.hovers_location = []
        for hover in hovers:
            self.hovers_location.append(hover.location())

class Mission(object):

    def __init__(self):
        self.hovers = []
        self.obstacles = []
        self.plateau = None

    def set_plateau_dimensions(self, x, y):
        self.plateau = Plateau(x, y)

    def add_hover(self, initial_loc, instructions):
        hover = Hover(*initial_loc, plateau=self.plateau)
        self.hovers.append((hover, instructions))
        self.obstacles.append(hover)

    def execute(self):
        for hover, instructions in self.hovers:
            hover.set_obstacles(self.obstacles)
            for instr in instructions:
                if instr is TURN_LEFT:
                    hover.turn_left()
                elif instr is TURN_RIGHT:
                    hover.turn_right()
                elif instr is MOVE:
                    hover.move()
                else:
                    raise InvalidInstruction
        return Report(hover for hover, _ in self.hovers)
