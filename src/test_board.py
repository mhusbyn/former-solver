from itertools import cycle

import pytest

from board import Colour, WIDTH, HEIGHT, Board, Point


class TestGetChoices:
    @pytest.mark.parametrize("odd_row_out_index", range(1, 8))
    def test_simple_row_choice(self, odd_row_out_index: int):
        common_row = [Colour.RED] * WIDTH
        odd_row = [Colour.BLUE] * WIDTH

        initial_board = [odd_row if i == odd_row_out_index else common_row for i in range(HEIGHT)]
        board = Board(initial_board)

        [first_row_choice, second_row_choice, third_row_choice] = sorted(board.get_choices(), key=lambda p: p.row)
        assert first_row_choice.row == 0
        assert second_row_choice.row == odd_row_out_index
        assert third_row_choice.row == odd_row_out_index + 1

    def test_alternating_rows(self):
        orange_row = [Colour.ORANGE] * WIDTH
        green_row = [Colour.GREEN] * WIDTH
        blue_row = [Colour.BLUE] * WIDTH
        red_row = [Colour.RED] * WIDTH

        initial_board = [
            orange_row,
            green_row,
            blue_row,
            red_row,
            orange_row,
            green_row,
            blue_row,
            red_row,
            orange_row,
        ]

        choices = sorted(Board(initial_board).get_choices())
        assert [p.row for p in choices] == list(range(HEIGHT))

    @pytest.mark.parametrize("odd_col_out_index", range(1, 6))
    def test_simple_col_choice(self, odd_col_out_index: int):
        initial_board = []
        for row_idx in range(HEIGHT):
            row = []
            for col_idx in range(WIDTH):
                row.append(Colour.RED if col_idx != odd_col_out_index else Colour.BLUE)
            initial_board.append(row)

        board = Board(initial_board)

        [first_choice, second_choice, third_choice] = sorted(board.get_choices())
        assert first_choice.column == 0
        assert second_choice.column == odd_col_out_index
        assert third_choice.column == odd_col_out_index + 1

    def test_alternating_cols(self):
        initial_board = []
        for row_idx in range(HEIGHT):
            row = []
            colour_iterable = cycle(Colour)
            for col_idx in range(WIDTH):
                row.append(next(colour_iterable))

            initial_board.append(row)

        choices = sorted(Board(initial_board).get_choices())
        assert [p.column for p in choices] == list(range(WIDTH))

    def test_complicated_board(self):
        initial_board = [
            [Colour.BLUE, Colour.RED, Colour.BLUE, Colour.BLUE, Colour.BLUE, Colour.GREEN, Colour.BLUE],
            [Colour.RED, Colour.RED, Colour.RED, Colour.BLUE, Colour.BLUE, Colour.GREEN, Colour.GREEN],
            [Colour.BLUE, Colour.RED, Colour.BLUE, Colour.BLUE, Colour.BLUE, Colour.BLUE, Colour.BLUE],
            [Colour.BLUE, Colour.BLUE, Colour.BLUE, Colour.ORANGE, Colour.BLUE, Colour.BLUE, Colour.BLUE],
            [Colour.BLUE, Colour.BLUE, Colour.ORANGE, Colour.ORANGE, Colour.ORANGE, Colour.BLUE, Colour.BLUE],
            [Colour.BLUE, Colour.BLUE, Colour.BLUE, Colour.ORANGE, Colour.BLUE, Colour.BLUE, Colour.BLUE],
            [Colour.BLUE, Colour.BLUE, Colour.BLUE, Colour.BLUE, Colour.BLUE, Colour.ORANGE, Colour.BLUE],
            [Colour.BLUE, Colour.BLUE, Colour.BLUE, Colour.BLUE, Colour.ORANGE, Colour.BLUE, Colour.ORANGE],
            [Colour.BLUE, Colour.BLUE, Colour.BLUE, Colour.BLUE, Colour.BLUE, Colour.ORANGE, Colour.BLUE],
        ]

        choices = sorted(Board(initial_board).get_choices())
        expected_choices = [
            Point(0, 0, Colour.BLUE),
            Point(0, 1, Colour.RED),
            Point(0, 2, Colour.BLUE),
            Point(0, 5, Colour.GREEN),
            Point(0, 6, Colour.BLUE),
            Point(3, 3, Colour.ORANGE),
            Point(6, 5, Colour.ORANGE),
            Point(7, 4, Colour.ORANGE),
            Point(7, 5, Colour.BLUE),
            Point(7, 6, Colour.ORANGE),
            Point(8, 5, Colour.ORANGE),
            Point(8, 6, Colour.BLUE),
        ]
        assert choices == expected_choices


class TestGetBoardState:
    def test_initial_board(self):
        row = [Colour.BLUE] * WIDTH
        initial_board = [row] * HEIGHT

        assert Board(initial_board).get_board_state() == initial_board


