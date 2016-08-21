#!/usr/bin/python
# -*- coding: utf-8 -*-

#pyinstaller --onefile --noconsole --clean stickify.py
#pyinstaller --onefile --noconsole --clean --icon logo.ico stickify.py
#a.datas += [ ('logo.ico', 'C:\\Users\\ansonl\\development\\stickify-pusher\\logo.ico', 'DATA')]
#pyinstaller stickify.spec
import olefile

import sys
import os.path
import re
import requests
import base64, zlib
import time
import datetime
import threading
import tempfile
from os.path import expanduser

import tkinter as tk
from tkinter import messagebox

import pickle

import extract_rtf

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import FileSystemEvent

username = ''
passcode = ''
#server = 'http://mich302csd17u' + ':' + '8080'
server = 'https://stickify.herokuapp.com'
#server = 'http://uakk62822589.ansonl.koding.io:8080'

#watchdog observer object
observer = None
#watchdog handler object
watchHandler = None

#observer last updated date
lastUpdated = None
#observer polling timer
lastUpdateCheckTimer = None

#ping server timer
pingServerTimer = None

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def pingServerToKeepAccount():
    print("Pinging server")
    updateUISendFile()

def tryToRegister():
    print("Checking username " + username)
    # create payload
    payload = {
        'user': username,
        'passcode': passcode,
        'number': 0,
        'data': 0,
        }

    try:
        # make POST request with payload
        r = requests.post(server + '/update', data=payload, timeout=5)
        #print (r.status_code, r.reason)
        if r.text[0:1] == '0':
            print('Success registering ' + username)
            return 0
        else:
            messagebox.showerror("Could not set nickname " + username, r.text)
            print(('Registering ' + username + ' failed: ' + r.text))
            return r.text
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error sending request to " + server, e)
        print('Connection error:', e)
        return "Update to " + server + " failed"



class WatchEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        global lastUpdated
        global watchHandler
        global lastUpdateCheckTimer
        #print("Directory modified")
        if lastUpdated is not None:
            if (datetime.datetime.now()-lastUpdated).total_seconds() >= 5:
                print("Last update > 5 seconds ago, sending files.")
                lastUpdated = datetime.datetime.now()
                updateUISendFile()
            else:
                print("Last update < 5 seconds, will check back...")
                
                if lastUpdateCheckTimer is not None:
                    lastUpdateCheckTimer.cancel()
                #schedule a handler event in 5 seconds
                lastUpdateCheckTimer = threading.Timer(5, lambda:watchHandler.on_modified(FileSystemEvent(getSNTDirectory())))
                lastUpdateCheckTimer.start()

        if lastUpdated is None:
            print("Updating")
            lastUpdated = datetime.datetime.now()
            updateUISendFile()

def getSNTDirectory():
    home = expanduser("~")
    home += "\AppData\Roaming\Microsoft\Sticky Notes\\"
    return home

def getSNTFilePath():
    return getSNTDirectory() + "StickyNotes.snt"

def setupFileObserver():
    global observer
    global watchHandler

    if observer is not None:
        print("Stopping existing watchdog observer...")
        observer.stop()
        observer.join()

    print("Set watchdog observer on " + getSNTFilePath())
    #setup watchdog
    watchHandler = WatchEventHandler()
    observer = Observer()
    observer.schedule(watchHandler, path=getSNTDirectory(), recursive=False)
    observer.start()

def updateUISendFile():
    valid = sendFile()
    if valid == 0:
        app.infoLabel['text'] = 'Updated ' +  time.strftime("%a %H:%M:%S")
        app.infoLabel['fg'] = 'black'
    else:
        app.infoLabel['text'] = valid

    #schedule a server ping in <24hrs
    global pingServerTimer
    if pingServerTimer is not None:
        pingServerTimer.cancel()
    pingServerTimer = threading.Timer(86300, lambda:pingServerToKeepAccount())
    pingServerTimer.start()

def sendFile():

    #bring app to foreground
    #root.deiconify()

    
    home = getSNTFilePath()

    try:
    	assert olefile.isOleFile(home)
    except (AssertionError,FileNotFoundError) as e:
    	root.deiconify()
    	if app is not None:
	      app.infoLabel['text'] = "No Sticky Notes file found at " + home + ".\nYou need to run the Sticky Notes application for the first time to create a Sticky Notes file."
	      app.infoLabel['fg'] = 'red'
      #bring app to foreground
      

    ole = olefile.OleFileIO(home)

    streamList = ole.listdir()

    counter = 0

    #print(streamList)
    for streamIndex in range(len(streamList)):
        # get zeroth streams
        #print(streamIndex)
        #print(len(streamList))
        #print(streamList[streamIndex])

        if (streamList[streamIndex])[len(streamList[streamIndex])
            - 1:][0] is '0':
            #print("valid stream with directory 0: "+ streamList[streamIndex])
            # print(ole.get_size(streamList[streamIndex]))

            # create file stream
            handle = ole.openstream(streamList[streamIndex])
            text = handle.read()
            ole.close()

            #find last index of actual closed bracket pair
            textDecode = text.decode("utf-8")
            openBracketsUnclosed = -1
            for searchIndex in range(len(textDecode)):
                if textDecode[searchIndex] == '{':
                    if openBracketsUnclosed == -1:
                        openBracketsUnclosed = 0
                    openBracketsUnclosed += 1
                if textDecode[searchIndex] == '}':
                    openBracketsUnclosed -= 1
                if openBracketsUnclosed == 0:
                    #print(searchIndex)
                    break;
            # base64 encode
            base64Encoded = base64.b64encode(extract_rtf.striprtf(textDecode[textDecode.find("{"):searchIndex+1].encode("utf-8")).encode('ascii'))
            #ascii preview with viewing as string so we can see newline and carriage return
            #print(textDecode.encode('ascii'))
            # create payload
            payload = {
                'user': username,
                'passcode': passcode,
                'number': counter,
                'data': base64Encoded,
                }

            try:
                # make POST request with payload
                r = requests.post(server+'/update',data=payload,timeout=5)
                #print((r.status_code, r.reason))
                if r.text[0:1] == '0':
                    print(('Sent note at index {0} success'.format(counter)))
                    app.infoLabel['text'] = 'Updated'
                    app.infoLabel['fg'] = 'black'
                    app.setUserPass['text'] = 'Update info'
                    counter = counter + 1



                else:
                    print('Failed to update note at index {0} {0}'.format(counter, r.text))
                    app.infoLabel['text'] = r.text
                    app.infoLabel['fg'] = 'red'
                    #bring app to foreground
                    root.deiconify()
                    return r.text
            except requests.exceptions.RequestException as e:
                #messagebox.showerror("Error sending request to " + server, e)
                print(e)
                return "Update to " + server + " failed"
    return 0

class Application(tk.Frame):
    
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()

         #load user data
        credsFilepath = expanduser("~") + "\AppData\Roaming\sticky-creds"
        
        global username 
        global passcode
        userSet = False
        try: 
            f = open(credsFilepath, "rb")
            shelf = pickle.load(f)
            if 'nickname' in shelf:
                username = shelf['nickname']
                userSet = True
            if 'passcode' in shelf:
                passcode = shelf['passcode']
            f.close()
        except:
            print("file open error " + credsFilepath)
        #setup widgets
        self.createWidgets()

        if userSet is True:
            #register user in background
            t = threading.Timer(0, lambda:self.setUserPassClick())
            t.start()

    def setUserPassClick(self):
        global username 
        global passcode
        global lastUpdated
        username = self.usernameEntry.get()
        passcode = self.passcodeEntry.get()

        valid = tryToRegister()
        if valid == 0:
            self.setUserPass['text'] = 'Update info'

            
            #write user data
            credsFilepath = expanduser("~") + "\AppData\Roaming\sticky-creds"
            shelf = {}
            shelf['nickname'] = username
            shelf['passcode'] = passcode
            f = open(credsFilepath, "wb")
            pickle.dump(shelf, f)

            
            
            #send stickies to server initially
            #wait 0.5 seconds for "app" to finish loading or else ui changes will crash
            lastUpdated = datetime.datetime.now()
            s = threading.Timer(0.5, lambda:updateUISendFile())
            s.start()

            #only send on file modification
            setupFileObserver()

            #sendFileTimer = threading.Timer(0, lambda:updateUISendFile())
            #sendFileTimer.start()

            #minimize after 1 second
            t = threading.Timer(1, lambda:root.iconify())
            t.start()

        else: #registration failed
            self.setUserPass['text'] = 'Set info'
            self.infoLabel['text'] = valid
            self.infoLabel['fg'] = 'red'



    def createWidgets(self):
        global username 
        global passcode

        self.usernameLabel = tk.Label(self, text='Nickname', width=12, anchor=tk.W)
        self.usernameLabel.grid(row=0, column=0, sticky=tk.W)
        self.usernameEntry = tk.Entry(self, width=12)
        self.usernameEntry.delete(0, tk.END)
        self.usernameEntry.insert(0, username)
        self.usernameEntry.grid(row=0, column=1)

        self.passcodeLabel = tk.Label(self, text='PIN', width=12, anchor=tk.W)
        self.passcodeLabel.grid(row=1, column=0, sticky=tk.W)
        self.passcodeEntry = tk.Entry(self, width=12, show="⚿")
        self.passcodeEntry.delete(0, tk.END)
        self.passcodeEntry.insert(0, passcode)
        self.passcodeEntry.grid(row=1, column=1)

        self.setUserPass = tk.Button(self)
        self.setUserPass['text'] = 'Set info'
        self.setUserPass['command'] = self.setUserPassClick
        self.setUserPass.grid(row=2, columnspan=2, sticky=tk.N + tk.S
                              + tk.E + tk.W)

        self.infoLabel = tk.Label(self, text='No nick/pass set',
                                  justify=tk.LEFT, anchor=tk.W,
                                  wraplength=160)
        self.infoLabel.grid(row=3, column=0, rowspan=2, columnspan=2,
                            sticky=tk.N + tk.S + tk.E + tk.W)

        #function to all setUserPassClick
        def enterButtonForm(event):
            self.setUserPass['text'] = 'Registering'

            #register in timer to update UI before network connection
            def register():
                self.setUserPassClick()
                #self.setUserPass['text'] = ''

            t = threading.Timer(0, lambda:register())
            t.start()


        #bind return key to username and password entry
        self.usernameEntry.bind('<Return>', enterButtonForm)
        self.passcodeEntry.bind('<Return>', enterButtonForm)
        self.setUserPass.bind('<Return>', enterButtonForm)


root = tk.Tk()
root.title('Stickify')
root.resizable(width=tk.FALSE, height=tk.FALSE)
root.iconbitmap(resource_path("logo.ico"))

app = Application(master=root)
root.mainloop()
print("Window closed")

#Cancel pending timers so that the app will quit
if lastUpdateCheckTimer is not None:
    lastUpdateCheckTimer.cancel()
if pingServerTimer is not None:
    pingServerTimer.cancel()

#Cancel watchdog observer
observer.stop()
observer.join()

print("App quit")