from items.item import Item

import pygame



class Sunglasses(Item):
    
    def __init__(self, game, scene, groups, pos=None, surf=None, z='foreground', tile=None):
        image_path = 'assets/tiles/items/sunglasses_right.png'
        image_path_left = 'assets/tiles/items/sunglasses_left.png'
        description = 'wow these are very cool'
        name = self.__class__.__name__.lower()
        if surf == None:
            surf = [pygame.image.load(image_path), pygame.image.load(image_path_left)]
        if pos == None and hasattr(scene, 'player'):
            pos = (scene.player.hitbox.centerx - surf[0].width/2, scene.player.hitbox.bottom - surf[0].height)
        elif pos == None:
            pos = (0,0)
        super().__init__(game, scene, groups, pos, surf, z, tile, name, image_path, description)

    def update(self, dt):
        if self.equipped == False:
            super().update(dt)
            return
        direction = self.scene.player.get_direction()
        if direction == 'right':
            self.image = self.frames[0]
            x_adjust = 2
        else:
            self.image = self.frames[1]
            x_adjust = -2
        self.rect.center = (self.scene.player.hitbox.centerx + x_adjust, self.scene.player.hitbox.centery - 2)