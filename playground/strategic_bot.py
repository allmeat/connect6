from collections import defaultdict
from operator import itemgetter
from typing import List, Dict
from random import randint, choice
from dataclasses import dataclass
from board import Stone, BoardConfig
from util import turn_check, Direction


@dataclass
class Edge:
	stone: Stone
	directions: List[str]


# edge is left most or upper most stone in a connection: left has priority
def is_stone_edge(s: Stone, log: List[Stone]) -> (bool, List[str]):
	is_present = {
		Direction.DOWN_RIGHT: Stone(str(int(s.x) - 1), str(int(s.y) - 1), s.color),
		Direction.DOWN: Stone(s.x, str(int(s.y) - 1), s.color),
		Direction.RIGHT: Stone(str(int(s.x) - 1), s.y, s.color),
		Direction.UP_RIGHT: Stone(str(int(s.x) - 1), str(int(s.y) + 1), s.color)
	}
	direction = defaultdict(int)
	for stone in log:
		for dr, p in is_present.items():
			direction[dr] = 1
			if stone == p:
				del direction[dr]
				break
	if len(direction) > 0:
		is_edge = True
	else:
		is_edge = False
	return is_edge, list(direction.keys())


class StrategicBot:
	def __init__(self, board_config: BoardConfig):
		self.k = board_config.connect
		self.m = board_config.row
		self.n = board_config.column
		self.p = board_config.each_move
		self.q = board_config.first_move
		# TODO: direction functions to be generalized to util (on the next phase)
		self.directions = {
			Direction.RIGHT: lambda x, y: (x + 1, y),
			Direction.DOWN: lambda x, y: (x, y + 1),
			Direction.DOWN_RIGHT: lambda x, y: (x + 1, y + 1),
			Direction.UP_RIGHT: lambda x, y: (x + 1, y - 1)
		}
		self.counter_directions = {
			Direction.RIGHT: lambda x, y: (x - 1, y),
			Direction.DOWN: lambda x, y: (x, y - 1),
			Direction.DOWN_RIGHT: lambda x, y: (x - 1, y - 1),
			Direction.UP_RIGHT: lambda x, y: (x - 1, y + 1)
		}

	# TODO: to be generalized to util (on the next phase)
	def connection_check(self, edge: Stone, log: List[Stone], num: int, dirs: List[str]):
		is_connected = False
		filtered_direction = {}
		for direction_name, direction in self.directions.items():
			if direction_name in dirs:
				filtered_direction[direction_name] = direction
		for _, direction in filtered_direction.items():
			connection_count = 1
			new_x, new_y = (edge.x, edge.y)
			while True:
				new_x, new_y = direction(int(new_x), int(new_y))
				new_stone = Stone(str(new_x), str(new_y), edge.color)
				if new_stone in log:
					connection_count += 1
				else:
					break
			if connection_count == num:
				is_connected = True
				break
		return is_connected

	def group_by_connected(self, log: List[Stone], color: str) -> Dict[int, List[Edge]]:
		groups = defaultdict(list)
		edges = defaultdict(list)
		for s in log:
			is_edge, directions = is_stone_edge(s, log)
			if s.color == color and is_edge:
				edges[(s.x, s.y, s.color)] = directions
		print(edges)
		# returns connected that are not closed
		for edge_, dirs in edges.items():
			edge = Stone(edge_[0], edge_[1], edge_[2])
			for num in list(range(6, 0, -1)):
				if self.connection_check(edge, log, num, dirs):
					groups[num].append(Edge(edge, dirs))
					break
		return groups

	def put_stone(self, log: List[Stone]) -> Stone:
		turn = turn_check(log, self.p, self.q)
		if turn == "w":
			opponent_color = "b"
		else:
			opponent_color = "w"
		mine = self.group_by_connected(log, turn)
		if len(mine) == 0:
			x = randint(1, self.n)
			y = randint(1, self.m)
			return Stone(str(x), str(y), turn)
		opponent = self.group_by_connected(log, opponent_color)
		opponent_keys = opponent.keys()
		if len(opponent_keys) == 0:
			s = self.optimal_stone(mine)
			s.color = turn
			return s
		opponent_max_key = max(opponent_keys)
		if opponent_max_key > 4:
			# mode defense
			s = self.optimal_stone(opponent)
		else:
			# mode offense
			s = self.optimal_stone(mine)
		s.color = turn
		return s

	def optimal_stone(self, possibles: Dict[int, List[Edge]]) -> Stone:
		sorted_keys = sorted(possibles.keys())
		for k in sorted_keys:
			corners = self.get_corners(k, possibles[k])
			if len(corners) > 0:
				return choice(corners)

	def get_corners(self, num: int, edges: List[Edge]) -> List[Stone]:
		corners = []
		for edge in edges:
			for direction in edge.directions:
				_x, _y = self.counter_directions[direction](int(edge.stone.x), int(edge.stone.y))
				corners.append(Stone(str(_x), str(_y), edge.stone.color))
				new_x, new_y = edge.stone.x, edge.stone.y
				for i in range(num):
					new_x, new_y = self.directions[direction](int(new_x), int(new_y))
				corners.append(Stone(str(new_x), str(new_y), edge.stone.color))
		return corners


if __name__ == "__main__":
	# TODO: test logs to be handled in a separated module (on the next phase)
	vertical_test_log = [
		Stone("3", "2", "b"),
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
		Stone("1", "8", "b"),
		Stone("5", "5", "w"),
		Stone("8", "4", "w"),
		Stone("7", "10", "b"),
		Stone("8", "10", "b"),
		Stone("9", "11", "w"),
		Stone("6", "7", "w"),
		Stone("4", "10", "b"),
		Stone("5", "10", "b"),
		Stone("7", "5", "w"),
	]

	config = BoardConfig(19, 19, 6, 2, 1)
	strategic_bot = StrategicBot(config)
	print("--Strategic bot")
	print("\t--x = 2, y = 6, color = w (vertical test): ", strategic_bot.put_stone(vertical_test_log))
	print("\t--x = 6, y = 6, color = w (diagonal test): ", strategic_bot.put_stone(diagonal_test_log))
