# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 20:15:05 2019

@author: nicwainwright
"""

import tkinter as tk

def retrieve_input():
    inputValue = emailBox.get("1.0","end-1c")
    print(inputValue)

root = Tk()
root.title('Final Project')
content = tk.Frame(root).grid(column=0, row=0)
root.geometry('400x200')
instruction_lbl = tk.Label(content, text='Please enter your email.').grid(column=2, row=1)
emailBox= tk.Entry(content).grid(column=2, row=2)
submit_btn = tk.Button(content, text='Submit Email', command=lambda: retrieve_input()).grid(column=2, row=3)

root.mainloop()





