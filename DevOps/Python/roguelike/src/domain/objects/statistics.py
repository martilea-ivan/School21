class Statistics:
    def __init__(self):
        self._enemies_killed = 0
        self._food_eaten = 0
        self._elixirs_drunk = 0
        self._scrolls_read = 0
        self._hits_dealt = 0
        self._hits_missed = 0
        self._cells_moved = 0
        self._treasures_collected = 0
        self._hp_lost = 0
        self._levels_passed = 0
        self._deaths = 0

    @property
    def enemies_killed(self): return self._enemies_killed
    @property
    def food_eaten(self): return self._food_eaten
    @property
    def elixirs_drunk(self): return self._elixirs_drunk
    @property
    def scrolls_read(self): return self._scrolls_read
    @property
    def hits_dealt(self): return self._hits_dealt
    @property
    def hits_missed(self): return self._hits_missed
    @property
    def cells_moved(self): return self._cells_moved
    @property
    def treasures_collected(self): return self._treasures_collected
    @property
    def hp_lost(self): return self._hp_lost
    @property
    def levels_passed(self): return self._levels_passed
    @property
    def deaths(self): return self._deaths

    def add_enemy_killed(self): self._enemies_killed += 1
    def add_food_eaten(self): self._food_eaten += 1
    def add_elixir_drunk(self): self._elixirs_drunk += 1
    def add_scroll_read(self): self._scrolls_read += 1
    def add_hit_dealt(self): self._hits_dealt += 1
    def add_hit_missed(self): self._hits_missed += 1
    def add_cell_moved(self): self._cells_moved += 1
    def add_treasure_collected(self, amount): self._treasures_collected += amount
    def add_hp_lost(self, amount): self._hp_lost += amount
    def add_level_passed(self): self._levels_passed += 1
    def add_death(self): self._deaths += 1

    def to_dict(self):
        return {
            "enemies_killed": self._enemies_killed,
            "food_eaten": self._food_eaten,
            "elixirs_drunk": self._elixirs_drunk,
            "scrolls_read": self._scrolls_read,
            "hits_dealt": self._hits_dealt,
            "hits_missed": self._hits_missed,
            "cells_moved": self._cells_moved,
            "treasures_collected": self._treasures_collected,
            "hp_lost": self._hp_lost,
            "levels_passed": self._levels_passed,
            "deaths": self._deaths,
        }

    @classmethod
    def from_dict(cls, data):
        s = cls()
        s._enemies_killed = data["enemies_killed"]
        s._food_eaten = data["food_eaten"]
        s._elixirs_drunk = data["elixirs_drunk"]
        s._scrolls_read = data["scrolls_read"]
        s._hits_dealt = data["hits_dealt"]
        s._hits_missed = data["hits_missed"]
        s._cells_moved = data["cells_moved"]
        s._treasures_collected = data["treasures_collected"]
        s._hp_lost = data.get("hp_lost", 0)
        s._levels_passed = data.get("levels_passed", 0)
        s._deaths = data.get("deaths", 0)
        return s
