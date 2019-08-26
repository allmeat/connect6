import logging
from game.common import Point, repr_direction

DIRECTIONS = [
	lambda x, y: (x + 1, y),
	lambda x, y: (x + 1, y + 1),
	lambda x, y: (x + 1, y - 1),
	lambda x, y: (x - 1, y),
	lambda x, y: (x - 1, y + 1),
	lambda x, y: (x - 1, y - 1),
	lambda x, y: (x, y - 1),
	lambda x, y: (x, y + 1),
]


# returns true if valid
def validate_coordinates(x, y):
	return 0 <= x < 19 and 0 <= y < 19


def reverse_of(dir_func):
	dx, dy = dir_func(0, 0)  # differentiate
	return lambda x, y: (x-dx, y-dy)


class Judge:
	def __init__(self, initial_board):
		self.board = initial_board
		self.last_move = (0, 0)

	def update(self, x, y, player):
		self.board[x][y] = player
		self.last_move = (x, y)

	def determine(self):
		board = self.board
		x, y = self.last_move

		# check 4 directions and start backtracking.
		for dir_func in DIRECTIONS:
			new_x, new_y = dir_func(x, y)
			if not validate_coordinates(new_x, new_y):
				continue

			if board[new_x][new_y] == board[x][y]:
				logging.DEBUG('Direction : ' + repr_direction(dir_func))
				logging.DEBUG('Start at {}'.format(Point(x, y)))

				# to check properly, go to the end of direction
				while board[new_x][new_y] == board[x][y]:
					new_x, new_y = dir_func(new_x, new_y)
					if not validate_coordinates(new_x, new_y):
						break

				reverse_dir_func = reverse_of(dir_func)
				new_x, new_y = reverse_dir_func(new_x, new_y)  # one step back.

				logging.DEBUG('End of direction : {}'.format(Point(new_x, new_y)))

				is_end = self._track(new_x, new_y, reverse_dir_func)
				if is_end:
					# return the winner
					return board[new_x][new_y]

	def _track(self, start_x, start_y, dir_func):
		x, y = start_x, start_y
		original_player = self.board[x][y]
		logging.DEBUG('Track started at {}'.format(Point(x, y)))

		step = 1
		while True:
			x, y = dir_func(x, y)
			if not validate_coordinates(x, y) or self.board[x][y] != original_player:
				if step == 6:
					return True
				logging.DEBUG('Track finished at step {}'.format(step))
				return False
			step += 1

	def can_place(self, x, y):
		if self.board[x][y] != 0:
			return False, 'Duplicated move'
		if not validate_coordinates(x, y):
			return False, 'Not a valid position. Choose between 0 and 19'
		return True, 'Ok'
