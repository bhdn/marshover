from marsmission.mission import TURN_LEFT, TURN_RIGHT, MOVE, Mission
from marsmission import Error, North, South, East, West

class InvalidInputFormat(Error):
    pass

orient_map = {"N": North, "S": South, "E": East, "W": West}
orient_names = dict((value, key) for key, value in orient_map.iteritems())

class TWMission(Mission):
    """The Thoughtworks saturday mission"""

    def __init__(self, fileobj):
        """
        @fileobj: a readable file with the text-format instructions
        """
        super(TWMission, self).__init__()
        self.fileobj = fileobj
        self._report = None

    def execute(self):
        state = 0
        for line in self.fileobj:
            if not line.strip():
                continue
            if state == 0:
                raw_mapspec = line.strip()
                try:
                    raw_x, raw_y = raw_mapspec.split(None, 2)
                    x = int(raw_x)
                    y = int(raw_y)
                except ValueError:
                    raise InvalidInputFormat
                self.set_plateau_dimensions(x, y)
                state = 1
            elif state == 1:
                raw_posspec = line.strip()
                try:
                    raw_h_x, raw_h_y, raw_orient = raw_posspec.split()
                    h_x = int(raw_h_x)
                    h_y = int(raw_h_y)
                    h_orient = orient_map[raw_orient]
                except (ValueError, KeyError):
                    raise InvalidInputFormat
                state = 2
            elif state == 2:
                raw_instrs = line.strip()
                instructions = []
                for ch in raw_instrs:
                    if ch == "L":
                        ins = TURN_LEFT
                    elif ch == "R":
                        ins = TURN_RIGHT
                    elif ch == "M":
                        ins = MOVE
                    else:
                        raise InvalidInputFormat
                    instructions.append(ins)
                self.add_hover(initial_loc=(h_x, h_y, h_orient),
                        instructions=instructions)
                state = 1
        if state != 1:
            raise InvalidInputFormat
        self._report = super(TWMission, self).execute()

    def report(self):
        entries = []
        for loc in self._report.hovers_location:
            entries.append("%s %s %s\n" % (loc.x, loc.y,
                orient_names[loc.orient]))
        line = "".join(entries)
        return line

