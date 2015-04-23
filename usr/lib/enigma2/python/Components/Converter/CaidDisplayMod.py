#
#  CaidDisplay - Converter
#

from Components.Converter.Converter import Converter
from enigma import iServiceInformation, iPlayableService
from Components.Element import cached
from Poll import Poll

class CaidDisplayMod(Poll, Converter, object):

	def __init__(self, type):
		Poll.__init__(self)
		Converter.__init__(self, type)
		self.type = type
		self.systemCaids = {
			"26" : "BI",
			"01" : "S",
			"06" : "I",
			"17" : "B",
			"05" : "V",
			"18" : "N",
			"09" : "ND",
			"0B" : "C",
			"0D" : "CW",
			"4A" : "D" }

		self.poll_interval = 2000
		self.poll_enabled = True

	@cached
	def get_caidlist(self):
		caidlist = {}
		service = self.source.service
		if service:
			info = service and service.info()
			if info:        
				caids = info.getInfoObject(iServiceInformation.sCAIDs)
				if caids:
				        for cs in self.systemCaids:
			                        caidlist[cs] = (self.systemCaids.get(cs),0)
			                
					for caid in caids:
						c = "%x" % int(caid)
						if len(c) == 3:
							c = "0%s" % c
						c = c[:2].upper()
						if self.systemCaids.has_key(c):
							caidlist[c] = (self.systemCaids.get(c),1)
							
					ecm_info = self.ecmfile()
					if ecm_info:
						emu_caid = ecm_info.get("caid", "")
						if emu_caid and emu_caid != "0x000":
							c = emu_caid.lstrip("0x")
							if len(c) == 3:
								c = "0%s" % c
							c = c[:2].upper()
							caidlist[c] = (self.systemCaids.get(c),2)
		return caidlist

	getCaidlist = property(get_caidlist)

	@cached
	def getText(self):
		textvalue = "No parse cannot emu"
		service = self.source.service
		if service:
			info = service and service.info()
			if info:
				if info.getInfoObject(iServiceInformation.sCAIDs):
					ecm_info = self.ecmfile()
					if ecm_info:
						# caid
						caid = ecm_info.get("caid", "")
						caid = caid.lstrip("0x")
						caid = caid.upper()
						caid = caid.zfill(4)
						caid = "Caid: %s" % caid
						# Provider wicard
						provider = ecm_info.get("Provider", "")
						provider = provider.lstrip("0x")
						provider = provider.upper()
						provider = provider.zfill(6)
						provider = "Prov: %s" % provider
					
						# hops
						reader = ecm_info.get("reader", None)
                                                reader = "%s" % reader
                                                # oscam
						prov = ecm_info.get("prov", "")
						prov = prov.lstrip("0x")
						prov = prov.upper()
						prov = prov.zfill(6)
						prov = "%s" % prov                                                
						from2 = ecm_info.get("from", None)
                                                from2 = "%s" % from2                                               
						# ecm time	
						ecm_time = ecm_info.get("ecm time", None)
						if ecm_time:
							if "msec" in ecm_time:
								ecm_time = "Ecm: %s " % ecm_time						
							else:
								ecm_time = "Ecm: %s s" % ecm_time
						# address
						address = ecm_info.get("address", "")
						#protocol
                                                protocol = ecm_info.get("protocol", "")						
						# source	
						using = ecm_info.get("using", "")
						if using:
							if using == "emu":
								textvalue = "(EMU) %s - %s" % (caid, ecm_time)
							elif using == "CCcam-s2s":
								textvalue = "(NET) %s - %s - %s - %s" % (caid, address, reader, ecm_time)							
							else:
								textvalue = "%s - %s - Reader: %s - %s" % (caid, address, reader, ecm_time)		
						else:
							# mgcamd
							source = ecm_info.get("source", None)
							if source:
								if source == "emu":
									textvalue = "Source:EMU %s" % (caid)
								else:	
									textvalue = "%s Prov: %s - %s - %s" % (caid, prov, source, ecm_time)
							# oscam
							oscsource = ecm_info.get("reader", None)
							if oscsource:
                                                                if oscsource == "emu":
                                                                        textvalue = "Source:EMU %s" % (caid)
                                                                else:        
								        textvalue = "Reader: %s ( %s Prov: %s - %s - %s - %s )" % (reader, caid,  prov, from2, ecm_time, protocol)
				                        # wicardd
							wicarddsource = ecm_info.get("response time", None)
							if wicarddsource:
                       
								        textvalue = "%s - %s - %s" % (caid, provider, wicarddsource)								        
							# gbox
							decode = ecm_info.get("decode", None)
							if decode:
								if decode == "Internal":
									textvalue = "(EMU) %s" % (caid)
								else:
									textvalue = "%s - %s" % (caid, decode)
							
		return textvalue 

	text = property(getText)

	def ecmfile(self):
		ecm = None
		info = {}
		service = self.source.service
		if service:
			frontendInfo = service.frontendInfo()
			if frontendInfo:
				try:
					ecmpath = "/tmp/ecm%s.info" % frontendInfo.getAll(False).get("tuner_number")
					ecm = open(ecmpath, "rb").readlines()
				except:
					try:
						ecm = open("/tmp/ecm.info", "rb").readlines()
					except: pass
			if ecm:
				for line in ecm:
					x = line.lower().find("msec")
					if x != -1:
						info["ecm time"] = line[0:x+4]
					else:
						item = line.split(":", 1)
						if len(item) > 1:
							info[item[0].strip().lower()] = item[1].strip()
						else:
							if not info.has_key("caid"):
								x = line.lower().find("caid")
								if x != -1:
									y = line.find(",")
									if y != -1:
										info["caid"] = line[x+5:y]

		return info

	def changed(self, what):
		if (what[0] == self.CHANGED_SPECIFIC and what[1] == iPlayableService.evUpdatedInfo) or what[0] == self.CHANGED_POLL:
			Converter.changed(self, what)
