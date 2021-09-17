import modules.possibility as possibility
from random import randint

def minimax(possibilities: "list[possibility.Possibility]") -> possibility.Possibility:
    try:
        return possibilities[randint(0,len(possibilities)-1)]
    except Exception:
        print(len(possibilities))