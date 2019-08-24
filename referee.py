from typing import List
from board import Stone

# 착수 요청된 돌이 유효한지, 중복된 위치는 아닌지 체크함
# 유효한 착수일 때, 6목 성사 여부 확인함 (가로, 세로, 대각선)


class Referee:

    @staticmethod
    def valid_check(new_stone: Stone, log: List[Stone]) -> bool:
        coordinate = [[stone.x, stone.y] for stone in log]
        return [new_stone.x, new_stone.y] not in coordinate


if __name__ == "__main__":
    referee = Referee()
    print(referee.valid_check(Stone("1", "1", "w"), [Stone("1", "3", "b"), Stone("2", "1", "w")]))
