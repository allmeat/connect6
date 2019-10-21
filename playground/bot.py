from typing import List, Tuple, Dict
from random import randint, random
from board import Stone


class Bot:

    def __init__(self, color: str):
        self.color = color

    def random_bot(self) -> Stone:
        x = randint(1, 19)
        y = randint(1, 19)
        return Stone(str(x), str(y), self.color)

    @staticmethod
    def limit_focus(stone: Stone, k: int = 6) -> List[List[Tuple[int, int]]]:
        x = int(stone.x)
        y = int(stone.y)
        focus_horizontal = [(focus_x, y) for focus_x in range(x - k + 1, x + k)]
        focus_vertical = [(x, focus_y) for focus_y in range(y - k + 1, y + k)]
        focus_positive_diagonal = []
        focus_negative_diagonal = []
        for d in range(-k + 1, k):
            focus_positive_diagonal.append((x + d, y + d))
            focus_negative_diagonal.append((x + d, y - d))
        return [focus_horizontal, focus_vertical, focus_positive_diagonal, focus_negative_diagonal]

    @staticmethod
    def list_to_dict(log: List[Stone]) -> Dict[Tuple[int, int], str]:
        stone_dict = {}
        for item in log:
            stone_dict[(int(item.x), int(item.y))] = item.color
        return stone_dict

    def basic_bot(self, log: List[Stone]) -> Stone:
        turn = "b" if (len(log) + 1) % 4 in [0, 1] else "w"
        if len(log) == 0:
            result = Stone(str(10), str(10), turn)
        elif len(log) == 1:
            next_x = int(log[0].x) + (1 if random() > 0.5 else -1)
            next_y = int(log[0].y) + (1 if random() > 0.5 else -1)
            result = Stone(str(next_x), str(next_y), turn)
        else:
            log_dict = self.list_to_dict(log)
            focus_latest = self.limit_focus(log[-1])
            for candidates in focus_latest:
                stone_color = []
                for candidate in candidates:
                    stone_color.append(log_dict.get(candidate, ""))
                print(stone_color)


            result = Stone(str(10), str(10), self.color)
            # latest_x = int(log[-1].x)
            # latest_y = int(log[-1].y)
            # focus_horizental = [(focus_x, latest_y) for focus_x in range(latest_x - 5, latest_x + 6)]
            # focus_vertical = [(latest_x, focus_y) for focus_y in range(latest_y - 5, latest_x + 6)]
            # focus_p_diagonal = [(latest_x, focus_y) for focus_y in range(latest_y - 5, latest_x + 6)]

        return result


if __name__ == "__main__":
    test_log = [
        Stone("1", "1", "b"),
        Stone("2", "1", "w"),
        Stone("2", "2", "w"),
        Stone("1", "2", "b"),
        Stone("1", "3", "b"),
        Stone("2", "3", "w"),
        Stone("2", "4", "w"),
        Stone("1", "4", "b"),
        Stone("1", "5", "b"),
        Stone("2", "5", "w"),
        # Stone("2", "8", "w"),
        # Stone("1", "10", "b"),
        # Stone("1", "11", "b"),
        # Stone("2", "9", "w"),
        # Stone("2", "6", "w"),
    ]
    bot = Bot("w")
    print("--random bot")
    print("\t--white random stone: ", bot.random_bot())
    print("\t--basic bot: ", bot.basic_bot(test_log))
