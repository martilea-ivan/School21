from domain.objects.room import Room


class TestRoom:
    def test_get_center(self):
        r = Room(0, 10, 5, 6, 4)
        cx, cy = r.get_center()
        assert cx == 13
        assert cy == 7

    def test_mark_visited(self):
        r = Room(0, 10, 5, 6, 4)
        assert r.is_visit is False
        r.mark_visited()
        assert r.is_visit is True

    def test_random_free_cell(self):
        r = Room(0, 10, 5, 6, 4)
        cell = r.get_random_free_cell()
        assert cell is not None
        x, y = cell
        assert 11 <= x <= 14
        assert 6 <= y <= 7
