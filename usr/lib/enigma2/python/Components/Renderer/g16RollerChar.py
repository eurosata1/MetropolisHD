#######################################################################
#
#    Renderer for Dreambox-Enigma2
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
from enigma import eLabel
from enigma import eTimer
from Components.VariableText import VariableText

class g16RollerChar(VariableText, Renderer):

	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)
		self.rollTimerText = eTimer()
		self.rollTimerText.timeout.get().append(self.rollText)    
    		
	GUI_WIDGET = eLabel

	def connect(self, source):
		Renderer.connect(self, source)
		self.changed((self.CHANGED_DEFAULT,))
		
	def changed(self, what):
		if self.rollTimerText.isActive():
			self.rollTimerText.stop()
		if what[0] == self.CHANGED_CLEAR:
			self.text = ""
		else:
			self.text = self.source.text
		if self.instance:
			self.idx = 0
			try:
				self.backtext = unicode(("               " + self.text + "               "),"utf-8")
			except: self.backtext = "               " + self.text + "               "
			self.x = len(self.backtext)
			self.rollTimerText.start(8500)
            				
	def rollText(self):
		self.rollTimerText.stop()
		if self.x > 0:
			txttmp = self.backtext[self.idx:]
			x = len(txttmp)
			try:
				self.text = str(txttmp[:x].encode("utf-8"))
			except: self.text = str(txttmp[:x])
			self.idx = self.idx+1
			self.x = self.x-1      
		if self.x == 0: 
			self.idx = 0     
			self.x = len(self.backtext) 
		self.rollTimerText.start(250)

