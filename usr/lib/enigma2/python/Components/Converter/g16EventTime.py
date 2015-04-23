from Converter import Converter
from Poll import Poll
from time import time, localtime
from Components.Element import cached, ElementError

class g16EventTime(Poll, Converter, object):
	REMAINING = 0
	STARTTIME = 1
	DURATION = 2
	ENDTIME = 3
    	
	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		if type == "Remaining":
			self.type = self.REMAINING
			self.poll_interval = 60000
			self.poll_enabled = True
		elif type == "StartTime":
			self.type = self.STARTTIME
		elif type == "Duration":
			self.type = self.DURATION
		elif type == "EndTime":
			self.type = self.ENDTIME
		else:
			raise ElementError("'%s' is not <Remaining> for g16EventTime converter" % type)

	@cached
	def getText(self):
		def conv_to_default(what):
			t = localtime(what)
			return "%2d:%02d" % (t.tm_hour, t.tm_min)
		def conv_to_min(what):
			return "%d min" % (what / 60)
		event = self.source.event
		if event is None:
			return "--"			
		if self.type == self.REMAINING:
			now = int(time())
			start = event.getBeginTime()
			duration = event.getDuration()
			end = start + duration
			if start <= now <= end:
				return conv_to_min(end - now) 
		elif self.type == self.STARTTIME:			
			return conv_to_default(event.getBeginTime())
		elif self.type == self.DURATION:
			return conv_to_min(event.getDuration())
		elif self.type == self.ENDTIME:
			return conv_to_default(event.getBeginTime() + event.getDuration())
		return "--"	

	text = property(getText)

	def changed(self, what):
		Converter.changed(self, what)
