import unittest

from strategic_bot import is_stone_edge, StrategicBot
from board import BoardConfig, Stone


class StrategicBotTest(unittest.TestCase):
	def __init__(self, *args, **kwargs):
		super(StrategicBotTest, self).__init__(*args, **kwargs)
		self.test_config = BoardConfig(19, 19, 6, 2, 1)
		self.vertical_test_log = [
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
		self.diagonal_test_log = [
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
		self.test_log = [
			Stone("3", "2", "b"),
			Stone("2", "1", "w"),
			Stone("2", "2", "w"),
			Stone("1", "2", "b"),
			Stone("1", "3", "b"),
		]
		self.sb = StrategicBot(self.test_config)

	def test_is_edge(self):
		self.assertTrue(is_stone_edge(self.vertical_test_log[0], self.vertical_test_log))
		self.assertTrue(is_stone_edge(self.vertical_test_log[1], self.vertical_test_log))
		self.assertFalse(is_stone_edge(self.vertical_test_log[2], self.vertical_test_log))
		self.assertTrue(is_stone_edge(self.vertical_test_log[3], self.vertical_test_log))
		self.assertFalse(is_stone_edge(self.vertical_test_log[4], self.vertical_test_log))

		self.assertTrue(is_stone_edge(self.diagonal_test_log[0], self.diagonal_test_log))
		self.assertTrue(is_stone_edge(self.diagonal_test_log[1], self.diagonal_test_log))
		self.assertFalse(is_stone_edge(self.diagonal_test_log[2], self.diagonal_test_log))
		self.assertFalse(is_stone_edge(self.diagonal_test_log[3], self.diagonal_test_log))
		self.assertFalse(is_stone_edge(self.diagonal_test_log[4], self.diagonal_test_log))

		self.assertTrue(is_stone_edge(self.diagonal_test_log[15], self.diagonal_test_log))

	def test_connection_check(self):
		vert_edges = [self.vertical_test_log[0], self.vertical_test_log[1], self.vertical_test_log[3]]
		self.assertTrue(self.sb.connection_check(vert_edges[0], self.vertical_test_log, 1))
		self.assertTrue(self.sb.connection_check(vert_edges[1], self.vertical_test_log, 5))
		self.assertTrue(self.sb.connection_check(vert_edges[2], self.vertical_test_log, 4))

		diag_edges = [self.diagonal_test_log[0], self.diagonal_test_log[1], self.diagonal_test_log[3]]
		self.assertTrue(self.sb.connection_check(diag_edges[0], self.diagonal_test_log, 4))
		self.assertTrue(self.sb.connection_check(diag_edges[1], self.diagonal_test_log, 5))

	def test_group_by_connected(self):
		result = self.sb.group_by_connected(self.test_log, "b")
		self.assertEqual(len(result[2]), 1)


if __name__ == '__main__':
	unittest.main()
