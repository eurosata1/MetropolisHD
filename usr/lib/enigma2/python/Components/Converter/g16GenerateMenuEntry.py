#######################################################################
#
#    Converter for Enigma2
#    edited original MenuEntryCompare by shamann (c)2012
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

from Components.Converter.Converter import Converter
from Components.Element import cached


class g16GenerateMenuEntry(Converter, object):
	def __init__(self, type):
		Converter.__init__(self, type)

	def selChanged(self):
		self.downstream_elements.changed((self.CHANGED_ALL, 0))

	@cached
	def getText(self):
		cur = self.source.current
		if cur and len(cur) > 2:
			EntryID = cur[2]
			return EntryID
		return ""

	entryName = property(getText)

	def changed(self, what):
		if what[0] == self.CHANGED_DEFAULT:
			self.source.onSelectionChanged.append(self.selChanged)
		Converter.changed(self, what)

