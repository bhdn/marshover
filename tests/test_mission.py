import tests

from marsmission import North, South, East, West
from marsmission.mission import (Mission, TURN_LEFT, TURN_RIGHT, MOVE,
        InvalidInstruction)

class TestMission(tests.Test):

    def base_mission(self):
        mission = Mission()
        return mission

    def test_instance(self):
        m = self.base_mission()

    def test_add_hover(self):
        m = self.base_mission()
        m.add_hover(initial_loc=(0, 0, North),
                instructions=(TURN_LEFT, MOVE))

    def test_execute(self):
        m = self.base_mission()
        m.set_plateau_dimensions(5, 5)
        m.add_hover(initial_loc=(1, 2, North),
                instructions=(TURN_LEFT, MOVE, TURN_LEFT, MOVE,
                    TURN_LEFT, MOVE, TURN_LEFT, MOVE, MOVE))
        report = m.execute()
        loc0 = report.hovers_location[0]
        self.assertEquals((loc0.x, loc0.y, loc0.orient), (1, 3, North))

    def test_multiple_hovers(self):
        m = self.base_mission()
        m.add_hover(initial_loc=(1, 2, North),
                instructions=(TURN_LEFT, MOVE, TURN_LEFT, MOVE,
                    TURN_LEFT, MOVE, TURN_LEFT, MOVE, MOVE))
        m.set_plateau_dimensions(5, 5)
        m.add_hover(initial_loc=(3, 3, East),
                instructions=(MOVE, MOVE, TURN_RIGHT, MOVE, MOVE,
                    TURN_RIGHT, MOVE, TURN_RIGHT, TURN_RIGHT, MOVE))
        report = m.execute()
        loc0 = report.hovers_location[0]
        self.assertEquals((loc0.x, loc0.y, loc0.orient), (1, 3, North))
        loc0 = report.hovers_location[1]
        self.assertEquals((loc0.x, loc0.y, loc0.orient), (5, 1, East))

    def test_invalid_instruction(self):
        m = self.base_mission()
        m.add_hover(initial_loc=(1, 2, North),
                instructions=(TURN_LEFT, MOVE, TURN_LEFT, MOVE,
                    TURN_LEFT, MOVE, TURN_LEFT, MOVE, MOVE))
        m.set_plateau_dimensions(5, 5)
        m.add_hover(initial_loc=(3, 3, East),
                instructions=(MOVE, MOVE, TURN_RIGHT, MOVE, MOVE,
                    TURN_RIGHT, MOVE, TURN_RIGHT, 666.0, MOVE))
        self.assertRaises(InvalidInstruction, m.execute)
