import unittest

from strategic_bot import *


class MyTest(unittest.TestCase):

    def test_is_edge(self):
        test_log = [
            Stone("3", "2", "b"),
            Stone("2", "1", "w"),
            Stone("2", "2", "w"),
            Stone("1", "2", "b"),
            Stone("1", "3", "b"),
        ]
        self.assertTrue(is_edge(test_log[0], test_log))
        self.assertTrue(is_edge(test_log[1], test_log))
        self.assertFalse(is_edge(test_log[2], test_log))
        self.assertTrue(is_edge(test_log[3], test_log))
        self.assertFalse(is_edge(test_log[4], test_log))

    def test_connection_check(self):
        test_config = BoardConfig(19, 19, 6, 2, 1)
        sb = StrategicBot(test_config)
        test_log = [
            Stone("3", "2", "b"),
            Stone("2", "1", "w"),
            Stone("2", "2", "w"),
            Stone("1", "2", "b"),
            Stone("1", "3", "b"),
        ]
        edges = [test_log[0], test_log[1], test_log[3]]
        self.assertTrue(sb.connection_check(edges[0], test_log, 1))
        self.assertTrue(sb.connection_check(edges[1], test_log, 2))
        self.assertTrue(sb.connection_check(edges[2], test_log, 2))


if __name__ == '__main__':
    unittest.main()
