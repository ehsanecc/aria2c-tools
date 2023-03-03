# aria2c-tools
Minitools for aria2c
## aria2c_broken_download.py
This tool really saved me about 30GB of data! I was downloading a game on my RPi4 at night, but my SD card got full, and aria2c couldn't write its control file (.aria2), so it couldn't resume my downloads. Therefore, I wrote this tool based on what the [aria2c documentation](http://aria2.github.io/manual/en/html/technical-notes.html) provides and recovered my corrupted downloads easily! Using it is simple: just provide your corrupted downloaded files, and the script will generate a new .aria2 file based on the downloaded parts. How does it know which parts are downloaded and which parts are not? Well, it's based on a guess of 1024*'\0' characters, which worked like a charm for me, and I'm sure it will work in almost all cases.

How to use:
> $ python3 aria2c_broken_download.py \<file1> \[\<file2>] \[\<file3>] ...
>> You can provide multiple files in a single run

## retry_error_downloads.py
Sometimes I face download errors for certain websites, and I don't know why it happens because there are no problems with the links. Therefore, I wrote this script to check for stopped downloads caused by errors and recreate them with the same options so that they can continue to download again, especially at night.

How to use:
> $ python3 retry_error_downloads.py -u \<aria2c-host> \[-p \<port>] \[-s \<secret>] \[-d \<delay-default=60>] \[--paused \<paused>]
>> providing port, secret, delay and paused options are not necessary. so you need only **-u** or **--host** option 
