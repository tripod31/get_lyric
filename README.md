# get_lyric
Command line tool to retrive lyric from sites.  
For mp3 files in specified directory,it search lyric from the site,and put it to file or tag of mp3.  

## development environment
python3.5  

## required libraries
robobrowser  
mutagen(for get_lyrics.py only)

## get_lyric.py
#### usage
    python get_lyric.py --artist "artist name" --song "song name"

When the lyric is found,the script put lyric to standard output.  
The script put some debug information to "get_lyric.log",in current directory.

## get_lyrics.py
#### usage
    python grt_lyrics.py --in_dir "mp3_files_dir" [--out_dir "output_dir"] [--write2tag] [--overwrite]

+    output_dir  
    The script puts lyric to file in "output_dir".  
    The format of filename is "artist - song.txt".  
    These file is useful for foo_uie_lyrics3(foobar2000 plugin to display lyric).They can be used by "local File Search" source.  

+    write2tag  
    The script puts lyric to unsynced lyrics tag of mp3.
    If lyric contains text like  
    [00:00.00]lyric text  

,lyric is saved to synced lyrics tag.Otherwise it is saved to unsynced lyrics tag.  
+    overwrite  
When specified,The script overwrites existing file or tag.  

The script put some debug information to "get_lyrics.log",in current directory.  
