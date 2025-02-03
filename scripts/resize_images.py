# this script is used to scale images to work with a tilesize of 32x32

import os
import pygame

image_folder = 'assets/characters/santa_fighter'

def scale_images(image_folder, target_size=(32, 32)):
    for root, dirs, files in os.walk(image_folder):
        for file in files:
            if file.endswith('.png'):
                file_path = os.path.join(root, file)
                image = pygame.image.load(file_path).convert_alpha()
                print(f'original size: {image.get_size()}')
                scaled_image = pygame.transform.smoothscale(image, target_size)
                print(f'scaled size: {scaled_image.get_size()}')
                pygame.image.save(scaled_image, file_path)




if __name__ == '__main__':
    pygame.init()
    # specify convert format
    pygame.display.set_mode((1, 1))
    scale_images(image_folder)