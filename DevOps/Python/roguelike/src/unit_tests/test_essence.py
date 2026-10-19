from domain.objects.player import Player


class TestEssence:
    def test_take_damage(self):
        p = Player("Тест", 0, 0)
        p.take_damage(30)
        assert p.health == 70
        assert p.is_alive is True

    def test_death_at_zero(self):
        p = Player("Тест", 0, 0)
        p.take_damage(150)
        assert p.health == 0
        assert p.is_alive is False
