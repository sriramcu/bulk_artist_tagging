import argparse
import csv
import os
import time
import warnings

import mutagen
from mutagen.easyid3 import EasyID3
from pydub import AudioSegment

untagged_genre_artists = []
untagged_songs = []
genres_csv_filename = "genres.csv"


def save_audio(audio, item):
    try:
        audio.save()
    except Exception as e:
        print(f"Unable to tag song {item}")
        print(e)
        untagged_songs.append(item)
        return False
    else:
        return True


def index_2d(my_list, v):
    # Returns (i,j) where i is the index of the 2d list and j is the index of the element in that list
    # i would be the genre or row index in the csv file and j would be the artist or column index
    desired_value = v.lower().strip()
    for i, sublist in enumerate(my_list):
        processed_sublist = [ele.lower().strip() for ele in sublist]
        if desired_value in processed_sublist:
            return list((i, processed_sublist.index(desired_value)))


def convert_flac_to_mp3(item_path):
    if ".flac" in item_path:
        old_item = item_path
        try:
            flac_audio = AudioSegment.from_file(item_path, format="flac")
            item_path = item_path[:-5] + ".mp3"
            flac_audio.export(item_path, format="mp3")
            print(f"Deleting {old_item}")
            os.remove(old_item)
        except Exception as e3:
            print(e3)
            print("Unable to convert flac to mp3, skipping")
            untagged_songs.append(old_item)
            item_path = old_item
    return item_path


def tag_full_folder(csv_data, current_artist, folder_abs_path, tag_genres, shorten_song_title):
    for item in os.listdir(folder_abs_path):
        item_path = os.path.join(folder_abs_path, item)
        try:
            if any([x in item_path.lower() for x in
                    [".txt", ".ico", ".jpg", ".nfo", ".f1 lac", ".m3u", ".png", ".pdf"]]):
                print(f"Skipping file {item_path}")
            elif os.path.isfile(item_path):
                os.chmod(item_path, 0o777)
                item_path = convert_flac_to_mp3(item_path)
                if not item_path.endswith(".mp3"):
                    continue
                try:
                    audio = EasyID3(item_path)
                except mutagen.id3.ID3NoHeaderError:
                    print("Mutagen ID3 error encountered. Trying with mutagen.file")
                    untagged_songs.append(item_path + " " + "(initial)")
                    # (initial) is because we are unsure if this approach would work instead
                    audio = mutagen.File(item_path, easy=True)
                    audio.add_tags()

                audio["artist"] = current_artist
                if not save_audio(audio, item_path):
                    continue
                if tag_genres and len(csv_data) > 0:
                    genre_2d_index = index_2d(csv_data, current_artist)
                    if genre_2d_index is None:
                        warnings.warn(
                            f"Genre for artist '{current_artist}' not found in the csv file, leaving genre tag unchanged")
                        untagged_genre_artists.append(current_artist)
                        continue
                    genre_index = genre_2d_index[0]
                    genre = csv_data[genre_index][0]
                    audio = EasyID3(item_path)
                    audio["genre"] = genre
                    if not save_audio(audio, item_path):
                        continue

                if shorten_song_title:
                    extension = item.split(".")[-1]
                    song_name_copy = " ".join(item.split(".")[:-1])
                    song_name_copy = song_name_copy.replace(current_artist, "")
                    song_name_copy = song_name_copy.replace(".", " ")
                    song_name_copy = song_name_copy.replace("-", " ")
                    song_name_copy = ''.join(i for i in song_name_copy if not i.isdigit())
                    song_name_copy = song_name_copy.strip()
                    newname = f"{song_name_copy}.{extension}"
                    audio = EasyID3(item_path)
                    audio["title"] = song_name_copy
                    if not save_audio(audio, item_path):
                        continue
                    os.rename(item_path, newname)


            elif os.path.isdir(item_path):
                tag_full_folder(csv_data, current_artist, os.path.join(folder_abs_path, item_path),
                                tag_genres,
                                shorten_song_title)

        except Exception as e:
            print("Unable to tag song " + item_path)
            raise e


def batch_tagger(root_dir_path, tag_genres, shorten_song_title):
    datafile = os.path.join(os.path.dirname(os.path.abspath(__file__)), genres_csv_filename)
    csv_data = []
    try:
        csv_data = list(csv.reader(open(datafile)))
    except FileNotFoundError:
        print(f"{datafile} not found. Genre tagging will be skipped.")

    list_of_artist_folders = os.listdir(root_dir_path)
    for artist in list_of_artist_folders:
        if not os.path.isdir(os.path.join(root_dir_path, artist)):
            print(f"Skipping file {artist}")
            continue
        tag_full_folder(csv_data, artist, os.path.abspath(os.path.join(root_dir_path, artist)), tag_genres,
                        shorten_song_title)


def main():
    ap = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("-d", "--root_music_directory", type=str, required=True, help="_")
    ap.add_argument("-tg", "--tag_genres", type=int, choices=[0, 1], default=1, help="_")
    ap.add_argument("-sh", "--shorten_song_title", type=int, choices=[0, 1], default=0, help="_")
    args = vars(ap.parse_args())
    tag_genres = bool(int(args["tag_genres"]))
    shorten_song_title = bool(int(args["shorten_song_title"]))
    root_dir_path = os.path.abspath(args["root_music_directory"])

    start_time = time.time()
    batch_tagger(root_dir_path, tag_genres, shorten_song_title)
    time_elapsed = time.time() - start_time

    print(f"Time taken for songs tagging = {time_elapsed // 60} minutes {round(time_elapsed % 60, 2)} seconds")
    if len(untagged_genre_artists):
        print(f"The following artists haven't been tagged with genre = {set(untagged_genre_artists)}")
    if len(untagged_songs):
        print("The following songs could not be tagged due to mutagen errors: ", untagged_songs)


if __name__ == "__main__":
    main()
