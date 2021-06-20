from random import choice, randint, randrange

class Opportunist(object):
    def update(self, gameinfo):
        pass
        # only send one fleet at a time
        if gameinfo.my_fleets:
            return
            # check if we should attack
        if gameinfo.my_planets and gameinfo.not_my_planets:
            #target either the planet with the lowest or highest amount of ships
            strategy = randrange(3)
            if strategy == 0:
                dest = min(gameinfo.not_my_planets.values(), key=lambda p: p.num_ships)
            elif strategy == 1:
                dest = max(gameinfo.not_my_planets.values(), key=lambda p:1.0 /(1 +p.num_ships))
            else:
                dest = choice(list(gameinfo.not_my_planets.values()))
            
            src = choice(list(gameinfo.my_planets.values()))
                 # launch new fleet if there's enough ships
            if src.num_ships > 10:
                gameinfo.planet_order(src, dest, int(src.num_ships * 0.75) )