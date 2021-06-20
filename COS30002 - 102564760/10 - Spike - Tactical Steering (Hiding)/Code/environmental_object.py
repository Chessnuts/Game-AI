from vector2d import Vector2D
from matrix33 import Matrix33
from graphics import egi
from random import *

class Environmental_Oject(object):
    
    def __init__(self, world, radius):
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
        self.radius = radius

    def random_position(self, world):
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))

    def render(self):
        egi.green_pen()
        egi.circle(self.pos, self.radius)
