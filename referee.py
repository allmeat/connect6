from typing import List
from board import Stone

# 착수 요청된 돌이 유효한지, 중복된 위치는 아닌지 체크함
# 유효한 착수일 때, 6목 성사 여부 확인함 (가로, 세로, 대각선)


class Referee:

    @staticmethod
    def valid_check(new_stone: Stone, log: List[Stone]) -> bool:
        x_valid_range = (int(new_stone.x) > 0) & (int(new_stone.x) < 20)
        y_valid_range = (int(new_stone.y) > 0) & (int(new_stone.y) < 20)
        coordinate = [[stone.x, stone.y] for stone in log]
        empty_seat = [new_stone.x, new_stone.y] not in coordinate
        return x_valid_range & y_valid_range & empty_seat

    @staticmethod
    def turn_check(log: List[Stone]) -> str:
        if (len(log) + 1) % 4 in [0, 1]:
            return "b"
        else:
            return "w"

    @staticmethod
    def end_check(log: List[Stone]) -> str:
        log_dict = {}
        for item in log:
            log_dict[item.color] = [item.x, item.y]

        # "keep play"
        # "black wins"
        # "white wins"
        if len(log) >= 4:
            return "abc"
        else:
            return "keep play"


if __name__ == "__main__":
    referee = Referee()
    log = [
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
        Stone("2", "6", "w"),
        Stone("1", "6", "b"),
        Stone("1", "7", "b"),
    ]
    print("--valid_check")
    print("\t--valid stone: ", referee.valid_check(Stone("10", "10", "b"), log))
    print("\t--invalid stone:", referee.valid_check(Stone("1", "1", "w"), log))
    print("--turn_check")
    print("\t--black turn: ", referee.turn_check(log[:-1]))
    print("\t--white turn: ", referee.turn_check(log))
    print("--end_check")
    print("\t--keep play: ", referee.end_check(log[:-1]))
    print("\t--black wins: ", referee.end_check(log))
