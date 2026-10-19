from domain.objects.player import Player
from domain.objects.enum import KeyType


class TestPlayer:
    def test_heal_caps_at_max(self):
        p = Player("Тест", 0, 0)
        p.take_damage(30)
        p.heal(100)
        assert p.health == p.max_health

    def test_add_max_health(self):
        p = Player("Тест", 0, 0)
        old_max = p.max_health
        old_hp = p.health
        p.add_max_health(10)
        assert p.max_health == old_max + 10
        assert p.health == old_hp + 10

    def test_keys(self):
        p = Player("Тест", 0, 0)
        assert not p.has_key(KeyType.RED)
        p.add_key(KeyType.RED)
        assert p.has_key(KeyType.RED)
        p.clear_keys()
        assert not p.has_key(KeyType.RED)

    def test_temp_bonuses_tick(self):
        p = Player("Тест", 0, 0)
        p.add_temp_bonus('st', 5, turns=3)
        assert p.get_effective_strength() == p.strength + 5
        p.tick_temp_bonuses()
        p.tick_temp_bonuses()
        p.tick_temp_bonuses()
        assert p.get_effective_strength() == p.strength
