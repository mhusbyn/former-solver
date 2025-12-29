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


class _InternalBoard:
    def __init__(self, board_repr: list[list[Colour | None]]):
        self._point_board = [Point(row_idx, col_idx, colour) for row_idx, row in enumerate(board_repr) for col_idx, colour in enumerate(row)]
        self._point_lookup = {(p.row, p.column): p for p in self.point_board}

    @property
    def point_board(self) -> list[Point]:
        return self._point_board

    @property
    def point_lookup(self):
        return self._point_lookup

    def get_list_board(self) -> list[list[Colour | None]]:
        board = []
        for row_idx in range(HEIGHT):
            row = []
            for col_idx in range(WIDTH):
                row.append(self._point_lookup[(row_idx, col_idx)].colour)
            board.append(row)

        return board

    def is_solved(self) -> bool:
        return all(p.colour is None for p in self.point_board)


def _get_nones_pushed_left(column: list[Colour | None]) -> list[Colour | None]:
    new_col: list[Colour | None] = column.count(None) * [None]
    for val in column:
        if val is None:
            continue
        new_col.append(val)

    return new_col


class Board:
    def __init__(self, initial_board: list[list[Colour]]):
        self._board = _InternalBoard(initial_board)

    def get_choices(self) -> set[Point]:
        choices = self._get_internal_choices()

        return {choice.get_point_repr() for choice in choices}

    def _get_internal_choices(self):
        choices: list[_Choice] = []
        for point in self._board.point_board:
            choice_candidates = [choice for choice in choices if choice.can_add(point)]
            if len(choice_candidates) == 1:
                choice_candidates[0].add_point(point)
                continue
            elif len(choice_candidates) > 1:
                new_choice = _Choice(
                    set(chain.from_iterable({frozenset(cc.points) for cc in choice_candidates})) | {point}
                    )
                for choice_candidate in choice_candidates:
                    choices.remove(choice_candidate)
                choices.append(new_choice)
                continue

            choice = _Choice({point})
            choices.append(choice)
        return choices

    def get_board_state(self) -> list[list[Colour | None]]:
        colour_lookup = {(p.row, p.column): p.colour for p in self._board.point_board}
        board = []
        for row_idx in range(HEIGHT):
            row = []
            for col_idx in range(WIDTH):
                row.append(colour_lookup.get((row_idx, col_idx), None))
            board.append(row)

        return board

    def select(self, point: Point) -> None:
        choice_lookup = {p: c for c in self._get_internal_choices() for p in c.points}
        selected_choice = choice_lookup[point]

        list_board = self._board.get_list_board()
        for p in selected_choice.points:
            list_board[p.row][p.column] = None

        columns = list(map(list, zip(*list_board)))

        for col_idx, column in enumerate(columns):
            columns[col_idx] = _get_nones_pushed_left(column)

        self._board = _InternalBoard(list(map(list, zip(*columns))))

    def is_solved(self) -> bool:
        return self._board.is_solved()


