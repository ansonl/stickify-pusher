Stickify
===================
![Stickify logo](https://raw.githubusercontent.com/ansonl/stickify-pusher/master/stickify-logo-256.png)

View your Microsoft Windows [Sticky Notes](http://windows.microsoft.com/en-us/windows7/using-sticky-notes) anywhere.

###### Code repositories on Github:  [Stickify Pusher](https://github.com/ansonl/stickify-pusher), [Stickify Server](https://github.com/ansonl/stickify-server), [Stickify web app](https://github.com/ansonl/stickify-web-app).

- **05FEB17 - Updated to work with new Windows 10 Anniversary Update Sticky Notes**
	 - Stickify will detect which type of Sticky Notes you have and automatically use the newer Sticky Notes if you have notes in it.
	 - To use old sticky notes app, please follow directions [here](http://www.winhelponline.com/blog/get-classic-sticky-notes-windows-10-anniversary/) AND delete/rename the new sticky notes app SQLite database file at `%USERPROFILE%\AppData\Local\Packages\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\LocalState\plum.sqlite`.

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
pyinstaller stickify.spec
```

Alternatively, you can try
```
pyinstaller --onefile --noconsole --clean --icon logo.ico stickify.py
```
- Move it to your user startup folder so that it runs on login. 
  - Navigate to **%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup** like below to get to your startup folder. 
  ![Windows 10 Explorer User Startup Folder Navigation](https://raw.githubusercontent.com/ansonl/stickify-pusher/master/images/win10-explorer-startup.png)

  - User startup folder may vary with your setup, some examples:
	  - **C:\Users\USERNAME\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup** *Replace **USERNAME** with your username.*
	  - **%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup**

Notes
-------------
Sticky Pusher is meant to be run on Windows 7 and up. 

Acknowledgements
-------------
[olefile](http://www.decalage.info/python/olefileio) for reading the MS Sticky OLE file format - [license](https://bitbucket.org/decalage/olefileio_pl/wiki/License).

[extract_rtf.py](https://gist.github.com/gilsondev/7c1d2d753ddb522e7bc22511cfb08676) the base Rich Text Format to plain text extracting regex. 

[Unsplash It](https://unsplash.it) for the randomized background picture in the Stickify Web App. 

License
-------------
OLEFile's license can be found [here](https://bitbucket.org/decalage/olefileio_pl/wiki/License).
All other parts of Stickify are made available under MIT License. 