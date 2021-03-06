import os
import csv
import re
import time
import argparse

datafile = "genres.csv"
csv_data = list(csv.reader(open(datafile)))

def index_2d(myList, v):
    vlower = v.lower().strip()
    for i, x in enumerate(myList):
        xlower = [ele.lower().strip() for ele in x]        
        if vlower in xlower:
            return list((i, xlower.index(vlower)))


current_artist = ""
# If shorten is True then remove artist names and leading numbers, spaces and hyphens from the title of a song
def tag_full_folder(folder_abs_path, original_dir,tag_genres=True, shorten_song_title=True):

    os.chdir(folder_abs_path)
    for item in os.listdir('.'):
        if item.endswith("txt"):
            print(f"Skipping text file {item}")
            continue
        elif os.path.isfile(item):
            # item is in current working directory, so no need to determine the absolute path
            cmd = f'mid3v2 -a "{current_artist}" "{item}"'
            print(cmd)
            os.system(cmd)
            if tag_genres:
                genre_2d_index = index_2d(csv_data, current_artist)
                if genre_2d_index == None:
                    print(f"Genre for artist '{current_artist}' not found in the csv file")
                    continue
                genre_index = genre_2d_index[0]
                genre = csv_data[genre_index][0]
                cmd = f'mid3v2 -g "{genre}" "{item}"' 
                print(cmd)
                os.system(cmd)
            
            if shorten_song_title:
                newname = re.sub(current_artist,"",item,count=0,flags=re.I).strip()
                newname = re.sub(r'^(\d)+',"",newname,count=0,flags=re.I).strip()
                newname = re.sub(current_artist,"",newname,count=0,flags=re.I).strip()
                prevname = newname
                while True:
                    matches = 0                
                    newname = re.sub(r'^-',"",prevname,count=0,flags=re.I).strip()
                    if prevname == newname:
                        matches += 1
                    newname = re.sub(r'^\.',"",prevname,count=0,flags=re.I).strip()
                    if prevname == newname:
                        matches += 1
                    
                    if matches == 2:
                        # means that song name did not change after attempting to remove leading dots and hyphens
                        break

                    prevname = newname
                
                # Now newname is final title name with .mp3 on the end
                newname_list = newname.split(".")
                del newname_list[-1]
                newname_title = ''.join(newname_list)
                cmd = f'mid3v2 -t "{newname_title}" "{item}"'
                print(cmd)
                os.system(cmd)
                os.rename(item,newname)


        elif os.path.isdir(item):
            tag_full_folder(os.path.join(folder_abs_path,item),folder_abs_path, tag_genres=tag_genres, shorten_song_title=shorten_song_title)
            

    os.chdir(original_dir)


def main():

    ap = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("-root_dir","--root_music_directory", type=str, required=True, help=" ")
    ap.add_argument("-tag_genres", type=int, choices=[0,1],required=True, help=" ")
    ap.add_argument("-shorten_song_title", type=int, choices=[0,1], default=0, help=" ")
    args = vars(ap.parse_args())

    tag_genres = int(args["tag_genres"])    
    
    shorten_song_title = int(args["shorten_song_title"])
    
    original_dir = os.path.abspath(os.getcwd())
    root_dir_path = os.path.abspath(args["root_music_directory"])
    list_of_artist_folders = os.listdir(root_dir_path)
    for artist in list_of_artist_folders:
        if artist.endswith("txt"):
            print(f"Skipping text file {artist}")
            continue
        global current_artist
        current_artist = artist
        tag_full_folder(os.path.abspath(os.path.join(root_dir_path, artist)), original_dir, tag_genres=tag_genres, shorten_song_title=shorten_song_title)
    
if __name__ == "__main__":
    start_time = time.time()
    main()
    time_elapsed = time.time() - start_time
    print(f"Time taken for songs tagging = {time_elapsed//60} minutes {round((time_elapsed%60)/60,2)} seconds")