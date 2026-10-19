class DomainError(Exception):
    pass


class InvalidBoardError(DomainError):
    pass


class InvalidMoveError(DomainError):
    pass


class GameNotFoundError(DomainError):
    pass


class GameAlreadyOverError(DomainError):
    pass
