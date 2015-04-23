######################################################################
#
#
#    Volume Text Renderer for Dreambox/Enigma-
#    Coded by Vali (c)2011, mod by Schomi
#    Support: www.dreambox-tools.info
#
#
#  This plugin is licensed under the Creative Commons 
#  Attribution-NonCommercial-ShareAlike 3.0 Unported License.
#  To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/
#  or send a letter to Creative Commons, 559 Nathan Abbott Way, Stanford, California 94305, USA.
#
#  Alternatively, this plugin may be distributed and executed on hardware which
#  is licensed by Dream Multimedia GmbH.
#
#
#  This plugin is NOT free software. It is open source, you are allowed to
#  modify it (if you keep the license), but it may not be commercially 
#  distributed other than under the conditions noted above.
#
#
#######################################################################

from Components.VariableText import VariableText
from enigma import eLabel, eDVBVolumecontrol, eTimer
from Renderer import Renderer

class SchoVolBar(Renderer, VariableText):
	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)
		self.vol_timer = eTimer()
		self.vol_timer.callback.append(self.pollme)
	GUI_WIDGET = eLabel

	def changed(self, what):
		if not self.suspended:
#			self.text = str(eDVBVolumecontrol.getInstance().getVolume())
			self.actvol = eDVBVolumecontrol.getInstance().getVolume()
			self.text = "3BYK: " + ((self.actvol/5) * "|")
			if self.actvol == 0:
				self.text="3BYK:OTK"

	def pollme(self):
		self.changed(None)

	def onShow(self):
		self.suspended = False
		self.vol_timer.start(200)

	def onHide(self):
		self.suspended = True
		self.vol_timer.stop()
		