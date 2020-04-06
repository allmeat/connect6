import os
from random import random, sample
import argparse

from house import House
from connect_db import DBConfig
from game import save_game_result

if not os.path.exists("templates"):
    os.mkdir("templates")


class LogCollector:

    def __init__(self):
        self.engine = "mysql+pymysql://root:allmeat@35.233.179.226:3306/playground_log"
        self.winner: str
        self.board_config: str
        self.black_player: str
        self.white_player: str
        self.logs: str

    def get_simulated_result(self, player1, player2: str):
        coin_toss = True if random() > 0.5 else False
        house = House(first_player_first_move=coin_toss)
        house.simulate(player1, player2, render_every=False, pause=0.5)
        if coin_toss:
            self.black_player, self.white_player = player1, player2
        else:
            self.black_player, self.white_player = player2, player1
        self.winner = house.winner
        self.board_config = house.board.config
        self.logs = house.board.log

    def insert(self):
        db = DBConfig()
        sess = db.setup_db_connection(self.engine)
        save_game_result(sess, self.winner, self.board_config, self.black_player, self.white_player, self.logs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("simulates and saves logs")
    parser.add_argument("total_simulations", type=int,
                        help="total number of simulations")
    args = parser.parse_args()

    simulation_counts = args.total_simulations
    lc = LogCollector()
    players = ["alex", "jw", "tei"]

    for i in range(simulation_counts):
        print("starting simulation: ", i)
        p1, p2 = sample(players, 2)
        print("p1:", p1, " and p2:", p2)
        lc.get_simulated_result(p1, p2)
        lc.insert()
        print("finishing simulation: ", i)
