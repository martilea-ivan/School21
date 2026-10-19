from domain.objects.item import Item
from domain.objects.enum import ItemType, KeyType


class Key(Item):

    def __init__(self, key_type: KeyType):
        super().__init__(key_type.name, ItemType.KEY)
        self._key_type = key_type

    @property
    def key_type(self):
        return self._key_type

    def use(self, target):
        target.add_key(self._key_type)

    def to_dict(self):
        return {
            "kind": "key",
            "name": self.name,
            "x": self.x,
            "y": self.y,
        }
