from Components.Converter.Converter import Converter
from enigma import iServiceInformation, iPlayableService
from Components.Element import cached
from Components.Language import language

class AudioInfo(Converter, object):
	AUDIO_LANGUAGE = 0
	SUBTITLES_AVAILABLE = 2
	AUDIO_DESCRIPTION = 3
	

	def __init__(self, type):
		Converter.__init__(self, type)
		self.type, self.interesting_events = {
				"AudioLanguage": (self.AUDIO_LANGUAGE, (iPlayableService.evUpdatedInfo,)),
				"SubtitlesAvailable": (self.SUBTITLES_AVAILABLE, (iPlayableService.evUpdatedInfo,)),
				"AudioDescription": (self.AUDIO_DESCRIPTION, (iPlayableService.evUpdatedInfo,)),
			}[type]

	def getServiceInfoString(self, info, what, convert = lambda x: "%d" % x):
		v = info.getInfo(what)
		if v == -1:
			return "N/A"
		if v == -2:
			return info.getInfoString(what)
		return convert(v)

	@cached
	def getBoolean(self):
		service = self.source.service
		info = service and service.info()
		if not info:
			return False
		
		if self.type == self.AUDIO_LANGUAGE:
			audio = service.audioTracks()
                        if audio:
				n = audio.getNumberOfTracks()
				idx = 0
				while idx < n:
					i = audio.getTrackInfo(idx)
                                        languages = i.getLanguage()
                                        description = i.getDescription()
					lang = language.getLanguage()
                                        # set not the following "word" (lang) in your own language, it will not work.... 
                                        if lang == 'de_DE':
                                                if "Englisch" in languages or "English" in languages or "Spanish" in languages or "Turkish" in languages or "Kommentar" in languages or "Stadion" in languages or "stereo englisch" in languages or "franz" in languages or "Franz\xc3\xb6sisch" in languages or "Italian" in languages or "Russian" in languages or "French" in languages or "Italienisch" in languages or "Tonopt. 2" in languages:
						        return True
                                        elif lang == 'en_EN':
                                                if "Deutsch" in languages or "German" in languages:
						        return True
					idx += 1
			return False

		elif self.type == self.SUBTITLES_AVAILABLE:
			subtitle = service and service.subtitle()
			subtitlelist = subtitle and subtitle.getSubtitleList()
			if subtitlelist:
				return len(subtitlelist) > 0
			return False
			
		elif self.type == self.AUDIO_DESCRIPTION:
			audio = service.audioTracks()
                        if audio:
				n = audio.getNumberOfTracks()
				idx = 0
				while idx < n:
					i = audio.getTrackInfo(idx)
                                        languages = i.getLanguage().split('/')
                                        description = i.getDescription()
					# set not the following "word" in your own language, it will not work.... 
                                        if "H\xc3\xb6rfilm" in languages or "Zweikanal" in languages or "mit Audiodeskription" in languages:
						return True
					idx += 1
			return False


	boolean = property(getBoolean)
	

	def changed(self, what):
		if what[0] != self.CHANGED_SPECIFIC or what[1] in self.interesting_events:
			Converter.changed(self, what)
