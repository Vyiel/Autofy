# Autofy
An automated migration application to be used to and from Amazon and Spotify

ABOUT: 
If you are on Spotify and have multiple libraries along with thousands of songs, and want to migrate to Amazon music,
This tool will automate the boring task of manually Creating playlist, searching, and adding each song to Amazon.
For now this is only unidirectional, but in future the reverse will also be implemented.

USAGE:
This is till now not an interactive platform, which means you have to install Python, and Required Modules (will be mentioned bellow),
then open up the Python file and edit some fields. For example,
There are specific variables for your Spotify and Amazon username and Passwords at the near top of the file,

Ex:
spotify_username: ""
spotify_password: ""
Amazon_username: ""
Amazon_Password: ""

You have to manually insert within the quotes Your respective Spotify and Amazon passwords. If 2step is enabled, you can increase sleep time from just bellow the variables. 
There is also a 
common_playlist: "" variable, where you have to manually type in the specific playlist you want to clone.
That same playlist will be cloned from Spotify and added to Amazon music.

There are functions made for each job for Rendering Spotify List, Transfering to Amazon, Rendering youtube links, Downloading from youtube etc.
And are commented out. You can run all at once or one by one by commenting in OR/AND out.
GRATITUDE Towards yt-dl.org and team for such an awesome contribution to the society. Thanks for letting me use it !!!

Modules Required: 
Selenium.
youtube-dl
ffmpeg
"FOR SIMPLER USE", make sure that Python, Selenium, youtube-dl, ffmpeg are on the same directory, Else wise, Just changing a very 
few lines of code will do the job for you.

just from command prompt, " pip install Selenium " and downloading ffmpeg and youtube-dl will do the job.

Notes: 
You can tweek the codes as you like depending upon your internet speed and browser. You have to change some codes if you want to do the job with
Mozzila Firefox. This project is only for Google Chrome. This until now, only works for Windows. 
More modules and features will be coming with time.

PS: You can extend our own code to this aswell making the whole operation in the reverse way, Way more exceptions, and verification handling could have been done. This is mainly a POC code to perform an automated operation. More updates, and bug fixes will be on their way with time.

Thank You ...
