import os
import os.path
from bs4 import BeautifulSoup

useFile = False

def fillImageLink(soup, imgFile, internal):
	for img in soup.find_all(id = 'imageLink'):
		if internal:
			img['src'] = imgFile
		else:
			img['src'] = getImageLinkUPC(imgFile)


def getImageLinkUPC(imgFile):
	base = "../../../../ca/media/la-upc/la-institucio/galeriaimatges-1/"
	cwd = os.path.basename(os.getcwd())
	fullPath = base + cwd + "/" + imgFile
	return fullPath


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
		previousM = flag

	for a in soup.find_all(id = "previous"):
		a['href'] = "#modal" + str(previousM)

	for a in soup.find_all(id = "next"):
		a['href'] = "#modal" + str(nextM)


def fillCaptionName(soup, imgFile):
	# For now just put the file's name in it
	# Change title based on file name
	result = soup.find(class_ = "caption")
	result.string.replace_with(imgFile)

def getIndividualImageHTML(currentFile, modal, flag, imgFile, internalLink):
	elementHTML = getSingleTemplate()
	elementSoup = BeautifulSoup(elementHTML, 'html.parser')

	fillModalIDs(elementSoup, modal)
	fillCaptionName(elementSoup, imgFile)
	fillArrowIDs(elementSoup, modal, flag)
	fillImageLink(elementSoup, imgFile, internalLink)

	contents = "\n" + elementSoup.prettify() + "\n"
	currentFile.write(str(contents))


def openRowHTML(currentFile):
	htmlCode = "<div class=\"row\">"
	currentFile.write(htmlCode)


def closeDivHTML(currentFile):
	htmlCode = "</div>\n"
	currentFile.write(htmlCode)


def getCurrentFlag(modal):
	# First -> flag = number of files
	# Normal -> flag = 1
	# Last -> flag = 0
	if modal == len(os.listdir()) - 5:
		return 0
	elif modal == 0:
		return len(os.listdir()) - 5
	else:
		return 1


def traverseFolder(currentFile):
	# internal = askQuestion("Internal src?")
	internal = True
	modal = 0
	
	openRowHTML(currentFile)
	
	for file in os.listdir():
		#if file != "generatePage.py" and file != "sliderModalNoFade.html" and file != "PythonGenerated.html":
		if not file.endswith(".sh") and not file.endswith(".zip") and not file.endswith(".py") and not file.endswith(".html") and not file.endswith(".exe"):
			if modal%3 == 0 and modal != 0:
				closeDivHTML(currentFile)
				openRowHTML(currentFile)
			flag = getCurrentFlag(modal)
			getIndividualImageHTML(currentFile, modal, flag, file, internal)
			modal += 1
	
	closeDivHTML(currentFile)

	# There should be more than 1 picture for the flag to work properly
	if modal <= 1:
		print("Warning, only one image => the previous/next navigation might not work properly")


def askQuestion(question):
	ans = str(input(question + " (y/n): "))
	if (ans == "y" or ans == "Y"):
		return True
	elif (ans == "n" or ans == "N"):
		return False
	else:
		askQuestion()


def main():
	cwd = os.path.basename(os.getcwd())
	fileName = cwd + "Py.html"
	currentFile = open(fileName, "w+")
	#useFile = askQuestion("Use file template or internal?")
	buildFullHTML(currentFile)

	currentFile.close()


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

def getSingleTemplate():
		# Hardocoded here so the template is not outside
		html = """<div class="col-lg-4 col-sm-6">
<div class="thumbnail" width="700px" height="389px">
	<a id="currentModal" href="@@@@@@"> 
		<img id="imageLink" data-toggle="modal" data-target="@@@@@@" alt="Exemple" src="@@@@@@" width="100%" height="100%" style="overflow: hidden;" class="image-inline"/> 
	</a>
	<div class="caption" align="center">@@@@@@CAPTION@@@@@@</div>
	<div class="modal" id="myModal" role="dialog" aria-labelledby="@@@@@@" tabindex="-1">
		<div class="modal-dialog modal-lg" role="document">
			<div class="modal-content">
				<a id="previous" class="left carousel-control" href="@@@@@@" data-toggle="modal" data-dismiss="modal">
				    <span class="glyphicon glyphicon-chevron-left"></span>
				</a>
				<img id="imageLink" class="img-responsive" src="@@@@@@" />
				<a id="next" class="right carousel-control" href="@@@@@@" data-toggle="modal" data-dismiss="modal">
				    <span class="glyphicon glyphicon-chevron-right"></span>
				</a>
			</div>
		</div>
	</div>
</div>
</div>
		"""
		return html

main()