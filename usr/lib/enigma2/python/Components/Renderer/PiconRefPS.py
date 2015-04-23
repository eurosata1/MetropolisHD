from Tools.LoadPixmap import LoadPixmap
from Components.Pixmap import Pixmap
from Renderer import Renderer
from enigma import ePixmap, eTimer, iServiceInformation, iPlayableService, eDVBFrontendParametersSatellite, eDVBFrontendParametersCable
from Tools.Directories import fileExists, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, resolveFilename
from Components.config import *

class PiconRefPS(Renderer):
    searchPaths = ('/usr/share/enigma2/%s/', '/media/ba/%s/', '/media/cf/%s/', '/media/sda1/%s/', '/media/sda/%s/', '/media/usb/%s/')

    def __init__(self):
        Renderer.__init__(self)
        self.path = 'picon'
        self.nameCache = {}
        self.nameCache1 = {}
        self.nameCache2 = {}
        self.pngname = ''
        self.pngname1 = ''
        self.pngname2 = ''
        self.timerpicsPS = eTimer()
        self.timerpicsPS.callback.append(self.timerpicsPSEvent)
        self.serv = ''
        self.tuntst = ''

    def applySkin(self, desktop, parent):
        attribs = []
        for attrib, value in self.skinAttributes:
            if attrib == 'path':
                self.path = value
            else:
                attribs.append((attrib, value))

        self.skinAttributes = attribs
        return Renderer.applySkin(self, desktop, parent)

    GUI_WIDGET = ePixmap

    def changed(self, what):
        pngname = self.instance and ''
        if what[0] != self.CHANGED_CLEAR:
            service = self.source.service
            if service:
                if service:
                    info = service.info()
                    if not info:
                        return
                    ref = None
                    self.path = 'picon'
                    sname = info.getInfoString(iServiceInformation.sServiceref)
                    tuntst = self.getTunerInfo(service)
                    swt = True
                    if self.tuntst != tuntst:
                        self.tuntst != tuntst
                    if self.serv != sname or swt == True:
                        sname2 = '%s' % (sname)
                        #sname = service.toString()
                        self.serv = sname
                        pos = sname.rfind(':')
                        if pos != -1:
                            sname = '_'.join(sname.split(':', 10)[:10])
                        pngname = self.nameCache.get(sname, '')
                        if pngname == '':
                            pngname = self.findPicon(sname)
                            if pngname != '':
                                self.nameCache[sname] = pngname
                        if pngname == '':
                            pngname = self.nameCache.get('default', '')
                            if pngname == '':
                                pngname = self.findPicon('picon_default')
                                if pngname == '':
                                    tmp = resolveFilename(SCOPE_CURRENT_SKIN, 'picon_default.png')
                                    if fileExists(tmp):
                                        pngname = tmp
                                    else:
                                        pngname = resolveFilename(SCOPE_SKIN_IMAGE, 'skin_default/picon_default.png')
                                self.nameCache['default'] = pngname
                        if self.pngname != pngname:
                            self.pngname = pngname
                        if SCOPE_CURRENT_SKIN:
                                ref = None
                                provname = info.getInfoString(iServiceInformation.sProvider) 
                                pngname1 = ''
                                provname = '%s' % (provname)
                                if 'tvshka' in sname2:
                                    sname = "SCHURA"
                                elif 'vsadmin' in sname2:
                                    sname = "Vsadmin"
                                else:    
                                    if provname.startswith('T-K'):
                                        sname = 'T-KABEL'
                                    elif provname == 'T-Systems/MTI':
                                        sname = 'T-SYSTEMS'
                                    else:
                                        sname = provname.upper()
                                pngname1 = self.nameCache1.get(sname, '')
                                self.path = 'piconProv'
                                if pngname1 == '':
                                    pngname1 = self.findPicon(sname)
                                    if pngname1 != '':
                                        self.nameCache1[sname] = pngname1
                                if pngname1 == '':
                                    pngname1 = self.nameCache1.get('default', '')
                                    if pngname1 == '':
                                        pngname1 = self.findPicon('picon_default')
                                        if pngname1 == '':
                                            tmp = resolveFilename(SCOPE_CURRENT_SKIN, 'picon_default.png')
                                            if fileExists(tmp):
                                                pngname1 = tmp
                                            else:
                                                pngname1 = resolveFilename(SCOPE_SKIN_IMAGE, 'skin_default/picon_default.png')
                                        self.nameCache1['default'] = pngname1
                                if self.pngname1 != pngname1:
                                    self.pngname1 = pngname1
                                if 'http' in sname2:
                                       sname = "00E"
                                else:       
                                       sname = self.getTunerInfo(service)
                                pngname2 = self.nameCache2.get(sname, '')
                                self.path = 'piconSat'
                                if pngname2 == '':
                                    pngname2 = self.findPicon(sname)
                                    if pngname2 != '':
                                        self.nameCache2[sname] = pngname2
                                if pngname2 == '':
                                    pngname2 = self.nameCache2.get('default', '')
                                    if pngname2 == '':
                                        pngname2 = self.findPicon('picon_default')
                                        if pngname2 == '':
                                            tmp = resolveFilename(SCOPE_CURRENT_SKIN, 'picon_default.png')
                                            if fileExists(tmp):
                                                pngname2 = tmp
                                            else:
                                                pngname2 = resolveFilename(SCOPE_SKIN_IMAGE, 'skin_default/picon_default.png')
                                        self.nameCache2['default'] = pngname2
                                if self.pngname2 != pngname2:
                                    self.pngname2 = pngname2
                                self.runanim2(pngname, pngname1, pngname2)


    def findPicon(self, serviceName):
        if fileExists('/etc/piconPaths.conf'):
            try:
                f = open('/etc/piconPaths.conf', 'r')
                content = f.read()
                f.close()
            except:
                content = ''

            contentInfo = content.split('\n')
            if content != '':
                for line in contentInfo:
                    if line.startswith(self.path):
                        if line.__contains__('='):
                            stmp = str(line.split('=')[1].split())
                            pngname = stmp[2:-2] + self.path + '/' + serviceName + '.png'
                            if fileExists(pngname):
                                return pngname

        for path in self.searchPaths:
            pngname = path % self.path + serviceName + '.png'
            if fileExists(pngname):
                return pngname

        return ''

    def runanim2(self, pic1, pic2, pic3):
        self.slide = 3
        self.steps = 9
        self.pics = []
        self.pics.append(LoadPixmap(pic3))
        self.pics.append(LoadPixmap(pic2))
        self.pics.append(LoadPixmap(pic1))
        self.timerpicsPS.start(100, True)

    def timerpicsPSEvent(self):
        if self.steps != 0:
            self.timerpicsPS.stop()
            self.instance.setPixmap(self.pics[self.slide - 1])
            self.steps = self.steps - 1
            self.slide = self.slide - 1
            if self.slide == 0:
                self.slide = 3
            self.timerpicsPS.start(1000, True)
        else:
            self.timerpicsPS.stop()
            self.instance.setPixmapFromFile(self.pngname)

    def getTunerInfo(self, service):
        tunerinfo = ''
        if service:
            feinfo = service.frontendInfo()
            if feinfo is not None:
                frontendData = feinfo and feinfo.getAll(True)
                if frontendData is not None and frontendData.get('tuner_type') == 'DVB-S':
                    try:
                        orb = {3590: '10W',
                         3560: '40W',
                         3550: '50W',
                         3530: '70W',
                         3520: '80W',
                         3475: '125W',
                         3460: '140)',
                         3450: '150W',
                         3420: '180W',
                         3380: '220W',
                         3355: '245W',
                         3325: '275W',
                         3300: '300W',
                         3285: '315W',
                         3170: '430W',
                         3150: '450W',
                         3070: '530W',
                         3045: '555W',
                         3020: '580W',
                         2990: '610W',
                         2900: '700W',
                         2880: '720W',
                         2875: '727W',
                         2860: '740W',
                         2810: '790W',
                         2780: '820W',
                         2690: '910W',
                         3592: '08W',
                         2985: '615W',
                         2830: '770W',
                         2630: '970W',
                         2500: '1100W',
                         2502: '1100W',
                         2410: '1190W',
                         2391: '1210W',
                         2390: '1210W',
                         2412: '1190W',
                         2310: '1290W',
                         2311: '1290W',
                         2120: '1480W',
                         1100: '1100E',
                         1101: '1100E',
                         1131: '1130E',
                         1440: '1440E',
                         1006: '1005E',
                         1030: '1030E',
                         1056: '1055E',
                         1082: '1082E',
                         881: '880E',
                         900: '900E',
                         917: '915E',
                         950: '950E',
                         951: '950E',
                         765: '765E',
                         785: '785E',
                         800: '800E',
                         830: '830E',
                         850: '852E',
                         750: '750E',
                         720: '720E',
                         705: '705E',
                         685: '685E',
                         620: '620E',
                         600: '600E',
                         570: '570E',
                         530: '530E',
                         480: '480E',
                         450: '450E',
                         420: '420E',
                         400: '400E',
                         390: '390E',
                         380: '380E',
                         360: '360E',
                         335: '335E',
                         330: '330E',
                         328: '328E',
                         315: '315E',
                         310: '310E',
                         305: '305E',
                         285: '285E',
                         284: '282E',
                         282: '282E',
                         1220: '1220E',
                         1380: '1380E',
                         260: '260E',
                         255: '255E',
                         235: '235E',
                         215: '215E',
                         216: '216E',
                         210: '210E',
                         192: '192E',
                         160: '160E',
                         130: '130E',
                         100: '100E',
                         90: '90E',
                         70: '70E',
                         50: '50E',
                         48: '48E',
                         30: '30E'}[frontendData.get('orbital_position', 'None')]
                    except:
                        orb = 'Unsupported SAT: %s' % str([frontendData.get('orbital_position', 'None')])

                    tunerinfo = orb
                    return tunerinfo
                else:
                    return ''
        return ''
