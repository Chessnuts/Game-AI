from agent import *

class Target(Agent):
    def __init__(self, world=None, scale=30.0, mass=1.0, mode='follow_path'):
        super().__init__(world=world, scale=scale, mass=mass, mode=mode)
        self.path = Path()
        self.randomise_path()  
        self.waypoint_threshold = 15.0
    
    def calculate(self, delta):
    # calculate the current steering force
        force = Vector2D()
        force = self.follow_path()
        self.force = force

        return force

    def follow_path(self):
        #If heading to final point (is_finished?), 
        if self.path.is_finished():
            self.randomise_path()
        # #     Return a slow down force vector (Arrive)
        elif (self.path.current_pt() - self.pos).length() <= self.waypoint_threshold:
        # #   If within threshold distance of current way point, inc to next in path
            self.path.inc_current_pt()
            return self.seek(self.path.current_pt()) 
           # return self.seek(self.path.current_pt())
        # #   Return a force vector to head to current point at full speed (Seek)
        return self.seek(self.path.current_pt()) 

    def randomise_path(self):
        cx = self.world.cx  # width
        cy = self.world.cy  # height
        margin = min(cx, cy) * (1/6)  # use this for padding in the next line ...
        self.path.create_random_path(8, margin, margin, (cx - margin), (cy - margin))  # you have to figure out the parameters

