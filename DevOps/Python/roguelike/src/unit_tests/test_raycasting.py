from presentation.raycasting import bresenham_line


class TestRaycasting:
    def test_bresenham_horizontal(self):
        line = bresenham_line(0, 0, 3, 0)
        assert (3, 0) in line
        assert (0, 0) not in line

    def test_bresenham_diagonal(self):
        line = bresenham_line(0, 0, 3, 3)
        assert (3, 3) in line
