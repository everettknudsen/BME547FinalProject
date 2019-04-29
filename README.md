# BME 547 Final Project: Image Processor [![Build Status](https://travis-ci.com/everettknudsen/BME547FinalProject.svg?branch=master)](https://travis-ci.com/everettknudsen/BME547FinalProject)

## Program Description
In this project, we created an image processor with a variety of processing types and an image database. A front-end client GUI interacts with a back-end server. The server is then responsible for processing and storing the images in a MongoDB database. The user can upload images and choose to apply an image processing method if desired. The original and processed images can later be downloaded from the image database.

### Program Overview
To start the program, run the `gui.py` code locally. A login screen will pop up on the user's desktop.
The server is housed on the virtual machine with address: `http://jek42@vcm-9066.vm.duke.edu:5000`. Upon login, the server will either create a new user or bring up the information associated with the current user.

#### Login
The user will be prompted to enter their email upon logging in. The email serves as the primary key within the MongoDB as it is a unique identifier for each user. After a new user is initiated, the server will be ready to receive images for uploading or downloading. After login, a new screen displays options to upload or download images. The user chooses an option; if they wish to perform some uploading actions, the some downloading options, they may choose the back button to toggle between modes.

#### Upload
Original image data will always be stored in the database on upload. When uploading images via an internally-delivered POST request to the server, the user can apply one of four processing methods:
1. Histogram equalization (default method)
2. Contrast stretching
3. Log compression
4. Reverse video

Image data for processed images is only stored for the chosen option. Later, the user may choose to download a processed image. We retrieve the image data and prepare it to be downloaded at that point.
After the user browses for a photo, the original photo and processed photo are displayed side-by-side. The user can then toggle between processing methods by clicking a bubble button.
Histograms of the pixel values are also displayed for uploaded images on the upload screen.
Metrics such as timestamp of upload, image size, and latency associated with processing are displayed alongside original and processed images. The user can then recall what date he or she uploaded or processed an image using this information. 

#### Image Conversion and Storage
In order to be sent to the server and database, images are passed through a series of conversions to ultimately be stored as strings. Images are initially uploaded in Python Imaging Library (PIL) format, which are easily implemented in the GUI. Subsequently, images are converted to `numpy` arrays, encoded in base64 and stored as strings.

#### Download
The download option opens a window with a dropdown menu containing the filenames of a user's uploaded images. Choosing a filename shows the original image as well as corresponding processed images, if any were created. The user can select images to download.

#### Database structure
Normal and processed images are separated from one another in the database to allow for ease of querying the database should the user wish to download a previously processed imaged in the future. It also allows for the user to retain their initial image and makes comparative display easier on the back end. Download as `.jpg`, `.png` or `.tiff` file.

`MongoDB`, an extremely popular database service, was used to construct the database for this image processor. Each user has a unique entry within the larger database based on the email. Email was chosen because it is unique to the user. For example, while could be different users with the last name Smith, only one user can have the email `stan_the_duke_fan@gmail.com`. Within each user, we keep running lists of dictionaries containing image information. Images are stored with the name of the image as a key and the image data as a value. Other keys contain metrics such as upload timestamp, latency (for processed images), file size, and processing type. Structuring the database with lists of dictionaries made it easy to append values each time a user added an image.
### Logging
All logging is saved to a file called `image_processor.log`

### Unit Testing
Unit testing is performed in `test_gui.py` and `test_image_encoding_tests.py`.

### Using the Image Processor
1. First, run the `GUI.py` script in the terminal. The login screen will appear.
2. Enter your email and press the button.
You will be asked if you would like to upload or download. Choose one.
3. If you upload as a new user, you should hit Browse and select a file. 
4. Then, choose any processing you would like to perform on the image. Make sure to wait for the processing to finish, some latency times are long. After you have chosen your processing, choose Upload to save the image to the database. 
5. After upload, you can return to the upload screen or go to the download screen. Choose one.
6. If you choose the download screen, first use the dropdown menue to select an original photo.
7. Next, select a processed image type for that original image.
8. Finally download the image in your desired format.
9. Repeat any of these actions as you desire!

### Docstrings
The sphinx docs have been generated, however, our main grpahical function that is our client, is not cooperating with the autogeneration. Even though it is docstringed in the same way, the module won't add it's functions to the docs. Please refer to the code itself to find descriptions.

### Deliverables
* [README.md](https://github.com/everettknudsen/BME547FinalProject/blob/master/README.md)
* Link to [Image Processing Server-Server On Page](http://vcm-9066.vm.duke.edu:5000/)
* Tagged project code: [BME547FinalProject](https://github.com/everettknudsen/BME547FinalProject/tree/master)
* Demo Video: [Image Processor Video](https://youtu.be/OIZSZuLOXlo)
### Future improvements
* Capability to handle multiple files or .zip files
* Decrease time latency for log compression and reverse video (better processing algorithms)

### Troubleshooting
Ensuring images were compatible with the server/database (in terms of data type and size) presented a challenge. Preliminary attempts to convert images to base64 strings were unsuccessful as the resulting strings were one-dimensional. Proper encoding to base64 strings, then decoding on download made it possible for the images to be stored.

While MongoDB is presented as "easy-to-use", we did not find this to be the case. It seemed like a better introduction might be necessary in order to really build out a fully functioning database. This is especially the case if the database will be used in commercial applications. We found there were many packages and methods of structuring your database or creating your class. Therefore, documentation is varied. It seems like people are just starting to fully embrace `pymodm` as compared to `mongoengine` or `pymongo`.

If, for some reason, the server crashes and needs to be restarted, you could log into my virtual machine using:

* Machine: `ssh jek42@vcm-9066.vm.duke.edu`
* Password: `Ji7jye7c!!!`
