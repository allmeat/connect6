from board import Board, Stone
from referee import Referee
from player import Player
from bot import Bot

board = Board()
referee = Referee()

player_first = False
if player_first:
    player = Player("b")
    bot = Bot("w")
else:
    player = Player("w")
    bot = Bot("b")


def play(order: str, color: str):
    while referee.turn_check(board.log) == color:
        if order == "player":
            stone = player.manual_input()
        else:
            stone = bot.random_bot()

        if referee.valid_check(stone, board.log):
            board.put_stone(stone)
            print(f"{order} stone: {stone.x},{stone.y},{color}")
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
