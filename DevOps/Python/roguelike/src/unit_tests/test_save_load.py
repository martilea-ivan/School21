from domain.logic.level_generator import LevelGenerator
from domain.objects.player import Player
from datalayer import save


class TestSaveLoad:
    def test_save_and_load(self, tmp_path, monkeypatch):
        monkeypatch.setattr(save, "SAVE_FILE", str(tmp_path / "test_save.json"))

        gen = LevelGenerator()
        level = gen.generate(1)
        cx, cy = level.start_room.get_center()
        player = Player("Тест", cx, cy)

        save.save_game(player, level)
        result = save.load_game()

        p2, l2 = result
        assert p2.name == "Тест"
        assert l2.number == 1
        assert len(l2.rooms) == 9
