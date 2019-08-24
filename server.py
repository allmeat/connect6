from dataclasses import dataclass
from board import Board
from bokeh.plotting import output_file, save
from flask import Flask, render_template, request


@dataclass
class Stone:
    x: int
    y: int
    stone: str


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
board_object = Board()
output_file("templates/board.html")
save(board_object.board)
log = []


@app.route("/")
def index():
    return render_template("board.html")


@app.route("/play", methods=["GET"])
def play():
    # TODO : input regex check
    x = request.args.get("x")
    y = request.args.get("y")
    stone = request.args.get("stone")
    log.append(Stone(x, y, stone))
    board_object.put_stone(x, y, stone)
    save(board_object.board)
    return render_template("board.html")


@app.route("/logging")
def logging():
    return "/".join([f"{i + 1},{item.x},{item.y},{item.stone}" for i, item in enumerate(log)])


@app.route("/reset")
def reset():
    log.clear()
    board_object.setup()
    save(board_object.board)
    return render_template("board.html")


if __name__ == "__main__":
    app.run(port=8080)
