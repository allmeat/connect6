from random import random
from board import Board
from referee import Referee
from player import Player
from bot import Bot


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

    def play(self, order: str, color: str):
        while self.referee.turn_check(self.board.log) == color:
            if order == "player":
                stone = self.player.manual_input()
            else:
                stone = self.bot.random_bot()

            if self.referee.valid_check(stone, self.board.log):
                self.board.put_stone(stone)
                print(f"{order} stone: {stone.x},{stone.y},{color}")
            else:
                print("invalid stone input")

    def game(self):
        while self.referee.end_check(self.board.log) == "keep play":
            if self.player_first:
                self.play("player", "b")
                if self.referee.end_check(self.board.log) != "keep play":
                    break
                self.play("bot", "w")
            else:
                self.play("bot", "b")
                if self.referee.end_check(self.board.log) != "keep play":
                    break
                self.play("player", "w")

        print(self.referee.end_check(self.board.log))
        self.board.render_figure()


if __name__ == "__main__":
    coin_toss = True if random() > 0.5 else False
    print("player first: ", coin_toss)
    house = House(coin_toss)
    house.game()
