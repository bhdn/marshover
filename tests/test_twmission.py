import tests
from marsmission.twmission import TWMission

from cStringIO import StringIO

class TestTWMission(tests.Test):

    def test_instance(self):
        sio = StringIO()
        twmission = TWMission(sio)

    def test_loading_instructions(self):
        contents = """\
5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM
"""
        sio = StringIO(contents)
        twmission = TWMission(sio)
        twmission.execute()
        self.assertEquals(twmission.report(),
                "1 3 N\n5 1 E\n")
