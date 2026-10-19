from domain.objects.item import Item
from domain.objects.enum import ItemType, ElixirType


class Elixir(Item):

    def __init__(self, elixir_type : ElixirType):
        super().__init__(elixir_type.name, ItemType.ELIXIR)
        self._effect = elixir_type.effect
        self._value = elixir_type.value

    @property
    def effect(self):
        return self._effect

    @property
    def value(self):
        return self._value

    def use(self, target):
        if self._effect == 'hp':
            target.add_temp_hp(self._value)
        elif self._effect == 'st':
            target.add_temp_bonus('st', self._value, turns=20)
        elif self._effect == 'dex':
            target.add_temp_bonus('dex', self._value, turns=20)

    def to_dict(self):
        return {
            "kind": "elixir",
            "name": self.name,
            "x": self.x,
            "y": self.y,
        }