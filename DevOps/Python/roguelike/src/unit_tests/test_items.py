from domain.objects.items.food import Food
from domain.objects.items.weapon import Weapon
from domain.objects.items.treasure import Treasure
from domain.objects.player import Player
from domain.objects.enum import FoodType, WeaponType, TreasureType


class TestItems:
    def test_food_heal(self):
        p = Player("Тест", 0, 0)
        p.take_damage(50)
        Food(FoodType.MEAT).use(p)
        assert p.health == 70

    def test_weapon_equip(self):
        p = Player("Тест", 0, 0)
        w = Weapon(WeaponType.SPEAR)
        w.use(p)
        assert p.weapon == w
        assert p.weapon.damage == 10

    def test_treasure_to_backpack(self):
        p = Player("Тест", 0, 0)
        Treasure(TreasureType.RUBY).use(p)
        assert p.gold == 50
