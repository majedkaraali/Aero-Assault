import pygame
import random
import os

pygame.init()
pygame.mixer.init()

bomber_list=['tu22','tu95']
strike_list=['su25','su25_2','su25_3','a7','a7_2','mig21']
fighter_list=['f16','su27','su27_2','j20','j20_2']
drone_list=['drone']
images_path='src/img/aircrafts'



#  sound paths and their corresponding keys

sound_paths = {
    "firing_sound": "src/sound/wopn/shoot.wav",
    "missile_sound3": "src/sound/wopn/missile3.wav",
    "missile_sound2": "src/sound/wopn/missile2.wav",
    "explosion_distant_001": "src/sound/wopn/explosion_distant_001.mp3",
    "explosion_distant_002": "src/sound/wopn/explosion_distant_002.mp3",
    "explosion_distant_003": "src/sound/wopn/explosion_distant_003.mp3",
    "explosion_medium": "src/sound/wopn/explosion_medium.mp3",
    "explosion_large": "src/sound/wopn/explosion_large.mp3",
    "explosion_small": "src/sound/wopn/explosion_small.mp3",
    "explod": "src/sound/wopn/Explosion3.wav",
    "explod1": "src/sound/wopn/Explosion.wav",
    "no_ammo": "src/sound/wopn/no-ammo.wav",
    "reloading": "src/sound/wopn/reloading2.wav",
    "pl_shell1": "src/sound/wopn/pl_shell1.wav",
    "pl_shell2": "src/sound/wopn/pl_shell2.wav",
    "pl_shell3": "src/sound/wopn/pl_shell3.wav",
    "player_exp": "src/sound/wopn/player_exp.wav",
    "tankidle": "src/sound/vehicle/tank1.wav"
}







sound_cache = {}
image_cache = {}



for key, path in sound_paths.items():
    sound_cache[key] = pygame.mixer.Sound(path)



def load_images(aircraft_list):
    for aircraft_type in aircraft_list:
        image_path = os.path.join(images_path, f"{aircraft_type}.png")
        image_cache[aircraft_type] = pygame.image.load(image_path)


load_images(bomber_list)
load_images(strike_list)
load_images(fighter_list)
load_images(drone_list)



print('Loaded')



def load_image(image_path):
    
    if image_path not in image_cache:
        image_cache[image_path] = pygame.image.load(image_path).convert_alpha()
    return image_cache[image_path]



def get_random_plane_image(plane_list):
    
    plane_name = random.choice(plane_list)
    image = pygame.image.load(f'src/img/aircrafts/{plane_name}.png').convert_alpha()
    print('image loaded')
    return image

def random_bomber():
    random_bomber_image = get_random_plane_image(bomber_list)
    return random_bomber_image

def random_strike():
    random_strike_image = get_random_plane_image(strike_list)
    return random_strike_image

def random_fighter():
    random_fighter_image = get_random_plane_image(fighter_list)
    return random_fighter_image

def random_drone():
    random_drone_image = get_random_plane_image(drone_list)
    return random_drone_image






