from obstacles.switch import Switch



class BinarySwitch(Switch):
    def __init__(self, scene, groups, pos, surf, z='obstacles', tile = None):
        """
        A switch with two possible positions- left or right. Switch always starts in the left position.
        """
        super().__init__(scene, groups, pos, surf, z, tile)
        self.positions = {
            0: 'left',
            1: 'right'
        }
        self.frame_index = 0
        self.image = self.frames[self.frame_index]