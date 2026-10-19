from domain.objects.item import Item
from domain.objects.enum import ItemType, TreasureType


class Treasure(Item):

    def __init__(self, treasure_type: TreasureType):
        super().__init__(treasure_type.name, ItemType.TREASURE)
        self._gold = treasure_type.value

    @property
    def gold(self):
        return self._gold

    @gold.setter
    def gold(self, value):
        self._gold = value

    def use(self, target):
        target.backpack.add_item(self)

    def to_dict(self):
        return {
            "kind": "treasure",
            "name": self.name,
            "gold": self._gold,
            "x": self.x,
            "y": self.y,
        }