from domain.objects.item import Item
from domain.objects.enum import ItemType, WeaponType


class Weapon(Item):
    def __init__(self, weapon_type : WeaponType):
        super().__init__(weapon_type.name, ItemType.WEAPON)
        self._damage = weapon_type.damage

    @property
    def damage(self): return self._damage

    def use(self, target):
        target.equip_weapon(self)

    def to_dict(self):
        return {
            "kind": "weapon",
            "name": self.name,
            "x": self.x,
            "y": self.y,
        }