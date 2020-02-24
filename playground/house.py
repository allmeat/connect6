import os
import time
from random import random
from board import Board, Stone
from referee import Referee
from bot import Bot
import util
from repo.game import Game, GameLog

if not os.path.exists("templates"):
    os.mkdir("templates")


class House:

    def __init__(self, first_player_first_move: bool):
        self.board = Board()
        self.referee = Referee()
        self.bot = Bot(self.board.config)
        self.first_player_first_move = first_player_first_move
        self.bot_alias = {
            "alex": self.bot.alex_bot,
            "tei": self.bot.tei_bot,
            "jw": self.bot.alex_bot
        }

    @staticmethod
    def player_input(color: str) -> Stone:
        x = input("x: ")
        y = input("y: ")
        return Stone(x, y, color)

    def play(self, render_every: bool = True):
        while True:
            turn = util.turn_check(self.board.log, self.board.config.each_move, self.board.config.first_move)
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
            end_check = self.referee.end_check(self.board.log, self.board.config)
            if end_check.is_end:
                winner = "no one" if end_check.is_tie else order
                print(f"{winner} wins")
                self.board.print_winner(winner)
                self.board.render_figure()
                break

            if render_every:
                self.board.render_figure()

    def simulate(self, p1: str, p2: str, render_every: bool = False, pause: float = 1.0):
        while True:
            turn = util.turn_check(self.board.log, self.board.config.each_move, self.board.config.first_move)
            if self.first_player_first_move == (turn == "b"):
                order = p1
                stone = self.bot_alias.get(p1, util.exit_by_alias)(self.board.log)
            else:
                order = p2
                stone = self.bot_alias.get(p2, util.exit_by_alias)(self.board.log)

            if not self.referee.valid_check(stone, self.board.log):
                print("invalid")
                continue

            game_info = {}

            self.board.put_stone(stone)
            print(f"{order} stone: {stone.x},{stone.y},{turn}")
            end_check = self.referee.end_check(self.board.log, self.board.config)
            if end_check.is_end:
                winner = "no one" if end_check.is_tie else order
                print(f"{winner} wins")
                self.board.print_winner(winner)
                self.board.render_figure()

                game_info["winner"] = winner
                game_info["config"] = self.board.config
                game_info["len_log"] = len(self.board.log)

                if self.first_player_first_move:
                    game_info["black_player"] = p1
                    game_info["white_player"] = p2
                    #black_player = p1
                    #white_player = p2
                else:
                    game_info["black_player"] = p2
                    game_info["white_player"] = p1
                    #black_player = p1
                    #white_player = p2

                game_info["first_move"] = self.first_player_first_move
                game_info["log"] = self.board.log

                game = Game(
                    winner = game_info['winner'],
                    board_config = game_info['config'],
                    black_player = game_info['black_player'],
                    white_player = game_info['white_player'],
                    logs = game_info['log'],
                )
                game_log=[]
                for i, stone in enumerate(self.board.log):
                    game_log.append(GameLog(game_id=1, index=i, stone=stone))

                return game, game_log#game_info

            if render_every:
                # self.board.render_figure()
                self.board.draw_board(self.board.log)
                time.sleep(pause)


if __name__ == "__main__":
    coin_toss = True if random() > 0.5 else False
    print("1p first: ", coin_toss)
    house = House(first_player_first_move=coin_toss)
    # house.simulate("alex", "tei", render_every=False, pause=0.5)
    aa = house.simulate("alex", "tei", render_every=False, pause=0.5)
    print(aa)