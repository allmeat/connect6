from bokeh.plotting import figure, show


class Board:

    def __init__(self):
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

        self.board = p

    def render(self):
        show(self.board)

    def put_stone(self, x, y, stone):
        if (stone == "black") | (stone == "b"):
            color = "black"
        elif (stone == "white") | (stone == "w"):
            color = "white"
        else:
            raise TypeError("stone color should be [black] or [white]")

        self.board.circle([str(x)],
                          [str(y)],
                          fill_color=color,
                          line_color="black",
                          line_width=1,
                          size=24)

        return x, y, color


board = Board()
board.put_stone(5, 5, "b")
board.put_stone(6, 5, "w")
board.put_stone(16, 16, "b")
board.put_stone(10, 16, "w")
board.render()
