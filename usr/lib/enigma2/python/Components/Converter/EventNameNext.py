# 2013.01.19 14:50:51 GST
#Embedded file name: /usr/lib/enigma2/python/Components/Converter/EventNameNext.py
from Components.Converter.Converter import Converter
from Components.Element import cached, ElementError
from Components.Converter.Poll import Poll
from enigma import eEPGCache

class EventNameNext(Poll, Converter, object):
    NAME = 0
    SHORT_DESCRIPTION = 1
    EXTENDED_DESCRIPTION = 2
    SHORT_EXTENDED_DESCRIPTION = 3
    ID = 4

    def __init__(self, type):
        Converter.__init__(self, type)
        Poll.__init__(self)
        self.poll_interval = 60000
        self.poll_enabled = True
        if type == 'Name':
            self.type = self.NAME
        elif type == 'Description':
            self.type = self.SHORT_DESCRIPTION
        elif type == 'ExtendedDescription':
            self.type = self.EXTENDED_DESCRIPTION
        elif type == 'ShortOrExtendedDescription':
            self.type = self.SHORT_EXTENDED_DESCRIPTION
        elif type == 'ID':
            self.type = self.ID
        else:
            raise ElementError("'%s' is not <Name|Description|ExtendedDescription|ShortOrExtendedDescription|ID> for EventTime converter" % type)
        self.epgcache = eEPGCache.getInstance()

    @cached
    def getText(self):
        ref = self.source.service
        info = ref and self.source.info
        if info is None:
            return ''
        eventNext = self.epgcache.lookupEvent(['IBDCTSERNX', (ref.toString(), 1, -1)])
        if eventNext:
            if self.type == self.SHORT_DESCRIPTION:
                return eventNext[0][5]
            if self.type == self.EXTENDED_DESCRIPTION:
                return eventNext[0][6]
            if self.type == self.SHORT_EXTENDED_DESCRIPTION:
                short = eventNext[0][5]
                ext = eventNext[0][6]
                text = ''
                if short is not None and ext is not None:
                    if len(short) > 0:
                        text = short
                    if len(ext) > 0:
                        text = text.strip() + ' ' + ext.strip()
                    text = text.lstrip().lstrip('-').lstrip()
                return text
            if self.type == self.NAME:
                return eventNext[0][4]
            if self.type == self.ID:
                return eventNext[0][7]
        return ''

    text = property(getText)
# okay decompyling /tmp/EventNameNext.pyo 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.01.19 14:51:01 GST
