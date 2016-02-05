get_lyric
=====
Command line tool to retrive lyric from sites.  

development environment
-----
python3.5  

required libraries
-----
robobrowser  
beautifulsoup4  
mutagen(for get_mp3_lyrics.py only)

get_lyric.py
-----
When the lyric is found,the script put lyric to standard output.  
#### usage
    python get_lyric.py --artist "artist name" --song "song name" [--proxy [site name in regular expression],[proxy url:port]] [--site site] [--list]

+    proxy  
    site name in regular expression and proxy url:port.When specified,the script use proxy to access to sites.   
    Example  
    >--proxy azlyrics,36.234.184.32:3128
    
+    site  
    Specify site name to serach,in regular expression.  
    Available site names are displayed by:  

    >python get_lyric.py --list

+    list  
    List Available site names,and exit.  

####log
The script put some debug information to "get_lyric.log",in current directory.

get_mp3_lyrics.py
-----
For mp3 files in specified directory,it search lyric from the site,and put it to file or tag of mp3.  
#### usage
    python grt_mp3_lyrics.py --in_dir "mp3_files_dir" 
    [--out_dir "output_dir"] [--write2tag] [--overwrite] [--proxy [site name in regular expression],[proxy url:port]] [--site site]

+    in_dir  
    directory where mp3 files are

+    output_dir  
    The script puts lyric to file in "output_dir".  
    The format of filename is "artist - song.txt".  
    These file is useful for foo_uie_lyrics3(foobar2000 plugin to display lyric).They can be used by "local File Search" source.  

+    write2tag  
    The script puts lyric to tag of mp3.
    If lyric contains text like  
    >[00:00.00]lyric text  

    ,lyric is saved to synced lyrics tag.Otherwise it is saved to unsynced lyrics tag.  
+    overwrite  
    When specified,The script overwrites existing file or tag.  

arguments below are same as get_lyric.py.  
+    proxy  
+    site  
    
####log
The script put some debug information to "get_lyrics.log",in current directory.  

get_lyric.cnf
-----
If there is this file in current directory,the script reads argument from it.  
Example:  

    [settings]
    proxy = azlyrics,36.234.184.32:3128
    #comment (ignored)
 
 The first line "[settings]" is mandetary.
