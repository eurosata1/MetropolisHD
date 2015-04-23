#
# <widget source="session.CurrentService" render="Label" position="189,397" zPosition="4" size="350,20" noWrap="1" valign="center" halign="center" font="Regular;14" foregroundColor="clText" transparent="1"  backgroundColor="#20002450">
#	<convert type="CamdInfo">Camd</convert>
# </widget>			

from enigma import iServiceInformation
from Components.Converter.Converter import Converter
from Components.Element import cached
from Tools.Directories import fileExists

class SrvGsu(Converter, object):
	def __init__(self, type):
		Converter.__init__(self, type)

	@cached
	def getText(self):
		service = self.source.service
		info = service and service.info()
		if not info:
			return ""
			camd = None
			
		# Bleck Hole 	
                if fileExists("/tmp/ucm_srv.info"):		
                   try:
			camdlist = open("/tmp/ucm_srv.info", "r")
		   except:
			return None
			
		# 	
		elif fileExists("/usr/bin/emuactive"):
		   try:
			camdlist = open("/usr/bin/emuactive", "r")
		   except:
			return None
		else:
                   camdlist = None
		
		if camdlist is not None:
			for current in camdlist:
				camd = current
			camdlist.close()
			return camd
		else:
			return ""

	text = property(getText)

	def changed(self, what):
		Converter.changed(self, what)




