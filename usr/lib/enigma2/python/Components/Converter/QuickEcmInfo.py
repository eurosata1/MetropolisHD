# QuickEcmInfo converter (c) 2boom 2012 v 0.6 07.4.2012
#<widget source="session.CurrentService" render="Label" position="462,153" size="50,22" font="Regular; 17" zPosition="2" backgroundColor="background1" foregroundColor="white" transparent="1">
#    <convert type="QuickEcmInfo">ecmfile | emuname | caids</convert>
#  </widget>

from Poll import Poll
from Components.Converter.Converter import Converter
from enigma import iServiceInformation, iPlayableService, eTimer
from Components.Element import cached
from Tools.Directories import fileExists
import os
try:
	from bitratecalc import eBitrateCalculator
except:
	pass

class QuickEcmInfo(Poll, Converter, object):
	ecmfile = 0
	emuname = 1
	caids = 2
	pids = 3
	vtype = 4
	activecaid = 5
	bitrate = 6
	txtcaid = 7
	
	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		if type == "ecmfile":
			self.type = self.ecmfile
		elif type == "emuname":
			self.type = self.emuname
		elif type == "caids":
			self.type = self.caids
		elif type == "pids":
			self.type = self.pids
		elif type == "vtype":
			self.type = self.vtype
		elif type == "activecaid":
			self.type = self.activecaid
		elif type == "bitrate":
			self.type = self.bitrate
		elif type == "txtcaid":
			self.type = self.txtcaid
		self.poll_interval = 1000
		self.poll_enabled = True
		self.clearData()
		self.initTimer = eTimer()
		self.initTimer.callback.append(self.initBitrateCalc)
		
		self.systemTxtCaids = {
			"26" : "BiSS",
			"01" : "Seca Mediaguard",
			"06" : "Irdeto",
			"17" : "BetaCrypt",
			"05" : "Viaccess",
			"18" : "Nagravision",
			"09" : "NDS-Videoguard",
			"0B" : "Conax",
			"0D" : "Cryptoworks",
			"4A" : "Pro-Crypt",
			"27" : "DRE-Crypt",
			"0E" : "PowerVu",
			"22" : "Codicrypt",
			"07" : "DigiCipher",
			"56" : "Verimatrix",
			"7B" : "DRE-Crypt",
			"A1" : "Rosscrypt"}

	def getServiceInfoString(self, info, what, convert = lambda x: "%d" % x):
		v = info.getInfo(what)
		if v == -1:
			return "N/A"
		if v == -2:
			return info.getInfoString(what)
		if v == -3:
			t_objs = info.getInfoObject(what)
			if t_objs and (len(t_objs) > 0):
				ret_val=""
				for t_obj in t_objs:
					ret_val += "%.4X " % t_obj
				return ret_val[:-1]
			else:
				return ""
		return convert(v)
		
	def clearData(self):
		self.videoBitrate = None
		self.audioBitrate = None
		self.video = self.audio = 0

	def initBitrateCalc(self):
		service = self.source.service
		vpid = apid = dvbnamespace = tsid = onid = -1
		if service:
			serviceInfo = service.info()
			vpid = serviceInfo.getInfo(iServiceInformation.sVideoPID)
			apid = serviceInfo.getInfo(iServiceInformation.sAudioPID)
			tsid = serviceInfo.getInfo(iServiceInformation.sTSID)
			onid = serviceInfo.getInfo(iServiceInformation.sONID)
			dvbnamespace = serviceInfo.getInfo(iServiceInformation.sNamespace)
		if vpid > 0 and self.type == self.bitrate:
			try:
				self.videoBitrate = eBitrateCalculator(vpid, dvbnamespace, tsid, onid, 1000, 1024*1024) 
				self.videoBitrate.callback.append(self.getVideoBitrateData)
			except:
				pass
		if apid > 0 and self.type == self.bitrate:
			try:
				self.audioBitrate = eBitrateCalculator(apid, dvbnamespace, tsid, onid, 1000, 64*1024)
				self.audioBitrate.callback.append(self.getAudioBitrateData)
			except:
				pass
		
	def caidstr(self):
		caidvalue = ""
		value = "0000"
		service = self.source.service
		info = service and service.info()
		if not info:
			return ""
		if self.getServiceInfoString(info, iServiceInformation.sCAIDs):
			if fileExists("/tmp/ecm.info"):
				try:
					for line in open("/tmp/ecm.info"):
						if line.find("caid:") > -1:
							caidvalue = line.strip("\n").split()[-1][2:]
							if len(caidvalue) < 4:
								caidvalue = value[len(caidvalue):] + caidvalue
						elif line.find("CaID") > -1 or line.find("CAID") > -1:
							caidvalue = line.split(",")[0].split()[-1][2:]
				except:
					pass
		return caidvalue
		
	@cached
	def getText(self):
		ecminfo = ""
		caidvalue = ""
		service = self.source.service
		info = service and service.info()
		if not info:
			return ""
			
		if self.type == self.vtype:
			try:
				return ("MPEG2", "MPEG4", "MPEG1", "MPEG4-II", "VC1", "VC1-SM", "")[info.getInfo(iServiceInformation.sVideoType)]
			except: 
				return " "
			
		elif self.type == self.bitrate:
			audio = service.audioTracks()
			yres = info.getInfo(iServiceInformation.sVideoHeight)
			mode = ("i", "p", "")[info.getInfo(iServiceInformation.sProgressive)]
			xres = info.getInfo(iServiceInformation.sVideoWidth)
			try:
				return "%sx%s(%s) VIDEO %s: %d kbit/s  AUDIO %s: %d kbit/s" % (str(xres), str(yres) + mode, self.getServiceInfoString(info, iServiceInformation.sFrameRate, lambda x: "%d" % ((x+500)/1000)), ("MPEG2", "MPEG4", "MPEG1", "MPEG4-II", "VC1", "VC1-SM", "")[info.getInfo(iServiceInformation.sVideoType)], self.video,str(audio.getTrackInfo(audio.getCurrentTrack()).getDescription()), self.audio)
			except: 
				return " "
				
		elif self.type == self.txtcaid:
			caidvalue = "%s" % self.systemTxtCaids.get(self.caidstr()[:2]) 
			if caidvalue != "None":
				return caidvalue
			else:
				return " "
			
		elif self.type == self.ecmfile:
			if self.getServiceInfoString(info, iServiceInformation.sCAIDs):
				try:
					ecmfiles = open("/tmp/ecm.info", "r")
					for line in ecmfiles:
						if line.find("caid:") > -1 or line.find("provider:") > -1 or line.find("provid:") > -1 or line.find("pid:") > -1 or line.find("hops:") > -1  or line.find("system:") > -1 or line.find("address:") > -1 or line.find("using:") > -1 or line.find("ecm time:") > -1:
							line = line.replace(' ',"").replace(":",": ")
						if line.find("caid:") > -1 or line.find("pid:") > -1 or line.find("reader:") > -1 or line.find("from:") > -1 or line.find("hops:") > -1  or line.find("system:") > -1 or line.find("Service:") > -1 or line.find("CAID:") > -1 or line.find("Provider:") > -1:
							line = line.strip('\n') + "  "
						if line.find("Signature") > -1:
							line = ""
						if line.find("=") > -1:
							line = line.lstrip('=').replace('======', "").replace('\n', "").rstrip() + ', '
						if line.find("ecmtime:") > -1:
							line = line.replace("ecmtime:", "ecm time:")
						if line.find("response time:") > -1:
							line = line.replace("response time:", "ecm time:").replace("decoded by", "by")
						if not line.startswith('\n'):
							if line.find('pkey:') > -1:
								line = '\n' + line + '\n'
							ecminfo += line
					ecmfiles.close()
				except:
					pass
###############################################################################
		elif self.type == self.activecaid:
			caidvalue = self.caidstr()
			return caidvalue
					
		elif self.type == self.pids:
			try:
				return "SID: %0.4X  VPID: %0.4X  APID: %0.4X  PRCPID: %0.4X  TSID: %0.4X  ONID: %0.4X" % (int(self.getServiceInfoString(info, iServiceInformation.sSID)), int(self.getServiceInfoString(info, iServiceInformation.sVideoPID)), int(self.getServiceInfoString(info, iServiceInformation.sAudioPID)), int(self.getServiceInfoString(info, iServiceInformation.sPCRPID)), int(self.getServiceInfoString(info, iServiceInformation.sTSID)), int(self.getServiceInfoString(info, iServiceInformation.sONID)))
			except:
				try:
					return "SID: %0.4X  APID: %0.4X  PRCPID: %0.4X  TSID: %0.4X  ONID: %0.4X" % (int(self.getServiceInfoString(info, iServiceInformation.sSID)), int(self.getServiceInfoString(info, iServiceInformation.sAudioPID)), int(self.getServiceInfoString(info, iServiceInformation.sPCRPID)), int(self.getServiceInfoString(info, iServiceInformation.sTSID)), int(self.getServiceInfoString(info, iServiceInformation.sONID)))
				except:
					return " "
			
		elif self.type == self.caids:
			try:
				ecminfo = self.getServiceInfoString(info, iServiceInformation.sCAIDs)
			except:
				ecminfo = " "
					
		if self.type == self.emuname:
			serlist = None
			camdlist = None
			nameemu = []
			nameser = []
			# TS-Panel
			if fileExists("/etc/startcam.sh"):
				try:
					for line in open("/etc/startcam.sh"):
						if line.find("script") > -1:
							return "%s" % line.split("/")[-1].split()[0][:-3]
				except:
					camdlist = None
					
					
			#HDMU
			elif fileExists("/etc/.emustart") and fileExists("/etc/image-version"):
				try:
					for line in open("/etc/.emustart"):
						return line.split()[0].split('/')[-1]
				except:
					camdlist = None
			# AAF
			elif fileExists("/etc/image-version") and not fileExists("/etc/.emustart"):
				for line in open("/etc/image-version"):
					if line.find("=AAF") > -1:
						for line in open("/etc/enigma2/settings"):
							if line.find("config.softcam.actCam=") > -1:
								return line.split("=")[-1].strip('\n')
			# VTI 	
			elif fileExists("/tmp/.emu.info"):
				try:
					camdlist = open("/tmp/.emu.info", "r")
				except:
					camdlist = None
			# BlackHole	
			elif fileExists("/etc/CurrentBhCamName"):
				try:
					camdlist = open("/etc/CurrentBhCamName", "r")
				except:
					camdlist = None
			# Domica	
			elif fileExists("/etc/active_emu.list"):
				try:
					camdlist = open("/etc/active_emu.list", "r")
				except:
					camdlist = None
			# domica 8120
			elif fileExists("/etc/init.d/cam"):
				for line in open("/etc/enigma2/settings"):
					if line.find("config.plugins.emuman.cam") > -1:
						return line.split("=")[-1].strip('\n')
			#Pli
			elif fileExists("/etc/init.d/softcam") or fileExists("/etc/init.d/cardserver"):
				try:
					for line in open("/etc/init.d/softcam"):
						if line.find("echo") > -1:
							nameemu.append(line)
					camdlist = "%s" % nameemu[1].split('"')[1]
				except:
					pass
				try:
					for line in open("/etc/init.d/cardserver"):
						if line.find("echo") > -1:
							nameser.append(line)
					serlist = "%s" % nameser[1].split('"')[1]
				except:
					pass
				if serlist is None:
					serlist = ""
				elif camdlist is None:
					camdlist = ""
				elif serlist is None and camdlist is None:
					serlist = ""
					camdlist = ""
				return ("%s %s" % (serlist, camdlist))
			# OoZooN
			elif fileExists("/tmp/cam.info"):
				try:
					camdlist = open("/tmp/cam.info", "r")
				except:
					camdlist = None
			# Merlin2	
			elif fileExists("/etc/clist.list"):
				try:
					camdlist = open("/etc/clist.list", "r")
				except:
					camdlist = None
			# GP3
			elif fileExists("/usr/lib/enigma2/python/Plugins/Bp/geminimain/lib/libgeminimain.so"):
				try:
					from Plugins.Bp.geminimain.plugin import GETCAMDLIST
					from Plugins.Bp.geminimain.lib import libgeminimain
					camdl = libgeminimain.getPyList(GETCAMDLIST)
					for x in camdl:
						if x[1] == 1:
							camdlist = x[2] 
				except:
					camdlist = None
			# Unknown emu
			else:
				camdlist = None
				
			if serlist is not None:
				try:
					cardserver = ""
					for current in serlist.readlines():
						cardserver = current
					serlist.close()
				except:
					pass
			else:
				cardserver = ""

			if camdlist is not None:
				try:
					emu = ""
					for current in camdlist.readlines():
						emu = current
					camdlist.close()
				except:
					pass
			else:
				emu = ""
			ecminfo = "%s %s" % (cardserver.split('\n')[0], emu.split('\n')[0])
		return ecminfo
		
	text = property(getText)
	
	def getVideoBitrateData(self, value, status):
		if status:
			self.video = value
		else:
			self.videoBitrate = None
			self.video = 0
		Converter.changed(self, (self.CHANGED_POLL,))

	def getAudioBitrateData(self, value, status):
		if status:
			self.audio = value
		else:
			self.audioBitrate = None
			self.audio = 0
		Converter.changed(self, (self.CHANGED_POLL,))

	def changed(self, what):
		if what[0] == self.CHANGED_SPECIFIC:
			if what[1] == iPlayableService.evStart:
				self.initTimer.start(200, True)
			elif what[1] == iPlayableService.evEnd:
				self.clearData()
				Converter.changed(self, what)
		elif what[0] == self.CHANGED_POLL:
			self.downstream_elements.changed(what)
