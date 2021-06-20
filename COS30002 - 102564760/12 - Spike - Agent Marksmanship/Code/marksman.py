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

    

    def __init__(self, world=None, scale=30.0, mass=1.0, mode='shoot'):
        super().__init__(world=world, scale=scale, mass=mass, mode=mode)
        self.color = 'YELLOW'
        self.weapon = 'Rifle'
        self.last_fired = 0.0

    def Random_pos(self, world):
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))

    def update(self, delta):
        if time.time() - self.last_fired > WEAPON_COOLDOWN[self.weapon]:
            self.last_fired = time.time()
            if not self.world.targets:
                return
            target = choice(self.world.targets)
            #self.heading = target.pos.get_normalised()
            self.shoot(target)
        
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
                self.world.projectiles.append(p)
            else:
                #add inaccuracy
                crosshair + Vector2D(randrange(-100.0, 100.0), randrange(-20.0, 20.0))
                p = Projectile(sp, crosshair, spd, self.world)
                self.world.projectiles.append(p)



    def render(self, color=None):
        super().render(color=color)
        egi.white_pen()
        egi.text_at_pos(0, 0, self.weapon)
        

    

    