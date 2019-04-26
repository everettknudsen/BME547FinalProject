# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 20:15:05 2019

@author: nicwainwright
"""

import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror


local_url = 'http://127.0.0.1:5000'

def retrieve_email(lbl, entryBox, btn):
    emailBox = entryBox
    global email
    email = emailBox.get()
    # requests.post(local_url+'/api/login', json=email)
    destroyEmail(lbl, entryBox, btn)
    getLoadType()


# ggets email and sends to server
def getEmail():
    root.title('Login Screen')
    content_email = tk.Frame(root).grid(column=0, row=0)
    root.geometry('400x200')
    instruction_lbl = tk.Label(content_email, text='Please enter your email.')
    instruction_lbl.grid(column=1, row=1)
    emailBox= tk.Entry(content_email)
    emailBox.grid(column=2, row=2)
    submit_btn = tk.Button(content_email, text='Submit Email', command=lambda: retrieve_email(instruction_lbl, emailBox, submit_btn))
    submit_btn.grid(column=2, row=3)
    root.mainloop()


def destroyEmail(lbl, box, btn):
    lbl.destroy()
    box.destroy()
    btn.destroy()


# this just lets user select upload or download. does not interact with server
def getLoadType():
    root.title('Load Type')
    content_loadType = tk.Frame(root).grid(column=0, row=0)
    root.geometry('400x200')
    instruction_lbl = tk.Label(content_loadType, text='Would you like to upload a photo(s) or download?')
    instruction_lbl.grid(column=2, row=1)
    upload_btn = tk.Button(content_loadType, text='Upload', command=lambda: uploadPressed(instruction_lbl, upload_btn, download_btn))
    upload_btn.grid(column=2, row=3)
    download_btn = tk.Button(content_loadType, text='Download', command="buttonpressed")
    download_btn.grid(column=3, row=3)
    root.mainloop()


def destroyLoadType(lbl, up, down):
    lbl.destroy()
    up.destroy()
    down.destroy()


def uploadPressed(lbl, btn1, btn2):
    destroyLoadType(lbl, btn1, btn2)
    root.title('Uploading')
    content_upload = tk.Frame(root).grid(column=0, row=0)
    root.geometry('400x200')
    instruction_lbl = tk.Label(content_upload, text='Choose a photo')
    instruction_lbl.grid(column=2, row=1)
    
    browse_btn = tk.Button(content_upload, text="Browse", command=lambda: load_file(), width=10)
    browse_btn.grid(row=2, column=1)

    def load_file():
        fname = askopenfilename(filetypes=(("Template files", "*.tplate"),
                                           ("HTML files", "*.html;*.htm"),
                                           ("All files", "*.*") ))
        if fname:
            try:
                print("""here it comes: self.settings["template"].set(fname)""")
            except:                     # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
            return

root = tk.Tk()
email = ''
getEmail()




