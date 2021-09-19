import modules.casilla as casilla
import modules.possibility as possibility
from random import randint
from planets_of_galaxy import N

class Board:
    def __init__(self, add):
        self.casillas =  []
        self.__availables = []
        self.red = []
        self.blue = []
        position = (190, 100)
        r = randint(0,1)
        for i in range(N):
            self.casillas.append([])
            for j in range(N):
                pos = (i, j)
                self.casillas[i].append(casilla.Casilla((position[0] + (104*i), position[1] + (104*j))))
                if(pos == (2+r, 2) or pos== (3-r, 3)):
                    self.getCasilla(pos).setDry()
                    self.red.append(pos)
                elif(pos== (3-r, 2) or pos == (2+r, 3)):
                    self.getCasilla(pos).setWet()
                    self.blue.append(pos)
                add(self.getCasilla(pos).sprite)

    def getCasilla(self, position: "tuple[int, int]", set=False) -> casilla.Casilla:
        i, j = position
        if type(set) == casilla.Casilla:
            self.casillas[i][j] = set
        return self.casillas[i][j]

    def updateScore(self):
        self.blue = []
        self.red = []
        for x in range(N):
            for y in range(N):
                position = (x, y)
                if self.getCasilla(position).value == "x":
                    self.red.append((x,y))
                if self.getCasilla(position).value == "o":
                    self.blue.append((x,y))

    def availables(self, set=False) -> "list[possibility.Possibility]":
        if type(set) == list:
            self.__availables = set
        return self.__availables