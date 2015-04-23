#######################################################################
#
#    Renderer for Enigma2
#    Coded by shamann (c)2011
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
from enigma import eDVBVolumecontrol, eTimer
from enigma import eCanvas, eRect, gRGB
from skin import parseColor

class g16VolumeGauge(Renderer):

	def __init__(self):
		Renderer.__init__(self)
		self.bgColor = gRGB(0, 0, 0, 255)
		self.allColors = {
     "0" : "#00A501FE", "5" : "#00A501FE", "10" : "#00A501FE", "15" : "#00A501FE", "20" : "#00A501FE", "25" : "#007F01FE",
     "30" : "#004D01FE", "35" : "#000166FE", "40" : "#0001A5FE", "45" : "#0001D8FE", "50" : "#0001FEE4", "55" : "#0001FEA5",
     "60" : "#0003FC41", "65" : "#0040FE01", "70" : "#00B2FE01", "75" : "#00F1FE01", "80" : "#00FED801", "85" : "#00FEB201",
     "90" : "#00FE8C01", "95" : "#00FF7300", "100" : "#00FF0000"
     }
		self.start = False                     		
		self.vTimer = eTimer()
		self.vTimer.callback.append(self.changed)
	GUI_WIDGET = eCanvas

	def applySkin(self, desktop, parent):
		attribs = [ ]		
		from enigma import eSize
		def parseSize(str):
			x, y = str.split(',')
			return eSize(int(x), int(y))
		for (attrib, value) in self.skinAttributes:
			if attrib == "size":
				self.instance.setSize(parseSize(value))
				attribs.append((attrib,value))
			elif attrib == "position":
				x, y = value.split(',')
				self.posX, self.posY = int(x), int(y)
				attribs.append((attrib,value))
			elif attrib == "backgroundColor":
				self.bgColor = parseColor(value)
				self.instance.clear(self.bgColor)
			else:
				attribs.append((attrib,value))
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	def changed(self, what=""):
		if self.instance is None:
			return
		if self.start:
			offset = eDVBVolumecontrol.getInstance().getVolume()
			if self.allColors.has_key(str(offset)):
				self.instance.clear(self.bgColor)
				color = parseColor(self.allColors.get(str(offset)))
				self.instance.fillRect(eRect(((2*offset)-10), 0, 10, 25), color)

		
	def onShow(self):
		self.start = True
		self.vTimer.start(200)

	def onHide(self):
		self.start = False
		self.vTimer.stop()		
