from typing import List
from board import Board, Stone


class Referee:

    @staticmethod
    def valid_check(new_stone: Stone, log: List[Stone]) -> bool:
        x_valid_range = (int(new_stone.x) > 0) & (int(new_stone.x) < 20)
        y_valid_range = (int(new_stone.y) > 0) & (int(new_stone.y) < 20)
        coordinate = [[stone.x, stone.y] for stone in log]
        empty_seat = [new_stone.x, new_stone.y] not in coordinate
        return x_valid_range & y_valid_range & empty_seat

    @staticmethod
    def turn_check(log: List[Stone]) -> str:
        if (len(log) + 1) % 4 in [0, 1]:
            return "b"
        else:
            return "w"

    def end_check(self, current_stone: Stone, previous_log: List[Stone]) -> str:
        is_win = self.connection_check(current_stone, previous_log)
        english = {"b": "black", "w": "white"}

        if is_win:
            return "%s wins" % english[current_stone.color]
        else:
            return "keep play"

    @staticmethod
    def filter_log(current_stone: Stone, previous_log: List[Stone]):
        filtered_history = []
        for item in previous_log:
            in_x = item.x in range(int(current_stone.x) - 5, int(current_stone.x) + 6)
            in_y = item.y in range(int(current_stone.y) - 5, int(current_stone.y) + 6)
            if in_x and in_y and item.color == current_stone.color:
                filtered_history.append(item)
        return filtered_history

    def connection_check(self, current_stone: Stone, stone_history: List[Stone]) -> bool:
        smaller_board = self.filter_log(current_stone, stone_history)
        horizontal_check = self.horizontal(current_stone, smaller_board)
        vertical_check = self.vertical(current_stone, smaller_board)
        diagonal_check = self.diagonal(current_stone, stone_history)

        return horizontal_check | vertical_check | diagonal_check

    @staticmethod
    def is_connected(numbers: List[int]) -> bool:
        print("lists:", numbers)
        last = sorted(numbers)[0]
        connect = 0
        for i in sorted(numbers):
            if i - last == 1:
                connect += 1
            else:
                connect = 0
            last = i
        print(connect)
        if connect >= 5:
            return True
        else:
            return False

    def horizontal(self, current_stone: Stone, stone_history: List[Stone]) -> bool:
        out = []
        for stone in stone_history:
            if stone.y == current_stone.y:
                out.append(int(stone.x))
        return self.is_connected(out)

    def vertical(self, current_stone: Stone, stone_history: List[Stone]) -> bool:
        out = []
        for stone in stone_history:
            if stone.x == current_stone.x:
                out.append(int(stone.y))
        return self.is_connected(out)

    def diagonal(self, current_stone: Stone, stone_history: List[Stone]) -> bool:
        # direction: /
        direction_positive = [
            lambda x, y: (x + 1, y + 1),
            lambda x, y: (x - 1, y - 1),
        ]
        # direction: \
        direction_negative = [
            lambda x, y: (x + 1, y - 1),
            lambda x, y: (x - 1, y + 1),
        ]
        bool_positive = self.check_diagonal_by_direction(stone_history, current_stone, direction_positive)
        bool_negative = self.check_diagonal_by_direction(stone_history, current_stone, direction_negative)

        return bool_positive | bool_negative

    @staticmethod
    def check_diagonal_by_direction(all_position, current_stone, direction) -> bool:
        dir_list = [Stone(current_stone.x, current_stone.y, current_stone.color)]
        for dir_func in direction:
            cx, cy = current_stone.x, current_stone.y
            for i in range(5):
                new_x, new_y = dir_func(cx, cy)
                dir_list.append(Stone(new_x, new_y, current_stone.color))
                cx, cy = new_x, new_y
        find = []
        for item in sorted(dir_list, key=lambda s: s.x):
            if item in all_position:
                find.append("1")
            else:
                find.append("0")

        find_string = "".join(find)
        return "111111" in find_string

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
        Stone("2", "6", "w"),
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
    print("\t--keep play: ", referee.end_check(test_log[-1], test_log[:-1]))
    print("\t--white wins (horizontal): ", referee.end_check(test_log[-1], test_log))
    print("\t--white wins (diagonal): ", referee.end_check(test_log[-1], diagonal_test_log))
