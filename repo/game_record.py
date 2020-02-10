from dataclasses import dataclass


@dataclass
class GameRecord:
    id: int
    winner: str
    total_size: int
    board_config: str
    black_player: str
    white_player: str


@dataclass
class GameRecordLog:
    id: int
    record_id: int #id from GameRecord
    index: int
    stone_color: str
    x_axis: int
    y_axis: int
    created_date: str
