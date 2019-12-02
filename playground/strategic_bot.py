from collections import defaultdict
from operator import itemgetter
from typing import List, Dict

from board import Stone
from referee import Referee


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
    def __init__(self, color):
        self.color = color
        self.referee = Referee()

    def group_by_connected(self, log: List[Stone], color: str) -> Dict[int, List[Stone]]:
        groups = defaultdict(List[Stone])
        filtered_log = [s for s in log if s.color == color and is_edge(s, log)]
        # returns connected that are not closed
        for edge in filtered_log:
            for num in list(range(6, 1, -1)):
                if self.referee.connection_check(edge, log, num):
                    groups[num].append(edge)
                    break
        return groups

    def get_scheme(self, log: List[Stone]) -> Stone:
        if self.color == "W":
            opponent_color = "B"
        else:
            opponent_color = "W"
        mine = self.group_by_connected(log, self.color)
        opponent = self.group_by_connected(log, opponent_color)
        opponent_max = max(opponent.items(), key=itemgetter[0])
        if opponent_max > 4:
            # mode defense
            s = self.right_stone(opponent)
        else:
            # mode offense
            s = self.right_stone(mine)
        s.color = self.color
        return s

    @staticmethod
    def right_stone(possibles: Dict[int, List[Stone]]) -> Stone:
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
