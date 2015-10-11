Stickify Pusher
===================
View your Microsoft Windows Sticky Notes anywhere. 

----------


Build to executable
-------------
Install Pyinstaller and required Python modules with `pip`.
```
pip install pyinstaller
pip install olefile
pip install requests==2.5.1
```
Build `stickify.py`
```
pyinstaller --onefile --noconsole --clean --icon logo.ico stickify.py
```
`stickify.exe` will be located in the created `dist` directory.

Move it to your user startup folder so that it runs on login. 

User startup folder may vary with your setup, some examples:

 - **C:\Users\USERNAME\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Starup**
 - **%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Starup**

