# FanTempInfo (c) 2boom 2012 v.0.2

from Poll import Poll
from Components.Converter.Converter import Converter
from Components.Element import cached
from Tools.Directories import fileExists

class FanTempInfo(Poll, Converter, object):
	FanInfo = 0
	TempInfo = 1
	
	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		if type == "FanInfo":
			self.type = self.FanInfo
		elif type == "TempInfo":
			self.type = self.TempInfo
		self.poll_interval = 3000
		self.poll_enabled = True
		
	@cached
	def getText(self):
		info = "N/A"
		tempvalue = " "
		tempunit = " "
		if self.type == self.FanInfo:
			if fileExists("/proc/stb/fp/fan_speed"):
				for line in open("/proc/stb/fp/fan_speed"):
					info = line.strip('\n')
			else:
				info = "N/A"
		elif self.type == self.TempInfo:
			if fileExists("/proc/stb/sensors/temp0/value") and fileExists("/proc/stb/sensors/temp0/unit"):
				for line in open("/proc/stb/sensors/temp0/value"):
					tempvalue = ("%s%s" % (line.strip('\n'), unichr(176).encode("latin-1")))
				for line in open("/proc/stb/sensors/temp0/unit"):
					tempunit = ("%s" % line.strip('\n'))
				info = tempvalue + tempunit
			else:
				info = "N/A"
		return info
		
	text = property(getText)
	
	def changed(self, what):
		if what[0] == self.CHANGED_POLL:
			self.downstream_elements.changed(what)
