# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 20:15:05 2019

@author: nicwainwright
"""


import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from PIL import Image, ImageTk
import base64
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from skimage import exposure


local_url = 'http://127.0.0.1:5000'


def retrieve_email(entryBox, window):
    emailBox = entryBox
    global email
    email = emailBox.get()
    # sending email to server, preps server for upload or polls for download
    # this will be primary key of database
    # for upload flow, not used until image is uploaded
    # for download flow, used immediately to populate dropdown of images
    # requests.post(local_url+'/api/login', json=email)
    destroyWindow(window)
    getLoadType()
    return


def destroyWindow(window):
    window.destroy()
    return


def getEmail():
    root.title('Login Screen')
    content_email = tk.Frame(root)
    content_email.grid(column=0, row=0)
    root.geometry('500x300')
    instruction_lbl = tk.Label(content_email, text='Please enter your email.')
    instruction_lbl.grid(column=1, row=1)
    emailBox = tk.Entry(content_email)
    emailBox.grid(column=2, row=2)
    submit_btn = tk.Button(content_email, text='Submit Email',
                           command=lambda: retrieve_email(emailBox,
                                                          content_email))
    submit_btn.grid(column=2, row=3)
    root.mainloop()
    return


def returnToLogin(loadWindow):
    destroyWindow(loadWindow)
    getEmail()
    return


def getLoadType():
    root.title('Load Type')
    content_loadType = tk.Frame(root)
    content_loadType.grid(column=0, row=0)
    root.geometry('500x300')
    instruction_lbl = tk.Label(content_loadType,
                               text='Would you like to upload a photo(s)'
                                    'or download?')
    instruction_lbl.grid(column=2, row=1, pady=20)
    upload_btn = tk.Button(content_loadType, text='Upload',
                           command=lambda: uploadPressed(content_loadType))
    upload_btn.grid(column=2, row=3)
    download_btn = tk.Button(content_loadType, text='Download',
                             command="buttonpressed")
    download_btn.grid(column=3, row=3)
    back_btn = tk.Button(content_loadType, text='Back to Login',
                         command=lambda: returnToLogin(content_loadType),
                         width=20)
    # add padding for button
    back_btn.grid(column=3, row=4, pady=100)
    root.mainloop()
    return


def uploadPressed(loadTypeWindow):
    destroyWindow(loadTypeWindow)
    uploadScreen()
    return


def uploadScreen():
    root.title('Uploading')
    content_upload = tk.Frame(root)
    content_upload.grid(column=0, row=0)
    root.geometry('700x300')
    instruction_lbl = tk.Label(content_upload, text='Choose a photo')
    instruction_lbl.grid(column=0, row=0, padx=20)
    # create browse button
    browse_btn = tk.Button(content_upload, text="Browse",
                           command=lambda: load_img(), width=10)
    browse_btn.grid(column=1, row=0, padx=20)
    # create upload button
    upload_btn = tk.Button(content_upload, text="Upload",
                           command=lambda: submit_img(content_upload),
                           width=10)
    upload_btn.grid(column=3, row=0, padx=20)
    # set slectedPhoto to False because no photo selected at this point
    selectedPhoto = False
    # intialize filename for photo
    fname = ''
    # create radiobuttons for what type of processing
    process = tk.StringVar()
    process.set("he")  # initialize
    he_btn = tk.Radiobutton(content_upload, text='Histogram Equalization',
                            variable=process, value='he',
                            command=lambda: updateProcessed())
    he_btn.grid(column=4, row=1)
    cs_btn = tk.Radiobutton(content_upload, text='Contrast Stretching',
                            variable=process, value='cs',
                            command=lambda: updateProcessed())
    cs_btn.grid(column=4, row=2)
    lc_btn = tk.Radiobutton(content_upload, text='Log Compression',
                            variable=process, value='lc',
                            command=lambda: updateProcessed())
    lc_btn.grid(column=4, row=3)
    rv_btn = tk.Radiobutton(content_upload, text='Reverse Video',
                            variable=process, value='rv',
                            command=lambda: updateProcessed())
    rv_btn.grid(column=4, row=4)

    back_btn = tk.Button(content_upload, text='Back',
                         command=lambda: returnToMenu_upload(content_upload),
                         width=20)
    back_btn.grid(column=4, row=6, pady=50)

    def load_img():
        nonlocal fname
        fname = askopenfilename(filetypes=(("Image Files", "*.jpeg;*.jpg;"
                                            "*.tiff;.*tif;*.png;"),
                                           ("All files", "*.*")))
        if fname.lower().endswith(('.jpeg', '.jpg', '.tiff', '.tif', '.png')):
            try:
                img = Image.open(fname)
                w, h = img.size
                resized = img.resize((100, int(h*(100/w))), Image.ANTIALIAS)
                imgTk = ImageTk.PhotoImage(resized)
                showUpload = tk.Label(content_upload, image=imgTk)
                showUpload.image = imgTk
                showUpload.grid(column=0, row=1, columnspan=2, rowspan=2)
                nonlocal selectedPhoto
                selectedPhoto = True
                # also set initial processed photo to histogram
                processedImg = histEQ(img)
                w, h = processedImg.size
                resizeProcess = processedImg.resize((100, int(h*(100/w))),
                                                    Image.ANTIALIAS)
                imgTkprocessed = ImageTk.PhotoImage(resizeProcess)
                showProcessed = tk.Label(content_upload, image=imgTkprocessed)
                showProcessed.image = imgTkprocessed
                showProcessed.grid(column=2, row=1, columnspan=2, rowspan=2)
            except:                     # <- naked except is a bad idea
                showerror("Open Source File",
                          "Failed to read file\n'%s'" % fname)
        else:
            print(fname.lower(), "is not a valid photo file")
        return

    def returnToMenu_upload(uploadWindow):
        destroyWindow(uploadWindow)
        getLoadType()
        return

    def returnToMenu_uploadSuccess(successWindow, uploadWindow):
        destroyWindow(successWindow)
        destroyWindow(uploadWindow)
        getLoadType()
        return

    def returnToUpload_uploadSuccess(successWindow):
        destroyWindow(successWindow)
        return

    def submit_img(uploadWindow):
        if selectedPhoto:
            print('submitting')
            # POST username, image and imgProcessed, and timestamp, latency
            submitSuccess = tk.Tk()
            submitSuccess.title('Submit Success')
            submitSuccess.geometry("400x150")  # (optional)
            lbl = tk.Label(submitSuccess, text='Successfully Submitted Photo')
            lbl.grid(column=0, row=0, columnspan=2)
            lbl2 = tk.Button(submitSuccess, text='Return to Main Menu',
                             command=lambda:
                                 returnToMenu_uploadSuccess(submitSuccess,
                                                            uploadWindow),
                             width=20)
            lbl2.grid(column=0, row=1, pady=20)
            lbl3 = tk.Button(submitSuccess, text='Upload Another Photo or'
                             'Process', command=lambda:
                                 returnToUpload_uploadSuccess(submitSuccess),
                                 width=30)
            lbl3.grid(column=1, row=1, pady=20)
            submitSuccess.mainloop()
        else:
            print('havent chosen photo')
        return

    def updateProcessed():
        nonlocal process
        nonlocal fname

        command = process.get()
        processedImg = ''
        if command == 'he':
            img = Image.open(fname)
            processedImg = histEQ(img)
        elif command == 'cs':
            img = Image.open(fname)
            processedImg = contrastStretch(img)
        else:
            print('no process selected')
            return
        w, h = processedImg.size
        resizeProcess = processedImg.resize((100, int(h*(100/w))),
                                            Image.ANTIALIAS)

        imgTkprocessed = ImageTk.PhotoImage(resizeProcess)
        showProcessed = tk.Label(content_upload, image=imgTkprocessed)
        showProcessed.image = imgTkprocessed
        showProcessed.grid(column=2, row=1, columnspan=2, rowspan=2)
        return
    root.mainloop()
    return


def PILtoNumpy(pilImg):
    return np.array(pilImg)


def NumpytoPIL(npImg):
    rescale_out = exposure.rescale_intensity(npImg, out_range=(0, 255))
    return Image.fromarray(rescale_out.astype('uint8'))


def histEQ(pilImg):
    npImg = PILtoNumpy(pilImg)
    return NumpytoPIL(exposure.equalize_hist(npImg))


def contrastStretch(pilImg):
    npImg = PILtoNumpy(pilImg)
    p30, p70 = np.percentile(npImg, (30, 70))
    return NumpytoPIL(exposure.rescale_intensity(npImg, in_range=(p30, p70)))


root = tk.Tk()
email = ''
getEmail()


# uncomment following block of code to prove that contrast stretch and
# histogram equalization work!
"""
filepath = 'C:/Users/wainw/Pictures/pass.jpg'
img = Image.open(filepath)
fig0 = plt.figure()
plt.imshow(PILtoNumpy(img))
fig1 = plt.figure()
plt.imshow(PILtoNumpy(contrastStretch(img)))
fig2 = plt.figure()
plt.imshow(PILtoNumpy(histEQ(img)))
"""
