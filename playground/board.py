from dataclasses import dataclass
from typing import List

import numpy as np
from bokeh.plotting import figure, output_file, save, show


@dataclass
class Stone:
    x: str
    y: str
    color: str


@dataclass
class BoardConfig:
    row: int
    column: int
    connect: int
    each_move: int
    first_move: int


class Board:

    def __init__(self,
                 m: int = 19,  # number of row on board
                 n: int = 19,  # number of column on board
                 k: int = 6,  # number of stones in a row for winning
                 p: int = 2,  # number of stones for each move
                 q: int = 1,  # number of stones for first move
                 ):
        self.config = BoardConfig(m, n, k, p, q)
        self.output_path = "templates/board.html"
        output_file(self.output_path)
        self.figure = figure()
        self.log = []
        self.setup()
        self.boardInterpreter = BoardInterpreter(self.config)

    def setup(self):
        x_tick = [str(x) for x in range(1, self.config.row + 1)]
        y_tick = [str(x) for x in range(self.config.column, 0, -1)]
        p = figure(x_range=x_tick,
                   y_range=y_tick,
                   x_axis_location="above",
                   tools="save")
        p.title.text = "on playing"
        p.plot_width = 800
        p.plot_height = 800
        p.outline_line_color = None
        p.grid.grid_line_color = None
        p.axis.axis_line_color = None
        p.axis.major_tick_line_color = None
        p.axis.major_label_text_font_size = "8pt"
        p.axis.major_label_standoff = 0

        for x in x_tick:
            p.line(["1", str(self.config.row)], [x, x], line_width=1, color="gray")
        for y in y_tick:
            p.line([y, y], ["1", str(self.config.column)], line_width=1, color="gray")

        if self.config.row == 19 & self.config.column == 19:
            for x in ["4", "10", "16"]:
                for y in ["4", "10", "16"]:
                    p.circle([x], [y], color="gray", size=10)

        self.figure = p
        self.log = []

    def save_figure(self):
        save(self.figure)

    def render_figure(self):
        show(self.figure, browser="safari")

    def put_stone(self, stone: Stone):
        if stone.color == "b":
            fill_color = "black"
        elif stone.color == "w":
            fill_color = "white"
        else:
            raise TypeError("stone color string should be [b] or [w]")

        self.log.append(stone)
        self.figure.circle([stone.x],
                           [stone.y],
                           fill_color=fill_color,
                           line_color="black",
                           line_width=1,
                           size=24)

    def print_winner(self, color: str):
        self.figure.title.text = f"winner: {color}"

    def print_illegal_turn(self):
        self.figure.title.text = "illegal turn"

    def print_illegal_stone(self):
        self.figure.title.text = "illegal stone"

    def print_on_playing(self):
        self.figure.title.text = "on playing"

    def draw_board(self, log: List[Stone]):
        self.boardInterpreter.draw_board(log)


class BoardInterpreter:

    def __init__(self, board_config: BoardConfig):
        self.k = board_config.connect
        self.m = board_config.row
        self.n = board_config.column
        self.p = board_config.each_move
        self.q = board_config.first_move

    @staticmethod
    def array_to_board(x: int) -> str:
        if x == 0:
            points = "+"
        elif x == 1:
            points = "B"
        elif x == 2:
            points = "W"
        else:  # x == -1:
            points = "S"
        return points

    def stone_to_array(self, log: List[Stone]) -> np.array:
        stone_array = np.zeros((self.m, self.n))
        for pos in log:
            x = int(pos.x) - 1
            y = int(pos.y) - 1
            if pos.color == "b":
                stone_array[y, x] = 1
            elif pos.color == "w":
                stone_array[y, x] = 2
            elif pos.color == "s":
                stone_array[y, x] = -1
        return stone_array

    @staticmethod
    def array_to_stone(stone_array: np.array, color: str) -> List[Stone]:
        if color == "b":
            out = 1
        elif color == "w":
            out = 2
        else:
            out = -1
        y, x = np.where(stone_array == out)
        positions = list(zip(list(x), list(y)))
        stones = [Stone(str(x + 1), str(y + 1), color) for x, y in positions]
        return stones

    def draw_board(self, log: List[Stone]):
        stone_array = self.stone_to_array(log)
        join_column = list(map(lambda y: " ".join([self.array_to_board(x) for i, x in enumerate(y)]), stone_array))
        join_row = "\n" + "\n".join(join_column)
        print(join_row)


if __name__ == "__main__":
    test_log = [
        Stone("3", "2", "b"),
        Stone("2", "1", "w"),
        Stone("2", "2", "w"),
        Stone("1", "2", "b"),
        Stone("1", "3", "b"),
        Stone("2", "3", "w"),
        Stone("2", "4", "w"),
        Stone("1", "4", "b"),
        Stone("1", "5", "b"),
        Stone("2", "5", "w"),
        Stone("2", "8", "w"),
        Stone("1", "10", "b"),
        Stone("1", "11", "b"),
        Stone("2", "9", "w"),
        Stone("2", "6", "w"),
    ]

    board = Board()
    print("--render board")
    board.render_figure()

    print("--put stones")
    for item in test_log:
        board.put_stone(item)
    board.render_figure()
    board.draw_board(board.log)
    print("--log ")
    for item in board.log:
        print("\t", item)
