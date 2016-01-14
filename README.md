# get_lyric
Command line tool to retrive lyric.  
Currentry it search lyric in "www.lyrics.az".  

## development environment
python3.5  

## required libraries
RoboBrowser  
Stagger(for get_lyrics.py only)

## get_lyric.py
#### usage
>python get_lyric.py --artist "artist name" --song "song name"

When the lyric is found,the script put lyric to standard output.  
The script put some debug information to "get_lyric.log",in current directory.

## get_lyrics.py
#### usage
>python grt_lyrics.py --in_dir "mp3_files_dir" --out_dir "output_dir"

When the lyric of mp3 in "mp3_files_dir" is found,the script puts lyric to file in "output_dir".
The format of filename "artist - song.txt".
