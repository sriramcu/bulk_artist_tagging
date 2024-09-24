# Batch Music Tagging Tool

A Python Script that recursively tags all songs by setting the artist tag of each song 
to be the name of the folder in which it is contained. Also supports setting the genre 
tag based on a CSV file. 
 
Suppose the script is set to run on a root directory named "Music" and we wish to tag 
all songs located inside it. A song whose full path is "Music/ArtistName/a/b/c/song.mp3" 
will have its Artist tag set to "ArtistName". In other words, the immediate subfolder 
to the root directory will always be the artist's name. The program works for all audio files, 
no matter how deeply they may be nested inside the root directory.

This project uses Mutagen and Easy ID3 for tagging.

## Setup 
1. `pip install -r requirements.txt`
2. (Optional) Create a CSV file called `genres.csv` in the root directory of this 
  project, where each line of the CSV is of the format `Genre, Artist 1, Artist 2.....` 

**Note- create a duplicate/backup of your music directory before running this script 
on it, to avoid any unforeseen loss of data.**

## Usage 
`python batch_tagger.py [-h] -d ROOT_MUSIC_DIRECTORY [-tg TAG_GENRES] [-sh 
SHORTEN_SONG_TITLE]` 

### Options
* -d, --root_music_directory : Path to the root directory containing music files (required)
* -tg, --tag_genres: Tag genres (0: disabled, 1: enabled) (default: 1)
* -sh, --shorten_song_title: Shorten song titles (0: disabled, 1: enabled) (default: 0)
* -h, --help: Show this help message and exit

### Options Description

1. The boolean argument `tag_genres` indicates whether you want to tag your music with 
   the genres described in `genres.csv`. If set to 0, genre tags will not be modified 
   or processed.
2. The `shorten_song_titles` parameter can be set to 1 if you wish to clean up or 
   sanitize the names 
   of song titles, which may appear to be a bit messy. This will remove the Artist's 
name from the song as well as removing dashes and dots from the song's title. The 
   song's title tag and the name of the file will be modified 
accordingly. There is no provision to undo these changes once done. By default, this 
   property is disabled.

## Note

1. .flac files will be converted to .mp3 before tagging.

## Miscellaneous Information

Run the following commands in an interactive python shell to get the ID3 tags of an 
individual song:
```
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
audio = MP3("myfile.mp3", ID3=EasyID3)
audio
```

 

 
