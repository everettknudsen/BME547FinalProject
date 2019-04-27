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

def destroyWindow(window):
    """Destroy the current screen, used to move between steps in GUI
    
    Args:
        window (tk.Frame): window to be destroyed before next screen
    """
    window.destroy()
    return

def retrieve_email(entryBox, window):
    """Get email string from login screen
    
    Args:
        entryBox (tk.Entry): location of typed email
        window (tk.Frame): window to be destroyed after pressing login
    
    Returns:
        email (string): email of user for logging in to database
    """
    emailBox = entryBox
    global email
    email = emailBox.get()
    # sending email to server, preps server for upload or polls for download
    # this will be primary key of database
    # for upload flow, not used until image is uploaded
    # for download flow, used immediately to populate dropdown of images
    # requests.post(local_url+'/api/login', json=email)
    destroyWindow(window)
    mainMenuScreen()
    return email




# ggets email and sends to server
def loginScreen():
    """First step/screen of GUI, prompts user for email to login
    """
    root.title('Login Screen')
    content_email = tk.Frame(root)
    content_email.grid(column=0, row=0)
    root.geometry('500x300')
    instruction_lbl = tk.Label(content_email, text='Please enter your email.')
    instruction_lbl.grid(column=1, row=1)
    emailBox= tk.Entry(content_email)
    emailBox.grid(column=2, row=2)
    submit_btn = tk.Button(content_email, text='Submit Email', command=lambda: retrieve_email(emailBox, content_email))
    submit_btn.grid(column=2, row=3)
    root.mainloop()
    return

def returnToLogin(loadWindow):
    """Helper function for a button to return to login screen
    
    Args:
        loadWindow (tk.Frame): window to be destroyed before moving to login
    """
    destroyWindow(loadWindow)
    loginScreen()
    return

# this just lets user select upload or download. does not interact with server
def mainMenuScreen():
    """Loads the main menu GUI. Options are to download, upload, or finish.
    Also has a back button to return to login screen.
    """
    root.title('Load Type')
    content_mainMenu = tk.Frame(root)
    content_mainMenu.grid(column=0, row=0)
    root.geometry('500x300')
    instruction_lbl = tk.Label(content_mainMenu, text='Would you like to upload a photo(s) or download?')
    instruction_lbl.grid(column=2, row=1, pady=20)
    upload_btn = tk.Button(content_mainMenu, text='Upload', command=lambda: uploadPressed(content_mainMenu))
    upload_btn.grid(column=2, row=3)
    download_btn = tk.Button(content_mainMenu, text='Download', command="buttonpressed")
    download_btn.grid(column=3, row=3)
    back_btn = tk.Button(content_mainMenu, text='Back to Login', command=lambda: returnToLogin(content_mainMenu), width=20)
    # add padding for button
    back_btn.grid(column=3, row=4, pady=100)
    
    root.mainloop()
    return

def uploadPressed(mainMenuWindow):
    """Helper function for a button to move from Main Menu to Upload screen
    
    Args:
        mainMenuWindow (tk.Frame): main menu window to be destroyed
        before moving to login
    """
    destroyWindow(mainMenuWindow)
    uploadScreen()
    return

def uploadScreen():
    """Upload Screen for uploading photos.
    
    Contains a browse button that opens a native browsing window to select a
    file for uploading. Once a photo is selected, it will display this photo
    along with a default processing option version of the photo. The default is
    'histogram equalization'. The user then has the option to change processing
    type, and the changes will be reflected in the visible processed photo.
    Once a final process format is selected, the user can then press 'upload'
    to upload the photo and processed photo to the server. If no photo is
    selected, an error message will appear. If successful, a success window
    will appear, prompting the user to return to Main Menu, or give option to
    upload another photo.
    """
    root.title('Uploading')
    content_upload = tk.Frame(root)
    content_upload.grid(column=0, row=0)
    root.geometry('700x300')
    instruction_lbl = tk.Label(content_upload, text='Choose a photo')
    instruction_lbl.grid(column=0, row=0, padx=20)

    # create browse button
    browse_btn = tk.Button(content_upload, text="Browse", command=lambda: load_img(), width=10)
    browse_btn.grid(column=1, row=0, padx=20)

    # create upload button
    upload_btn = tk.Button(content_upload, text="Upload", command=lambda: submit_img(content_upload), width=10)
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
    
    back_btn = tk.Button(content_upload, text='Back', command=lambda: returnToMenu_upload(content_upload), width=20)
    back_btn.grid(column=4, row=6, pady=50)
    
    def load_img():
        """Function called when 'browse' button is pressed. Opens a native
        browsing window. It will load image as described in parent function,
        uploadScreen().
        """
        nonlocal fname
        fname = askopenfilename(filetypes=(("Image Files", "*.jpeg;*.jpg;*.tiff;.*tif;*.png;"),
                                           ("All files", "*.*")))
        if fname.lower().endswith(('.jpeg','.jpg','.tiff','.tif','.png')):
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
                resizeProcess = processedImg.resize((100, int(h*(100/w))), Image.ANTIALIAS)
                imgTkprocessed = ImageTk.PhotoImage(resizeProcess) 
                showProcessed = tk.Label(content_upload, image=imgTkprocessed)
                showProcessed.image = imgTkprocessed
                showProcessed.grid(column=2, row=1, columnspan=2, rowspan=2)
            except:                     # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
        else:
            print(fname.lower(), "is not a valid photo file")
        return
    
    def returnToMenu_upload(uploadWindow):
        """Helper function for a 'back' button to move from Upload screen to
        Main Menu
    
        Args:
            uploadWindow (tk.Frame): upload window to be destroyed before
            moving to main menu
        """
        destroyWindow(uploadWindow)
        mainMenuScreen()
        return

    
    def returnToMenu_uploadSuccess(successWindow, uploadWindow):
        """Helper function for a 'return to main menu' button to move from
        Upload success screen to Main Menu
    
        Args:
            uploadWindow (tk.Frame): upload window to be destroyed before
            moving to main menu
            successWindow (tk.Frame): success window to be destroyed before
            moving to main menu
        """
        destroyWindow(successWindow)
        destroyWindow(uploadWindow)
        mainMenuScreen()
        return
    
    def returnToUpload_uploadSuccess(successWindow):
        """Helper function for a button to move back from upload success
        screen to Upload screen. Preserves previously selected image, but
        allows new images to be selected.
    
        Args:
            successWindow (tk.Frame): success window to be destroyed before
            moving to back to upload window
        """
        destroyWindow(successWindow)
        
        return
    
    def submit_img(uploadWindow):
        """Function carried out on button press of 'upload'. POSTs image data
        to server and opens a success window
        
        Args:
            uploadWindow (tk.Frame): upload window to either destroy or return
            to depending on user action after upload
        """
        if selectedPhoto:
            print('submitting')
            # POST username, image and imgProcessed, and timestamp, latency
            submitSuccess = tk.Tk()
            submitSuccess.title('Submit Success')
            submitSuccess.geometry("400x150") # (optional)    
            lbl = tk.Label(submitSuccess, text='Successfully Submitted Photo')
            lbl.grid(column=0, row=0, columnspan=2)
            lbl2 = tk.Button(submitSuccess, text='Return to Main Menu', command=lambda: returnToMenu_uploadSuccess(submitSuccess, uploadWindow), width=20)
            lbl2.grid(column=0, row=1, pady=20)
            lbl3 = tk.Button(submitSuccess, text='Upload Another Photo or Process', command=lambda: returnToUpload_uploadSuccess(submitSuccess), width=30)
            lbl3.grid(column=1, row=1, pady=20)
            
            
            submitSuccess.mainloop()
        else:
            print('havent chosen photo')
        return

    
    def updateProcessed():
        """Command for radioButton of photo processing options. Uses nonlocal
        'process' (which is changed by the currently active radioButton) and
        nonlocal 'fname' which selects the image to be processed based on
        'browse' button.
        """
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
        resizeProcess = processedImg.resize((100, int(h*(100/w))), Image.ANTIALIAS)
        
        imgTkprocessed = ImageTk.PhotoImage(resizeProcess) 
        showProcessed = tk.Label(content_upload, image=imgTkprocessed)
        showProcessed.image = imgTkprocessed
        showProcessed.grid(column=2, row=1, columnspan=2, rowspan=2)
    
        return
    
    root.mainloop()
    return  # finishes uploadScreen() function


def PILtoNumpy(pilImg):
    """Helper function to convert a PIL image format to numpy.ndarray for
    processing.
    
    Args:
        pilImg (PIL Image format image): the image to be converted
    """
    return np.array(pilImg)

def NumpytoPIL(npImg):
    """Helper function to convert numpy.ndarray formatted image to PIL format
    for processing.
    
    Args:
        npImg (numpy.ndarray): the image to be converted
    """
    rescale_out = exposure.rescale_intensity(npImg, out_range=(0, 255))
    return Image.fromarray(rescale_out.astype('uint8'))

def histEQ(pilImg):
    """Does histogram equalization processing on a photo
    
    Args:
        pilImg (PIL Image format image): Image to be processed
    """
    npImg = PILtoNumpy(pilImg)
    return NumpytoPIL(exposure.equalize_hist(npImg))

def contrastStretch(pilImg):
    """Does contrast stretch processing on a photo with percentiles 30 and 70
    
    Args:
        pilImg (PIL Image format image): Image to be processed
    """
    npImg = PILtoNumpy(pilImg)
    p30, p70 = np.percentile(npImg, (30, 70))
    return NumpytoPIL(exposure.rescale_intensity(npImg, in_range=(p30, p70)))

root = tk.Tk()
email = ''
loginScreen()


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

