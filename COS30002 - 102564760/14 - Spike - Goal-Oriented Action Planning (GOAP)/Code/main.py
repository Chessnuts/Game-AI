from copy import deepcopy
from state import *
from goal import *
from agent import *
from action import *

def print_actions(agent):
    print ('ACTIONS:')
    for k, v in agent.actions.items():
        print (" - ", v)


def print_action_evals(agent):
    print ('VALID ACTIONS (DISCONTENTMENT)')
    for action in agent.valid_actions():
        print ("- [%s] (%d " % (action.name, agent.action_discontentment(action)))


def dog_goap():
    #list that is then converted to dictionary
    goals = {
        Goal('Food', 1, 0),
        Goal('Enjoyment', 8, 0),
    }

    goals = {g.name: g for g in goals}

    actions = {
        Action('Play Fetch', goals={'Enjoyment': -2, 'Food': 1}, costs={'Time in day': -2}),
        Action('Go on walk', goals={'Enjoyment': -6, 'Food': 3}, costs={'Time in day': -3}),
        Action('Drink water', goals={'Food': -1}, costs={'Time in day': -1}),
        Action('Eat food', goals={'Food': -2}, costs={'Time in day': -2}),
    }
    steps = 1
    actions = dict([(a.name, a) for a in actions])
    costs = {'Time in day': 10}
    dog = Agent(goals, actions, costs)
    #how far should the program look ahead
    depth = 6
    HR = '-'*60
    #Big O notation => O(n^d), number of goals to the power of depth
    print_actions(dog)
    #Start
    print('>> Start <<')
    while dog.costs['Time in day'] > 0:
        print(HR)
        time = dog.costs['Time in day']
        print (str(steps))
        #print current statistics
        print ('Current Goals (Discontentment= %d) ' % dog.overall_discontentment())
        print (' - ', ', '.join(['%s=%s' % (v.name, str(v.value)) for k, v in dog.goals.items()]))
        print (('Current Costs'), str(dog.costs))

        #Choose action
        action, plan = dog.choose_action_goap(depth)
        print ('Best Action: \n = %s (%d)' % (action.name, dog.action_discontentment(action)))
        dog.apply_action(action)
        print ('New Goals (Discontentment=%d)' % dog.overall_discontentment())
        print (' - ' ', '.join('%s=%s' % (v.name, str(v.value)) for k, v in dog.goals.items()))
        steps += 1
        #reduce depth to avoid indexing errors with different depth sizes
        if depth > 2:
            depth -= 1

    print (HR)
    print ('Day over!')
    print (HR)
    print ('>> Done! <<\n\n')

if __name__ == '__main__':
    dog_goap()