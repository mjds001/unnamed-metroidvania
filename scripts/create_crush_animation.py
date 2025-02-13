# this script is one time use to create the crush animation

import os
import pygame

image_folder = 'assets/characters/santa_merry/crush_right'
base_image = '0.png'

def scale_images(image_folder, target_size=(32, 32), index=0):
    image = pygame.image.load(f'{image_folder}/{base_image}').convert_alpha()
    print(f'original size: {image.get_size()}')
    scaled_image = pygame.transform.smoothscale(image, target_size)
    print(f'scaled size: {scaled_image.get_size()}')
    save_path = f'{image_folder}/{index}.png'
    pygame.image.save(scaled_image, save_path)




if __name__ == '__main__':
    pygame.init()
    # specify convert format
    pygame.display.set_mode((1, 1))
    target_size_x = 27
    target_size_y = 26
    for i in range(1,8):
        target_size_x += 1
        target_size_y -= 3
        scale_images(image_folder, (target_size_x, target_size_y), i)