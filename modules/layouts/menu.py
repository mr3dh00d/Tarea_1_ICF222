import cocos
import pyglet
from cocos.scenes import *
from modules.game import game
from modules.layouts import background
from modules.utiles import createLabel
from modules.env import ENV

class MenuLayer(cocos.layer.Layer):
    is_event_handler = True
    def __init__(self) -> None:
        super().__init__()
        self.canSelect = True
        self.options_area = []
        sprite = pyglet.image.ImageGrid(pyglet.image.load(ENV["assets_paths"]["dry_path_img"]), 1, 10)
        sprite = pyglet.image.Animation.from_image_sequence(sprite[0:], 0.4)
        sprite = cocos.sprite.Sprite(sprite, (100, 800), scale=1.5)
        self.add(sprite)
        sprite = pyglet.image.ImageGrid(pyglet.image.load(ENV["assets_paths"]["wet_path_img"]), 1, 10)
        sprite = pyglet.image.Animation.from_image_sequence(sprite[0:], 0.4)
        sprite = cocos.sprite.Sprite(sprite, (800, 100), scale=1.5)
        self.add(sprite)
        self.select = None
        self.view_select_sprite = False
        self.select_sprite = pyglet.image.ImageGrid(pyglet.image.load(ENV["assets_paths"]["default_path_img"]), 1, 10)
        self.select_sprite = pyglet.image.Animation.from_image_sequence(self.select_sprite[0:], 0.4)
        self.select_sprite = cocos.sprite.Sprite(self.select_sprite, (0, 0), scale=0.4)
        self.add(createLabel('Planets of the Galaxy', (450, 700), size=50))
        self.add(createLabel('Reversi Edition', (450, 650), size=28))
        self.add(createLabel("The martians want to conquer the galaxy", (450, 540), size=20))
        self.add(createLabel("but the human race wont allow it.", (450, 510), size=20))
        self.add(createLabel("Take the place of humanity and make sure", (450, 480), size=20))
        self.add(createLabel("to get more planets than them so they dont erradicate us.", (450, 450), size=20))
        self.label_difficulty = {
            'Easy': createLabel('Easy', (450, 360), color=(79, 164, 184, 255), size=40),
            'Hard': createLabel('Hard', (450, 300), color=(230, 69, 57, 255), size=40),
            'Exit': createLabel('Exit', (450, 240), color=(1, 152, 64, 255), size=40)
        }
        [self.add(label) for key, label in self.label_difficulty.items()]
        self.options_area = self.setOptionsArea()

    def setOptionsArea(self) -> "dict[tuple[tuple[int, int], tuple[int, int]]]":
        res = {}
        for key, label in self.label_difficulty.items():
            disx = int((len(label.element.text)*25)/2)
            point_1 = (label.position[0]-disx, label.position[1]-20)
            point_2 = (label.position[0]+disx, label.position[1]+20)
            res[label.element.text] = (point_1, point_2)
        return res
    
    def inOptionArea(self, position: "tuple[int, int]", option_area: "tuple[tuple[int, int], tuple[int, int]]") -> bool:
        x , y = position
        x1, x2 = option_area[0][0], option_area[1][0]
        y1, y2 = option_area[0][1], option_area[1][1]
        if x1 <= x <= x2:
            if y1 <= y <= y2:
                return True
        return False

    def on_mouse_motion (self, x, y, dx, dy) -> None:
        if self.canSelect:
            position = (int(x), int(y))
            inOp = False
            for key, option_area in self.options_area.items():
                if self.inOptionArea(position, option_area):
                    inOp = True
                    self.select = {key: self.label_difficulty[key]}
                    break
            if inOp and not self.view_select_sprite:
                self.view_select_sprite = True
                label = list(self.select.values())[0]
                option_position = label.position
                self.select_sprite.position = (option_position[0]-(int((len(label.element.text)*25)/2))-30, option_position[1])
                self.add(self.select_sprite)
            elif not inOp and self.view_select_sprite:
                self.view_select_sprite = None
                self.select = None
                self.remove(self.select_sprite)

    def on_mouse_press (self, x, y, buttons, modifiers):
        if self.canSelect and self.select:
            self.canSelect = False
            level = list(self.select.keys())[0]
            if level == "Easy":
                difficulty = 0
            elif level == "Hard":
                difficulty = 1
            else:
                exit()
            newScene = cocos.scene.Scene()
            newScene.add(background.BackgroundLayer())
            newScene.add(game.Game(difficulty))
            cocos.director.director.replace(FadeTRTransition(newScene, duration=1))
