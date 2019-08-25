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
            x = input("x: ")
            y = input("y: ")
            stone = Stone(x, y, color)
        else:
            stone = bot.random_bot()
        if referee.valid_check(stone, board.log):
            board.put_stone(stone)
            print(f"{turn} stone = {stone.x}, {stone.y}, {color}")
        else:
            print("invalid stone input")


while referee.end_check(board.log) == "keep play":
    if player_first:
        play("player", "b")
        if referee.end_check(board.log) != "keep play":
            break
        play("bot", "w")
    else:
        play("bot", "b")
        if referee.end_check(board.log) != "keep play":
            break
        play("player", "w")

print(referee.end_check(board.log))
board.render_figure()
