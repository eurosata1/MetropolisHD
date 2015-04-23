#Coders by Nikolasi
# -*- coding: UTF-8 -*-
from Tools.Directories import fileExists
from Tools.LoadPixmap import LoadPixmap 
from Components.Pixmap import Pixmap 
from Renderer import Renderer
from enigma import eServiceCenter, eServiceReference, iServiceInformation, iPlayableService, eDVBFrontendParametersSatellite, eDVBFrontendParametersCable 
from string import upper 
from enigma import ePixmap, eServiceCenter, loadPic, eTimer
from Tools.Directories import fileExists, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, resolveFilename 
from Components.config import config
from Components.Converter.Poll import Poll

class CoverTech(Renderer, Poll):
	__module__ = __name__
	searchPaths = ('/media/hdd/%s/',  '/media/usb/%s/', '/media/sdb2/%s/')
	
	def __init__(self):
                Poll.__init__(self)
		Renderer.__init__(self)
		self.path = 'covers'
		self.nameCache = {}
		self.pngname = ''
		self.picon_default = "picon_default.png"
		
	def applySkin(self, desktop, parent):
		attribs = []
		for (attrib, value,) in self.skinAttributes:
			if (attrib == 'path'):
				self.path = value
			elif (attrib == 'picon_default'):
				self.picon_default = value
			else:
				attribs.append((attrib, value))
				
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)
		
	GUI_WIDGET = ePixmap
	
	def changed(self, what):
	        self.poll_interval = 2000
	        self.poll_enabled = True                 
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
					    tmp = '/usr/lib/enigma2/python/Plugins/Extensions/TMBD/picon_default.png'
					    if fileExists(tmp):
						    pngname = tmp
					    self.nameCache['default'] = pngname
					
			if (self.pngname != pngname):
				self.pngname = pngname
				png = loadPic(self.pngname, 188, 280, 0, 0, 0, 1)
				self.instance.setPixmap(png)
			
					
	def findPicon(self, serviceName):
		for path in self.searchPaths:
			pngname = (((path % self.path) + serviceName) + '.jpg')
			if fileExists(pngname):
				return pngname
				
		return ''

