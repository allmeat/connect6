import unittest

from connect_db import DBConfig
from game import *
from playground.board import BoardConfig
from playground.house import Stone


class GameTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GameTest, self).__init__(*args, **kwargs)
        self.engine = "mysql+pymysql://root:allmeat@35.233.179.226:3306/playground_log"
        self.db = DBConfig()
        self.session = self.db.setup_db_connection(self.engine)

    def test_save_game(self):
        winner = "monkey"
        board_config = BoardConfig(19, 19, 6, 2, 1)
        black_player = "dog"
        white_player = "monkey"
        logs = [Stone("3", "2", "b"),
                Stone("2", "1", "w"),
                Stone("2", "2", "w")]
        gid = save_game_and_return_id(
            session=self.session, winner=winner,
            board_config=board_config,
            black_player=black_player, white_player=white_player,
            logs=logs)
        res = self.session.query(Game).filter(Game.id == gid).first()
        self.assertEqual(gid, res.id)
        self.assertEqual(winner, res.winner)
        self.assertEqual(white_player, res.white_player)
        self.assertEqual(black_player, res.black_player)

    def test_save_game_logs(self):
        game_id = 0
        logs = [Stone("3", "2", "b"),
                Stone("2", "1", "w"),
                Stone("2", "2", "w")]
        save_game_logs(self.session, game_id, logs)
        res = self.session.query(Game).filter(GameLog.game_id == game_id).all()
        self.assertEqual(3, len(res))
        self.assertEqual(0,res(0).index)

    def test_save_game_result(self):
        winner = "monkey"
        board_config = BoardConfig(19, 19, 6, 2, 1)
        black_player = "dog"
        white_player = "monkey"
        logs = [Stone("3", "2", "b"),
                Stone("2", "1", "w"),
                Stone("2", "2", "w")]
        save_game_result(self.session, winner, board_config, black_player, white_player, logs)
