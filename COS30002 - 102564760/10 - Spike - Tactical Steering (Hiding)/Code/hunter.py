from agent import *

from vector2d import Vector2D
from matrix33 import Matrix33
from graphics import egi
from random import *

class Hunter(Agent):
    
    def __init__(self, world=None, scale=40.0, mass=80.0, mode='wander'):
        super().__init__(world=world, scale=scale, mass=mass, mode=mode)

    def calculate(self, delta):
        # calculate the current steering force

        force = self.wander(delta)
        self.force = force
        return force

    def update(self, delta):
        ''' update vehicle position and orientation '''
        # calculate and set self.force to be applied
        ## force = self.calculate()
        #force = self.calculate(delta)  # <-- delta needed for wander
        ## limit force? <-- for wander
        force = self.calculate(delta)
        #if self.mode == 'wander':
        
        force.truncate(self.max_force) # <--new force limiting code
        # determin the new accelteration
        self.accel = force / self.mass  # not needed if mass = 1.0
        # new velocity
        self.vel += self.accel * delta
        # check for limits of new velocity
        self.vel.truncate(self.max_speed)
        # update position
        self.pos += self.vel * delta
        # update heading is non-zero velocity (moving)
        if self.vel.length() > 0.00000001:
            self.heading = self.vel.get_normalised()
            self.side = self.heading.perp()
        # treat world as continuous space - wrap new position if needed
        self.world.wrap_around(self.pos)

    def render(self):
            ''' Draw the triangle agent with color'''
            # draw the path if it exists and the mode is follow
            if self.mode == 'follow_path':
                pth = self.path.get_pts()

                egi.polyline(pth)

            # draw the ship
            egi.red_pen()
            pts = self.world.transform_points(self.vehicle_shape, self.pos,
                                            self.heading, self.side, self.scale)
            # draw it!
            egi.closed_shape(pts)

            # draw wander info?
            if self.mode == 'wander':
                if self.mode == 'wander':# calculate the centerof the wander circle in front of the agent
                    wnd_pos = Vector2D(self.wander_dist, 0)
                    wld_pos = self.world.transform_point(wnd_pos, self.pos, self.heading, self.side)# draw the wander circle
                    egi.green_pen()
                    egi.circle(wld_pos, self.wander_radius) # draw the wander target (little circle on the big circle)
                    egi.red_pen()
                    wnd_pos = (self.wander_target + Vector2D(self.wander_dist, 0))
                    wld_pos = self.world.transform_point(wnd_pos, self.pos, self.heading, self.side)
                    egi.circle(wld_pos, 3)

            # add some handy debug drawing info lines - force and velocity
            if self.show_info:
                s = 0.5 # <-- scaling factor
                # force
                egi.red_pen()
                egi.line_with_arrow(self.pos, self.pos + self.force * s, 5)
                # velocity
                egi.grey_pen()
                egi.line_with_arrow(self.pos, self.pos + self.vel * s, 5)
                # net (desired) change
                egi.white_pen()
                egi.line_with_arrow(self.pos+self.vel * s, self.pos+ (self.force+self.vel) * s, 5)
                egi.line_with_arrow(self.pos, self.pos+ (self.force+self.vel) * s, 5)

    def calculate(self, delta):
        force = self.wander(delta)
        return force


