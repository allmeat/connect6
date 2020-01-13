from collections import defaultdict
from dataclasses import dataclass
from random import randint, choice
from typing import List, Dict

from board import Stone, BoardConfig
from util import turn_check, Direction


@dataclass
class Edge:
	stone: Stone
	directions: List[str]


class StrategicBot:
	def __init__(self, board_config: BoardConfig):
		self.k = board_config.connect
		self.m = board_config.row
		self.n = board_config.column
		self.p = board_config.each_move
		self.q = board_config.first_move

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

		self.opponent_color = ""
		self.my_color = ""

	# edge is left most or upper most stone in a connection size greater than 1: left has priority
	def is_stone_edge(self, stone: Stone, log: List[Stone]) -> (bool, List[str]):
		default_directions = [Direction.RIGHT, Direction.DOWN, Direction.DOWN_RIGHT, Direction.UP_RIGHT]
		directions = []
		for dd in default_directions:
			counter_f = self.counter_directions[dd]
			m_x, m_y = counter_f(int(stone.x), int(stone.y))
			m_stone = Stone(str(m_x), str(m_y), stone.color)
			if m_stone in log:
				break
			f = self.directions[dd]
			m_x, m_y = f(int(stone.x), int(stone.y))
			m_stone = Stone(str(m_x), str(m_y), stone.color)
			if m_stone in log:
				directions.append(dd)
		if len(directions) > 0:
			is_edge = True
		else:
			is_edge = False
		return is_edge, directions

	# TODO: to be generalized to util (on the next phase)
	def check_connection(self, edge: Edge, log: List[Stone], num: int) -> bool:
		is_connected = False
		filtered_direction = {}
		for direction_name, direction in self.directions.items():
			if direction_name in edge.directions:
				filtered_direction[direction_name] = direction
		for _, direction in filtered_direction.items():
			connection_count = 1
			new_x, new_y = (edge.stone.x, edge.stone.y)
			while True:
				new_x, new_y = direction(int(new_x), int(new_y))
				new_stone = Stone(str(new_x), str(new_y), edge.stone.color)
				if new_stone in log:
					connection_count += 1
				else:
					break
			if connection_count == num:
				return True
		return is_connected

	def group_by_connected(self, log: List[Stone], color: str) -> Dict[int, List[Edge]]:
		groups = defaultdict(list)
		edges = defaultdict(list)
		for s in log:
			is_edge, directions = self.is_stone_edge(s, log)
			if s.color == color and is_edge:
				edges[(s.x, s.y, s.color)] = directions
		# returns connected that are not closed
		for edge_, dirs in edges.items():
			edge = Edge(Stone(edge_[0], edge_[1], edge_[2]), dirs)
			for num in list(range(6, 1, -1)):
				if self.check_connection(edge, log, num):
					groups[num].append(edge)
					break
		return groups

	def put_stone(self, log: List[Stone]) -> Stone:
		self.my_color = turn_check(log, self.p, self.q)
		if self.my_color == "w":
			self.opponent_color = "b"
		else:
			self.opponent_color = "w"
		mine = self.group_by_connected(log, self.opponent_color)
		if len(mine) == 0:
			return self.random_stone(log)
		opponent = self.group_by_connected(log, self.opponent_color)
		opponent_keys = opponent.keys()
		if len(opponent_keys) == 0:
			s = self.optimal_stone(mine, log)
			s.color = self.my_color
			return s
		opponent_max_key = max(opponent_keys)
		if opponent_max_key >= 3:
			# mode defense
			s = self.optimal_stone(opponent, log)
		else:
			# mode offense
			s = self.optimal_stone(mine, log)
		s.color = self.my_color
		return s

	def filter_valid(self, corners: List[Stone], log: List[Stone]) -> List[Stone]:
		final_result = []
		for corner in corners:
			if self.is_valid(corner, log):
				final_result.append(corner)
		return final_result

	def is_valid(self, stone: Stone, log: List[Stone]) -> bool:
		if int(stone.x) < 0 or int(stone.x) > self.m or int(stone.y) < 0 or int(stone.y) > self.n:
			return False
		for l in log:
			if stone.x == l.x and stone.y == l.y:
				return False
		return True

	def optimal_stone(self, possibles: Dict[int, List[Edge]], log: List[Stone]) -> Stone:
		possible_key = list(possibles.keys())
		possible_key.sort(reverse=True)
		for k in possible_key:
			candidates = self.get_corners(k, possibles[k])
			corners = self.filter_valid(candidates, log)
			if len(corners) > 0:
				c = choice(corners)
				return c
		return self.random_stone(log)

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

	def random_stone(self, log: List[Stone]) -> Stone:
		valid = False
		s = Stone
		while not valid:
			x = randint(1, self.n)
			y = randint(1, self.m)
			s = Stone(str(x), str(y), self.my_color)
			valid = self.is_valid(s, log)
		return s


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
