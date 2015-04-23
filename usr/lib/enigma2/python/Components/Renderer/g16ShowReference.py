#######################################################################
#
#    Renderer for Enigma2
#    Coded by shamann (c)2013
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
from Components.VariableText import VariableText
from enigma import eServiceReference

class g16ShowReference(VariableText, Renderer):

	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)
		
	GUI_WIDGET = eLabel

	def connect(self, source):
		Renderer.connect(self, source)
		self.changed((self.CHANGED_DEFAULT,))
		
	def changed(self, what):
		if self.instance:
			self.text = "Reference: X:X:X:XXXX:XXX:X:XXXXXX:X:X:X"
			if what[0] != self.CHANGED_CLEAR:
				service = self.source.service
				marker = (service.flags & eServiceReference.isMarker == eServiceReference.isMarker)
				bouquet = (service.flags & eServiceReference.flagDirectory == eServiceReference.flagDirectory)
				sname = service.toString()
				if not marker and not bouquet and sname is not None and sname != "":
					if '4097:0' in sname:
						sname = sname.replace('rtmpe','').replace('4097:0:1','').replace('4097:0:2','').replace('4097:0:0','')
						sname = sname.replace('1:0:1:1:1:0:820000:0:0:0:http%3a//127.0.0.1%3a4050/rtp/','').replace('%3a','').replace('.','').replace(' ','').replace(':0:0:0:0:0:0:0:','').replace('/','').replace('http','').replace('rtmp','').replace('rtsp','')
					pos = sname.rfind(':')
					if pos != -1:
						sname = sname[:pos].rstrip(':')
						if not "::" in sname:
							self.text = "Reference: " + sname

