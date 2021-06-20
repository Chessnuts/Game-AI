from copy import deepcopy

class Action(object):

    def __init__(self, name, goals=None, costs=None):
        self.name = name
        
        #set dict of goals and costs
        self.goals = goals if goals else {}
        self.costs = costs if costs else {}

        if 'time' not in self.costs:
            self.costs['time'] = 0

    #add deepcopy
    def __deepcopy__(self, memo):
        return Action(self.name, deepcopy(self.goals), deepcopy(self.costs))

    #str
    def __str__(self):
        return '%s, %s, Time: %s' % (self.name, str(self.goals), str(self.costs.get('Time')))