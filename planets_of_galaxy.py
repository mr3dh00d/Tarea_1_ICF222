import cocos
import modules.background as background

if __name__ == "__main__":
    cocos.director.director.init(width=900, height=900, caption="Reversi")
    scene = cocos.scene.Scene()
    bkg = background.BackgroundLayer()
    scene.add(bkg)
    cocos.director.director.run(scene)
