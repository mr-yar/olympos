import os
import shutil


def remake_folder(folder_name):
    folder_path = os.path.join('downloads', folder_name)
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)
