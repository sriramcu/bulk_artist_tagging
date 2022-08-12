# bulk_artist_tagging
Python Script that recursively tags all songs by setting the artist tag of each song to be the name of the folder in which it is contained.  
  
Suppose the script is set to run on a root directory named "Music" and we need to tag all songs nested inside it. A song whose full path is "Music/ArtistName/a/b/c/song.mp3" will have its Artist tag set to "ArtistName". The program works for all songs, no matter how deeply they may be nested inside the root directory.  

## Setup  
1. Create a CSV file called `genres.csv` where each line of the CSV is of the format `Genre, Artist 1, Artist 2.....`  

2. Run the command as shown under "Usage", the boolean argument tag_genres indicates whether you want to tag your music with the genres described in `genres.csv` (even if this is set to 0, at the very list an empty `genres.csv` file must be present in the directory for the program to function) and the `shorten_song_titles` parameter is set to 1 if you want to remove the Artist's name from the song as well as stripping leading dashes, dots, underscores and numbers from the song's title. The song's title tag and the name of the file will be modified  accordingly. Set to 0 to disable this behaviour.

## Usage  
`python3 full_tagger.py -d root_music_directory -tg tag_genres -sh shorten_song_title`  
  
**Note- create a duplicate/backup of your music directory before running this script on it, to avoid an unforeseen loss of data.**
 
