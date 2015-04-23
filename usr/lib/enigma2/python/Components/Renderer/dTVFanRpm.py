from Components.VariableText import VariableText
from enigma import eLabel
from Components.Sensors import sensors
from Renderer import Renderer

class dTVFanRpm(Renderer, VariableText):
	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)
	GUI_WIDGET = eLabel

	def changed(self, what):
		if not self.suspended:
			tt = 0
			try:
				templist = sensors.getSensorsList(sensors.TYPE_FAN_RPM)
				id = templist[0]
				tt = sensors.getSensorValue(id)
			except:
				pass
			self.text = str(tt/2)

	def onShow(self):
		self.suspended = False
		self.changed(None)

	def onHide(self):
		self.suspended = True
