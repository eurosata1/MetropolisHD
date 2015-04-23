# ClockToText german version
# modded by hardy73 v1.1

from Converter import Converter
from time import localtime, strftime
from Components.Element import cached
from Components.config import config

class hardyClockToText(Converter, object):
	DEFAULT = 0
	WITH_SECONDS = 1
	IN_MINUTES = 2
	DATE = 3
	FORMAT = 4
	AS_LENGTH = 5
	TIMESTAMP = 6
	
	# add: date, date as string, weekday, ... 
	# (whatever you need!)
	
	def __init__(self, type):
		Converter.__init__(self, type)
		if type == "WithSeconds":
			self.type = self.WITH_SECONDS
		elif type == "InMinutes":
			self.type = self.IN_MINUTES
		elif type == "Date":
			self.type = self.DATE
		elif type == "AsLength":
			self.type = self.AS_LENGTH
		elif type == "Timestamp":	
			self.type = self.TIMESTAMP
		elif str(type).find("Format") != -1:
			self.type = self.FORMAT
			self.fmt_string = type[7:]
		else:
			self.type = self.DEFAULT

	@cached
	def getText(self):
		time = self.source.time
		if time is None:
			return ""

		# handle durations
		if self.type == self.IN_MINUTES:
			return "%d min" % (time / 60)
		elif self.type == self.AS_LENGTH:
			return "%d:%02d" % (time / 60, time % 60)
		elif self.type == self.TIMESTAMP:
			return str(time)
		
		t = localtime(time)
		
		if self.type == self.WITH_SECONDS:
			return "%2d:%02d:%02d" % (t.tm_hour, t.tm_min, t.tm_sec)
		elif self.type == self.DEFAULT:
			return "%02d:%02d" % (t.tm_hour, t.tm_min)
		elif self.type == self.DATE:
			datestring = "%A %B %d, %Y"
			if config.osd.language.value == "de_DE":
				datestring = "%A, %d. %B %Y"
				t2 = ["Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag","Sonntag"][t.tm_wday]
				m2 = ["Januar","Februar",u"M\xe4rz","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"][t.tm_mon - 1]
				datestring = datestring.replace('%A', t2)
				datestring = datestring.replace('%B', m2)				
			return strftime(datestring, t)
		elif self.type == self.FORMAT:	   
		# Datumsuebersetzung
			if config.osd.language.value == "de_DE":
				t1 = ["Mo","Di","Mi","Do","Fr","Sa","So"][t.tm_wday]
				t2 = ["Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag","Sonntag"][t.tm_wday]
				m1 = ["Jan","Feb","Mrz","Apr","Mai","Jun","Jul","Aug","Sep","Okt","Nov","Dez"][t.tm_mon - 1]
				m2 = ["Januar","Februar",u"M\xe4rz","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"][t.tm_mon - 1]
				self.fmt_string = self.fmt_string.replace('%a', t1)
				self.fmt_string = self.fmt_string.replace('%A', t2)
				self.fmt_string = self.fmt_string.replace('%b', m1)
				self.fmt_string = self.fmt_string.replace('%B', m2)			
			spos = self.fmt_string.find('%')
			if spos > 0:
				s1 = self.fmt_string[:spos]
				s2 = strftime(self.fmt_string[spos:], t)
				return str(s1+s2)
			else:
				return strftime(self.fmt_string, t)
		else:
			return "???"

	text = property(getText)
