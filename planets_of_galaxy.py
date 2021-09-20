import cocos
from modules.layouts import background, menu

if __name__ == "__main__":
    cocos.director.director.init(width=900, height=900, caption="Planets of the Galaxy")
    scene = cocos.scene.Scene()
    bkg = background.BackgroundLayer()
    mn = menu.MenuLayer()
    scene.add(bkg)
    scene.add(mn)
    cocos.director.director.run(scene)