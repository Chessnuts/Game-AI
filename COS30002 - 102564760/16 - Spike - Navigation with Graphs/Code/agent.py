'''An agent with Seek, Flee, Arrive, Pursuit behaviours

Created for COS30002 AI for Games by Clinton Woodward <cwoodward@swin.edu.au>

For class use only. Do not publically share or post this code without permission.

'''

from searches import SearchAStar, SearchDijkstra
from agentpath import Agentpath
from os import SEEK_CUR
from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians
from random import random, randrange, uniform
from agentpath import Agentpath
from copy import *
from box_world import *

AGENT_MODES = {
    KEY._1: 'seek',
    KEY._2: 'arrive_slow',
    KEY._3: 'arrive_normal',
    KEY._4: 'arrive_fast',
    KEY._5: 'flee',
    KEY._6: 'pursuit',
    KEY._7: 'follow_path',
    KEY._8: 'wander',
}

class Agent(object):

    # NOTE: Class Object (not *instance*) variables!
    DECELERATION_SPEEDS = {
        'slow': 0.9,
        'normal': 1.0,
        'fast': 1.1
    }

    def __init__(self, wrld, indx, bool, scale=30.0, mass=1.0, mode='seek'):
        # keep a reference to the world object
        self.world = wrld
        self.mode = mode
        # where am i and where am i going? random start pos
        self.idx = indx
        self.pos = self.idx._vc
        self.startpos = self.idx._vc
        self.path = None
        self.travelpath = Agentpath()
        self.use_a_star = bool
        #self.vel = Vector2D()
        #self.heading = Vector2D(sin(dir), cos(dir))
        #self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)  # easy scaling of agent size
        #self.force = Vector2D()  # current steering force
        #self.accel = Vector2D() # current acceleration due to force
        #self.mass = 0.6

        # data for drawing this agent
        self.color = 'ORANGE'
        if self.use_a_star == True:
            self.color = 'BLUE'
        if self.use_a_star == False:
            self.color = 'RED'

        #self.vehicle_shape = [
        #    Point2D(-1.0,  0.6),
        #    Point2D( 1.0,  0.0),
        #    Point2D(-1.0, -0.6)
        #]
        ### path to follow?
        #self.path = Path()
        #self.randomise_path()  
        #self.waypoint_threshold = 15.0
        # NEW WANDER INFO
        #self.wander_target = Vector2D(1, 0)
        #self.wander_dist = 1.0* scale
        #self.wander_radius = 1.0* scale 
        #self.wander_jitter = 20.0* scale
        #self.bRadius = scale
        # Force and speed limiting code
        #self.max_speed = 10.0* scale
        #self.max_force = 100.0

        # debug draw info?
        self.show_info = False


    def update(self):
        #check for a target

        #if target
        if self.world.target != None:
            #self.travelpath.clear()
            #run a search
            if self.use_a_star == True:
                self.path = SearchAStar(self.world.graph, self.idx.idx, self.world.target.idx, 0)
            else:
                self.path = SearchDijkstra(self.world.graph, self.idx.idx, self.world.target.idx, 0)
            points = []
            print(self.path.path)
            #convert path into position
            for point in self.path.path:
                pos = Point2D()
                pos = self.world.boxes[point]._vc
                print(pos)
                points.append(pos)
            #create a path based on search
            self.travelpath.set_pts(points)
            print(self.travelpath.get_pts())
            #follow the path
            print(self.travelpath.current_pt())
            self.follow_path()
             


    def render(self, color=None):
        ''' Draw the triangle agent with color'''
        # draw the path if it exists and the mode is follow
        #if self.mode == 'follow_path':
        #    pth = self.path.get_pts()

        #    egi.polyline(pth)

        # draw the ship
        egi.set_pen_color(name=self.color)
        # draw it!
        egi.circle(self.pos, 10)


    def move(self, p):
        #set index to index at position
        self.idx = self.world.get_box_by_pos(int(p.x), int(p.y))
        #set position to index posision
        self.pos = self.idx._vc

    def follow_path(self):
        #If heading to final point (is_finished?), 
        if self.travelpath.is_finished():
            #go back to start
            self.move(self.startpos)
        else:
            self.travelpath.inc_current_pt()
            self.move(self.travelpath.current_pt())
            
            
        

