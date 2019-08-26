from game.rules import Judge
from game.common import Coord


PLAYER = ['W', 'B']


def show_board(coord_in_board, player=0, nth_move=0):
	stone_color = PLAYER[player]
	print('{} turn.'.format(stone_color))
	print('- number of move : {}'.format(nth_move))
	print()
	print('\t', ' '.join('  {:>2d} |'.format(t+1) for t in range(19)))
	print('\t', '-'*(len(' '.join('  {:>2d} |'.format(t+1) for t in range(19)))))

	for y in range(19):
		print('  {:>2d} |'.format(y+1), end='')  # line no.
		for x in range(19):
			if coord_in_board.x_axis != 0 and coord_in_board.y_axis != 0:
				print(' ' + stone_color, end='')
			else:
				print(' *', end='')
		print(' |')

	print('     +---------------------------------------+')


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


def main(bots):
	# to align index with player variable.
	bot_set = [None] + bots

	board = Coord
	judge = Judge(board)

	nth_move = 1
	player = 2  # 1=white 2=black. black moves first
	player_moved_count = 1  # at first time, black can only move once.

	while True:
		draw_board(board, player, nth_move)

		# input loop.
		while True:
			try:
				x, y = bot_set[player].move(board, nth_move)
				able_to_place, msg = judge.can_place(x, y)
				if not able_to_place:
					print('{}. Try again in another place.'.format(msg))
					continue
				break

			except KeyboardInterrupt:
				print('\n' + 'Bye...')
				finish_game(logger)
				return

			except Exception as e:
				raise e
				print('Wrong input.')
				continue

		# place stone
		board.x_axis = player
		board.y_axis = player
		judge.update(x, y, player)

		won_player = judge.determine()
		if won_player is not None:
			finish_game(logger, bot_set[won_player])
			return

		player_moved_count += 1
		if player_moved_count == 2:
			# Change turn : a player can move 2 times per turn.
			nth_move += 1
			player_moved_count = 0
			player = 2 if player == 1 else 1


if __name__ == '__main__':
	human = input('Select the stone color. Black goes first. (B=Black W=White)')
	while valid_user_input(human):
		human = input('Select the stone color. Black goes first. (B=Black W=White)')

	human = human.upper()
	if human.upper() == 'B':
		bot = 'W'
	else:
		bot = 'B'
	main()
