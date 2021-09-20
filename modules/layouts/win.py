import cocos
from modules.utiles import createLabel
from modules.env import ENV

class WinLayer(cocos.layer.Layer):
    is_event_handler = True
    def __init__(self, win: bool) -> None:
        super().__init__()
        if win:
            self.add(cocos.sprite.Sprite(ENV["assets_paths"]["win_wet_path"], (450, 550), scale=0.8))
            self.add(createLabel("HUMANS WIN", (450, 200), color=(79, 164, 184, 255), size=50))
            self.add(createLabel("An age of prosperity and unity begins", (450, 120), size=20))
            self.add(createLabel("to set in as the few strongholds of the warrior race start to fall.", (450, 90), size=20))
            self.add(createLabel("An age of exploration looms in the horizon.", (450, 60), size=20))
        else:
            self.add(cocos.sprite.Sprite(ENV["assets_paths"]["win_dry_path"], (450, 550), scale=0.8))
            self.add(createLabel("MARTIANS WIN", (450, 160), color=(230, 69, 57, 255), size=50))
            self.add(createLabel("As they consolidate their power on the galaxy", (450, 90), size=20))
            self.add(createLabel("humanity starts to wither away and the cosmos grows silent.", (450, 60), size=20))
        self.add(createLabel("Click on the screen to exit", (450, 25), color=(1, 152, 64, 255), size=18))
    
    def on_mouse_press (self, x, y, buttons, modifiers):
        exit()