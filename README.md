# bulk_artist_tagging
Python Script that recursively tags all songs by setting the artist tag of each song to be the name of the folder in which it is contained.  
  
Suppose the script is set to run on a root directory named "Music" and we need to tag all songs nested inside it. A song whose full path is "Music/ArtistName/a/b/c/song.mp3" will have its Artist tag set to "ArtistName". The program works for all songs, no matter how deeply they may be nested inside the root directory.  

## Usage  
`python3 full_tagger.py <absolute_path_to_music_directory>`  
  
**Note- create a duplicate/backup of your music directory before running this script on it, to avoid an unforeseen loss of data.**
