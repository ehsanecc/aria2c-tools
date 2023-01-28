# aria2c-tools
Minitools for aria2c
## aria2c_broken_download.py
This tools really saved me about 30GB of data! I downloaded a game in my RPi4 in night but my sdcard\
get fulled and aria2c cannot write its control file (.aria2) so it cannot resume my downloads!!\
So I wrote this tool based on what [aria2c documentation](http://aria2.github.io/manual/en/html/technical-notes.html) provide, \
and recover my corrupted downloads easily!
The use is simple, just provide your corrupted downloaded files and the script will generate a new .aria2 file based on downloaded parts.\
How it know which parts are downloaded and which parts not? Well, It's based on guess of 1024*'\0' chars which works for me like a charm\
and I'm sure will work on almost all cased.

How to use:
> $ python3 aria2c_broken_download.py \<file1> \[\<file2>] \[\<file3>] ...
>> You can provide multiple files in a single run

## retry_error_downloads.py
Sometimes I face download errors for some websites which I don't know why it happens because there 
is no problem with links, so I wrote this script to check for stopped downloads (caused by error)\
and recreate them with same options so it will continue to download again. (especially for night)

How to use:
> $ python3 retry_error_downloads.py -u \<aria2c-host> \[-p \<port>] \[-s \<secret>] \[-d \<delay-default=60>] \[--paused \<paused>]
>> providing port, secret, delay and paused options are not necessary. so you need only **-u** or **--host** option 
