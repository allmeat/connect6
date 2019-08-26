import os
import re
import json
from flask import Flask, render_template, request
from board import Board, Stone

if not os.path.exists("templates"):
    os.mkdir("templates")

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
board = Board()
board.save_figure()
regex_digit = re.compile(r"\d+")
regex_color = re.compile(r"[bw]")


@app.route("/")
def index():
    return render_template("board.html")


@app.route("/play", methods=["GET"])
def play():
    x = request.args.get("x")
    y = request.args.get("y")
    color = request.args.get("color")

    if regex_digit.match(x) is None:
        return {"code": 400, "message": "illegal input in x"}, 400
    elif regex_digit.match(y) is None:
        return {"code": 400, "message": "illegal input in y"}, 400
    elif regex_color.match(color) is None:
        return {"code": 400, "message": "illegal input in stone"}, 400
    else:
        # TODO : set referee here
        board.put_stone(Stone(x, y, color))
        board.save_figure()
        return render_template("board.html")


@app.route("/history")
def history():
    board_log = [f"{item.x},{item.y},{item.color}" for item in board.log]
    return json.dumps({"code": 200, "data": board_log})


@app.route("/reset")
def reset():
    board.log.clear()
    board.setup()
    board.save_figure()
    return render_template("board.html")


if __name__ == "__main__":
    app.run(port=8080)
