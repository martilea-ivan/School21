from domain.objects.item import Item
from domain.objects.enum import ItemType , FoodType


class Food(Item):

    def __init__(self, food_type : FoodType):
        super().__init__(food_type.name, ItemType.FOOD)
        self._heal_amount = food_type.value
    @property
    def heal_amount(self):
        return self._heal_amount

    def use(self, target):
        target.heal(self._heal_amount)

    def to_dict(self):
        return {
            "kind": "food",
            "name": self.name,
            "x": self.x,
            "y": self.y,
        }