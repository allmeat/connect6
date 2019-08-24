from dataclasses import dataclass
from bokeh.plotting import figure, output_file, save


@dataclass
class Stone:
    x: str
    y: str
    color: str


class Board:

    def __init__(self):
        output_file("templates/board.html")
        self.figure = figure()
        self.log = []
        self.setup()

    def setup(self):
        x_tick = [str(x) for x in range(1, 20)]
        y_tick = [str(x) for x in range(19, 0, -1)]
        p = figure(x_range=x_tick,
                   y_range=y_tick,
                   x_axis_location="above",
                   tools="save")
        p.plot_width = 800
        p.plot_height = 800
        p.outline_line_color = None
        p.grid.grid_line_color = None
        p.axis.axis_line_color = None
        p.axis.major_tick_line_color = None
        p.axis.major_label_text_font_size = "8pt"
        p.axis.major_label_standoff = 0

        for x in x_tick:
            p.line(["1", "19"], [x, x], line_width=1, color="gray")
            p.line([x, x], ["1", "19"], line_width=1, color="gray")

        for x in ["4", "10", "16"]:
            for y in ["4", "10", "16"]:
                p.circle([x], [y], color="gray", size=10)

        self.figure = p
        self.log = []

    def save_figure(self):
        save(self.figure)

    def put_stone(self, stone: Stone):
        if stone.color == "b":
            fill_color = "black"
        elif stone.color == "w":
            fill_color = "white"
        else:
            raise TypeError("stone color string should be [b] or [w]")

        self.figure.circle([stone.x],
                           [stone.y],
                           fill_color=fill_color,
                           line_color="black",
                           line_width=1,
                           size=24)
