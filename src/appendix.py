from characters.npc import NPC
from characters.friendly_npc import FriendlyNPC
from characters.random_number_guy import RandomNumberGuy
from characters.sign import Sign
from obstacles.wall import Wall
from obstacles.spike import Spike
from obstacles.one_way_platform import OneWayPlatform
from obstacles.moving_platform import MovingPlatform
from obstacles.ladder import Ladder
from obstacles.button import Button

from dynamic_objects.box import Box


OBSTACLES = {
    "wall": Wall,
    "spike": Spike,
    "moving_platform": MovingPlatform,
    "one_way_platform": OneWayPlatform,
    "ladder": Ladder,
    "button": Button
}

DYNAMIC_OBJECTS = {
    "box": Box
}

ENTITIES = {
    "friendly_npc": FriendlyNPC,
    "random_number_guy": RandomNumberGuy,
    "sign": Sign
}