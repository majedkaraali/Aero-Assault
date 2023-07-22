import random

def respawn_enemy():
    respawn_chance = random.random()

    if respawn_chance <= 0.7:  
        return 'strike_aircraft'
    elif respawn_chance <= 0.8:  
        return 'bomber'
    elif respawn_chance <= 1.0:  
        return 'kamikaze_drone'
    else:
        return None  

respawned_enemy = respawn_enemy()

