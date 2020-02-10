import datetime
from dataclasses import dataclass
from typing import List

from board import Stone, BoardConfig


@dataclass
class Game:
    winner: str
    total_size: int
    board_config: str
    black_player: str
    white_player: str
    created_time: datetime


@dataclass
class GameLog:
    game_id: int  # id from GameRecord
    idx: int
    stone_color: str
    x_axis: int
    y_axis: int


def convert_to_game(winner: str, board_config: BoardConfig, black_player: str, white_player: str,
                    logs: List[Stone]) -> Game:
    return Game(winner=winner,
                total_size=len(logs),
                board_config=str(board_config),
                black_player=black_player,
                white_player=white_player,
                created_time=datetime.datetime.now)


def convert_to_game_log(game_id: int, index: int, stone: Stone) -> GameLog:
    return GameLog(game_id=game_id, idx=index, stone_color=stone.color, x_axis=int(stone.x), y_axis=int(stone.y))
