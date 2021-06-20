
from os import remove
from agent import *

class Projectile(Agent):
    def __init__(self, s, h, speed, world, scale=5.0, mass=1.0, mode='seek'):
        super().__init__(world=world, scale=scale, mass=mass, mode=mode)
        self.pos = s
        self.vel = Vector2D()
        self.vel = speed
        self.heading = h
        self.detection_radius = 50.0
        self.start_pos = s

    def update(self, delta):
        if (self.pos - self.start_pos).length() > 2000.0:
            if self in self.world.agents:
                self.world.agents.remove(self)
        for target in self.world.targets:
            if (self.pos - target.pos).length() < self.detection_radius:
                #for testing when it didn't delete
                target.color = 'BLUE'
                self.world.targets.remove(target)
                if self in self.world.agents:
                    self.world.agents.remove(self)
                
                
                
        self.pos += (self.heading * self.vel) * delta

        
        