from copy import deepcopy

#goals for goap
class Goal(object):
    def __init__(self, name, value=0, rate=0.0):
        self.name = name
        self.value = value
        self.rate = rate

    def update(self, time):
        self.value += self.rate * time

    def _deepcopy__(self, memo):
        return Goal(self.name, self.value, self.rate)

    def apply_action(self, action):
        self.update(action.costs['time'])
        if self.name in action.goals:
            self.value = max(self.value + action.goals[self.name], 0)

    def discontentment(self):
        return self.value**2

    def __str__(self):
        return 'Name: %s, Value %s, Rate: %s' % (self.name, str(self.value), str(self.rate))