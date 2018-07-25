import os
import os.path
from bs4 import BeautifulSoup

useFile = False

def fillImageLink(soup, imgFile):
	for img in soup.find_all(id = 'imageLink'):
			img['src'] = imgFile


def fillModalIDs(soup, modal):
	idModal = "modal" + str(modal)

	# Current modal link
	for a in soup.find_all(id = "currentModal"):
		a['href'] = "#" + idModal

	# Current modal id
	for div in soup.find_all(id = 'myModal'):
		div['id'] = idModal
		div['aria-labelledby'] = idModal

	# Image data target
	for img in soup.find_all(class_ = 'image-inline'):
		img['data-target'] = "#" + idModal


def fillArrowIDs(soup, modal, flag):
	# Previous and next modals links
	nextM = modal+1
	previousM = modal-1
	if flag == 0: # Last
		nextM = 0
	elif flag != 1: # First
		previousM = flag - 1

	for a in soup.find_all(id = "previous"):
		a['href'] = "#modal" + str(previousM)

	for a in soup.find_all(id = "next"):
		a['href'] = "#modal" + str(nextM)


def fillCaptionName(soup, imgFile):
	# For now just put the file's name in it
	# Change title based on file name
	result = soup.find(class_ = "caption")
	result.string.replace_with(imgFile)


def getIndividualImageHTML(currentFile, modal, flag, imgFile):
    try:
        elementHTML = open("sliderModalNoFade.html", "r")
        elementSoup = BeautifulSoup(elementHTML, 'html.parser')
        fillModalIDs(elementSoup, modal)
        fillCaptionName(elementSoup, imgFile)
        fillArrowIDs(elementSoup, modal, flag)
        fillImageLink(elementSoup, imgFile)

        contents = "\n" + elementSoup.prettify() + "\n"
        currentFile.write(str(contents))
    except:
        print("The sliderModalNoFade.html file could not be found")


def openRowHTML(currentFile):
	htmlCode = "<div class=\"row\">"
	currentFile.write(htmlCode)


def closeDivHTML(currentFile):
	htmlCode = "</div>\n"
	currentFile.write(htmlCode)


def getCurrentFlag(modal, length):
	# First -> flag = number of files
	# Normal -> flag = 1
	# Last -> flag = 0
	if modal == length - 1:
		return 0
	elif modal == 0:
		return length
	else:
		return 1


def filterList(dirFiles):
	imgExtensions = ('.ras', '.xwd', '.bmp', '.jpe', '.jpg', '.jpeg', '.xpm', '.ief', '.pbm', '.tif', '.gif', '.ppm', '.xbm', '.tiff', '.rgb', '.pgm', '.png', '.pnm')
	func = (lambda file: any([file.endswith(x) for x in imgExtensions]))
	newList = filter(func, dirFiles)
	return list(newList)


def traverseFolder(currentFile):
	modal = 0
	
	openRowHTML(currentFile)

	imageList = filterList(os.listdir())
	length = len(imageList)
	for file in imageList:
		if modal%3 == 0 and modal != 0:
			closeDivHTML(currentFile)
			openRowHTML(currentFile)
		flag = getCurrentFlag(modal, length)
		getIndividualImageHTML(currentFile, modal, flag, file)
		modal += 1
	
	closeDivHTML(currentFile)

	# There should be more than 1 picture for the flag to work properly
	if modal <= 1:
		print("Warning, only one image => the previous/next navigation might not work properly")


def askQuestion(question):
	ans = str(input(question + " (y/n): "))
	if ans == "y" or ans == "Y":
		return True
	elif ans == "n" or ans == "N":
		return False
	else:
		askQuestion()


def buildFullHTML(currentFile):
	htmlCodeHeader = """
	<!DOCTYPE html>
	<html>
		<head>
		<title>Generated Gallery</title>
		  <meta charset="utf-8">
		  <meta name="viewport" content="width=device-width, initial-scale=1">
		  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
		  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
		  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
		</head>
		<body>
		<div class="container" """

	headerSoup = BeautifulSoup(htmlCodeHeader, 'html.parser')
	headerSoup.prettify()

	htmlCodeFooter = """</div></body>\n</html>\n"""

	footerSoup = BeautifulSoup(htmlCodeFooter, 'html.parser')
	footerSoup.prettify()

	currentFile.write(str(headerSoup))
	traverseFolder(currentFile)
	currentFile.write(htmlCodeFooter)


if __name__ == "__main__":
    cwd = os.path.basename(os.getcwd())
    fileName = cwd + "Py.html"
    currentFile = open(fileName, "w+")
    #useFile = askQuestion("Use file template or internal?")
    buildFullHTML(currentFile)
    print(fileName + " successfully generated")
    currentFile.close()
