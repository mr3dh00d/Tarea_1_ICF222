import cocos
from modules.board import board, tile

def copyBoard(original: board.Board) -> board.Board:
    board_result = board.Board(create_sprites=False)
    for i in range(len(original.tiles)):
        board_result.tiles.append([])
        for j in range(len(original.tiles[0])):
            tl = tile.Tile()
            tl.value = original.getTile((i,j)).value
            board_result.tiles[i].append(tl)
    return board_result

def printBoard(brd: board.Board):
    for i in range(len(brd.tiles)):
        for j in range(len(brd.tiles[0])):
            print(brd.getTile((i,j)).value, end=" ")
        print()
            

def inPlanet(planet_center: "tuple [int, int]", position: "tuple [int, int]") -> bool:
    rectangle = [(planet_center[0]-32, planet_center[1]-32), (planet_center[0]+32, planet_center[1]+32)]
    if(rectangle[0][0] <= position[0] <= rectangle[1][0]):
        if(rectangle[0][1] <= position[1] <= rectangle[1][1]):
            return True
    return False

def reverse(value: str) -> str:
    if value == "x":
        return "o"
    elif value == "o":
        return "x"

def createLabel(text: str, position: "tuple[int, int]", color=(255, 255, 255, 255), size=32) -> cocos.text.Label:
        return cocos.text.Label(text,
        font_name = 'DPComic',
        font_size = size,
        position = position,
        color = color,
        anchor_x = 'center', anchor_y = 'center')