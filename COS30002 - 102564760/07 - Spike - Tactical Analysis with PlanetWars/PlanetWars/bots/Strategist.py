from random import choice, randint, randrange

class Strategist(object):
    def update(self, gameinfo):
        pass
        # only send one fleet at a time
        if len(gameinfo.my_fleets) > 1:
            return
        # check if we should attack
        if gameinfo.my_planets and gameinfo.not_my_planets:
            #target either the planet with the lowest or highest amount of ships
            
            #elif len(gameinfo.my_planets) < len(gameinfo.not_my_planets):
            dest = max(gameinfo.not_my_planets.values(), key=lambda p:p.num_ships)
            src = max(gameinfo.my_planets.values(), key = lambda p: p.num_ships)
            if src.num_ships > 10:
                gameinfo.planet_order(src, dest, int(src.num_ships * 0.9) )

            #if len(gameinfo.my_planets) < len(gameinfo.not_my_planets):
            dest = min(gameinfo.not_my_planets.values(), key=lambda p: p.num_ships)
            src = min(gameinfo.my_planets.values(), key = lambda p: (p.num_ships)*0.7 > dest.num_ships)
            if src.num_ships > 10:
                gameinfo.planet_order(src, dest, int(src.num_ships * 0.75) )
            
            
#            dest = choice(list(gameinfo.not_my_planets.values()))
#            src = choice(list(gameinfo.my_planets.values()))
#                 # launch new fleet if there's enough ships
#            if src.num_ships > 10:
#                gameinfo.planet_order(src, dest, int(src.num_ships * 0.75) )
            

            
           
        