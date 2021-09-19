# import copy
import modules.possibility as possibility
import modules.board as board
from modules.utiles import reverse
from random import randint
from planets_of_galaxy import N

class IA:
    def __init__(self):
        pass

    def minimax(self, possibilities: "list[possibility.Possibility]") -> possibility.Possibility:
        return possibilities[randint(0,len(possibilities)-1)]

    def checkAvailablesFor(self, board: board.Board, objetives: str) -> bool:
        board.availables([])
        if objetives == "x":
            objetives = board.red
        elif objetives == "o":
            objetives = board.blue
        for objetive in objetives:
            self.checkAdjacency(board, objetive)
        if len(board.availables()) > 0:
            return True
        else:
            return False

    def checkAdjacency(self, board: board.Board, point: "tuple[int, int]") -> None:
        x, y = point
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if (N > i >= 0 and N > j >= 0) and (i != x or j != y):
                    val = board.getCasilla((i, j)).value
                    # print("del punto:", point, board.getCasilla(point).value, "reviso casilla:", (i, j), "su valor es:", val, end=" ")
                    if(val == reverse(board.getCasilla(point).value)):
                        # print("revisare su posiblidad...", end=" ")
                        available = self.checkPossibility(board, point, (i-x, j-y))
                        if available:
                            # print("es posible en el punto", available, end=" ")
                            if available not in [a.point for a in board.availables()]:
                                pos = possibility.Possibility()
                                pos.point = available
                                pos.objetives.append(point)
                                ava = board.availables()
                                ava.append(pos)
                                board.availables(ava)
                            else:
                                for ava in board.availables():
                                    if ava.point == available:
                                        ava.objetives.append(point)

                    #     else: 
                    #         print("no es posible", end=" ")
                    # print()

    def checkPossibility(self, board: board.Board, point: "tuple[int, int]", direction: "tuple[int, int]"):
        x, y = point
        dirx, diry = direction
        count = 1
        posibility = False
        obj = reverse(board.getCasilla(point).value)
        while True:
            i, j = x+(dirx*count), y+(diry*count)
            if 0 > i or i > N-1 or 0 > j or j > N-1:
                posibility = False
                break
            cursor = board.getCasilla((i, j)).value
            if cursor == obj:
                posibility = True
                count += 1
                continue
            if posibility and cursor == "-":
                posibility = (i, j)
                break
            else:
                posibility = False
                break
        return posibility