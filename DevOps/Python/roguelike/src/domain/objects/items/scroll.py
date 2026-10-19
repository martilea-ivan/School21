from domain.objects.item import Item
from domain.objects.enum import ItemType,ScrollType


class Scroll(Item):

    def __init__(self, scroll_type: ScrollType):
        super().__init__(scroll_type.name, ItemType.SCROLL)
        self._effect = scroll_type.effect
        self._value = scroll_type.value

    @property
    def effect(self):
        return self._effect

    @property
    def value(self):
        return self._value

    def use(self, target):
        if self._effect == 'max_hp':
            target.add_max_health(self._value)
        elif self._effect == 'st':
            target.add_strength(self._value)
        elif self._effect == 'dex':
            target.add_dexterity(self._value)

    def to_dict(self):
        return {
            "kind": "scroll",
            "name": self.name,
            "x": self.x,
            "y": self.y,
        }