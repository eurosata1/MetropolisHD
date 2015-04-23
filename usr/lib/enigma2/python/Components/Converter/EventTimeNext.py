# 2013.01.19 14:49:26 GST
#Embedded file name: /usr/lib/enigma2/python/Components/Converter/EventTimeNext.py
from Components.Converter.Converter import Converter
from Components.Element import cached, ElementError
from Components.Converter.Poll import Poll
from enigma import eEPGCache

class EventTimeNext(Poll, Converter, object):
    STARTTIME = 0
    ENDTIME = 1
    DURATION = 2

    def __init__(self, type):
        Converter.__init__(self, type)
        Poll.__init__(self)
        self.poll_interval = 60000
        self.poll_enabled = True
        if type == 'StartTime':
            self.type = self.STARTTIME
        elif type == 'EndTime':
            self.type = self.ENDTIME
        elif type == 'Duration':
            self.type = self.DURATION
        else:
            raise ElementError("'%s' is not <StartTime|EndTime|Duration> for EventTime converter" % type)
        self.epgcache = eEPGCache.getInstance()

    @cached
    def getTime(self):
        ref = self.source.service
        info = ref and self.source.info
        if info is None:
            return
        eventNext = self.epgcache.lookupEvent(['IBDCTSERNX', (ref.toString(), 1, -1)])
        if eventNext:
            if self.type == self.STARTTIME:
                return eventNext[0][1]
            if self.type == self.ENDTIME:
                if eventNext[0][1] is not None and eventNext[0][2] is not None:
                    return eventNext[0][1] + eventNext[0][2]
            elif self.type == self.DURATION:
                return eventNext[0][2]

    time = property(getTime)
# okay decompyling /tmp/EventTimeNext.pyo 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.01.19 14:49:35 GST
