#######################################################################
#
#    Renderer for Enigma2
#    Coded by shamann (c)2012
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

from Tools.LoadPixmap import LoadPixmap
from Components.Pixmap import Pixmap
from Renderer import Renderer
from Tools.Directories import fileExists
from Components.config import config
from enigma import ePixmap, eTimer

class g16MenuEntry(Renderer):

	def __init__(self):
		Renderer.__init__(self)
		self.delayInitTimer = eTimer()
		self.delayInitTimer.timeout.get().append(self.changed)		
	GUI_WIDGET = ePixmap
        
	def changed(self, what=None):
		if self.delayInitTimer.isActive():
			self.delayInitTimer.stop()
		if self.instance:
			pixpath = config.plugins.setupGlass16.par39.value + '/menuIcons/' + str(config.plugins.setupGlass16.par69.value) + "/" + self.source.entryName + '.png'
			if not fileExists(pixpath):
				pixpath = config.plugins.setupGlass16.par39.value + '/menuIcons/' + str(config.plugins.setupGlass16.par69.value) + "/undefined.png"
				if not fileExists(pixpath):
					pixpath = "/usr/share/enigma2/hd_glass16/menu/undefined.png"
			self.instance.setPixmapFromFile(pixpath)					
		else:
			self.delayInitTimer.start(500)        
