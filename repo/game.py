import datetime
import json
from typing import List

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from board import Stone, BoardConfig

Base = declarative_base()

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    winner = Column(String)
    total_size = Column(Integer)
    board_config = Column(String)
    black_player = Column(String)
    white_player = Column(String)
    created_time = Column(DateTime)

    def __init__(self,
                 winner: str,
                 board_config: BoardConfig,
                 black_player: str,
                 white_player: str,
                 logs: List[Stone],
                 ):
        self.winner = winner
        self.total_size = len(logs)
        self.board_config = json.dumps(board_config.__dict__)
        self.black_player = black_player
        self.white_player = white_player
        self.created_time = datetime.datetime.now()


class GameLog(Base):
    __tablename__ = "game_logs"

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id"))  # id from GameRecord
    idx = Column(Integer)
    stone_color = Column(String)
    x_axis = Column(Integer)
    y_axis = Column(Integer)

    def __init__(self,
                 game_id: int,
                 index: int,
                 stone: Stone,
                 ):
        self.game_id = game_id
        self.idx = index
        self.stone_color = stone.color
        self.x_axis = int(stone.x)
        self.y_axis = int(stone.y)


def save_game_and_return_id(session: Session,
                            winner: str,
                            board_config: BoardConfig,
                            black_player: str,
                            white_player: str,
                            logs: List[Stone],
                            ) -> int:
    game = Game(
        winner=winner,
        board_config=board_config,
        black_player=black_player,
        white_player=white_player,
        logs=logs,
    )
    session.add(game)
    session.flush()
    game_id = game.id
    session.commit()
    return game_id


def save_game_logs(session: Session,
                   game_id: int,
                   logs: List[Stone],
                   ):
    for i, stone in enumerate(logs):
        game_log = GameLog(game_id=game_id, index=i, stone=stone)
        session.add(game_log)
        session.commit()


def save_game_result(session: Session,
                     winner: str,
                     board_config: BoardConfig,
                     black_player: str,
                     white_player: str,
                     logs: List[Stone],
                     ):
    game_id = save_game_and_return_id(session, winner, board_config, black_player, white_player, logs)
    save_game_logs(session, game_id, logs)
