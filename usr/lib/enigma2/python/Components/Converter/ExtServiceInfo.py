# 2013.01.19 14:36:38 GST
#Embedded file name: /usr/lib/enigma2/python/Components/Converter/ExtServiceInfo.py
from Components.config import config
from Components.Converter.Converter import Converter
from Components.Element import cached
from enigma import eServiceCenter, eServiceReference, iServiceInformation, iPlayableService, iPlayableServicePtr
from Tools.Transponder import ConvertToHumanReadable
from Tools.Directories import pathExists
from string import upper, zfill
from xml.etree.cElementTree import parse

class CashSatList:
    CashSatList = {}

    def __init__(self):
        basicsatxml = parse('/etc/tuxbox/satellites.xml').getroot()
        if basicsatxml is not None:
            for sat in basicsatxml.findall('sat'):
                satname = str(sat.get('name').encode('UTF-8')).split('(')[0][:-1]
                satpos = int(sat.get('position'))
                if satpos < 0:
                    satpos += 3600
                self.CashSatList[str(satpos)] = satname


class CashServiceList:
    CashServiceList = {}

    def __init__(self):
        if not pathExists('/etc/enigma2/lamedb'):
            return
        file = open('/etc/enigma2/lamedb')
        readlines = file.readlines()
        f_service = False
        i = 0
        for n in xrange(0, len(readlines)):
            if readlines[n] == 'services\n':
                f_service = True
                continue
            if not f_service:
                continue
            if readlines[n] == 'end\n':
                break
            if i == 0:
                referens = [ x.upper() for x in readlines[n].split(':') ]
                if referens[0] == 'S':
                    serviceid = zfill(referens[4], 4) + ':' + zfill(referens[7], 8) + ':' + zfill(referens[5], 4) + ':' + zfill(referens[6], 4)
                else:
                    serviceid = referens[0] + ':' + referens[1] + ':' + referens[2] + ':' + referens[3]
            if i == 2:
                provider = readlines[n].split(':')[1].split(',')[0].rstrip('\n')
            i += 1
            if i == 3:
                i = 0
                self.CashServiceList[serviceid] = provider

        file.close()


cashSatList = CashSatList()
cashServiceList = CashServiceList()

class ExtServiceInfo(Converter, object):
    PROVIDER = 0
    SERVICENAME = 1
    SATNAME = 2
    ORBITALPOSITION = 3
    SATNAMEORBITALPOSITION = 4
    FROMCONFIGPROVIDER = 5
    FROMCONFIGPROVIDERMULTILINE = 6
    FREQUENCY = 7
    MODULATION = 8
    SYMBOLRATE = 9
    POLARIZATION = 10
    POLARIZATIONSHORT = 11
    FECINNER = 12
    TUNER = 13
    ALL = 14

    def __init__(self, type):
        Converter.__init__(self, type)
        if type == 'Provider':
            self.type = self.PROVIDER
        elif type == 'ServiceName':
            self.type = self.SERVICENAME
        elif type == 'SatName':
            self.type = self.SATNAME
        elif type == 'OrbitalPosition':
            self.type = self.ORBITALPOSITION
        elif type == 'SatNameOrbitalPosition':
            self.type = self.SATNAMEORBITALPOSITION
        elif type == 'ConfigProvider':
            self.type = self.FROMCONFIGPROVIDER
        elif type == 'ConfigProviderMultiline':
            self.type = self.FROMCONFIGPROVIDERMULTILINE
        elif type == 'ServiceFrequency':
            self.type = self.FREQUENCY
        elif type == 'ServiceModulation':
            self.type = self.MODULATION
        elif type == 'ServiceSymbolrate':
            self.type = self.SYMBOLRATE
        elif type == 'ServicePolarization':
            self.type = self.POLARIZATION
        elif type == 'ServicePolarizationShort':
            self.type = self.POLARIZATIONSHORT
        elif type == 'ServiceFEC':
            self.type = self.FECINNER
        elif type == 'Tuner':
            self.type = self.TUNER
        else:
            self.type = self.ALL

    @cached
    def getText(self):
        service = self.source.service
        if isinstance(service, iPlayableServicePtr):
            info = service and service.info()
            ref = None
        else:
            info = service and self.source.info
            ref = service
        if info is None:
            return ''
        elif self.type == self.SERVICENAME:
            return self.getServiceName(info, ref)
        elif self.type == self.PROVIDER:
            return self.getProviderName(service, info, ref)
        elif self.type == self.SATNAME:
            return self.getSatName(service, info, ref)
        elif self.type == self.ORBITALPOSITION:
            return self.getOrbitalPosition(service)
        elif self.type == self.SATNAMEORBITALPOSITION:
            satname = self.getSatName(service, info, ref)
            position = self.getOrbitalPosition(service)
            ret = satname
            if not position == '':
                ret = satname + ' (' + position + ')'
            return ret
        elif self.type == self.FREQUENCY:
            return self.getServiceFrequency(service)
        elif self.type == self.MODULATION:
            return self.getServiceModulation(service)
        elif self.type == self.SYMBOLRATE:
            return self.getServiceSymbolrate(service)
        elif self.type == self.POLARIZATION:
            return self.getServicePolarization(service)
        elif self.type == self.POLARIZATIONSHORT:
            return self.getServicePolarizationShort(service)
        elif self.type == self.FECINNER:
            return self.getServiceFEC(service)
        elif self.type == self.TUNER:
            return self.getServiceTuner(service)
        elif self.type == self.FROMCONFIGPROVIDER:
            provider = self.getProviderName(service, info, ref)
            satname = self.getSatName(service, info, ref)
            position = self.getOrbitalPosition(service)
            ret = provider
            if config.usage.show_sat_name_of_infobar.value == True and not satname == '':
                ret += ' / ' + satname
            if config.usage.show_orbital_position_of_infobar.value == True and not position == '':
                ret += ' (' + position + ')'
            return ret
        elif self.type == self.FROMCONFIGPROVIDERMULTILINE:
            provider = self.getProviderName(service, info, ref)
            satname = self.getSatName(service, info, ref)
            position = self.getOrbitalPosition(service)
            ret = provider
            if config.usage.show_sat_name_of_infobar.value == True and not satname == '':
                ret += '\n' + satname
            if config.usage.show_orbital_position_of_infobar.value == True and not position == '':
                ret += ' (' + position + ')'
            return ret
        else:
            name = self.getServiceName(info, ref)
            provider = self.getProviderName(service, info, ref)
            satname = self.getSatName(service, info, ref)
            position = self.getOrbitalPosition(service)
            return '%s - %s / %s (%s)' % (name,
             provider,
             satname,
             position)

    text = property(getText)

    def getServiceInfoValue(self, info, what, ref = None):
        v = ref and info.getInfo(ref, what) or info.getInfo(what)
        if v != iServiceInformation.resIsString:
            return 'N/A'
        return ref and info.getInfoString(ref, what) or info.getInfoString(what)

    def getServiceName(self, info, ref):
        name = ref and info.getName(ref)
        if name is None:
            name = info.getName()
        return name.replace('\xc2\x86', '').replace('\xc2\x87', '')

    def getSatName(self, service, info, ref):
        frontendDataOrg = None
        if isinstance(service, iPlayableServicePtr):
            feinfo = service.frontendInfo()
            if feinfo is not None:
                frontendDataOrg = feinfo and feinfo.getAll(True)
        if isinstance(service, eServiceReference):
            infoService = eServiceCenter.getInstance().info(service)
            frontendDataOrg = infoService.getInfoObject(service, iServiceInformation.sTransponderData)
        if frontendDataOrg and len(frontendDataOrg):
            frontendData = ConvertToHumanReadable(frontendDataOrg)
            if frontendDataOrg['tuner_type'] == 'DVB-S':
                orb = self.getOrbitalPosition(service, 1)
                if orb in cashSatList.CashSatList:
                    return str(cashSatList.CashSatList[orb])
                return ''
            if frontendDataOrg['tuner_type'] == 'DVB-T':
                return _('Terrestrial')
            if frontendDataOrg['tuner_type'] == 'DVB-C':
                return _('Cable')
        if isinstance(service, eServiceReference):
            referens = service.toString()
        else:
            referens = self.getServiceInfoValue(info, iServiceInformation.sServiceref, ref)
        pos = referens.find(':')
        if pos != -1:
            referens = [ x.upper() for x in referens.split(':') ]
            if referens[0] == '1' and referens[1] == '0' and referens[2] == '1' and referens[3] == '0' and referens[4] != '0' and referens[5] == '0' and referens[6] != '0' and referens[7] == '0' and referens[8] == '0' and referens[9] == '0':
                return 'IPTV'
            if referens[0] == '1' and referens[1] == '0' and referens[2] == '0' and referens[3] == '0' and referens[4] == '0' and referens[5] == '0' and referens[6] == '0' and referens[7] == '0' and referens[8] == '0' and referens[9] == '0':
                return 'IPTV'
        return ''

    def getProviderName(self, service, info, ref):
        if isinstance(service, eServiceReference):
            referens = service.toString()
        else:
            referens = self.getServiceInfoValue(info, iServiceInformation.sServiceref, ref)
        pos = referens.find(':')
        if pos != -1:
            referens = [ x.upper() for x in referens.split(':') ]
            serviceid = zfill(referens[3], 4) + ':' + zfill(referens[6], 8) + ':' + zfill(referens[4], 4) + ':' + zfill(referens[5], 4)
            if cashServiceList.CashServiceList.has_key(serviceid):
                return cashServiceList.CashServiceList[serviceid]
        return ''

    def getOrbitalPosition(self, service, mode = 0):
        orbital = 0
        frontendDataOrg = None
        if isinstance(service, iPlayableServicePtr):
            feinfo = service.frontendInfo()
            if feinfo is not None:
                frontendDataOrg = feinfo and feinfo.getAll(True)
        if isinstance(service, eServiceReference):
            info = eServiceCenter.getInstance().info(service)
            frontendDataOrg = info.getInfoObject(service, iServiceInformation.sTransponderData)
        if frontendDataOrg and len(frontendDataOrg):
            if frontendDataOrg['tuner_type'] == 'DVB-S':
                orbital = int(frontendDataOrg['orbital_position'])
                if mode == 1:
                    return str(orbital)
                if orbital > 3600:
                    return ''
                if orbital > 1800:
                    return str(float(3600 - orbital) / 10.0) + 'W'
                if orbital > 0:
                    return str(float(orbital) / 10.0) + 'E'
        return ''

    def getServiceFrequency(self, service):
        frontendDataOrg = None
        if isinstance(service, iPlayableServicePtr):
            feinfo = service.frontendInfo()
            if feinfo is not None:
                frontendDataOrg = feinfo and feinfo.getAll(True)
        if isinstance(service, eServiceReference):
            info = eServiceCenter.getInstance().info(service)
            frontendDataOrg = info.getInfoObject(service, iServiceInformation.sTransponderData)
        if frontendDataOrg and len(frontendDataOrg):
            frontendData = ConvertToHumanReadable(frontendDataOrg)
            if frontendDataOrg['tuner_type'] == 'DVB-S':
                return str(int(frontendData['frequency']) / 1000) + 'MHz'
            if frontendDataOrg['tuner_type'] == 'DVB-T':
                return str(int(frontendData['frequency']) / 1000000) + 'MHz'
            if frontendDataOrg['tuner_type'] == 'DVB-C':
                return str(int(frontendData['frequency']) / 1000) + 'MHz'
        return ''

    def getServiceModulation(self, service):
        frontendDataOrg = None
        if isinstance(service, iPlayableServicePtr):
            feinfo = service.frontendInfo()
            if feinfo is not None:
                frontendDataOrg = feinfo and feinfo.getAll(True)
        if isinstance(service, eServiceReference):
            info = eServiceCenter.getInstance().info(service)
            frontendDataOrg = info.getInfoObject(service, iServiceInformation.sTransponderData)
        if frontendDataOrg and len(frontendDataOrg):
            frontendData = ConvertToHumanReadable(frontendDataOrg)
            if frontendDataOrg['tuner_type'] == 'DVB-S':
                return str(frontendData['modulation'])
        return ''

    def getServiceSymbolrate(self, service):
        frontendDataOrg = None
        if isinstance(service, iPlayableServicePtr):
            feinfo = service.frontendInfo()
            if feinfo is not None:
                frontendDataOrg = feinfo and feinfo.getAll(True)
        if isinstance(service, eServiceReference):
            info = eServiceCenter.getInstance().info(service)
            frontendDataOrg = info.getInfoObject(service, iServiceInformation.sTransponderData)
        if frontendDataOrg and len(frontendDataOrg):
            frontendData = ConvertToHumanReadable(frontendDataOrg)
            if frontendDataOrg['tuner_type'] == 'DVB-S':
                return str(int(frontendData['symbol_rate']) / 1000)
        return ''

    def getServicePolarization(self, service):
        frontendDataOrg = None
        if isinstance(service, iPlayableServicePtr):
            feinfo = service.frontendInfo()
            if feinfo is not None:
                frontendDataOrg = feinfo and feinfo.getAll(True)
        if isinstance(service, eServiceReference):
            info = eServiceCenter.getInstance().info(service)
            frontendDataOrg = info.getInfoObject(service, iServiceInformation.sTransponderData)
        if frontendDataOrg and len(frontendDataOrg):
            frontendData = ConvertToHumanReadable(frontendDataOrg)
            if frontendDataOrg['tuner_type'] == 'DVB-S':
                return upper(str(frontendData['polarization']))
        return ''

    def getServicePolarizationShort(self, service):
        frontendDataOrg = None
        if isinstance(service, iPlayableServicePtr):
            feinfo = service.frontendInfo()
            if feinfo is not None:
                frontendDataOrg = feinfo and feinfo.getAll(True)
        if isinstance(service, eServiceReference):
            info = eServiceCenter.getInstance().info(service)
            frontendDataOrg = info.getInfoObject(service, iServiceInformation.sTransponderData)
        if frontendDataOrg and len(frontendDataOrg):
            frontendData = ConvertToHumanReadable(frontendDataOrg)
            if frontendDataOrg['tuner_type'] == 'DVB-S':
                return upper(str(frontendData['polarization_short']))
        return ''

    def getServiceFEC(self, service):
        frontendDataOrg = None
        if isinstance(service, iPlayableServicePtr):
            feinfo = service.frontendInfo()
            if feinfo is not None:
                frontendDataOrg = feinfo and feinfo.getAll(True)
        if isinstance(service, eServiceReference):
            info = eServiceCenter.getInstance().info(service)
            frontendDataOrg = info.getInfoObject(service, iServiceInformation.sTransponderData)
        if frontendDataOrg and len(frontendDataOrg):
            frontendData = ConvertToHumanReadable(frontendDataOrg)
            if frontendDataOrg['tuner_type'] == 'DVB-S':
                return str(frontendData['fec_inner'])
        return ''

    def changed(self, what):
        if what[0] != self.CHANGED_SPECIFIC or what[1] in [iPlayableService.evUpdatedInfo] or what[1] in [iPlayableService.evStart]:
            Converter.changed(self, what)
# okay decompyling /tmp/ExtServiceInfo.pyo 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.01.19 14:37:37 GST
