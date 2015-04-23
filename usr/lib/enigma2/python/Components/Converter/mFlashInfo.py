#
#  FlashInfo - Converter
#
#  Coded by Dr.Best (c) 2012
#  Support: www.dreambox-tools.info
#
#  This plugin is licensed under the Creative Commons 
#  Attribution-NonCommercial-ShareAlike 3.0 Unported 
#  License. To view a copy of this license, visit
#  http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative
#  Commons, 559 Nathan Abbott Way, Stanford, California 94305, USA.
#
#  Alternatively, this plugin may be distributed and executed on hardware which
#  is licensed by Dream Multimedia GmbH.

#  This plugin is NOT free software. It is open source, you are allowed to
#  modify it (if you keep the license), but it may not be commercially 
#  distributed other than under the conditions noted above.
#

from Components.Converter.Converter import Converter
from Components.Element import cached
from os import statvfs
from Poll import Poll
from Components.config import config

class mFlashInfo(Poll, Converter, object):
	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		self.path = "/"
		if type == "DefaultRecordingPath":
			self.path = config.usage.default_path.value
			self.long_display = 1
		elif type == "Long":
			self.long_display = 1
		else:
 			self.long_display = 0
		self.poll_interval = 5000
		self.poll_enabled = True

	@cached
	def getText(self):
		try:
			# Deprecated since version 2.6: The statvfs module has been removed in Python 3.
			st = statvfs(self.path)
		except OSError:
			st = None
			
		if st is not None:
			size = st.f_bsize * st.f_blocks
			available = st.f_bsize * st.f_bavail
			used = size - available
			if (size > 0):
				usedpercent = "%d %%" % int(used * 100 / size)
			else:
				usedpercent = "n/a"
			if self.long_display == 1:
				return _("Size: %s Used: %s Available: %s Use%%: %s") % (self.formatFileSize(size),self.formatFileSize(used),self.formatFileSize(available),usedpercent)
			else:
				return _("%s free, %s in Use") % (self.formatFileSize(available),usedpercent)
		else:
			return "No infos available"

	text = property(getText)


	def formatFileSize(self, size):
		filesize = size
		suffix = ('bytes', 'KB', 'MB', 'GB', 'TB')
		index = 0
		while filesize > 1024:
			filesize = float(filesize) / 1024.0
			index += 1
		filesize_string = "%.2f" % filesize
		if not filesize_string:
			filesize_string = '0'
		return "%s %s" % (filesize_string, suffix[min(index, 4)])
