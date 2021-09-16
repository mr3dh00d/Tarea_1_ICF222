class Possibility:
    def __init__(self):
        self.point = ()
        self.objetives = []
    
    def getTilesToChange(self):
        res = []
        for objetive in self.objetives:
            x, y = objetive
            x = self.point[0] - x
            y = self.point[1] - y
            i, j = 0, 0
            while True:
                if i == x and j == y:
                    break
                p = (objetive[0]+i, objetive[1]+j)
                if p not in res:
                    if objetive != p:
                        res.append(p)
                i += 1 * (0 if x == 0 else (1 if x > 0 else -1))
                j += 1 * (0 if y == 0 else (1 if y > 0 else -1))
        res.append(self.point)
        return res