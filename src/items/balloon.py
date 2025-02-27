from items.item import Item
from settings import *




class Balloon(Item):

    def __init__(self, game, scene, groups, pos=None, surf=None, z='foreground', tile = None):
        image_path = 'assets/tiles/items/balloon.png'
        description = 'its a balloon!'
        name = self.__class__.__name__.lower()
        if surf == None:
            surf = pygame.image.load(image_path)
        if pos == None and hasattr(scene, 'player'):
            pos = (scene.player.hitbox.centerx - surf.width/2, scene.player.hitbox.top - surf.height)
        elif pos == None:
            pos = (0,0)
        super().__init__(game, scene, groups, pos, surf, z, tile, name, image_path, description)

    def update(self, dt):
        player = self.scene.player
        if self.equipped == False:
            super().update(dt)
            return
        self.hitbox.bottom = player.hitbox.top
        self.hitbox.centerx = player.hitbox.centerx
        self.rect.center = self.hitbox.center
        if player.on_ground == False and player.state.__class__.__name__.lower() != 'climbing':
            player.y_forces.append(-1*player.mass*GRAVITY/3)
        