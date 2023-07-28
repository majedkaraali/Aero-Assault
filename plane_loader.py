import pygame
import random



bomber_list=['tu22','tu95']
strike_list=['su25','su25_2','su25_3','a7','a7_2','mig21']
fighter_list=['f16','su27','su27_2','j20','j20_2']
drone_list=['drone']




# a7_left_1=pygame.image.load('src/img/Air/a7-left.png')
# a7_rigt_1=pygame.image.load('src/img/Air/a7-right.png')
# a7_left_2=pygame.image.load('src/img/Air/a7_2-left.png')
# a7_rigt_2=pygame.image.load('src/img/Air/a7_2-right.png')
        

# drone_left=pygame.image.load('src/img/Air/drone-left.png')
# drone_right=pygame.image.load('src/img/Air/drone-right.png')

# f16_left=pygame.image.load('src/img/Air/f16-left.png')
# f16_right=pygame.image.load('src/img/Air/f16-right.png')

# j20_left=pygame.image.load('src/img/Air/j20-left.png')
# j20_right=pygame.image.load('src/img/Air/j20-right.png')
# j20_left2=pygame.image.load('src/img/Air/j20_2-left.png')
# j20_right2=pygame.image.load('src/img/Air/j20_2-right.png')

# mig21_left=pygame.image.load('src/img/Air/mig21-left.png')
# mig21_right=pygame.image.load('src/img/Air/mig21-right.png')

# su25_left=pygame.image.load('src/img/Air/su25-left.png')
# su25_right=pygame.image.load('src/img/Air/su25-right.png')
# su25_left2=pygame.image.load('src/img/Air/su25_2-left.png')
# su25_right2=pygame.image.load('src/img/Air/su25_2-right.png')
# su25_left3=pygame.image.load('src/img/Air/su25_3-left.png')
# su25_right3=pygame.image.load('src/img/Air/su25_3-right.png')

# su27_left=pygame.image.load('src/img/Air/su27-left.png')
# su27_right=pygame.image.load('src/img/Air/su27-right.png')
# su27_left2=pygame.image.load('src/img/Air/su27_2-left.png')
# su27_right2=pygame.image.load('src/img/Air/su27_2-right.png')

# tu22_left=pygame.image.load('src/img/Air/tu22-left.png')
# tu22_right=pygame.image.load('src/img/Air/tu22-right.png')

# tu95_left=pygame.image.load('src/img/Air/tu95-left.png')
# tu95_right=pygame.image.load('src/img/Air/tu95-right.png')



def get_random_plane_image(plane_list):
    plane_name = random.choice(plane_list)
    left_image = pygame.image.load(f'src/img/Air/{plane_name}-left.png')
    right_image = pygame.image.load(f'src/img/Air/{plane_name}-right.png')

    selected_image = left_image, right_image

    return selected_image

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






