get_lyric
=====
Command line tool to retrive lyric from sites.  

windows binary
-----
dist/\*.exe  
python and required libraries are included in them.  
I used pyinstaller to make windows binaries from python sources.I tried some combinations of pyinstaller version and python version.  

| python        | pyinstaller   | executable is runnable |
| ------------- |:-------------:| ----------------------:|
| 3.5.3/64bit   | 3.2.1         | No                     |
| 3.5.3/64bit   | 3.1.1         | No                     |
| 3.5.3/32bit   | 3.1.1         | Yes                    |

development environment
-----
Windows10  
python3.5.3

required libraries
-----
robobrowser  
beautifulsoup4  
mutagen

get_lyric.py
-----
When the lyric is found,the script put lyric to standard output.  
#### usage
```
python get_lyric.py --artist "artist name" --song "song name"  
     [--proxy PROXY]] [--sites SITES] [--list]
```
+ proxy  
Format is [site name=proxy url:port],spllited by ','.
When specified,the script use proxy to access to sites.   
Example  
```
--proxy www.azlyrics.com=36.234.184.32:3128
```
+ sites  
name of sites to search,splitted by ','.  
You can specify sites order with this argument.  
site names are displayed py 'get_lyric.py --list'.  

+ list  
List Available site names,and exit.  

#### log
The script put some debug information to "get_lyric.log",in current directory.

get_mp3_lyrics.py
-----
For mp3 files in specified directory,it search lyric from the site,and put it to file or tag of mp3.  
#### usage
```
python grt_mp3_lyrics.py --in_dir "mp3_files_dir"
    [--out_dir OUT_DIR] [--write2tag] [--overwrite]  
    [--proxy PROXY] [--sites SITES]
```
+ in_dir  
directory where mp3 files are.default is current directory.

+ output_dir  
The script puts lyric to file in "output_dir".  
The format of filename is "artist - song.txt".  
These file is useful for foo_uie_lyrics3(foobar2000 plugin to display lyric).They can be used by "local File Search" source.  

+ write2tag  
The script puts lyric to tag of mp3.  
If lyric contains text like [00:00.00] it is saved to synced lyrics tag,otherwise it is saved to unsynced lyrics tag.  

+ overwrite  
When specified,The script overwrites existing file or tag.  

arguments below are same as get_lyric.py.  
+ proxy  
+ sites  

#### log
The script put some debug information to "get_lyrics.log",in current directory.  

get_lyric.cnf
-----
If there is this file in current directory,the script reads argument from it.  
Example:  
```
[settings]
proxy = www.azzlyrics.com=36.234.184.32:3128
#comment (ignored)
```
The first line "[settings]" is mandetary.

changelog  
-----
#### 2016/02/10  
changed argument 'site' to 'sites'.It is not in regular expression.It can specify sites order.

#### 2016/02/10  
changed argument 'proxy' format.It is not in regular expression.

#### 2017/07/19  
update sites.py,according to changes of sites.
