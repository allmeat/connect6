import os
from random import random
from playground.board import Board
from playground.referee import Referee
from playground.player import Player
from playground.bot import Bot

if not os.path.exists("templates"):
    os.mkdir("templates")


class House:

    def __init__(self, player_first: bool):
        self.board = Board()
        self.referee = Referee()
        self.player_first = player_first

        if self.player_first:
            self.player = Player("b")
            self.bot = Bot("w")
        else:
            self.player = Player("w")
            self.bot = Bot("b")

    def play(self):
        while True:
            turn = self.referee.turn_check(self.board.log)
            if self.player_first == (turn == "b"):
                order = "player"
                stone = self.player.manual_input()
            else:
                order = "bot"
                stone = self.bot.random_bot()

            if self.referee.valid_check(stone, self.board.log):
                self.board.put_stone(stone)
                print(f"{order} stone: {stone.x},{stone.y},{turn}")
                if self.referee.end_check(self.board.log) != "keep play":
                    break
            else:
                print("invalid stone input")

        print(self.referee.end_check(self.board.log))
        self.board.render_figure()


if __name__ == "__main__":
    coin_toss = True if random() > 0.5 else False
    print("player first: ", coin_toss)
    house = House(coin_toss)
    house.play()
