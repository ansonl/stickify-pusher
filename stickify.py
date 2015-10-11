#!/usr/bin/python
# -*- coding: utf-8 -*-

#pyinstaller --onefile --noconsole --clean stickify.py
#pyinstaller --onefile --noconsole --clean --icon logo.ico stickify.py
import olefile

import sys
import os.path
import re
import requests
import base64, zlib
import time
import threading
import tempfile
from os.path import expanduser

import tkinter as tk
from tkinter import messagebox

import pickle

username = ''
passcode = ''

port = '8080'
server = 'http://mich302csd17u' + ':' + '8080'
server = 'https://stickify.herokuapp.com'

sendFileTimer = None

updateLoop = False

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

def updateUISendFile():
    valid = sendFile()
    if valid == 0:
        app.infoLabel['text'] = 'Updated ' +  time.strftime("%a %H:%M:%S")
        app.infoLabel['fg'] = 'black'
    else:
        self.infoLabel['text'] = valid

def sendFile():
    global sendFileTimer
    sendFileTimer = threading.Timer(10, updateUISendFile)
    sendFileTimer.start()

    #bring app to foreground
    #root.deiconify()

    
    home = expanduser("~")
    home += "\AppData\Roaming\Microsoft\Sticky Notes\StickyNotes.snt"

    assert olefile.isOleFile(home)

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
            #print text
            # base64 encode
            base64Encoded = base64.b64encode(text)

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
                    print('Fail update note at index {0} {0}'.format(counter, r.text))
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
            self.setUserPassClick()

    def setUserPassClick(self):
        global username 
        global passcode
        username = self.usernameEntry.get()
        passcode = self.passcodeEntry.get()

        global sendFileTimer
        if sendFileTimer is not None:
            print("Cancelled existing timer")
            sendFileTimer.cancel()

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

            sendFileTimer = threading.Timer(0, lambda:updateUISendFile())
            sendFileTimer.start()

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
        self.passcodeEntry = tk.Entry(self, width=12)
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
                                  wraplength=128)
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



#make transparent app icon on the fly http://stackoverflow.com/a/18277350
#if building on OSX, you may need to comment this out
ICON = zlib.decompress(base64.b64decode('eJxjYGAEQgEBBiDJwZDBy'
    'sAgxsDAoAHEQCEGBQaIOAg4sDIgACMUj4JRMApGwQgF/ykEAFXxQRc='))
_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, 'wb') as icon_file:
    icon_file.write(ICON)
root.iconbitmap(default=ICON_PATH)

app = Application(master=root)
app.mainloop()

print("Window closed, cleaning up timer")
if sendFileTimer is not None:
    print("Cancelled existing timer")
    sendFileTimer.cancel()
print("App quit")
