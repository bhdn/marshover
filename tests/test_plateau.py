import tests

from marsmission.plateau import Plateau

class TestPlateau(tests.Test):

    def test_instance(self):
        p = Plateau(1, 2)
        self.assertEquals(p.right_boundary, 1)
        self.assertEquals(p.top_boundary, 2)
