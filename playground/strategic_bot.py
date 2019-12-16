from collections import defaultdict
from operator import itemgetter
from typing import List, Dict

from board import Stone, BoardConfig
from util import turn_check, Direction


# edge is left most or upper most stone in a connection
def is_edge(s: Stone, log: List[Stone]):
    is_present = [Stone(str(int(s.x) - 1), str(int(s.y) - 1), s.color),
                  Stone(s.x, str(int(s.y) - 1), s.color),
                  Stone(str(int(s.x) - 1), s.y, s.color)]
    edge = True
    for stone in log:
        for p in is_present:
            if stone == p:
                edge = False
                break
    return edge


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
        }

    # TODO: to be generalized to util (on the next phase)
    def connection_check(self, edge, log, num):
        is_connected = False
        for _, direction in self.directions.items():
            connection_count = 1
            new_x, new_y = direction(int(edge.x), int(edge.y))
            if Stone(str(new_x), str(new_y), edge.color) in log:
                connection_count += 1
            if connection_count == num:
                is_connected = True
                break
        return is_connected

    def group_by_connected(self, log: List[Stone], color: str) -> Dict[int, List[Stone]]:
        groups = defaultdict(List[Stone])
        filtered_log = [s for s in log if s.color == color and is_edge(s, log)]
        # returns connected that are not closed
        for edge in filtered_log:
            for num in list(range(6, 1, -1)):
                if self.connection_check(edge, log, num):
                    groups[num].append(edge)
                    break
        return groups

    def put_stone(self, log: List[Stone]) -> Stone:
        turn = turn_check(log, self.p, self.q)
        if turn == "W":
            opponent_color = "B"
        else:
            opponent_color = "W"
        mine = self.group_by_connected(log, turn)
        opponent = self.group_by_connected(log, opponent_color)
        opponent_max = max(opponent.items(), key=itemgetter[0])
        if opponent_max > 4:
            # mode defense
            s = self.optimal_stone(opponent)
        else:
            # mode offense
            s = self.optimal_stone(mine)
        s.color = turn
        return s

    @staticmethod
    def optimal_stone(possibles: Dict[int, List[Stone]]) -> Stone:
        maximum_possible = max(possibles.items(), key=itemgetter[0])
        if len(possibles[maximum_possible]) != 1:
            counts = defaultdict(int)
            for num in list(range(maximum_possible, 1, -1)):
                for pos in possibles[maximum_possible]:
                    if pos in possibles[num]:
                        counts[pos] += 1
                count_desc = sorted(counts.items(), key=itemgetter(1))
                if count_desc[0] != count_desc[1]:
                    return count_desc[0]
        return possibles[maximum_possible][0]


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
