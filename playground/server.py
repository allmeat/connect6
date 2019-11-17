import os
import re
import json
from flask import Flask, render_template, request
from board import Board, Stone
from referee import Referee

if not os.path.exists("templates"):
    os.mkdir("templates")

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
board = Board()
board.save_figure()
referee = Referee()
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

    if regex_digit.match(y) is None:
        return {"code": 400, "message": "illegal input in y"}, 400

    if regex_color.match(color) is None:
        return {"code": 400, "message": "illegal input in stone"}, 400

    if color != referee.turn_check(board.log):
        board.print_illegal_turn()
        board.save_figure()
        return render_template("board.html")

    stone = Stone(x, y, color)
    if not referee.valid_check(stone, board.log):
        board.print_illegal_stone()
        board.save_figure()
        return render_template("board.html")

    board.put_stone(stone)
    end_check = referee.end_check(board.log, board.config)
    if end_check.is_end:
        winner = "no one" if end_check.is_tie else color
        board.print_winner(winner)
        board.save_figure()
        return render_template("board.html")

    board.print_on_playing()
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

"""
request sample
board       : http://127.0.0.1:8080

stone log   : http://127.0.0.1:8080/history

reset board : http://127.0.0.1:8080/reset  

1st move    : http://127.0.0.1:8080/play?x=10&y=10&color=b
2nd move    : http://127.0.0.1:8080/play?x=10&y=11&color=w
3rd move    : http://127.0.0.1:8080/play?x=9&y=11&color=w
4th move    : http://127.0.0.1:8080/play?x=9&y=9&color=b
5th move    : http://127.0.0.1:8080/play?x=11&y=11&color=b
6th move    : http://127.0.0.1:8080/play?x=8&y=11&color=w
7th move    : http://127.0.0.1:8080/play?x=8&y=8&color=w
8th move    : http://127.0.0.1:8080/play?x=11&y=10&color=b
9th move    : http://127.0.0.1:8080/play?x=12&y=10&color=b
10th move   : http://127.0.0.1:8080/play?x=8&y=10&color=w
11th move   : http://127.0.0.1:8080/play?x=8&y=9&color=w
12th move   : http://127.0.0.1:8080/play?x=13&y=10&color=b
13th move    : http://127.0.0.1:8080/play?x=14&y=10&color=b
14th move   : http://127.0.0.1:8080/play?x=8&y=12&color=w
15th move   : http://127.0.0.1:8080/play?x=8&y=7&color=w
"""
