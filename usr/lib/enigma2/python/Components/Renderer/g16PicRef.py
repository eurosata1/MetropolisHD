from Tools.LoadPixmap import LoadPixmap
from Components.Pixmap import Pixmap
from Renderer import Renderer
from enigma import ePixmap, eTimer
from Tools.Directories import fileExists, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, resolveFilename
from Components.config import *

class g16PicRef(Renderer):

	def __init__(self):
		Renderer.__init__(self)
		self.nameCache = { }
		self.pngname = ""
		self.path = "picon"
		
	def applySkin(self, desktop, parent):
		attribs = [ ]
		for (attrib, value) in self.skinAttributes:
			if attrib == "path":
				self.path = value
			else:
				attribs.append((attrib,value))
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)
		
	GUI_WIDGET = ePixmap

	def changed(self, what):
		if self.instance:
			pngname = ""
			if what[0] != self.CHANGED_CLEAR:
				sname = self.source.text
				if sname is not None and sname != "":
					if sname[-1] != ":" and ("http" in sname or "//" in sname):
						sname = sname.replace(':','_').replace(' ','_').replace('%','_').replace('/','')
					else:
						pos = sname.rfind(':')
						if pos != -1:
							sname = sname[:pos].rstrip(':').replace(':','_')
					pngname = self.nameCache.get(sname, "")
					if pngname == "":
						pngname = self.findPicon(sname)
						if pngname != "":
							self.nameCache[sname] = pngname
			if pngname == "":
				pngname = self.nameCache.get("default", "")
				if pngname == "":
					pngname = self.findPicon("picon_default")
					if pngname == "":
						tmp = resolveFilename(SCOPE_CURRENT_SKIN, "picon_default.png")
						if fileExists(tmp):
							pngname = tmp
						else:
							pngname = resolveFilename(SCOPE_SKIN_IMAGE, "skin_default/picon_default.png")
					self.nameCache["default"] = pngname
			if self.pngname != pngname:
				self.pngname = pngname
				self.instance.setPixmapFromFile(self.pngname)

	def findPicon(self, serviceName):
		try:
			pngname = "%s/%s/%s.png" % (config.plugins.setupGlass16.par39.value, self.path, serviceName)
			if fileExists(pngname):
				return pngname
		except: pass
		return ""
