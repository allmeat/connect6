from board import Board, Stone
from referee import Referee
from bot import Bot

board = Board()
referee = Referee()

player_first = True
bot = Bot("w") if player_first else Bot("b")


def play(turn: str, color: str):
    while referee.turn_check(board.log) == color:
        if turn == "player":
            x = input("x : ")
            y = input("y : ")
            stone = Stone(x, y, "b")
        else:
            stone = bot.random_bot()
        if referee.valid_check(stone, board.log):
            board.log.append(stone)
            board.put_stone(stone)
            print(f"{turn} stone = {stone.x}, {stone.y}, {color}")
            if referee.end_check(board.log):
                break
        else:
            print("invalid stone input")


while not referee.end_check(board.log):
    if player_first:
        play("player", "b")
        play("bot", "w")
    else:
        play("bot", "b")
        play("player", "w")

board.render_figure()
