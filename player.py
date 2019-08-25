from board import Stone


class Player:

    def __init__(self, color):
        self.color = color

    def manual_input(self) -> Stone:
        x = input("x: ")
        y = input("y: ")
        return Stone(x, y, self.color)


if __name__ == "__main__":
    player = Player("w")
    print("--manual input")
    print("\t--white manual stone: ", player.manual_input())
