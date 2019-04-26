# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 20:15:05 2019

@author: nicwainwright
"""

import tkinter as tk


def retrieve_input(entryBox):
    emailBox = entryBox
    global email
    email = emailBox.get()
    global root
    root.destroy()
    print(email)


def getEmail():
    root.title('Final Project')
    content_email = tk.Frame(root).grid(column=0, row=0)
    root.geometry('400x200')
    instruction_lbl = tk.Label(content_email, text='Please enter your email.')
    instruction_lbl.grid(column=1, row=1)
    emailBox= tk.Entry(content_email)
    emailBox.grid(column=2, row=2)
    submit_btn = tk.Button(content_email, text='Submit Email', command=lambda: retrieve_input(emailBox))
    submit_btn.grid(column=2, row=3)
    root.mainloop()


def getLoadType():
    root.title('Final Project')
    content_loadType = tk.Frame(root).grid(column=0, row=0)
    root.geometry('400x200')
    instruction_lbl = tk.Label(content_loadType, text='Would you like to upload a photo(s) or download?')
    instruction_lbl.grid(column=2, row=1)
    upload_btn = tk.Button(content_loadType, text='', command="buttonpressed")
    upload_btn.grid(column=2, row=3)
    root.mainloop()


root = Tk()
email = ''
getEmail()



