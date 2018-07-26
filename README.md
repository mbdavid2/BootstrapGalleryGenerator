# Bootstrap Gallery Generator
Python script to automatically create an HTML Gallery using Bootstrap with the images inside a folder.

I had to make a bootstrap gallery for work: had to write the html with more than 50 images and change each modal with the links to the previous/next images manually. On top of that, every day new images had to be added, some had to be removed, etc. So I basically wrote this script to do that automatically. :/ Here it is, if you want to use it/improve it (there's a lot of room for improvement xD)

### Requirements

```Python3```

```BeautifulSoup4``` (used to parse and modify the html file)

### Usage

To use it you will need the files generatePage.py (the script) and sliderModalNoFade.html (the template it uses for each image). These two files can be found in the "src" folder. 

As for now it works like this because I didn't want to hardcode the html in the script and this way changes can be made to the template. 

The html header for the general file, however (with the links to Bootstrap dependencies) is hardcoded in the script xD (for the moment)

Put these two files (generatePage.py and sliderModalNoFade.html) in a folder with some images and simply do:

```python generatePage.py```

If you don't have python installed or you just simply want to test it yourself, a Windows executable can be downloaded. It is found in dist/Windows/BootstrapGalleryGeneratorExample.zip (the zip contains the .exe, the .html and some royalty free images to test it) or you can only download the exe and html. 

The executable has been built using [Pyinstaller](https://www.pyinstaller.org/). With this, you don't need to have Python installed in your system to test it. Be careful with what changes you make to the html, the script uses different id's and classes to identify and change the tags and links of the different images.

### Example:

![exampleGif](https://github.com/mbdavid2/BootsrapGalleryGenerator/raw/master/doc/example.gif)

## TODO/Things that could be improved

* Overall better implementation? Idk if modals are the best option to do this
* Compress de fokin images
* Don't have the base html hardcoded?¿?
* Change the size of the modal based on the image's size (currently this can only be done adding/deleting the "modal-lg" class)
