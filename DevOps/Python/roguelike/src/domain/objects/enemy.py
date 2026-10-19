from domain.objects.enum import EnemyType
from domain.objects.essence import Essence
import random

SYMBOLS = {
    EnemyType.ZOMBI: "z",
    EnemyType.VAMPIRE: "v",
    EnemyType.PHANTOM: "g",
    EnemyType.ORGE: "O",
    EnemyType.SNACE_MAGE: "s",
    EnemyType.MIMIC: "m",
}


class Enemy(Essence):

    def __init__(self, enemy_type: EnemyType, x, y, dungeon_level=1):
        super().__init__(
            health=enemy_type.hp,
            strength=enemy_type.st,
            dexterity=enemy_type.dex,
            x=x,
            y=y
        )
        self._enemy_type = enemy_type
        self._symbol = SYMBOLS[enemy_type]
        self._vrability = min(enemy_type.vrability + dungeon_level, 10)
        self._status_chase = False
        self._has_attacked = False
        self._is_resting = False
        self._disguise_symbol = None
        if enemy_type == EnemyType.MIMIC:
            self._disguise_symbol = random.choice(['$', '!', '/', '?', '%', 'b', 'a', 'm', 'f', 'e'])

    @property
    def enemy_type(self):
        return self._enemy_type

    @property
    def symbol(self):
        return self._symbol

    @property
    def vrability(self):
        return self._vrability

    @property
    def status_chase(self):
        return self._status_chase

    @status_chase.setter
    def status_chase(self, value):
        self._status_chase = value

    @property
    def has_attacked(self):
        return self._has_attacked

    @has_attacked.setter
    def has_attacked(self, value):
        self._has_attacked = value

    @property
    def is_resting(self):
        return self._is_resting

    @is_resting.setter
    def is_resting(self, value):
        self._is_resting = value

    @property
    def disguise_symbol(self):
        return self._disguise_symbol

    def to_dict(self):
        return {
            "type": self._enemy_type.name,
            "x": self._x,
            "y": self._y,
            "health": self._health,
            "is_alive": self._is_alive,
            "vrability": self._vrability,
            "status_chase": self._status_chase,
            "has_attacked": self._has_attacked,
            "is_resting": self._is_resting,
            "disguise_symbol": self._disguise_symbol,
        }