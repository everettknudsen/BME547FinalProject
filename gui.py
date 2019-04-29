# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 20:15:05 2019

@author: nicwainwright
"""
# server
import pymongo
import requests
# graphics
import tkinter as tk
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.messagebox import showerror
# image processing
from PIL import Image, ImageTk
from skimage import exposure
import image_encoding_tests as CODER
import log_compression as logger
# misc
import os
import numpy as np
import logging
import datetime


global email
local_url = 'http://127.0.0.1:5000'
# server = 'http://jek42@vcm-9066.vm.duke.edu:5000'


def json_serial_date(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def destroyWindow(window):
    """Destroy the current screen, used to move between steps in GUI

    Args:
        window (tk.Frame): window to be destroyed before next screen
    """
    window.destroy()


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
    requests.post(local_url + '/api/login', json=email)
    # run this to confirm full user list
    # requests.post(local_url + '/api/logConfirm', json=email)
    destroyWindow(window)
    mainMenuScreen()
    return email


def loginScreen():
    """First step/screen of GUI, prompts user for email to login
    """
    root.title('Login Screen')
    content_email = tk.Frame(root)
    content_email.grid(column=0, row=0)
    root.geometry('500x300')
    welcome_lbl = tk.Label(content_email, text='Welcome!')
    welcome_lbl.grid(column=0, row=1, columnspan=2, pady=10, padx=60)
    welcome_lbl.config(font=("Courier", 44))
    instruction_lbl = tk.Label(content_email, text='Please enter your email.')
    instruction_lbl.grid(column=0, row=2, columnspan=2, pady=10, padx=190)
    emailBox = tk.Entry(content_email)
    emailBox.grid(column=0, row=3, columnspan=2)
    submit_btn = tk.Button(content_email, text='Submit Email',
                           command=lambda: retrieve_email(emailBox,
                                                          content_email))
    submit_btn.grid(column=0, row=4, columnspan=2, pady=10, padx=190)
    root.mainloop()


def returnToLogin(loadWindow):
    """Helper function for a button to return to login screen

    Args:
        loadWindow (tk.Frame): window to be destroyed before moving to login
    """
    destroyWindow(loadWindow)
    loginScreen()


def mainMenuScreen():
    """Loads the main menu GUI. Options are to download, upload, or finish.
    Also has a back button to return to login screen.
    """
    root.title('Load Type')
    content_mainMenu = tk.Frame(root)
    content_mainMenu.grid(column=0, row=0)
    root.geometry('500x300')
    instruction_lbl = tk.Label(content_mainMenu,
                               text='Would you like to upload a'
                                    ' photo(s) or download?')
    instruction_lbl.grid(column=0, row=0, pady=30, columnspan=4, padx=120)
    upload_btn = tk.Button(content_mainMenu, text='Upload',
                           command=lambda: uploadPressed(content_mainMenu))
    upload_btn.grid(column=1, row=2)
    download_btn = tk.Button(content_mainMenu, text='Download',
                             command=lambda: downloadPressed(content_mainMenu))
    download_btn.grid(column=2, row=2)
    back_btn = tk.Button(content_mainMenu, text='Back to Login',
                         command=lambda: returnToLogin(content_mainMenu))
    # add padding for button
    back_btn.grid(column=2, row=6, pady=100)
    root.mainloop()


def uploadPressed(mainMenuWindow):
    """Helper function for a button to move from Main Menu to Upload screen

    Args:
        mainMenuWindow (tk.Frame): main menu window to be destroyed
        before moving to uploadScreen()
    """
    destroyWindow(mainMenuWindow)
    uploadScreen()


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
    img = ''
    processedImg = ''
    showProcessed = ''
    imgTkProcessed = ''
    latency = 0.0
    w = 0
    h = 0
    w2 = 0
    h2 = 0

    # create radiobuttons for what type of processing
    process = tk.StringVar(content_upload)
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
    back_btn.grid(column=0, row=5, pady=10)

    def load_img():
        """Function called when 'browse' button is pressed. Opens a native
        browsing window. It will load image as described in parent function,
        uploadScreen().
        """
        nonlocal fname, img, processedImg, latency, w, h, w2, h2
        nonlocal showProcessed, imgTkProcessed
        fname = askopenfilename(filetypes=(("Image Files", "*.jpeg;*.jpg;"
                                            "*.tiff;.*tif;*.png;"),
                                           ("All files", "*.*")))

        if fname.lower().endswith(('.jpeg', '.jpg', '.tiff', '.tif', '.png')):
            nonlocal processedImg
            try:
                img = Image.open(fname)
                w, h = img.size
                resized = img.resize((100, int(h*(100/w))), Image.ANTIALIAS)
                imgTk = ImageTk.PhotoImage(resized)
                showUpload = tk.Label(content_upload, image=imgTk)
                showUpload.image = imgTk
                showUpload.grid(column=0, row=1, columnspan=2, rowspan=2)
                sizeStr = 'w:' + str(w) + 'h:' + str(h)
                size_lbl = tk.Label(content_upload, text=sizeStr)
                size_lbl.text = sizeStr
                size_lbl.grid(column=0, row=3, columnspan=2)
                rightNow = datetime.datetime.now()
                time_lbl = tk.Label(content_upload, text=str(rightNow))
                time_lbl.text = rightNow
                time_lbl.grid(column=0, row=4, columnspan=2)
                nonlocal selectedPhoto
                selectedPhoto = True
                # also set initial processed photo to histogram
                preProcessTime = datetime.datetime.now()
                processedImg = histEQ(img)
                postProcessTime = datetime.datetime.now()
                latency = (postProcessTime-preProcessTime).total_seconds()
                w2, h2 = processedImg.size
                resizeProcess = processedImg.resize((100, int(h*(100/w))),
                                                    Image.ANTIALIAS)
                imgTkprocessed = ImageTk.PhotoImage(resizeProcess)
                showProcessed = tk.Label(content_upload, image=imgTkprocessed)
                showProcessed.image = imgTkprocessed
                showProcessed.grid(column=2, row=1, columnspan=2, rowspan=2)
                sizeStr_pro = 'w: ' + str(w2) + ' h:' + str(h2)
                size_lbl2 = tk.Label(content_upload, text=sizeStr_pro)
                size_lbl2.text = sizeStr_pro
                size_lbl2.grid(column=2, row=3, columnspan=2)
                rightNow2 = datetime.datetime.now()
                time_lbl2 = tk.Label(content_upload, text=str(rightNow2))
                time_lbl2.text = rightNow2
                time_lbl2.grid(column=2, row=4, columnspan=2)
                latStr = 'latency:' + str(round(latency, 2)) + ' sec'
                lat_lbl = tk.Label(content_upload, text=latStr)
                lat_lbl.text = latStr
                lat_lbl.grid(column=2, row=5, columnspan=2)
            except:                     # <- naked except is a bad idea
                showerror("Open Source File",
                          "Failed to read file\n'%s'" % fname)
                logging.error('Failed to read image file.')
        else:
            print(fname.lower(), "is not a valid photo file")

    def returnToMenu_upload(uploadWindow):
        """Helper function for a 'back' button to move from Upload screen to
        Main Menu

        Args:
            uploadWindow (tk.Frame): upload window to be destroyed before
            moving to main menu
        """
        destroyWindow(uploadWindow)
        mainMenuScreen()

    def returnToMenu_uploadSucc(successWindow, uploadWindow):
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

    def returnToUpload_upSucc(successWindow):
        """Helper function for a button to move back from upload success
        screen to Upload screen. Preserves previously selected image, but
        allows new images to be selected.

        Args:
            successWindow (tk.Frame): success window to be destroyed before
            moving to back to upload window
        """
        destroyWindow(successWindow)

    def submit_img(uploadWindow):
        """Function carried out on button press of 'upload'. POSTs image data
        to server and opens a success window

        Args:
            uploadWindow (tk.Frame): upload window to either destroy or return
            to depending on user action after upload
        """
        nonlocal fname, img, processedImg, latency, process, w, h, w2, h2
        if selectedPhoto:
            print('submitting')
            # POST username, image and imgProcessed, and timestamp, latency

            img_name = os.path.basename(fname)
            # nameNoExt = os.path.splitext(img_name)[0]
            # ext = os.path.splitext(img_name)[1]
            # img_name_processed = nameNoExt + '_' + process.get() + ext

            # print(np.asarray(img).nbytes)
            # create normal package
            # print(sys.getsizeof(im2str(img)))
            currTime = datetime.datetime.now()
            serialDate = json_serial_date(currTime)
            enc_img = CODER.encode_image_as_b64(np.asarray(img))
            upload_package = {'img_name': img_name, 'img_data': enc_img,
                              'img_size': [w, h],
                              'timestamp': serialDate}
            try:
                r = requests.post(local_url+'/api/'+email+'/post_new_image',
                                  json=upload_package)
                print("response", r)
                # create processed package
                npIMGshort = np.asarray(processedImg)
                enc_img_pro = CODER.encode_image_as_b64(npIMGshort)
                upload_package_processed = {'img_name': img_name,
                                            'img_data_processed': enc_img_pro,
                                            'img_size_processed': [w2, h2],
                                            'process_type': process.get(),
                                            'timestamp': serialDate,
                                            'latency': latency}
                r2 = requests.post(local_url+'/api/'+email+'/post_new_'
                                   'image_pro',
                                   json=upload_package_processed)
                print("response", r2)
                if (r.content == 500 or r2.content == 500):
                    print("failed to add to MONGO, try again.")
                else:
                    submitSuccess = tk.Toplevel(content_upload)
                    # submitSucess.geometry("400x150")  # (optional)
                    lbl_suc = tk.Label(submitSuccess,
                                       text='Successfully Submitted Photo')
                    lbl_suc.grid(column=0, row=0, columnspan=2)
                    lbl2_suc = tk.Button(submitSuccess, text='Return t'
                                         'o Main Menu',
                                         width=20, command=lambda:
                                         returnToMenu_uploadSucc(submitSuccess,
                                                                 uploadWindow))
                    lbl2_suc.grid(column=0, row=1, pady=20)
                    lbl3_suc = tk.Button(submitSuccess, text='Upload Another'
                                         'Photo or Process', width=30,
                                         command=lambda:
                                         returnToUpload_upSucc(submitSuccess))
                    lbl3_suc.grid(column=1, row=1, pady=20)
            except pymongo.errors.WriteError:
                print('database full')
                logging.error('Database full.')
        else:
            print('havent chosen photo')

    def updateProcessed():
        """Command for radioButton of photo processing options. Uses nonlocal
        'process' (which is changed by the currently active radioButton) and
        nonlocal 'fname' which selects the image to be processed based on
        'browse' button.
        """
        nonlocal process, imgTkProcessed, showProcessed, processedImg
        nonlocal fname
        nonlocal latency, w, h, w2, h2

        processType = process.get()
        processedImg = ''
        if processType == 'he':
            img = Image.open(fname)
            preProcessTime = datetime.datetime.now()
            processedImg = histEQ(img)
            postProcessTime = datetime.datetime.now()
            latency = (postProcessTime-preProcessTime).total_seconds()
        elif processType == 'cs':
            img = Image.open(fname)
            preProcessTime = datetime.datetime.now()
            processedImg = contrastStretch(img)
            postProcessTime = datetime.datetime.now()
            latency = (postProcessTime-preProcessTime).total_seconds()
        elif processType == 'lc':
            img = Image.open(fname)
            preProcessTime = datetime.datetime.now()
            processedImg = logCompression(img)
            postProcessTime = datetime.datetime.now()
            latency = (postProcessTime-preProcessTime).total_seconds()
        elif processType == 'rv':
            img = Image.open(fname)
            preProcessTime = datetime.datetime.now()
            processedImg = reverseVideo(img)
            postProcessTime = datetime.datetime.now()
            latency = (postProcessTime-preProcessTime).total_seconds()
        else:
            print('no process selected')
            return
        w2, h2 = processedImg.size
        resizeProcess = processedImg.resize((100, int(h*(100/w))),
                                            Image.ANTIALIAS)
        imgTkprocessed = ImageTk.PhotoImage(resizeProcess)
        showProcessed = tk.Label(content_upload, image=imgTkprocessed)
        showProcessed.image = imgTkprocessed
        showProcessed.grid(column=2, row=1, columnspan=2, rowspan=2)
        rightNow2 = datetime.datetime.now()
        time_lbl2 = tk.Label(content_upload, text=str(rightNow2))
        time_lbl2.text = rightNow2
        time_lbl2.grid(column=2, row=4, columnspan=2)
        latStr = 'latency: ' + str(round(latency, 2)) + ' sec'
        print(latStr)
        lat_lbl = tk.Label(content_upload, text=latStr)
        lat_lbl.text = latStr
        lat_lbl.grid(column=2, row=5, columnspan=2)

    root.mainloop()


def downloadPressed(mainMenuWindow):
    """Helper function for a button to move from Main Menu to download screen

    Args:
        mainMenuWindow (tk.Frame): main menu window to be destroyed
        before moving to downloadScreen()
    """
    destroyWindow(mainMenuWindow)
    downloadScreen()
    return


def downloadScreen():
    """Download Screen for downloading photos.

    Contains an initial dropdown menu that is populated by the unique original
    images that a user has uploaded. Once they select a normal_image, that
    image will be displayed and then another dropdown list will appear,
    populated by the versions of the original image that the use has
    processed during uploads. Once selected, the processed image will appear as
    well. Both images have individual download buttons that prompt a folder to
    download to using the image's filename. On download press, a success
    window will appear if successful and prompt the user if they wish to return
    to menu or download another image.
    """
    # carry out a GET request based on username to get list of photo originals
    root.title('Downloading')
    content_download = tk.Frame(root)
    content_download.grid(column=0, row=0)
    root.geometry('800x300')

    instruction_lbl = tk.Label(content_download,
                               text='Choose a uploaded photo')
    instruction_lbl.grid(column=0, row=0, padx=20, pady=10)

    r = requests.get(local_url+'/api/'+email+'/get_image_list')
    imageList = r.json()

    imageName_normal = tk.StringVar()

    # if no images for this user
    if not imageList:
        choices = {'no images'}
        imageName_normal.set('no_images')
    else:
        choices = imageList
        imageName_normal.set(imageList[0])  # set default option

    # create dropdown menu that create a new menu for processed options
    imageMenu = tk.OptionMenu(content_download, imageName_normal, *choices,
                              command=lambda _: processedOptions())
    imageMenu.grid(column=1, row=0, pady=10)

    # create a back button
    back_btn = tk.Button(content_download, text='Back to Menu', width=20,
                         command=lambda:
                             returnToMenu_download(content_download))
    # add padding for button
    back_btn.grid(column=0, row=6, pady=30)

    # initialize width and height variables
    w = 0
    h = 0
    w2 = 0
    h2 = 0

    # when dropdown value changes, do this
    def change_dropdown(*args):
        """Function called when dropdown of image is changed. Displays the
        image.

        Args:
            *args: takes tk.OptionMenu values and updates correspondingly
        """
        nonlocal imageName_normal, w, h
        """
        dirPath = 'C:/Users/wainw/Pictures/'
        filename = imageName_normal.get()
        fname = dirPath + filename
        """
        imName = imageName_normal.get()
        rDown = requests.get(local_url + '/api/' + email + '/'
                             '' + imName + '/get_image')
        imgStr_download = rDown.json()
        decodedDL_norm = CODER.decode_image_from_b64(imgStr_download)
        PILdl_norm = Image.fromarray(decodedDL_norm)
        # also get timestamp
        rTim = requests.get(local_url + '/api/' + email + '/'
                            '' + imName + '/get_time')
        timestamp = rTim.json()
        try:
            w, h = PILdl_norm.size
            resized = PILdl_norm.resize((100, int(h*(100/w))),
                                        Image.ANTIALIAS)
            imgTk = ImageTk.PhotoImage(resized)
            showDownload = tk.Label(content_download, image=imgTk)
            showDownload.image = imgTk
            showDownload.grid(column=0, row=1, columnspan=2, rowspan=2)
            sizeStr_dl = 'w:' + str(w) + ' h:' + str(h)
            size_lbl_dl = tk.Label(content_download, text=sizeStr_dl)
            size_lbl_dl.grid(column=0, row=3, columnspan=2)
            time_lbl = tk.Label(content_download, text=str(timestamp))
            time_lbl.text = timestamp
            time_lbl.grid(column=0, row=4, columnspan=2)
            # create download buttons
            download_btn_1 = tk.Button(content_download, text='Download '
                                                              'Original',
                                       width=20, command=lambda:
                                           downloadPhoto(content_download,
                                                         PILdl_norm, imName))
            download_btn_1.grid(column=0, row=6, pady=10)
        except:  # <- naked except is a bad idea
            showerror("Open Source File", "Failed to read file\n'%s'" % imName)
            logging.error('Failed to read image file.')
        return

    # link function to change dropdown
    imageName_normal.trace('w', change_dropdown)

    def downloadPhoto(downloadWindow, img, filename):
        """

        Args:
            downloadWindow (tk.Frame): frame to be destroyed potentially
            img (PIL Image Format): image to be downloaded
            filename (str): string for corresponding image that will be the
            savefile name
        """
        # nameNoExt = os.path.splitext(imageName_normal.get())[0]
        # ext = os.path.splitext(imageName_normal.get())[1]
        saveDir = askdirectory()
        img.save(saveDir + '/' + filename)
        downloadSuccess = tk.Toplevel(downloadWindow)
        # submitSucess.geometry("400x150")  # (optional)
        lbl_down = tk.Label(downloadSuccess,
                            text='Successfully Downloaded Photo: ' + filename)
        lbl_down.grid(column=0, row=0, columnspan=2)
        lbl2_down = tk.Button(downloadSuccess, text='Return to Main Menu',
                              width=20, command=lambda:
                              returnToMenu_downloadSucc(downloadSuccess,
                                                        downloadWindow))
        lbl2_down.grid(column=0, row=1, pady=20)
        lbl3_down = tk.Button(downloadSuccess, text='Download Another'
                              'Photo or Process', width=30,
                              command=lambda:
                              returnToDownload_downloadSucc(downloadSuccess))
        lbl3_down.grid(column=1, row=1, pady=20)

    def processedOptions():
        """Populates the second OptionMenu dropdown list using a list of
        processed images. Performs a GET request to get the list of images
        using email and image_name
        """
        nonlocal imageName_normal
        normImg_str = imageName_normal.get()
        nameNoExt = os.path.splitext(normImg_str)[0]
        ext = os.path.splitext(normImg_str)[1]
        # find in list user photos key.lower().startswith('imageName_normal')
        # use this sublist to populate choicesProcessed dictionary
        # secondary dropdown that populates once normal image selected
        # get all images names that start with imageName_normal
        rr = requests.get(local_url+'/api/' + email + '/get_image_list_pro'
                          '_' + normImg_str)
        processedList = rr.json()
        displayList = [nameNoExt+'_'+item+ext for item in processedList]
        processType = tk.StringVar()
        # if no processed images for this user
        if not processedList:
            choicesProcessed = {'no images'}
            processType.set('no_images')
        else:
            choicesProcessed = displayList
            processType.set(displayList[0])  # set default option

        # give further instructions
        instruction_lbl2 = tk.Label(content_download,
                                    text='Compare to a processed version')
        instruction_lbl2.grid(column=2, row=0, padx=20, pady=10)
        # create dropdown menu
        processedMenu = tk.OptionMenu(content_download, processType,
                                      *choicesProcessed)
        processedMenu.grid(column=3, row=0, pady=10)

        # when dropdown value changes, do this
        def change_dropdownProcessed(*args):
            """Function called when dropdown of image is changed. Displays the
            image. Uses a get request with email, image_name, and processType
            to determine which img_data to acquire

            Args:
                *args: takes tk.OptionMenu values and updates correspondingly
            """
            nonlocal processType, w2, h2, imageName_normal
            imName = imageName_normal.get()
            nameNoExt = os.path.splitext(imName)[0]
            ext = os.path.splitext(imName)[1]
            process = processType.get().replace(nameNoExt+'_', '')
            process = process.replace(ext, '')
            procName = nameNoExt+'_'+process+ext
            # print(procName)  # this is correct . displays im1_rv.jpg
            rDown_pro = requests.get(local_url + '/api/' + email + '/'
                                     '' + imName+'/get_image_pro_'+process)
            imgStr_download_pro = rDown_pro.json()
            decodedDL = CODER.decode_image_from_b64(imgStr_download_pro)
            PILdl = Image.fromarray(decodedDL)
            imgStr_download_pro = rDown_pro.json()
            # also get timestamp
            rTim = requests.get(local_url + '/api/' + email + '/'
                                '' + imName + '/get_time_pro_' + process)
            timestamp2 = rTim.json()
            # also get latency
            rLat = requests.get(local_url+'/api/'+email+'/'+imName+'/'
                                'get_latency_'+process)
            oneLatency = rLat.json()
            try:
                w2, h2 = PILdl.size
                resized_pro = PILdl.resize((100, int(h2*(100/w2))),
                                           Image.ANTIALIAS)
                imgTk_pro = ImageTk.PhotoImage(resized_pro)
                showDownload_pro = tk.Label(content_download, image=imgTk_pro)
                showDownload_pro.image = imgTk_pro
                showDownload_pro.grid(column=2, row=1, columnspan=2, rowspan=2)
                sizeStr2_dl = 'w:' + str(w2) + ' h:' + str(h2)
                size_lbl2_dl = tk.Label(content_download, text=sizeStr2_dl)
                size_lbl2_dl.grid(column=2, row=3, columnspan=2)
                time_lbl2 = tk.Label(content_download, text=str(timestamp2))
                time_lbl2.text = timestamp2
                time_lbl2.grid(column=2, row=4, columnspan=2)
                latStr_dl = 'latency: ' + str(round(oneLatency, 2)) + ' sec'
                lat_lbl_dl = tk.Label(content_download, text=latStr_dl)
                lat_lbl_dl.text = latStr_dl
                lat_lbl_dl.grid(column=2, row=5, columnspan=2)
                # create download buttons
                download_btn_2 = tk.Button(content_download, text='Download '
                                                                  'Processed',
                                           width=20, command=lambda:
                                               downloadPhoto(content_download,
                                                             PILdl, procName))
                download_btn_2.grid(column=2, row=6, pady=10)
            except:  # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read f"
                          "ile\n'%s'" % procName)
                logging.error('Failed to read image file.')
            return

        # link function to change dropdown
        processType.trace('w', change_dropdownProcessed)
        return

    def returnToMenu_download(downloadWindow):
        """Helper function for a 'back' button to move from Download screen to
        Main Menu

        Args:
            downloadWindow (tk.Frame): download window to be destroyed before
            moving to main menu
        """
        destroyWindow(downloadWindow)
        mainMenuScreen()
        return

    def returnToMenu_downloadSucc(successWindow, downloadWindow):
        """Helper function for a 'return to main menu' button to move from
        Download success screen to Main Menu

        Args:
            downloadWindow (tk.Frame): download window to be destroyed before
            moving to main menu
            successWindow (tk.Frame): success window to be destroyed before
            moving to main menu
        """
        destroyWindow(successWindow)
        destroyWindow(downloadWindow)
        mainMenuScreen()

    def returnToDownload_downloadSucc(successWindow):
        """Helper function for a button to move back from download success
        screen to Download screen. Preserves previously selected images, but
        allows new images to be selected.

        Args:
            successWindow (tk.Frame): success window to be destroyed before
            moving to back to download window
        """
        destroyWindow(successWindow)

    root.mainloop()
    return


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


def logCompression(pilImg):
    """Does log compression processing on a photo

    Args:
        pilImg (PIL Image format image): Image to be processed
    """
    npImg = PILtoNumpy(pilImg)
    c = 255 / (np.log10(1 + np.amax(npImg)))
    for all_pixels in np.nditer(npImg, op_flags=['readwrite']):
        all_pixels[...] = c * np.log10(1 + all_pixels)
    return NumpytoPIL(npImg)


def reverseVideo(pilImg):
    """Does reverse video (negative) processing on a photo

    Args:
        pilImg (PIL Image format image): Image to be processed
    """
    npImg = PILtoNumpy(pilImg)
    for all_pixels in np.nditer(npImg, op_flags=['readwrite']):
        all_pixels[...] = 255 - all_pixels
    return NumpytoPIL(npImg)


email = ''
root = ''
if __name__ == "__main__":
    root = tk.Tk()
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
