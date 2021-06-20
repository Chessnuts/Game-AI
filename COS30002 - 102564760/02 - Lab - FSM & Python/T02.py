# Bow and Arrow enemy FSM code - Ryan Chessum 102564760
import random

# variables
arrows = 5
player_nearby = False

states = ['attacking','hiding','reloading','searching']
current_state = 'searching'

running = True
max_limit = 100
game_time = 0

while running:
    game_time += 1

    # Searching: search for a player to shoot at 
    if current_state == 'searching':
       
        # Do things for this state
        print("Searching...")

        rn = random.randint(0, 1)
        if rn == 0:
            player_nearby = False
        if rn == 1:
            player_nearby = True
        
        # Check for change state
        if player_nearby == True:
            current_state = 'attacking'

    # Attacking: Shoots arrows at the player
    elif current_state == 'attacking':
        
        # Do things for this state
        print("FIRE!!!!!")
        
        arrows -= 1

        # Check for change state
        if arrows <= 0:
            current_state = 'hiding'
    
    # Hiding: Runs away until the player is no longer nearby
    elif current_state == 'hiding':
        
        # Do things for this state
        print("RUN AWAY!!")
        
        rn = random.randint(0, 1)
        if rn == 0:
            player_nearby = False
        if rn == 1:
            player_nearby = True

        # Check for change state
        if player_nearby == False:
            current_state = 'reloading'
        
    # Reloading: reloads arrows into hand unless the player comes near
    elif current_state == 'reloading':
        
        # Do things for this state
        print("Reloading...")

        arrows += 1
        
        rn = random.randint(0, 1)
        if rn == 0:
            player_nearby = False
        if rn == 1:
            player_nearby = True

        # Check for change state
        if arrows >= 5:
            current_state = 'searching'
        elif player_nearby == True:
            current_state = 'hiding'
            
    # check for broken ... :(
    else:
        print("AH! BROKEN .... how did you get here?")

    # Check for end of game time
    if game_time > max_limit:
        running = False

print('-- The End --')
