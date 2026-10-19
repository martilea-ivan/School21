class GameSession:

    def __init__(self, session_id, name_player):
        self._id = session_id
        self._name_player = name_player
        self._current_level = 1
        self._score = 0
        self._is_active = True

    @property
    def id(self):
        return self._id

    @property
    def name_player(self):
        return self._name_player

    @property
    def current_level(self):
        return self._current_level

    @property
    def score(self):
        return self._score

    @property
    def is_active(self):
        return self._is_active

    @current_level.setter
    def current_level(self, value):
        self._current_level = value

    @score.setter
    def score(self, value):
        self._score = value

    @is_active.setter
    def is_active(self, value):
        self._is_active = value