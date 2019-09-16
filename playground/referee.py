from typing import List
from board import Board, Stone


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
        else:
            return "w"

    def end_check(self, log: List[Stone]) -> str:
        current_stone = log[-1]
        is_win = self.connection_check(current_stone, log)
        color_fullname = {"b": "black", "w": "white"}

        if is_win:
            return f"{color_fullname[current_stone.color]} wins"
        else:
            return "keep play"

    @staticmethod
    def filter_log(log: List[Stone], radius=6):
        current_stone = log[-1]
        filtered_history = []
        for item in log:
            in_x = int(item.x) in range(int(current_stone.x) - (radius - 1), int(current_stone.x) + radius)
            in_y = int(item.y) in range(int(current_stone.y) - (radius - 1), int(current_stone.y) + radius)
            if in_x and in_y and item.color == current_stone.color:
                filtered_history.append(item)
        return filtered_history

    def connection_check(self, current_stone: Stone, stone_history: List[Stone]) -> bool:
        smaller_board = self.filter_log(stone_history)
        horizontal_check = self.horizontal(current_stone, smaller_board)
        vertical_check = self.vertical(current_stone, smaller_board)
        diagonal_check = self.diagonal(current_stone, stone_history)
        return horizontal_check or vertical_check or diagonal_check

    @staticmethod
    def is_connected(stone_positions: List[int]) -> bool:
        connection = False
        i = 0
        connect = 0
        sort_positions = sorted(stone_positions)
        while i <= len(sort_positions) - 2:
            if sort_positions[i + 1] - sort_positions[i] == 1:
                connect += 1
            else:
                connect = 0
            if connect >= 5:
                connection = True
                break
            i += 1
        return connection

    def horizontal(self, current_stone: Stone, stone_history: List[Stone]) -> bool:
        x_positions = []
        for stone in stone_history:
            if stone.y == current_stone.y:
                x_positions.append(int(stone.x))
        return self.is_connected(x_positions)

    def vertical(self, current_stone: Stone, stone_history: List[Stone]) -> bool:
        y_positions = []
        for stone in stone_history:
            if stone.x == current_stone.x:
                y_positions.append(int(stone.y))
        return self.is_connected(y_positions)

    def diagonal(self, current_stone: Stone, stone_history: List[Stone]) -> bool:
        is_positive_diagonal_connected = self.check_diagonal_by_direction(stone_history,
                                                                          current_stone,
                                                                          self.direction_positive)
        is_negative_diagonal_connected = self.check_diagonal_by_direction(stone_history,
                                                                          current_stone,
                                                                          self.direction_negative)
        return is_positive_diagonal_connected or is_negative_diagonal_connected

    @staticmethod
    def check_diagonal_by_direction(all_positions: List[Stone],
                                    current_stone: Stone,
                                    directions
                                    ) -> bool:
        direction_list = [Stone(current_stone.x, current_stone.y, current_stone.color)]
        for direction in directions:
            current_x, current_y = int(current_stone.x), int(current_stone.y)
            for i in range(5):
                new_x, new_y = direction(current_x, current_y)
                direction_list.append(Stone(str(new_x), str(new_y), current_stone.color))
                current_x, current_y = new_x, new_y
        in_position = []
        for item in sorted(direction_list, key=lambda s: int(s.x)):
            if item in all_positions:
                in_position.append("1")
            else:
                in_position.append("0")

        in_position_concat = "".join(in_position)
        return "111111" in in_position_concat

    @staticmethod
    def tie_check(log: List[Stone], board: Board) -> bool:
        max_turn = board.config.column * board.config.row
        current_turn = len(log)
        if max_turn - current_turn == 1:
            return True
        else:
            return False


if __name__ == "__main__":
    referee = Referee()
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
        Stone("8", "2", "w"),
        Stone("10", "1", "b"),
        Stone("11", "1", "b"),
        Stone("9", "2", "w"),
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

    test_board = Board(2, 2, 2, 1, 1)
    tie_check_log = [
        Stone("1", "1", "b"),
        Stone("1", "2", "b"),
        Stone("2", "1", "w")
    ]

    print("--tie_check")
    print("\t--tie: ", referee.tie_check(tie_check_log, test_board))
    print("\t--not tie: ", referee.tie_check(tie_check_log[:1], test_board))
    print("--valid_check")
    print("\t--valid stone: ", referee.valid_check(Stone("10", "10", "b"), test_log))
    print("\t--invalid stone:", referee.valid_check(Stone("1", "1", "w"), test_log))
    print("--turn_check")
    print("\t--white turn: ", referee.turn_check(test_log[:-1]))
    print("\t--black turn: ", referee.turn_check(test_log))
    print("--end_check")
    print("\t--keep play: ", referee.end_check(test_log[:-1]))
    print("\t--white wins (vertical): ", referee.end_check(test_log))
    print("\t--white wins (horizontal): ", referee.end_check(horizontal_test_log))
    print("\t--white wins (diagonal): ", referee.end_check(diagonal_test_log))
