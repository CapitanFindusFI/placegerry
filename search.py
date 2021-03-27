import os
import random

def search_image(width, height):
    print("Searching image {}x{}".format(width, height))
    search_path = "./downloaded"
    files_list = list(os.listdir(search_path))
    valid_files_path = "{}-{}".format(width, height)
    target_files = []
    for name in files_list:
        file_fullpath = (os.path.join(search_path, name))
        if(os.path.isfile(file_fullpath) and name.startswith(valid_files_path)):
            target_files.append(name)

    print(target_files)
    if(len(target_files) > 0):
        target_file = random.choice(target_files)
    else:
        target_file = random.choice(files_list)
    
    return target_file
