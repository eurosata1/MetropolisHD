
from Components.Pixmap import Pixmap
from Renderer import Renderer
from enigma import ePixmap, eTimer
from Tools.Directories import fileExists
from Components.config import config

class g16PicRefBig(Renderer):

	def __init__(self):
		Renderer.__init__(self)
		
	GUI_WIDGET = ePixmap

	def connect(self, source):
		Renderer.connect(self, source)
		self.changed((self.CHANGED_DEFAULT,))
		
	def changed(self, what):
		if self.instance:
			pngname = ""
			sname = self.source.text
			if sname != "":
				sname = sname.replace('%3a','').replace(' ','').replace('4097:0:0:0:0:0:0:0:0:0:','').replace('/','').replace('http','').replace('rtsp','')
				pos = sname.rfind(':')
				if pos != -1:
					sname = sname[:pos].rstrip(':').replace(':','_')
				try:
					pngname = "%s/piconcache/%s.png" % (config.plugins.setupGlass16.par39.value, sname)
				except: pass
			if pngname == "":
				pngname = "/usr/share/enigma2/hd_glass16/frame/picon_big.png"
			if fileExists(pngname):
				self.instance.setPixmapFromFile(pngname)

	def postWidgetCreate(self, instance):
		self.changed((self.CHANGED_DEFAULT,))
		