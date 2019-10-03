# Autofy
An automated migration application to be used to and from Amazon and Spotify

ABOUT: 
If you are on Spotify and have multiple libraries along with thousands of songs, and want to migrate to Amazon music,
This tool will automate the boring task of manually Creating playlist, searching, and adding each song to Amazon.
For now this is only unidirectional, but in future the reverse will also be implemented.

USAGE:
This is till now not an interactive platform, which means you have to install Python, and Required Modules (will be mentioned bellow),
then open up the Python file and edit some fields. For example,
There are variables like
uname = ""
passw = ""
You have to manually insert within the quotes Your respective Spotify and Amazon passwords. If 2step is enabled, you can increase sleep time
from just bellow the variables. 
There is also a 
playlist = "" variable, where you have to manually type in the specific playlist you want to clone.
That same playlist will be cloned from Spotify and added to Amazon music.

Modules Required: 
Selenium.
just from command prompt, " pip install Selenium " will do the job.

Notes: 
You can tweek the codes as you like depending upon your internet speed and browser. You have to change some codes if you want to do the job with
Mozzila Firefox. This project is only for Google Chrome. This until now, only works for Windows. 
More modules and features will be coming with time.

Thank You ...
