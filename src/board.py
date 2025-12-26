# 7 x 9 board
import dataclasses
from enum import Enum, StrEnum
from itertools import chain


class Colour(StrEnum):
    ORANGE = "O"
    GREEN = "G"
    BLUE = "B"
    RED = "R"


@dataclasses.dataclass(frozen=True, order=True)
class Point:
    row: int
    column: int
    colour: Colour


@dataclasses.dataclass(frozen=True, order=True)
class _Choice:
    points: set[Point]

    @property
    def colour(self) -> Colour:
        return next(iter(self.points)).colour

    def add_point(self, point: Point) -> None:
        self.points.add(point)

    def is_touching(self, point: Point) -> bool:
        colour = self.colour
        candidates = [
            Point(point.row, point.column + 1, colour), Point(point.row, point.column - 1, colour),
            Point(point.row + 1, point.column, colour), Point(point.row - 1, point.column, colour),
        ]
        return any(c in self.points for c in candidates)

    def get_point_repr(self) -> Point:
        return sorted(self.points)[0]

    def can_add(self, point: Point) -> bool:
        return self.colour == point.colour and self.is_touching(point)


WIDTH = 7
HEIGHT = 9


class Board:
    def __init__(self, initial_board: list[list[Colour]]):
        self._board = [Point(row_idx, col_idx, colour) for row_idx, row in enumerate(initial_board) for col_idx, colour in enumerate(row)]

    def get_choices(self) -> set[Point]:
        choices: list[_Choice] = []
        for point in self._board:
            choice_candidates = [choice for choice in choices if choice.can_add(point)]
            if len(choice_candidates) == 1:
                choice_candidates[0].add_point(point)
                continue
            elif len(choice_candidates) > 1:
                new_choice = _Choice(set(chain.from_iterable({frozenset(cc.points) for cc in choice_candidates})) | {point})
                for choice_candidate in choice_candidates:
                    choices.remove(choice_candidate)
                choices.append(new_choice)
                continue

            choice = _Choice({point})
            choices.append(choice)

        return {choice.get_point_repr() for choice in choices}

    def get_board_state(self) -> list[list[Colour | None]]:
        colour_lookup = {(p.row, p.column): p.colour for p in self._board}
        board = []
        for row_idx in range(HEIGHT):
            row = []
            for col_idx in range(WIDTH):
                row.append(colour_lookup.get((row_idx, col_idx), None))
            board.append(row)

        return board

    def select(self, point: Point) -> None:
        pass
