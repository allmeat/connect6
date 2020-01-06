import unittest

from strategic_bot import is_stone_edge, StrategicBot
from board import BoardConfig, Stone


class StrategicBotTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(StrategicBotTest, self).__init__(*args, **kwargs)
        self.test_config = BoardConfig(19, 19, 6, 2, 1)
        self.test_log = [
            Stone("3", "2", "b"),
            Stone("2", "1", "w"),
            Stone("2", "2", "w"),
            Stone("1", "2", "b"),
            Stone("1", "3", "b"),
        ]
        self.sb = StrategicBot(self.test_config)

    def test_is_edge(self):
        self.assertTrue(is_stone_edge(self.test_log[0], self.test_log))
        self.assertTrue(is_stone_edge(self.test_log[1], self.test_log))
        self.assertFalse(is_stone_edge(self.test_log[2], self.test_log))
        self.assertTrue(is_stone_edge(self.test_log[3], self.test_log))
        self.assertFalse(is_stone_edge(self.test_log[4], self.test_log))

    def test_connection_check(self):
        edges = [self.test_log[0], self.test_log[1], self.test_log[3]]
        self.assertTrue(self.sb.connection_check(edges[0], self.test_log, 1))
        self.assertTrue(self.sb.connection_check(edges[1], self.test_log, 2))
        self.assertTrue(self.sb.connection_check(edges[2], self.test_log, 2))

    def test_group_by_connected(self):
        result = self.sb.group_by_connected(self.test_log, "b")
        self.assertEqual(len(result[2]), 1)


if __name__ == '__main__':
    unittest.main()
