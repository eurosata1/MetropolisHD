#######################################################################
#
#    Renderer for Enigma2
#    Coded by shamann (c)2013
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    
#######################################################################

from Renderer import Renderer
from enigma import eLabel, eServiceReference, eEPGCache, eSize
from Components.VariableText import VariableText
from time import localtime
from skin import parseFont

class g16ShowExtEpg(VariableText, Renderer):

	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)
		self.EPGcache = eEPGCache.getInstance()
		self.numEvents = 4
		self.testSizeLabel = None           	

	GUI_WIDGET = eLabel

	def applySkin(self, desktop, parent):
		attribs = [ ]
		for (attrib, value) in self.skinAttributes:
			if attrib == "size":
				self.sizeX = int(value.strip().split(",")[0])
				attribs.append((attrib,value))
			elif attrib == "numEvents":
				self.numEvents = int(value) + 1
			elif attrib == "font":
				self.used_font = parseFont(value, ((1,1),(1,1)))
				attribs.append((attrib,value))
			else:
				attribs.append((attrib,value))
		self.skinAttributes = attribs
		self.testSizeLabel.setFont(self.used_font)
		self.testSizeLabel.resize(eSize(self.sizeX+500,20))
		self.testSizeLabel.setVAlign(eLabel.alignTop)
		self.testSizeLabel.setHAlign(eLabel.alignLeft)
		self.testSizeLabel.setNoWrap(1)
		return Renderer.applySkin(self, desktop, parent)

	def connect(self, source):
		Renderer.connect(self, source)
		self.changed((self.CHANGED_DEFAULT,))
		
	def changed(self, what):
		if self.instance:
			self.text = "Extended EPG is not available!"
			if what[0] != self.CHANGED_CLEAR:
				try:
					service = self.source.service
					marker = (service.flags & eServiceReference.isMarker == eServiceReference.isMarker)
					bouquet = (service.flags & eServiceReference.flagDirectory == eServiceReference.flagDirectory)
					sname = service.toString()
				except:
					marker = False
					bouquet = False
					sname = self.source.text
				if not marker and not bouquet and self.EPGcache is not None:
					pos = sname.rfind(':')
					if pos != -1:
						sname = sname[:pos].rstrip(':')
						if not "::" in sname:
							try:
								info = service and self.source.info
							except: info = True
							if info is not None:
								epgList =  self.EPGcache.lookupEvent(['TBX', (sname, 1, -1, 1440)])
								extEpg = "" 
								for x in range(1,self.numEvents):
									try:
										t = localtime(int(epgList[x][1]))
										tmp = "%02d:%02d  %s" % (t.tm_hour, t.tm_min, epgList[x][0])
										self.testSizeLabel.setText(tmp)
										text_width = self.testSizeLabel.calculateSize().width()
										if text_width > (self.sizeX - 30):
											while (text_width > (self.sizeX - 30)):
												tmp = tmp[:-1] 
												self.testSizeLabel.setText(tmp)
												text_width = self.testSizeLabel.calculateSize().width()
											pos = tmp.rfind(' ')
											if pos != -1:
												tmp = tmp[:pos].rstrip(' ') + ".."
										extEpg += "%s\n" % tmp
									except: pass
								if extEpg != "":
									self.text = extEpg

	def preWidgetRemove(self, instance):
		self.testSizeLabel = None

	def postWidgetCreate(self, instance):
		self.testSizeLabel = eLabel(instance)
		self.testSizeLabel.hide()
		
		
		
