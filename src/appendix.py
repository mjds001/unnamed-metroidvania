from characters.npc import NPC
from characters.friendly_npc import FriendlyNPC
from characters.random_number_guy import RandomNumberGuy
from characters.sign import Sign

from obstacles.obstacle import Obstacle
from obstacles.wall import Wall
from obstacles.ice import Ice
from obstacles.spike import Spike
from obstacles.one_way_platform import OneWayPlatform
from obstacles.moving_platform import MovingPlatform
from obstacles.ladder import Ladder
from obstacles.button import Button
from obstacles.switch import Switch
from obstacles.binary_switch import BinarySwitch
from obstacles.chimney import Chimney
from obstacles.indoor_chimney import IndoorChimney
from obstacles.smoke import Smoke
from obstacles.fire import Fire
from obstacles.door import Door

from dynamic_objects.bubble import Bubble
from dynamic_objects.box import Box

from items.balloon import Balloon
from items.sunglasses import Sunglasses

from backgrounds.parallax_background import ParallaxBackground
from backgrounds.background import Background
from backgrounds.snow_background import SnowBackground


import pygame


OBSTACLES = {
    'obstacle': Obstacle,
    "wall": Wall,
    'ice': Ice,
    "spike": Spike,
    "moving_platform": MovingPlatform,
    "one_way_platform": OneWayPlatform,
    "ladder": Ladder,
    "button": Button,
    "switch": Switch,
    'binary_switch': BinarySwitch,
    'chimney': Chimney,
    'indoor_chimney': IndoorChimney,
    'smoke': Smoke,
    'fire': Fire,
    'door': Door
}

DYNAMIC_OBJECTS = {
    "box": Box,
    "bubble": Bubble
}

ITEMS = {
    'balloon': Balloon,
    'sunglasses': Sunglasses
}

ENTITIES = {
    "friendly_npc": FriendlyNPC,
    "random_number_guy": RandomNumberGuy,
    "sign": Sign
}

BACKGROUNDS = {
    'snow': SnowBackground,
    'parallax': ParallaxBackground,
    'solid': Background
}
