from copy import deepcopy

class State(object):
    id = 0

    def __init__(self, goals, actions, costs):
        self.goals = deepcopy(goals)
        self.actions = deepcopy(actions)
        self.costs = deepcopy(costs)
        self.reset_next_action()
        State.id += 1
        self.id = State.id

    def __deepcopy__(self, memo):
        return State(self.goals, self.actions, self.costs)

    def reset_next_action(self):
        self.current_actions = self.valid_actions()
        self.valid_action_len = len(self.current_actions)

    def apply_action(self, action, goals=None, costs=None):
        #use agent self.goals/costs if none provided
        goals = goals if goals else self.goals
        costs = costs if costs else self.costs

        #go through all goals of the action influences and change
        #apply this action to all goals

        for name, goal in goals.items():
            goal.apply_action(action)

        for cost, change in self.actions[action.name].costs.items():
            costs[cost] = costs[cost] + change

        return goals, costs

    def apply_action_reset(self, action):
        self.apply_action(action)
        self.reset_next_action()


    def try_action(self, action):
        goals = deepcopy(self.goals)
        costs = deepcopy(self.costs)
        return self.apply_action(action, goals, costs)



    def valid_actions(self):
        actions = []
        for name, action in self.actions.items():
            goals, costs = self.try_action(action)
            if all( [value >= 0 for key, value in costs.items() ]):
                actions.append(action)
        return actions

    def next_action(self):
        return self.current_actions.pop() if self.current_actions else None

    ############
    def discontentment(self):
        return sum([goal.discontentment() for name, goal in self.goals.items()])


    #str
    def __str__(self):
        goals = ', '.join(([ '%s %d' %  (v.name, v.value) for k,v in self.goals.items() ]))
        costs = str(self.costs)
        actions = ', '.join([a.name for a in self.valid_actions() ])
        next = '%d:%d' % (self.valid_action_len, len(self._current_actions))

        #return sting formatting
        return 'id: %d, goals: {%s}, costs: %s, actions: {%s}, next: %s' % (self.id, goals, costs, actions, next)