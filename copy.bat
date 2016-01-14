cd /d %~dp0
rem copy get_lyric_main.py "D:\devel_open\dotnet\foobar2000\foo_uie_lyrics3 SDK\foo_lyricsource\"
rem xcopy get_lyric "D:\devel_open\dotnet\foobar2000\foo_uie_lyrics3 SDK\foo_lyricsource\"
copy get_lyric.py "D:\Program Files (x86)\foobar2000"
xcopy /e /s /y get_lyric "D:\Program Files (x86)\foobar2000\get_lyric"
pause
