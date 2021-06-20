from math import sqrt
from agent import *
from random import *
from projectile import *
import time
import copy

WEAPON_TYPES = {
    KEY._1: 'Rifle',
    KEY._2: 'Rocket Launcher',
    KEY._3: 'Hand Gun',
    KEY._4: 'Grenade'
    }

WEAPON_COOLDOWN = {
    'Rifle': 1.0,
    'Rocket Launcher': 1.2,
    'Hand Gun': 0.2,
    'Grenade': 1.0
}

PROJECTILE_SPEED = {
    'Rifle': 500.0,
    'Rocket Launcher': 200.0,
    'Hand Gun': 350.0,
    'Grenade': 150.0
}


class Marksman(Agent):

    

    def __init__(self, world=None, scale=30.0, mass=1.0, mode='Patrol'):
        super().__init__(world=world, scale=scale, mass=mass, mode=mode)
        self.color = 'YELLOW'
        self.weapon = 'Rifle'
        self.last_fired = 0.0
        self.waypoint_number = 6
        self.patrol_mode = 'Stopped'
        self.attack_mode = 'Loaded'
        self.last_stopped = time.time()
        self.waypoints = [self.pos.copy()]
        i = 1
        while i < self.waypoint_number:
            self.add_waypoint(Vector2D(randrange(self.world.cx), randrange(self.world.cy)))
            i += 1

        self.current_waypoint = 0

    def Random_pos(self, world):
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
        self.waypoints.clear()
        i = 0
        while i < self.waypoint_number:
            self.add_waypoint(Vector2D(randrange(self.world.cx), randrange(self.world.cy)))
            i += 1
    
    def calculate(self, delta, target):
        force = Vector2D()
        mode = self.mode
        if mode == 'Patrol':
            force = self.patrol()
        elif mode == 'Attack':
            force = self.arrive(target.pos, 'normal')
        else:
            force = Vector2D()
        self.force = force
        return force
        #return super().calculate(delta)

    def find_target(self):
        #add targets to list in range
        found_targets = []
        for target in self.world.targets:
            if Vector2D.distance(self.pos, target.pos) < 200.0:
                found_targets.append(target)

        shortest_dist = 1000000000000

        closest_target = None
        for target in found_targets:
            if Vector2D.distance(self.pos, target.pos) < shortest_dist:
                shortest_dist = Vector2D.distance(self.pos, target.pos)
                closest_target = target
        if closest_target != None:
            self.mode = 'Attack'
        else:
            self.mode = 'Patrol'
        return closest_target    

    def update(self, delta):
        target = self.find_target()
        force = self.calculate(delta, target)
        if time.time() - self.last_fired > WEAPON_COOLDOWN[self.weapon]:
            self.attack_mode = 'Loaded'
        if target != None and self.attack_mode == 'Loaded':
            self.shoot(target)
            self.attack_mode = 'Reloading'
            #self.heading = target.pos.get_normalised()
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

    def patrol(self):
        force = Vector2D()
        if self.patrol_mode == 'Stopped' and time.time() - self.last_stopped > 1:
            self.patrol_mode = 'Walking'

        if self.patrol_mode == 'Walking':
            force = self.arrive(self.waypoints[self.current_waypoint], 'slow')

            if self.pos.distanceSq(self.waypoints[self.current_waypoint]) < 25:
                self.next_waypoint()
                self.last_stopped = time.time()
                self.patrol_mode = 'Stopped'
        return force

    def add_waypoint(self, point):
        self.waypoints.append(point)

    def next_waypoint(self):
        self.current_waypoint += 1
        if self.current_waypoint >= len(self.waypoints):
            self.current_waypoint = 0        

    def predict(self, rp, rv):
        #solve using quadtatics
        a = rv.dot(rv) - PROJECTILE_SPEED[self.weapon] * PROJECTILE_SPEED[self.weapon]
        b = 2.0 * rv.dot(rp)
        c = rp.dot(rp)

        d = b * b - 4.0 * a * c

        if (d > 0.0):
            return 2 * c / (sqrt(d) - b)
        else:
            return - 1


    def shoot(self, target):

        #copies
        mksmn = copy.deepcopy(self)
        trgt = copy.deepcopy(target)
        
        #relative position
        rp = trgt.pos - mksmn.pos

        #relative velocity
        rv = trgt.vel - mksmn.vel

        dt = self.predict(rp, rv)

        if (dt > 0):
            crosshair = Vector2D()
            crosshair = trgt.pos + (trgt.vel * dt)
            #crosshair.normalise()
            #crosshair = crosshair * PROJECTILE_SPEED[self.weapon]
            crosshair = (crosshair - mksmn.pos).normalise()

            #Create bullets
            #Define stuff here so init paramaeters aren't confusing

            #startinf position
            sp = Vector2D()
            sp = mksmn.pos
            #speed
            spd = (PROJECTILE_SPEED[self.weapon])


            #heading
            #just use crosshair variable, it works

            if self.weapon == 'Rifle' or 'Rocket Laucher':
                p = Projectile(sp, crosshair, spd, self.world)
                self.world.agents.append(p)
                
                self.last_fired = time.time()
                self.attack_mode = 'Reloading'
            else:
                #add inaccuracy
                crosshair + Vector2D(randrange(-20.0, 20.0), randrange(-20.0, 20.0))
                p = Projectile(sp, crosshair, spd, self.world)
                self.world.agents.append(p)
                
                self.last_fired = time.time()
                self.attack_mode = 'Reloading'



    def render(self, color=None):
        super().render(color=color)
        egi.white_pen()
        egi.text_at_pos(0, 0, self.weapon)
        for waypoint in self.waypoints:
            if waypoint == self.waypoints[self.current_waypoint]:
                egi.green_pen()
                egi.circle(waypoint, 20.0)
            else:
                egi.blue_pen()
                egi.circle(waypoint, 20.0)
        

    

    