from typing import List
from dataclasses import dataclass
from board import BoardConfig, Stone


@dataclass
class EndCheck:
    is_end: bool
    is_tie: bool


class Referee:
    def __init__(self):
        # direction: /
        self.direction_positive = [
            lambda x, y: (x + 1, y + 1),
            lambda x, y: (x - 1, y - 1),
        ]
        # direction: \
        self.direction_negative = [
            lambda x, y: (x + 1, y - 1),
            lambda x, y: (x - 1, y + 1),
        ]
        self.color_fullname = {"b": "black", "w": "white"}

    @staticmethod
    def valid_check(new_stone: Stone, log: List[Stone]) -> bool:
        x_valid_range = (int(new_stone.x) > 0) and (int(new_stone.x) < 20)
        y_valid_range = (int(new_stone.y) > 0) and (int(new_stone.y) < 20)
        positions = [[stone.x, stone.y] for stone in log]
        empty_position = [new_stone.x, new_stone.y] not in positions
        return x_valid_range and y_valid_range and empty_position

    @staticmethod
    def turn_check(log: List[Stone]) -> str:
        if (len(log) + 1) % 4 in [0, 1]:
            return "b"
        return "w"

    def end_check(self, log: List[Stone], board_config: BoardConfig) -> EndCheck:
        is_win = self.connection_check(log, board_config.connect)
        if is_win:
            return EndCheck(True, False)
        is_tie = self.tie_check(is_win, log, board_config)
        if is_tie:
            return EndCheck(True, True)
        return EndCheck(False, False)

    @staticmethod
    def tie_check(has_winner: bool, log: List[Stone], board_config: BoardConfig) -> bool:
        if has_winner:
            return False
        if len(log) != board_config.column * board_config.row:
            return False
        return True

    def connection_check(self, log: List[Stone], radius: int) -> bool:
        current_stone = log[-1]
        check_target = self.restrict_log(current_stone, log, radius)
        horizontal_check = self.horizontal(current_stone, check_target, radius)
        vertical_check = self.vertical(current_stone, check_target, radius)
        diagonal_check = self.diagonal(current_stone, check_target, radius)
        return horizontal_check or vertical_check or diagonal_check

    @staticmethod
    def restrict_log(current_stone: Stone, log: List[Stone], radius: int) -> List[Stone]:
        result = []
        for item in log:
            in_x = int(item.x) in range(int(current_stone.x) - (radius - 1), int(current_stone.x) + radius)
            in_y = int(item.y) in range(int(current_stone.y) - (radius - 1), int(current_stone.y) + radius)
            if in_x and in_y and item.color == current_stone.color:
                result.append(item)
        return result

    @staticmethod
    def is_connected(stone_positions: List[int], radius: int) -> bool:
        connection = False
        i = 0
        connect = 0
        sort_positions = sorted(stone_positions)
        while i <= len(sort_positions) - 2:
            if sort_positions[i + 1] - sort_positions[i] == 1:
                connect += 1
            else:
                connect = 0
            if connect >= radius - 1:
                connection = True
                break
            i += 1
        return connection

    def horizontal(self, current_stone: Stone, stone_history: List[Stone], radius: int) -> bool:
        x_positions = []
        for stone in stone_history:
            if stone.y == current_stone.y:
                x_positions.append(int(stone.x))
        return self.is_connected(x_positions, radius)

    def vertical(self, current_stone: Stone, stone_history: List[Stone], radius: int) -> bool:
        y_positions = []
        for stone in stone_history:
            if stone.x == current_stone.x:
                y_positions.append(int(stone.y))
        return self.is_connected(y_positions, radius)

    def diagonal(self, current_stone: Stone, stone_history: List[Stone], radius: int) -> bool:
        is_positive_diagonal_connected = (
            self.check_diagonal_by_direction(
                current_stone,
                stone_history,
                radius,
                self.direction_positive,
            )
        )
        is_negative_diagonal_connected = (
            self.check_diagonal_by_direction(
                current_stone,
                stone_history,
                radius,
                self.direction_negative,
            )
        )
        return is_positive_diagonal_connected or is_negative_diagonal_connected

    @staticmethod
    def check_diagonal_by_direction(current_stone: Stone,
                                    stone_history: List[Stone],
                                    radius: int,
                                    directions,
                                    ) -> bool:
        direction_list = [Stone(current_stone.x, current_stone.y, current_stone.color)]
        for direction in directions:
            current_x, current_y = int(current_stone.x), int(current_stone.y)
            for i in range(radius - 1):
                new_x, new_y = direction(current_x, current_y)
                direction_list.append(Stone(str(new_x), str(new_y), current_stone.color))
                current_x, current_y = new_x, new_y
        in_position = []
        for item in sorted(direction_list, key=lambda s: int(s.x)):
            if item in stone_history:
                in_position.append("1")
            else:
                in_position.append("0")
        in_position_concat = "".join(in_position)
        return "1" * radius in in_position_concat


if __name__ == "__main__":
    test_board_config = BoardConfig(19, 19, 6, 2, 1)
    test_log = [
        Stone("1", "1", "b"),
        Stone("2", "1", "w"),
        Stone("2", "2", "w"),
        Stone("1", "2", "b"),
        Stone("1", "3", "b"),
        Stone("2", "3", "w"),
        Stone("2", "4", "w"),
        Stone("1", "4", "b"),
        Stone("1", "5", "b"),
        Stone("2", "5", "w"),
        Stone("2", "8", "w"),
        Stone("1", "10", "b"),
        Stone("1", "11", "b"),
        Stone("2", "9", "w"),
        Stone("2", "6", "w"),
    ]
    horizontal_test_log = [
        Stone("1", "1", "b"),
        Stone("1", "2", "w"),
        Stone("2", "2", "w"),
        Stone("2", "1", "b"),
        Stone("3", "1", "b"),
        Stone("3", "2", "w"),
        Stone("4", "2", "w"),
        Stone("4", "1", "b"),
        Stone("5", "1", "b"),
        Stone("5", "2", "w"),
        Stone("15", "2", "w"),
        Stone("5", "4", "b"),
        Stone("7", "3", "b"),
        Stone("6", "2", "w"),
    ]
    diagonal_test_log = [
        Stone("1", "2", "b"),
        Stone("1", "1", "w"),
        Stone("2", "2", "w"),
        Stone("1", "3", "b"),
        Stone("1", "4", "b"),
        Stone("3", "3", "w"),
        Stone("4", "4", "w"),
        Stone("1", "5", "b"),
        Stone("1", "6", "b"),
        Stone("5", "5", "w"),
        Stone("6", "5", "w"),
        Stone("10", "11", "b"),
        Stone("11", "11", "b"),
        Stone("12", "12", "w"),
        Stone("13", "13", "w"),
        Stone("14", "14", "b"),
        Stone("15", "15", "b"),
        Stone("6", "6", "w"),
    ]
    tie_test_board_config = BoardConfig(3, 3, 3, 1, 1)
    tie_test_log = [
        Stone("1", "1", "b"),
        Stone("1", "2", "w"),
        Stone("1", "3", "b"),
        Stone("2", "3", "w"),
        Stone("3", "3", "b"),
        Stone("2", "2", "w"),
        Stone("2", "1", "b"),
        Stone("3", "1", "w"),
        Stone("3", "2", "b"),
    ]

    referee = Referee()
    print("--valid_check")
    print("\t--True (valid stone input): ", referee.valid_check(Stone("10", "10", "b"), test_log))
    print("\t--False (invalid stone input):", referee.valid_check(Stone("1", "1", "w"), test_log))
    print("--turn_check")
    print("\t--w (white turn): ", referee.turn_check(test_log[:-1]))
    print("\t--b (black turn): ", referee.turn_check(test_log))
    print("--end_check")
    print("\t--end = False, tie = False (not end): ", referee.end_check(test_log[:-1], test_board_config))
    print("\t--end = True, tie = False (horizontal win): ", referee.end_check(horizontal_test_log, test_board_config))
    print("\t--end = True, tie = False (vertical win): ", referee.end_check(test_log, test_board_config))
    print("\t--end = True, tie = False (diagonal win): ", referee.end_check(diagonal_test_log, test_board_config))
    print("\t--end = True, tie = True (tie): ", referee.end_check(tie_test_log, tie_test_board_config))
    print("--tie_check")
    print("\t--True (tie): ", referee.tie_check(False, tie_test_log, tie_test_board_config))
    print("\t--False (not full): ", referee.tie_check(False, tie_test_log[:-1], tie_test_board_config))
    print("\t--False (not full): ", referee.tie_check(False, diagonal_test_log, test_board_config))
    print("\t--False (has winner): ", referee.tie_check(True, diagonal_test_log, test_board_config))
