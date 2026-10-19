from domain.objects.essence import Essence
from domain.objects.backpack import Backpack
from domain.objects.enum import ItemType
from domain.objects.statistics import Statistics


class Player(Essence):

    def __init__(self, name, x, y):
        super().__init__(health=100, strength=100, dexterity=100, x=x, y=y)
        self._name = name
        self._max_health = 100
        self._weapon = None
        self._backpack = Backpack()
        self._temp_bonuses = {}
        self._is_sleeping = False
        self._statistics = Statistics()
        self._keys = set()
        self._angle = 0.0


    @property
    def name(self):
        return self._name

    @property
    def max_health(self):
        return self._max_health

    @property
    def gold(self):
        total = 0
        for item in self._backpack.items:
            if item.type == ItemType.TREASURE:
                total += item.gold
        return total

    @property
    def weapon(self):
        return self._weapon

    @property
    def backpack(self):
        return self._backpack

    @property
    def temp_bonuses(self):
        return self._temp_bonuses

    @property
    def is_sleeping(self):
        return self._is_sleeping

    @property
    def statistics(self):
        return self._statistics

    @property
    def keys(self):
        return self._keys

    def add_key(self, key_type):
        self._keys.add(key_type)

    def has_key(self, key_type):
        return key_type in self._keys

    def clear_keys(self):
        self._keys = set()

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value

    @is_sleeping.setter
    def is_sleeping(self, value):
        self._is_sleeping = value

    def heal(self, amount):
        self._health = min(self._max_health, self._health + amount)

    def add_temp_hp(self, amount):
        self._health += amount

    def add_max_health(self, value):
        self._max_health += value
        self._health += value

    def add_temp_bonus(self, key, value, turns=20):
        self._temp_bonuses[key] = (value, turns)

    def equip_weapon(self, weapon):
        self._weapon = weapon

    def add_strength(self, value):
        self._strength += value

    def add_dexterity(self, value):
        self._dexterity += value

    def tick_temp_bonuses(self):
        for key in list(self._temp_bonuses.keys()):
            val, turns = self._temp_bonuses[key]
            if turns <= 1:
                del self._temp_bonuses[key]
            else:
                self._temp_bonuses[key] = (val, turns - 1)

    def get_effective_strength(self):
        bonus = self._temp_bonuses.get('st', (0, 0))[0]
        return self._strength + bonus

    def get_effective_dexterity(self):
        bonus = self._temp_bonuses.get('dex', (0, 0))[0]
        return self._dexterity + bonus

    def reduce_max_health(self, amount):
        self._max_health = max(1, self._max_health - amount)
        self._health = min(self._health, self._max_health)

    def to_dict(self):
        return {
            "name": self._name,
            "x": self._x,
            "y": self._y,
            "health": self._health,
            "max_health": self._max_health,
            "strength": self._strength,
            "dexterity": self._dexterity,
            "is_alive": self._is_alive,
            "is_sleeping": self._is_sleeping,
            "weapon": self._weapon.to_dict() if self._weapon else None,
            "backpack": self._backpack.to_dict(),
            "temp_bonuses": {k: list(v) for k, v in self._temp_bonuses.items()},
            "statistics": self._statistics.to_dict(),
            "keys": [k.name for k in self._keys],
            "angle": self._angle,
        }