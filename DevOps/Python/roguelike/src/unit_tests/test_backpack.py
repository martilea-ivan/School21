from domain.objects.backpack import Backpack
from domain.objects.items.food import Food
from domain.objects.items.treasure import Treasure
from domain.objects.enum import FoodType, TreasureType


class TestBackpack:
    def test_add_item(self):
        b = Backpack()
        food = Food(FoodType.MEAT)
        assert b.add_item(food) is True
        assert len(b.items) == 1

    def test_max_items_per_type(self):
        b = Backpack()
        for _ in range(9):
            b.add_item(Food(FoodType.MEAT))
        assert b.add_item(Food(FoodType.MEAT)) is False

    def test_treasure_stack(self):
        b = Backpack()
        b.add_item(Treasure(TreasureType.GOLD_COIN))
        b.add_item(Treasure(TreasureType.RUBY))
        assert len(b.items) == 1
        assert b.items[0].gold == 60
