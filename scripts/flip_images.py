import os
from PIL import Image
import shutil

# this script duplicates and flips images in a folder


base_path = "assets/characters/santa_merry"

def rename_files_in_folder(folder):
    """Renames all files in a folder to sequential numbers starting from 0."""
    files = sorted(os.listdir(folder))
    for index, file_name in enumerate(files):
        if file_name.endswith('.png'):
            new_name = f"{index}.png"
            old_path = os.path.join(folder, file_name)
            new_path = os.path.join(folder, new_name)
            os.rename(old_path, new_path)

def duplicate_and_flip_folder(folder):
    """Creates a duplicate of the folder with images flipped horizontally."""
    parent_dir, folder_name = os.path.split(folder)
    left_folder_name = folder_name.replace("right", "left")
    left_folder = os.path.join(parent_dir, left_folder_name)

    # Duplicate the folder
    if not os.path.exists(left_folder):
        shutil.copytree(folder, left_folder)

    # Flip each image in the new folder
    for file_name in os.listdir(left_folder):
        if file_name.endswith('.png'):
            file_path = os.path.join(left_folder, file_name)
            with Image.open(file_path) as img:
                flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)
                flipped_img.save(file_path)

def process_character_animations(base_path):
    """Processes all folders in the base path for animation states."""
    for folder_name in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder_name)
        if os.path.isdir(folder_path):
            if "right" not in folder_path:
                os.rename(folder_path, f'{folder_path}_right')
                folder_path = f'{folder_path}_right'
            print(f"Processing folder: {folder_path}")
            rename_files_in_folder(folder_path)
            duplicate_and_flip_folder(folder_path)



if __name__ == "__main__":
    process_character_animations(base_path)