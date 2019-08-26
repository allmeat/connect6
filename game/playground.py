from game.rules import Judge
from game.random_bot import find_empty_spot
PLAYER = ['W', 'B']


def show_board(coord_in_board, player=0, nth_move=0):
	stone_color = PLAYER[player]
	print('{} turn.'.format(stone_color))
	print('- number of move : {}'.format(nth_move))
	print()
	print('\t', '|'.join('{:>2d}'.format(t+1) for t in range(19)))
	print('\t', '-'*(len('|'.join('{:>2d}'.format(t+1) for t in range(19)))))

	for y in range(19):
		print(' {:>2d} |'.format(y+1), end='')  # line no.
		for x in range(19):
			if coord_in_board[x][y] != 0:
				print(' ' + stone_color, end='')
			else:
				print(' * ', end='')
		print('|')

	print('\t', '-'*(len('|'.join('{:>2d}'.format(t+1) for t in range(19)))))


def finish_game(won_bot=None):
	if won_bot is not None:
		print('{} won.'.format(PLAYER[won_bot]))
	else:
		print('No one won.')


def valid_user_input(inp):
	try:
		val = str(inp)
		idx = ['B', 'W'].index(val.upper())
		print("You have chosen: ", val)
	except ValueError:
		print("Please select a valid stone color")
		print("B or W (B=Black W=White)")


def manual_input(coord_info):
	x_input = input('input x coordinate')
	y_input = input('input y coordinate')
	return x_input, y_input


def get_inputs(coord_info, is_bot=True):
	if is_bot:
		return find_empty_spot(coord_info)
	else:
		return manual_input(coord_info)


def main(human_color):

	if human_color == 'B':
		bot = 'W'
	else:
		bot = 'B'

	board = [[0 for x in range(19)] for y in range(19)]
	judge = Judge(board)
	nth_move = 1
	player = PLAYER.index(human_color)
	player_moved_count = 1  # at first time, black can only move once.
	while True:
		show_board(board, player, nth_move)

		# input loop.
		while True:
			try:
				x, y = get_inputs(board,)
				able_to_place, msg = judge.can_place(x, y)
				if not able_to_place:
					print('{}. Try again in another place.'.format(msg))
					continue
				break

			except KeyboardInterrupt:
				print('\n' + 'Game Over')
				finish_game(logger)
				return

			except Exception as e:
				raise e
				print('Wrong input.')
				continue

		# place stone
		board[x][y] = player
		judge.update(x, y, player)

		won_player = judge.determine()
		if won_player is not None:
			finish_game(logger, )
			return

		player_moved_count += 1
		if player_moved_count == 2:
			# Change turn : a player can move 2 times per turn.
			nth_move += 1
			player_moved_count = 0
			player = 1 if player == 0 else 0


if __name__ == '__main__':
	human = input('Select the stone color. Black goes first. (B=Black W=White)')
	while valid_user_input(human):
		human = input('Select the stone color. Black goes first. (B=Black W=White)')

	human = human.upper()

	main(human)
