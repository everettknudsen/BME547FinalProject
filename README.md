# BME 547 Final Project: Image Processor

## Program Description
Our program creates an image processor that interacts with a server and database and implements a GUI. The original images and their corresponding processed images are stored in a Mongo database. The user can upload images and choose to apply an image processing method if desired. The original and processed images can later be downloaded if desired.

### User instructions
To start the program, run the `gui.py` code locally.
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`http://jek42@vcm-9066.vm.duke.edu:5000`

#### Login
The user will be prompted to enter their email upon logging in. The email serves as the primary key within the MongoDB as it is a unique identifier for each user.

* How we handle new users

The next screen displays options to upload or download images.

#### Upload
When uploading images, the user can apply one of four processing methods:
1. Histogram equalization
2. Contrast stretching
3. Log compression
4. Reverse video

* Ability to compare original and processed images
* View histogram
* View metrics?

In order to be sent to the server and database, images are passed through a series of conversions to ultimately be stored as strings. Images are initially uploaded in Python Imaging Library (PIL) format, which are easily implemented in the GUI. Subsequently, images are converted to `numpy` arrays, encoded in base64 and stored as strings.

#### Download
The download option opens a window with a dropdown menu containing the filenames of a user's uploaded images. Choosing a filename shows the original image as well as corresponding processed images, if any were created. The user can select images to download.

The images can be downloaded as `.jpg`, `.png` or `.tiff` files.

### Database structure
* Differentiating between normal vs. processed images
* Describe database structure
* Describe the data stored: timestamp (of upload?), latency, filename, image size

### Future improvements
* Capability to handle .zip files
* Sphinx documentation

## Notes
### Troubleshooting
Ensuring images were compatible with the server/database (in terms of data type and size) presented a challenge. Preliminary attempts to convert images to base64 strings were unsuccessful as the resulting strings were one-dimensional. However, the `pickle` module was helpful in this regard by preserving the serialized structure of the images during conversion to a string format.

* Discuss `image_encoding_tests.py`