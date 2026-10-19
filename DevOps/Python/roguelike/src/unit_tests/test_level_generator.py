from domain.logic.level_generator import LevelGenerator


class TestLevelGenerator:
    def test_generates_9_rooms(self):
        gen = LevelGenerator()
        level = gen.generate(1)
        assert len(level.rooms) == 9

    def test_hallways_connect(self):
        gen = LevelGenerator()
        level = gen.generate(1)
        assert len(level.hallways) >= 8

    def test_start_and_exit(self):
        gen = LevelGenerator()
        level = gen.generate(1)
        assert level.start_room.id == 0
        assert level.exit_room.id == 8

    def test_bfs_all_reachable(self):
        gen = LevelGenerator()
        level = gen.generate(1)
        reachable = LevelGenerator._bfs_reachable(
            level.rooms, level.hallways, level.start_room
        )
        assert len(reachable) == 9

    def test_level_2_has_doors(self):
        gen = LevelGenerator()
        level = gen.generate(2)
        doors = [h for h in level.hallways if h.door_color is not None]
        assert len(doors) == 2
