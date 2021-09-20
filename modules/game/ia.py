import copy
from modules.game import possibility
from modules.board import board
from modules.utiles import reverse, copyBoard
from math import inf
from modules.env import ENV

N = ENV["number_of_tiles"]

class IA:
    def __init__(self, difficulty: int) -> None:
        self.difficulty = difficulty
        pass

    def bestMove(self, brd: board.Board) -> possibility.Possibility:
        possibilities = brd.availables()
        bestScore = -inf
        move = None
        for possibility in possibilities:
            copy_board = copyBoard(brd)
            for tile in possibility.getTilesToChange():
                copy_board.setTile(tile, "x")
            score = self.minimax(copy_board, 0, False)
            if score > bestScore:
                bestScore = score
                move = possibility
        return move
    
    def minimax(self, brd: board.Board, depth: int, isMaximizing: bool) -> int:
        result = self.checkWinner(brd)
        if result != False or depth == (2 if self.difficulty else 0):
            brd.updateScore()
            return len(brd.red)
        if isMaximizing:
            self.checkAvailablesFor(brd, "x")
            bestScore = -inf
            possibilities = brd.availables().copy()
            if len(possibilities) > 0:
                for possibility in possibilities:
                    copy_board = copyBoard(brd)
                    for tile in possibility.getTilesToChange():
                        copy_board.setTile(tile, "x")
                    score = self.minimax(copy_board, depth+1, False)
                    if self.difficulty:
                        if possibility.point in [(0,0), (0,5), (5,0), (5,5)]:
                            score += 20
                        if possibility.point in [(1,1), (4,4), (1,4), (4,1)]:
                            score -= 3
                        if possibility.point in [(0,1), (1,0), (4,0), (5,1), (0,4), (1,5), (4,5), (5,4)]:
                            score -= 1
                        if possibility.point in [(2,0), (0,2), (3,0), (5,2), (0,3), (2,5), (3,5), (5,3)]:
                            score += 4
                    bestScore = max(bestScore, score)
                return bestScore
            else:
                brd.updateScore()
                return len(brd.red)
        else:
            self.checkAvailablesFor(brd, "o")
            bestScore = inf
            possibilities = brd.availables().copy()
            if len(possibilities) > 0:
                for possibility in possibilities:
                    copy_board = copyBoard(brd)
                    for tile in possibility.getTilesToChange():
                        copy_board.setTile(tile, "o")
                    score = self.minimax(copy_board, depth+1, True)
                    if self.difficulty:
                        if possibility.point in [(0,0), (0,5), (5,0), (5,5)]:
                            score -= 20
                        if possibility.point in [(1,1), (4,4), (1,4), (4,1)]:
                            score += 3
                        if possibility.point in [(0,1), (1,0), (4,0), (5,1), (0,4), (1,5), (4,5), (5,4)]:
                            score += 1
                        if possibility.point in [(2,0), (0,2), (3,0), (5,2), (0,3), (2,5), (3,5), (5,3)]:
                            score -= 4
                    bestScore = min(bestScore, score)
                return bestScore
            else:
                brd.updateScore()
                return len(brd.red)

    def checkWinner(self, brd: board.Board):
        if not self.checkAvailablesFor(brd, "x") and not self.checkAvailablesFor(brd, "o"):
            return 1 if len(brd.blue) > len(brd.red) else -1 if len(brd.red) > len(brd.blue) else 0
        return False
        


    def checkAvailablesFor(self, brd: board.Board, objetives: str) -> bool:
        brd.availables([])
        if objetives == "x":
            objetives = brd.red
        elif objetives == "o":
            objetives = brd.blue
        for objetive in objetives:
            self.checkAdjacency(brd, objetive)
        if len(brd.availables()) > 0:
            return True
        else:
            return False

    def checkAdjacency(self, brd: board.Board, point: "tuple[int, int]") -> None:
        x, y = point
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if (N > i >= 0 and N > j >= 0) and (i != x or j != y):
                    val = brd.getTile((i, j)).value
                    if(val == reverse(brd.getTile(point).value)):
                        available = self.checkPossibility(brd, point, (i-x, j-y))
                        if available:
                            if available not in [a.point for a in brd.availables()]:
                                pos = possibility.Possibility()
                                pos.point = available
                                pos.objetives.append(point)
                                ava = brd.availables()
                                ava.append(pos)
                                brd.availables(ava)
                            else:
                                for ava in brd.availables():
                                    if ava.point == available:
                                        ava.objetives.append(point)

    def checkPossibility(self, brd: board.Board, point: "tuple[int, int]", direction: "tuple[int, int]") -> bool:
        x, y = point
        dirx, diry = direction
        count = 1
        posibility = False
        obj = reverse(brd.getTile(point).value)
        while True:
            i, j = x+(dirx*count), y+(diry*count)
            if 0 > i or i > N-1 or 0 > j or j > N-1:
                posibility = False
                break
            cursor = brd.getTile((i, j)).value
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