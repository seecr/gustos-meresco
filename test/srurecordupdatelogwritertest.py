## begin license ##
#
# "Gustos-Meresco" is a set of Gustos components for Meresco based projects.
#
# Copyright (C) 2014 Seecr (Seek You Too B.V.) http://seecr.nl
#
# This file is part of "Gustos-Meresco"
#
# "Gustos-Meresco" is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# "Gustos-Meresco" is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with "Gustos-Meresco"; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
## end license ##

from seecr.test import SeecrTestCase, CallTrace
from weightless.core import be
from meresco.core import Observable
from gustos.meresco import SruRecordUpdateCountLogWriter, HttpRequestUploadLogWriter
from gustos.common.units import TIME, COUNT, MEMORY
from time import sleep

class SruRecordUpdateLogWriterTest(SeecrTestCase):
    def setUp(self):
        SeecrTestCase.setUp(self)
        self.observerTime = CallTrace('gustosclient')
        self.observerCount = CallTrace('gustosclient')
        self.top = be((Observable(),
            (HttpRequestUploadLogWriter(gustosGroup='gustosGroup', scopeNames=('update-scope',)),
                (self.observerTime,)
            ),
            (SruRecordUpdateCountLogWriter(gustosGroup='gustosGroup', scopeNames=('update-scope',), interval=0.1),
                (self.observerCount,)
            )
        ))

    def testUpdate(self):
        collectedLog = exampleUpdateLog()
        self.top.do.writeLog(collectedLog)
        self.assertEquals(['report'], self.observerTime.calledMethodNames())
        self.assertEquals(['report'], self.observerCount.calledMethodNames())
        self.maxDiff = None
        self.assertEquals({
            'gustosGroup': {
                'Upload duration': {
                    'duration': { TIME: 0.3 }
                },
                'Upload size': {
                    'size': { MEMORY: 3120 },
                },
            }
        }, self.observerTime.calledMethods[-1].kwargs['values'])
        self.assertEquals({
            'gustosGroup': {
                'Upload count': {
                    'Uploads': { COUNT: 1 },
                    'Add': { COUNT: 1 },
                    'Delete': { COUNT: 0},
                },
            }
        }, self.observerCount.calledMethods[-1].kwargs['values'])

    def testDoNotLogIfNotEnabled(self):
        collectedLog = exampleUpdateLog()
        collectedLog['sruRecordUpdate'] = collectedLog['update-scope']['sruRecordUpdate']
        del collectedLog['update-scope']
        self.top.do.writeLog(collectedLog)
        self.assertEquals([], self.observerTime.calledMethodNames())
        self.assertEquals([], self.observerCount.calledMethodNames())

    def testReportInterval(self):
        self.top.do.writeLog(createCollectedLog(size=100))
        self.assertEquals(['report'], self.observerTime.calledMethodNames())
        self.assertEquals(['report'], self.observerCount.calledMethodNames())
        self.assertEquals(1, self.lastUploadsCount())
        self.assertEquals(100, self.lastUploadSize())
        self.top.do.writeLog(createCollectedLog(size=200))
        self.assertEquals(['report', 'report'], self.observerTime.calledMethodNames())
        self.assertEquals(['report'], self.observerCount.calledMethodNames())
        sleep(0.11)
        self.top.do.writeLog(createCollectedLog(size=400))
        self.assertEquals(['report', 'report', 'report'], self.observerTime.calledMethodNames())
        self.assertEquals(['report', 'report'], self.observerCount.calledMethodNames())
        self.assertEquals(3, self.lastUploadsCount())
        self.assertEquals(400, self.lastUploadSize())

    def testReportIntervalEnabledForAll(self):
        self.top.do.setInterval(0.1)
        self.top.do.writeLog(createCollectedLog(size=100))
        self.assertEquals(['report'], self.observerTime.calledMethodNames())
        self.assertEquals(['report'], self.observerCount.calledMethodNames())
        self.assertEquals(1, self.lastUploadsCount())
        self.assertEquals(100, self.lastUploadSize())
        self.top.do.writeLog(createCollectedLog(size=200))
        self.assertEquals(['report'], self.observerTime.calledMethodNames())
        self.assertEquals(['report'], self.observerCount.calledMethodNames())
        sleep(0.11)
        self.top.do.writeLog(createCollectedLog(size=400))
        self.assertEquals(['report', 'report'], self.observerTime.calledMethodNames())
        self.assertEquals(['report', 'report'], self.observerCount.calledMethodNames())
        self.assertEquals(3, self.lastUploadsCount())
        self.assertEquals(400, self.lastUploadSize())

    def testReportIntervalDisabledForAll(self):
        self.top.do.setInterval(None)
        self.top.do.writeLog(createCollectedLog(size=100))
        self.assertEquals(['report'], self.observerTime.calledMethodNames())
        self.assertEquals(['report'], self.observerCount.calledMethodNames())
        self.assertEquals(1, self.lastUploadsCount())
        self.assertEquals(100, self.lastUploadSize())
        self.top.do.writeLog(createCollectedLog(size=200))
        self.assertEquals(['report', 'report'], self.observerTime.calledMethodNames())
        self.assertEquals(['report', 'report'], self.observerCount.calledMethodNames())
        sleep(0.11)
        self.top.do.writeLog(createCollectedLog(size=400))
        self.assertEquals(['report', 'report', 'report'], self.observerTime.calledMethodNames())
        self.assertEquals(['report', 'report', 'report'], self.observerCount.calledMethodNames())
        self.assertEquals(3, self.lastUploadsCount())
        self.assertEquals(400, self.lastUploadSize())

    def lastUploadsCount(self):
        return self.observerCount.calledMethods[-1].kwargs['values']['gustosGroup']['Upload count']['Uploads'][COUNT]
    def lastUploadSize(self):
        return self.observerTime.calledMethods[-1].kwargs['values']['gustosGroup']['Upload size']['size'][MEMORY]

def createCollectedLog(size):
    collectedLog = exampleUpdateLog()
    collectedLog['httpRequest']['bodySize'] = [size]
    return collectedLog

def exampleUpdateLog():
    return {
        'httpRequest': {
            'timestamp': [1396605006.383859],
            'Headers': [{'Content-Length': '3120', 'Content-Type': 'text/xml; charset="utf-8"'}],
            'Client': [('127.0.0.1', 55015)],
            'arguments': [{}],
            'RequestURI': ['/edurep/update'],
            'query': [''],
            'path': ['/edurep/update'],
            'HTTPVersion': ['1.0'],
            'Method': ['POST'],
            'bodySize': [3120]
        },
        'httpResponse': {
            'duration': [0.3],
            'httpStatus': ['200'],
            'size': [306]
        },
        'update-scope': {
            'sruRecordUpdate': {
                'add': ['EdurepDev:http://take-shape-share.fenc.org.uk/rsrc/rsrc_opn.aspx?id=222']
            }
        }
    }


def exampleValidationError():
    return {
        'httpRequest': {
            'timestamp': [1396605121.423284],
            'Headers': [{
                'Content-Length': '2306',
                'Content-Type': 'text/xml; charset="utf-8"'
            }],
            'Client': [('127.0.0.1', 58952)],
            'arguments': [{}],
            'RequestURI': ['/edurep/update'],
            'query': [''],
            'path': ['/edurep/update'],
            'HTTPVersion': ['1.0'],
            'Method': ['POST'],
            'bodySize': [2306]
        },
        'httpResponse': {
            'duration': [0.013213872909545898],
            'httpStatus': ['200'],
            'size': [1984]
        },
        'update-scope': {
            'sruRecordUpdate': {
                'errorType': ['ValidateException'],
                'add': ['EdurepDev:http://take-shape-share.fenc.org.uk/rsrc/rsrc_opn.aspx?id=1002'],
                'errorMessage': ['Something very bad happened.']
            }
        }
    }
