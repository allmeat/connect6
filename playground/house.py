import os
import time
from random import random
from board import Board, Stone
from referee import Referee
from bot import Bot

if not os.path.exists("templates"):
    os.mkdir("templates")


class House:

    def __init__(self, first_player_first_move: bool):
        self.board = Board()
        self.referee = Referee()
        self.bot = Bot()
        self.first_player_first_move = first_player_first_move

    @staticmethod
    def player_input(color: str) -> Stone:
        x = input("x: ")
        y = input("y: ")
        return Stone(x, y, color)

    def play(self, render_every: bool = True):
        while True:
            turn = self.referee.turn_check(self.board.log)
            if self.first_player_first_move == (turn == "b"):
                order = "player"
                stone = self.player_input(turn)
            else:
                order = "bot"
                stone = self.bot.random_bot(turn)

            if not self.referee.valid_check(stone, self.board.log):
                print("invalid")
                continue

            self.board.put_stone(stone)
            print(f"{order} stone: {stone.x},{stone.y},{turn}")
            placement_result = self.referee.end_check(self.board.log)
            tie_check = self.referee.tie_check(self.board.log, self.board)

            if render_every:
                self.board.render_figure()

            if (placement_result != "keep play") | tie_check:
                print(f"{order} wins")
                break

        if not render_every:
            self.board.render_figure()

    def simulate(self, render_every: bool = False, pause: int = 1):
        while True:
            turn = self.referee.turn_check(self.board.log)
            if self.first_player_first_move == (turn == "b"):
                order = "tei"
                stone = Bot().tei_bot(self.board.log)
            else:
                order = "alex"
                stone = Bot().alex_bot(self.board.log)

            if not self.referee.valid_check(stone, self.board.log):
                print("invalid")
                continue

            self.board.put_stone(stone)
            print(f"{order} stone: {stone.x},{stone.y},{turn}")
            placement_result = self.referee.end_check(self.board.log)
            tie_check = self.referee.tie_check(self.board.log, self.board)

            if render_every:
                self.board.render_figure()
                time.sleep(pause)

            if (placement_result != "keep play") | tie_check:
                print(f"{order} wins")
                break

        if not render_every:
            self.board.render_figure()


if __name__ == "__main__":
    coin_toss = True if random() > 0.5 else False
    print("1p first: ", coin_toss)
    house = House(first_player_first_move=coin_toss)
    house.simulate(render_every=True)
