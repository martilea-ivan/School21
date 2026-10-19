from enum import Enum


class EnemyType(Enum):
    #        st  dex hp  vr lvl
    ZOMBI = (14, 6, 30, 4, 2)
    VAMPIRE = (12, 18, 25, 6, 4)
    PHANTOM = (6, 17, 10, 2, 1)
    ORGE = (20, 5, 40, 5, 5)
    SNACE_MAGE = (10, 19, 18, 7, 4)
    MIMIC = (10, 20, 50, 3, 2)

    def __init__(self, st, dex, hp, vr, level):
        self._st = st
        self._dex = dex
        self._hp = hp
        self._vr = vr
        self._level = level

    @property
    def st(self): return self._st

    @property
    def dex(self): return self._dex

    @property
    def hp(self): return self._hp

    @property
    def vrability(self): return self._vr

    @property
    def level(self): return self._level

class ItemType(Enum):
    FOOD = 'food'
    WEAPON = 'weapon'
    SCROLL = 'scroll'
    ELIXIR = 'elixir'
    TREASURE = 'treasure'
    KEY = 'key'

class FoodType(Enum):
    BANANA = 10
    APPLE = 5
    MEAT = 20
    FISH = 15
    EGG = 12

class ElixirType(Enum):
    ELIXIR_HP  = ('hp', 10)
    ELIXIR_ST  = ('st', 1)
    ELIXIR_DEX = ('dex', 1)

    def __init__(self, effect, value):
        self._effect = effect
        self._value = value

    @property
    def effect(self): return self._effect

    @property
    def value(self): return self._value

class WeaponType(Enum):
        DAGGER = 5  # кинжал
        SPEAR = 10 # копьё
        MACE = 15  # булава

        def __init__(self, damage):
            self._damage = damage

        @property
        def damage(self):
            return self._damage

class TreasureType(Enum):
    SILVER_COIN = 5
    GOLD_COIN   = 10
    RUBY        = 50
    DRAGON_GEM  = 100

class ScrollType(Enum):
    SCROLL_MAX_HP = ('max_hp', 5)
    SCROLL_ST     = ('st', 1)
    SCROLL_DEX    = ('dex', 1)

    def __init__(self, effect, value):
        self._effect = effect
        self._value = value

    @property
    def effect(self):
        return self._effect

    @property
    def value(self):
        return self._value


class GenerationConfig(Enum):
    MAX_ITEMS_PER_TYPE = 9
    MAP_WIDTH = 60
    MAP_HEIGHT = 30
    ROOM_COUNT = 9
    MIN_ROOM_SIZE = 4
    MAX_ROOM_SIZE = 8
    PADDING = 2
    BASE_ENEMY_CHANCE = 0.5
    ENEMY_CHANCE_INCREMENT = 0.04
    MAX_ENEMY_CHANCE = 0.85
    BASE_ITEM_CHANCE = 0.3
    ITEM_CHANCE_DECREMENT = 0.02
    MAX_ITEM_CHANCE = 0.85
    MIN_ITEM_CHANCE = 0.8
    MIN_ENEMIES_PER_ROOM = 1
    MAX_ENEMIES_PER_ROOM_BASE = 1
    MAX_ENEMIES_PER_ROOM_INCREMENT = 0.2
    MAX_ENEMIES_PER_ROOM_ABSOLUTE = 4
    MIN_ITEMS_PER_ROOM = 0
    MAX_ITEMS_PER_ROOM_BASE = 1
    MAX_ITEMS_PER_ROOM_INCREMENT = 0.2
    MAX_ITEMS_PER_ROOM_ABSOLUTE = 3


class KeyType(Enum):
    RED = 'red'
    BLUE = 'blue'
    GREEN = 'green'
