#Coders by Nikolasi
# -*- coding: UTF-8 -*-
from Tools.Directories import fileExists
from Tools.LoadPixmap import LoadPixmap 
from Components.Pixmap import Pixmap 
from Renderer import Renderer
from enigma import ePixmap, loadPic
from Tools.Directories import fileExists, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, resolveFilename 

class CoverTmbdBig(Renderer):
	__module__ = __name__
	searchPaths = ('/media/hdd/%s/',  '/media/usb/%s/', '/media/sdb2/%s/')
	
	def __init__(self):
		Renderer.__init__(self)
		self.path = 'covers'
		self.nameCache = {}
		self.pngname = ''
		self.size = []

        def applySkin(self, desktop, parent):
            atrs = []
            for atr, value in self.skinAttributes:
		if (atr == 'path'):
			self.path = value                    
                elif atr == 'size':
                    self.size = value.split(',')
                atrs.append((atr, value))
            self.skinAttributes = atrs
            aply = Renderer.applySkin(self, desktop, parent)
            return aply
		
	GUI_WIDGET = ePixmap
	
	def changed(self, what):
		if self.instance:
			pngname = ''
			if (what[0] != self.CHANGED_CLEAR):
				sname = self.source.text
				pngname = self.nameCache.get(sname, '')
				if (pngname == ''):
					pngname = self.findPicon(sname)
					if (pngname != ''):
						self.nameCache[sname] = pngname
			if (pngname == ''):
				pngname = self.nameCache.get('default', '')
				if (pngname == ''):
                                        pngname = self.findPicon('picon_default')
                                        if (pngname == ''):
					    tmp = '/usr/lib/enigma2/python/Plugins/Extensions/TMBD/picon_default_big.png'
					    if fileExists(tmp):
						    pngname = tmp
					    self.nameCache['default'] = pngname
			if (self.pngname != pngname):
				self.pngname = pngname
				png = loadPic(self.pngname, int(self.size[0]), int(self.size[1]), 0, 0, 0, 1)
				self.instance.setPixmap(png)
			
	def findPicon(self, serviceName):
		for path in self.searchPaths:
			pngname = (((path % self.path) + serviceName) + '_big.png')
			if fileExists(pngname):
				return pngname
		return ''
