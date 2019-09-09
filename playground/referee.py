from typing import List, DefaultDict
from collections import defaultdict
from playground.board import Board, Stone


# TODO : sparse
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

	def end_check_new(self, log: List[Stone]) -> str:
		last_stone = log[-1]
		is_win = self.connection_check_new(last_stone, log)
		english = {"b": "black", "w": "white"}

		if is_win:
			return "%s wins" % english[last_stone.color]
		else:
			return "keep play"

	@staticmethod
	def filter_log(current_position: Stone, all_position: List[Stone]):
		filtered = []
		for item in all_position:
			in_x = item.x in range(int(current_position.x - 5), int(current_position.x + 6))
			in_y = item.y in range(int(current_position.y - 5), int(current_position.y + 6))
			if in_x and in_y and item.color == current_position.color:
				filtered.append(item)
		return filtered

	def connection_check_new(self, last_stone: Stone, log: List[Stone]) -> bool:
		smaller_board = self.filter_log(last_stone, log)
		ew = self.east_west(last_stone, smaller_board)
		ns = self.north_south(last_stone, smaller_board)
		diagonal_check = self.diagonal_connection_check(last_stone, log)

		return ew | ns | diagonal_check

	@staticmethod
	def is_connected6(numbers: List[int]) -> bool:
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

	def east_west(self, current_stone: Stone, smaller_log: List[Stone]) -> bool:
		out = []
		for stone in smaller_log:
			if stone.y == current_stone.y:
				out.append(stone.x)
		return self.is_connected6(out)

	def north_south(self, current_stone: Stone, smaller_log: List[Stone]) -> bool:
		out = []
		for stone in smaller_log:
			if stone.x == current_stone.x:
				out.append(stone.y)
		return self.is_connected6(out)

	@staticmethod
	def diagonal_connection_check(current_position: Stone, all_position: List[Stone]) -> bool:

		DIRECTIONS1 = [
			lambda x, y: (x + 1, y + 1),
			lambda x, y: (x - 1, y - 1),
		]
		DIRECTIONS2 = [
			lambda x, y: (x + 1, y - 1),
			lambda x, y: (x - 1, y + 1),
		]
		dir1_list = [Stone(current_position.x, current_position.y, current_position.color)]
		dir2_list = [Stone(current_position.x, current_position.y, current_position.color)]

		for dir_func in DIRECTIONS1:
			cx, cy = current_position.x, current_position.y
			for i in range(5):
				newx, newy = dir_func(cx, cy)
				dir1_list.append(Stone(newx, newy, current_position.color))
				cx, cy = newx, newy

		for dir_func in DIRECTIONS2:
			cx, cy = current_position.x, current_position.y
			for i in range(5):
				newx, newy = dir_func(cx, cy)
				dir2_list.append(Stone(newx, newy, current_position.color))
				cx, cy = newx, newy
		find1 = []
		for item in sorted(dir1_list, key=lambda s: s.x):
			if item in all_position:
				find1.append("1")
			else:
				find1.append("0")
		find2 = []
		for item in sorted(dir2_list, key=lambda s: s.x):
			if item in all_position:
				find2.append("1")
			else:
				find2.append("0")

		findstring1 = "".join(find1)
		findstring2 = "".join(find2)
		bool1 = "111111" in findstring1
		bool2 = "111111" in findstring2
		return bool1 | bool2

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
    print("\t--keep play: ", referee.end_check(test_log[:-1]))
    print("\t--white wins (horizontal): ", referee.end_check(test_log))
    print("\t--white wins (diagonal): ", referee.end_check(diagonal_test_log))
  