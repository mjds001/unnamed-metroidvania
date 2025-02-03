# a script to get individual images from a spritesheet
import os
from PIL import Image
import pygame

pwd = os.getcwd()
base_path = f'{pwd}/assets/characters/santa_merry'
sprite_sheet_path = f'{base_path}/run_sheet.png'
rows = 1
images_per_row = 6

# sprite sheet contains potentially several rows, each with different numbers of images. Each row contains all the images for a single animation
# each animation should go into a separate folder, and each image should be named with a sequential number starting from 0

def get_images_from_spritesheet(sprite_sheet_path):
    sprite_sheet = Image.open(sprite_sheet_path)
    sheet_width = sprite_sheet.width
    sheet_height = sprite_sheet.height
    print(f'sheet width: {sheet_width}, sheet height: {sheet_height}')
    tile_size = sheet_width // images_per_row
    tile_size_2 = sheet_height // (rows)
    if tile_size != tile_size_2:
        print(f'tile size: {tile_size} != {tile_size_2}')
        print('error: sprite sheet is not square')
        return
    print(f'tile size: {tile_size}')
    folders = []

    images = []
    for row in range(rows):
        for image in range(images_per_row):
            left = image * tile_size
            upper = row * tile_size
            right = left + tile_size
            lower = upper + tile_size
            box = (left, upper, right, lower)
            img = sprite_sheet.crop(box)
            images.append(img)

    # save each image in a separate folder
    for index, img in enumerate(images):
        if index % images_per_row == 0:
            folder_index = index // images_per_row
            os.makedirs(f'{base_path}/{folder_index}', exist_ok=True)
            folders.append(folder_index)
        img.save(f'{base_path}/{folder_index}/{index % images_per_row}.png')
    
    # open each image with pygame and crop out the transparent border
    for folder in folders:
        for file in os.listdir(f'{base_path}/{folder}'):
            img = pygame.image.load(f'{base_path}/{folder}/{file}')
            bounding_rect = img.get_bounding_rect()
            img = img.subsurface(bounding_rect).copy()
            # check if the image is empty
            if img.get_width() == 0 or img.get_height() == 0:
                # delete the file
                os.remove(f'{base_path}/{folder}/{file}')
                continue
            pygame.image.save(img, f'{base_path}/{folder}/{file}')


if __name__ == '__main__':
    print(sprite_sheet_path)
    get_images_from_spritesheet(sprite_sheet_path)