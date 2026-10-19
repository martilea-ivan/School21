from abc import ABC


class Essence(ABC):

    def __init__(self, health, strength, dexterity, x, y):
        self._health = health
        self._strength = strength
        self._dexterity = dexterity
        self.x = x
        self.y = y
        self._is_alive = True

    @property
    def health(self):
        return self._health

    @property
    def strength(self):
        return self._strength

    @property
    def dexterity(self):
        return self._dexterity

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def is_alive(self):
        return self._is_alive

    def take_damage(self, amount):
        self._health -= amount
        if self._health <= 0:
            self._health = 0
            self._is_alive = False

    def get_effective_dexterity(self):
        return self._dexterity

    def get_effective_strength(self):
        return self._strength