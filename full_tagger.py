import os
import sys

current_artist = ""
def tag_full_folder(folder_abs_path, original_dir):
    os.chdir(folder_abs_path)
    for item in os.listdir('.'):
        if os.path.isfile(item):
            cmd = 'mid3v2 -a "{}" "{}"'.format(current_artist,item)
            print(cmd)
            os.system(cmd)
        elif os.path.isdir(item):
            tag_full_folder(os.path.join(folder_abs_path,item),folder_abs_path)
            

    os.chdir(original_dir)


def main():
    original_dir = os.path.abspath(os.getcwd())
    root_dir_path = os.path.abspath(sys.argv[1])
    list_of_artist_folders = os.listdir(root_dir_path)
    for artist in list_of_artist_folders:
        global current_artist
        current_artist = artist
        tag_full_folder(os.path.abspath(os.path.join(root_dir_path, artist)), original_dir)
    
if __name__ == "__main__":
    main()