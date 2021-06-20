from copy import deepcopy
from goal import *
from action import *
from state import *

class Agent(object):
    def __init__(self, goals=None, actions=None, costs=None):
        self.goals = deepcopy(goals) if goals else {}
        self.actions = deepcopy(actions) if actions else {}
        self.costs = deepcopy(costs) if costs else {}

        if 'time' not in self.costs:
            self.costs['time'] = 0

    #apply the action
    def apply_action(self, action, goals=None, costs=None):
        goals = goals if goals else self.goals
        costs = costs if costs else self.costs

        for name, goal in goals.items():
            goal.apply_action(action)

        for cost, change in self.actions[action.name].costs.items():
            costs[cost] = costs[cost] + change
        return goals, costs

    def overall_discontentment(self, goals=None, costs=None):
        #calculates overall total discontentment
        goals = goals if goals else self.goals
        costs = costs if costs else self.costs
        return sum([goal.discontentment() for name, goal in goals.items()])

    #validations
    def valid_actions(self):
        for name, action in self.actions.items():
            goals, costs = self.apply_action(action)
            if all( [value >= 0 for key, value in costs.items() ]):
                self.actions.append(action)
        return self.actions

    #try the action by making a copy of the goals and costs and applying the action to find the result
    def try_action(self, action):
        goals = deepcopy(self.goals)
        costs = deepcopy(self.costs)
        #return the result of the action
        return self.apply_action(action, goals, costs)

    def action_discontentment(self, action):
        goals, costs = self.try_action(action)
        return self.overall_discontentment(goals, costs)

    #use look ahead to find best action and plan
    def choose_action_goap(self, max_depth):
        #storage for world state and the actions used
        states = [[ State(self.goals, self.actions, self.costs), Action('Base')]]

        #keep track of current best actions
        best_action = None
        best_value = 1000000
        best_plan = []

        verbose = True

        if verbose:
            print('Searching...')

        changed = True

        while states:
            current_value = states[-1][0].discontentment()

            if verbose and changed:
                changed = False
                level = len(states) - 1
                #print actions and discontentment in indednted format
                for i, state in enumerate(states[level:], start=level):
                    print('    '*i, '', state[1].name,' (', str(current_value) ,')')


            if len(states) >= max_depth:
                if current_value < best_value:
                    best_action = states[1][1]
                    best_value = current_value
                    best_plan = [state[1].name for state in states if state[1]] + [best_value]

                states.pop()
                continue

            next_action = states[-1][0].next_action()

            if next_action:
                new_state = deepcopy(states[-1][0])
                states.append([new_state, None])
                states[-1][1] = next_action
                new_state.apply_action_reset(next_action)
                changed = True
            else:
                states.pop()


        return best_action, best_plan