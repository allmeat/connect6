import os
import time
import util
from repo.game import save_game_result
from connect_db import DBConfig
from random import random
from board import Board
from referee import Referee
from bot import Bot

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

    def simulate(self, p1: str, p2: str, render_every: bool = False, pause: float = 1.0, save: bool = False):
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

            self.board.put_stone(stone)
            print(f"{order} stone: {stone.x},{stone.y},{turn}")

            game_info = {}
            end_check = self.referee.end_check(self.board.log, self.board.config)
            if end_check.is_end:
                winner = "no one" if end_check.is_tie else order
                print(f"{winner} wins")
                self.board.print_winner(winner)

                if end_check.is_tie:
                    print("No winner")
                    break

                if save:
                    game_info["winner"] = winner
                    game_info["config"] = self.board.config
                    game_info["len_log"] = len(self.board.log)

                    if self.first_player_first_move:
                        game_info["black_player"] = p1
                        game_info["white_player"] = p2
                    else:
                        game_info["black_player"] = p2
                        game_info["white_player"] = p1

                    game_info["first_move"] = self.first_player_first_move
                    game_info["log"] = self.board.log

                    engine = "mysql+pymysql://root:allmeat@35.233.179.226:3306/playground_log"
                    db = DBConfig()
                    session = db.setup_db_connection(engine)
                    save_game_result(
                        session, winner=game_info['winner'],
                        board_config=game_info['config'],
                        black_player=game_info['black_player'],
                        white_player=game_info['white_player'],
                        logs=game_info['log']
                    )

                    print("Saved game result")
                    break
                else:
                    self.board.render_figure()
                    break

            if render_every:
                self.board.draw_board(self.board.log)
                time.sleep(pause)


if __name__ == "__main__":
    coin_toss = True if random() > 0.5 else False
    print("1p first: ", coin_toss)
    house2 = House(first_player_first_move=coin_toss)
    house2.simulate("tei", "jw", render_every=False, pause=0.5, save=True)
