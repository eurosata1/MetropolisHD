# GWeather by 2boom 2012 v.0.6
# xml from google weather
from Components.Converter.Converter import Converter
from Components.Element import cached
from Tools.Directories import fileExists
from Poll import Poll
import time
import os

weather_city = 'Москва'
time_update = 27
lang = 'ru'
time_update_ms = 30000

class GWeather(Poll, Converter, object):
	Temperature = 0
	City = 1
	Condition = 2
	Wind = 3
	Humidity = 4
	Icon = 5

	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		if type == "Temperature":
			self.type = self.Temperature
		elif type == "City":
			self.type = self.City
		elif type == "Condition":
			self.type = self.Condition
		elif type == "Wind":
			self.type = self.Wind
		elif type == "Humidity":
			self.type = self.Humidity
		elif type == "Icon":
			self.type = self.Icon
		self.poll_interval = time_update_ms
		self.poll_enabled = True
		
	def getXMLfile(self):
		os.system("wget -P /tmp 'http://www.google.com/ig/api?weather=%s&hl=%s' -O /tmp/forecast.xml" % (weather_city, lang))
		if fileExists("/tmp/forecast.xml"):
			os.chmod("/tmp/forecast.xml", 0644)
			infore = open("/tmp/forecast.xml", "r")
			outfore = open("/tmp/foreout.xml", "w")
			for line in infore:
				outfore.write(line.replace('><', '>\n<'))
			infore.close()
			outfore.close()
			os.system("rm /tmp/forecast.xml")
			os.system("mv /tmp/foreout.xml /tmp/forecast.xml")
		else:
			return 'NA'
		
	@cached
	def getText(self):
		info = ""
		plustemp = ""
		if fileExists("/tmp/forecast.xml"):
			if int((time.time() - os.stat("/tmp/forecast.xml").st_mtime)/60) >= time_update:
				os.system("rm /tmp/forecast.xml")
				self.getXMLfile()
		else:
			self.getXMLfile()
		if not fileExists("/tmp/forecast.xml"):
			return 'NA'
		for line in open("/tmp/forecast.xml"):
			if self.type == self.Temperature and line.find('temp') > -1:
				if line.split('"')[1][0] != '-':
					plustemp = "+%s" % line.split('"')[1]
				else:
					plustemp = line.split('"')[1]
				info = "%s%s" % (plustemp, unichr(176).encode("latin-1"))
			elif self.type == self.City and line.find('city') > -1:
				info = line.split('"')[1].split(',')[0]
			elif self.type == self.Condition and line.find('<condition data') > -1:
				info = line.split('"')[1]
			elif self.type == self.Wind and line.find('wind') > -1:
				info = line.split('"')[1].replace('mph', 'kmph')
			elif self.type == self.Humidity and line.find('humidity') > -1:
				info = line.split('"')[1]
			elif self.type == self.Icon and line.find('icon') > -1:
				info = line.split('"')[1].split('/')[-1][:-4]
			elif line.find('/current_conditions') > -1:
				break
		return info

	text = property(getText)

	def changed(self, what):
		Converter.changed(self, (self.CHANGED_POLL,))
