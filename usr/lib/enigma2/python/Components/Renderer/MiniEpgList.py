from Components.VariableText import VariableText
from enigma import eLabel, eEPGCache
from Renderer import Renderer
from time import localtime


class MiniEpgList(Renderer, VariableText):

	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)
		self.epgcache = eEPGCache.getInstance()

	GUI_WIDGET = eLabel

	def changed(self, what):
		event = self.source.event

		if event is None:
			self.text = ""
			return

		service = self.source.service
		text = ""
		list = None

		if self.epgcache is not None:
			list = self.epgcache.lookupEvent(['IBDCT', (service.toString(), 0, -1, -1)])

		if list:
			maxx = 0
			for event in list:
				if maxx > 0:
					if event[4]:
						begin = localtime(event[1])
						end = localtime(event[1]+event[2])
						event_str = "%02d:%02d - %02d:%02d %s\n" % (begin[3], begin[4], end[3], end[4], event[4])
						text = text + event_str
					else:
						text = text + "n/a\n"

				maxx += 1
				if maxx > 4:
					break
		self.text = text
