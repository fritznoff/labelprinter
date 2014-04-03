import os, tempfile
import cups
from PIL import Image, ImageDraw, ImageFont


class LabelPrinter(object):

	def __init__(self, printerName=None):
		if printerName is None:
			raise ValueError('No printer name specified')

		self.cupsConnection = cups.Connection()
		self.setPrinter(printerName)


	def setPrinter(self, printerName):
		availablePrinters = self.cupsConnection.getPrinters()
		try:
			availablePrinters[printerName]
		except KeyError:
			raise ValueError("The printer with the name '" + printerName + "' is not available")
		else:
			self.printer = printerName

	def renderImageFromText(self, text, font, fontSize):
		thisFilePath = os.path.dirname(os.path.realpath(__file__))
		fontPath = os.path.join(thisFilePath, 'fonts', font + '.ttf')
		imageFont = ImageFont.truetype(fontPath, fontSize, encoding='unic')
		(width, height) = imageFont.getsize(text)
		image = Image.new('1', (width, 64), 1)
		draw = ImageDraw.Draw(image)
		draw.text((0,32-(height/2)), text, font=imageFont)
		return image

	def initstring(self):
		return chr(0x1B) + '@' + chr(0x1B) + 'iS' + chr(0x1B) + 'iR' + chr(0x01)

	def linefeed(self, feed):
		output = ""
		for i in xrange(0, feed +1):
			output = output + 'Z'
		output = output + chr(0x1A)
		return output

	def processimage(self, image):
		image = image.rotate(270)
		(width, height) = image.size
		output = ""
		for y in xrange(height-1, -1, -1):
			output = output + 'G' + chr((width/8)+4) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)
			for x in xrange(0, width/8):
				pixelbyte = 0
				for b in xrange(0, 8):
					pixellocation = (x*8 + b, y)
					thispixel = image.getpixel(pixellocation)
					thispixel = 1 != thispixel
					pixelbyte = pixelbyte + thispixel * (2 ** (7-b))
				output = output + chr(pixelbyte)
		return output

	def printLabel(self, text, font='Lato-Bold', fontSize=60):
		printSequence = self.initstring() + self.processimage(self.renderImageFromText(text, font, fontSize)) + self.linefeed(5)
		tempFile = tempfile.NamedTemporaryFile()
		tempFile.write(printSequence)
		tempFile.file.flush()
		self.cupsConnection.printFile(self.printer, tempFile.name, text, {})
		tempFile.close()
