import unittest

from connect_db import DBConfig
from game import *
from playground.board import BoardConfig
from playground.house import Stone


class GameTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GameTest, self).__init__(*args, **kwargs)
        self.engine = "mysql+pymysql://root:allmeat@35.233.179.226:3306/playground_log"

    def test_save_game_logs(self):
        db = DBConfig()
        sess = db.setup_db_connection(self.engine)
        winner = "monkey"
        board_config = BoardConfig(19, 19, 6, 2, 1)
        black_player = "dog"
        white_player = "monkey"
        logs = [Stone("3", "2", "b"),
                Stone("2", "1", "w"),
                Stone("2", "2", "w")]
        game = Game(
            winner=winner,
            board_config=board_config,
            black_player=black_player,
            white_player=white_player,
            logs=logs,
        )
        self.assertEqual(winner, game.winner)
        sess.add(game)
        sess.flush()
        gid = game.id
        self.assertEqual(0, gid)
