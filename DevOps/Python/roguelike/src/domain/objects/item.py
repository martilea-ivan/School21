from abc import ABC, abstractmethod


class Item(ABC):

    def __init__(self, name, item_type, x=0, y=0):
        self._name = name
        self._type = item_type
        self._x = x
        self._y = y

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def set_position(self, x, y):
        self._x = x
        self._y = y

    @abstractmethod
    def use(self, target):
        pass