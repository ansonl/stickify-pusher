Stickify
===================
![Stickify logo](https://raw.githubusercontent.com/ansonl/stickify-pusher/master/stickify-logo-256.png)

View your Microsoft Windows [Sticky Notes](http://windows.microsoft.com/en-us/windows7/using-sticky-notes) anywhere.

###### Code repositories on Github:  [Stickify Pusher](https://github.com/ansonl/stickify-pusher), [Stickify Server](https://github.com/ansonl/stickify-server), [Stickify web app](https://github.com/ansonl/stickify-web-app).

↓ Stickify Pusher
===================
 - **Pre-built executable is in the `dist` folder if you do not want to compile Stickify Pusher yourself.**  
	 - This executable connects to the *stickify.herokuapp.com* server. 
		 - Provided server is set to wipe nicknames and associated sticky notes if Sticky Pusher has not contacted the server in 24 hours. 
		 - [Stickify Server source](https://github.com/ansonl/stickify-server). 
	 - If you get an error about a missing DLL, your computer is missing the Microsoft Visual C++ Redistributable for VS 2015. The patch can be downloaded [here](http://www.microsoft.com/en-us/download/details.aspx?id=48145). Pyinstaller currently has an issue with bundling the required library in an executable [#1588](https://github.com/pyinstaller/pyinstaller/issues/1588).
 - You may use the [Stickify web app](https://stickify.gq) to view sticky notes on your phone/other computer. 
	 - [Stickify web app source](https://github.com/ansonl/stickify-web-app). 


Build to executable
-------------
- Install Pyinstaller and required Python modules with `pip`.
```
pip install pyinstaller
pip install olefile
pip install requests==2.5.1
```
- Build `stickify.py`, `stickify.exe` will be located in the created `dist` directory.
```
pyinstaller --onefile --noconsole --clean --icon logo.ico stickify.py
```
- Move it to your user startup folder so that it runs on login. 

  - User startup folder may vary with your setup, some examples:
	  -  **C:\Users\USERNAME\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup**
	  - **%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup**

Notes
-------------
Sticky Pusher is meant to be run on Windows. 

Acknowledgements
-------------
[olefile](http://www.decalage.info/python/olefileio) for reading the MS Sticky OLE file format - [license](https://bitbucket.org/decalage/olefileio_pl/wiki/License).

[Unsplash It](https://unsplash.it) for the randomized background picture in the Stickify Web App. 