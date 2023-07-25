import pygame
import random






a7_left_1=pygame.image.load('src/img/a7-left.png')
a7_left_2=pygame.image.load('src/img/a7-left2.png')
a7_rigt_1=pygame.image.load('src/img/a7-right.png')
a7_rigt_2=pygame.image.load('src/img/a7-right2.png')
        

drone_left=pygame.image.load('src/img/drone-left.png')
drone_right=pygame.image.load('src/img/drone-right.png')

f16_left=pygame.image.load('src/img/f16-left.png')
f16_right=pygame.image.load('src/img/f16-right.png')

j20_left=pygame.image.load('src/img/j20-left.png')
j20_right=pygame.image.load('src/img/j20-right.png')
j20_left2=pygame.image.load('src/img/j20-left2.png')
j20_right2=pygame.image.load('src/img/j20-right2.png')

mig21_left=pygame.image.load('src/img/mig21-left.png')
mig21_right=pygame.image.load('src/img/mig21-right.png')

su25_left=pygame.image.load('src/img/su25-left.png')
su25_right=pygame.image.load('src/img/su25-right.png')
su25_left2=pygame.image.load('src/img/su25-left2.png')
su25_right2=pygame.image.load('src/img/su25-right2.png')
su25_left3=pygame.image.load('src/img/su25-left3.png')
su25_right3=pygame.image.load('src/img/su25-right3.png')

su27_left=pygame.image.load('src/img/su27-left.png')
su27_right=pygame.image.load('src/img/su27-right.png')
su27_left2=pygame.image.load('src/img/su27-left2.png')
su27_right2=pygame.image.load('src/img/su27-right2.png')

tu22_left=pygame.image.load('src/img/tu22-left.png')
tu22_right=pygame.image.load('src/img/tu22-right.png')

tu95_left=pygame.image.load('src/img/tu95-left.png')
tu95_right=pygame.image.load('src/img/tu95-right.png')




bomber_list=['tu22','tu95']
strike_list=['su25','su25_2','su25_3','a7','a7_2','mig21']
fighter_list=['f16','su27','su27_2','j20','j20_2']
drone_list=['kamikaze']

def get_random_plane_image(plane_list):
    plane_name = random.choice(plane_list)
    left_image = pygame.image.load(f'src/img/{plane_name}-left.png')
    right_image = pygame.image.load(f'src/img/{plane_name}-right.png')

    # Randomly choose between left and right images
    selected_image = random.choice([left_image, right_image])

    return selected_image


random_bomber_image = get_random_plane_image(bomber_list)
random_strike_image = get_random_plane_image(strike_list)
random_fighter_image = get_random_plane_image(fighter_list)
random_drone_image = get_random_plane_image(drone_list)



