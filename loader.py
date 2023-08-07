import pygame
import random

bomber_list=['tu22','tu95']
strike_list=['su25','su25_2','su25_3','a7','a7_2','mig21']
fighter_list=['f16','su27','su27_2','j20','j20_2']
drone_list=['drone']



def get_random_plane_image(plane_list):
    plane_name = random.choice(plane_list)
    image = pygame.image.load(f'src/img/aircrafts/{plane_name}.png').convert_alpha()

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






