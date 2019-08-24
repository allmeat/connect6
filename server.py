import re
from board import Board, Stone
from bokeh.plotting import output_file, save
from flask import Flask, render_template, request


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
board_object = Board()
output_file("templates/board.html")
save(board_object.board)
regex_digit = re.compile(r"\d+")
regex_stone = re.compile(r"[bw]")


@app.route("/")
def index():
    return render_template("board.html")


@app.route("/play", methods=["GET"])
def play():
    x = request.args.get("x")
    y = request.args.get("y")
    stone = request.args.get("stone")

    if regex_digit.match(x) is None:
        return {"code": 400, "message": "illegal input in x"}, 400
    elif regex_digit.match(y) is None:
        return {"code": 400, "message": "illegal input in y"}, 400
    elif regex_stone.match(stone) is None:
        return {"code": 400, "message": "illegal input in stone"}, 400
    else:
        board_object.log.append(Stone(x, y, stone))
        board_object.put_stone(x, y, stone)
        save(board_object.board)
        return render_template("board.html")


@app.route("/history")
def history():
    return "/".join([f"{i + 1},{item.x},{item.y},{item.stone}" for i, item in enumerate(board_object.log)])


@app.route("/reset")
def reset():
    board_object.log.clear()
    board_object.setup()
    save(board_object.board)
    return render_template("board.html")


if __name__ == "__main__":
    app.run(port=8080)
