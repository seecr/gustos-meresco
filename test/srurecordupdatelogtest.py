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
from gustos.meresco import SruRecordUpdateLog
from gustos.common.units import TIME, COUNT, MEMORY

class SruRecordUpdateLogTest(SeecrTestCase):
    def setUp(self):
        SeecrTestCase.setUp(self)
        self.observer = CallTrace('gustosclient')
        self.top = be((Observable(),
            (SruRecordUpdateLog(gustosGroup='gustosGroup', scopeNames=('update-scope',)),
                (self.observer,)
            )
        ))

    def testUpdate(self):
        collectedLog = exampleUpdateLog()
        self.top.do.writeLog(collectedLog)
        self.assertEquals(['report'], self.observer.calledMethodNames())
        self.maxDiff = None
        self.assertEquals(({
            'gustosGroup': {
                'Upload count': {
                    'Uploads': { COUNT: 1 },
                    'Add': { COUNT: 1 },
                    'Delete': { COUNT: 0},
                },
                'Upload duration': {
                    'duration': { TIME: 0.3 }
                },
                'Upload size': {
                    'size': { MEMORY: 3120 },
                },
            }
        },), self.observer.calledMethods[-1].args)


    def testDoNotLogIfNotEnabled(self):
        collectedLog = exampleUpdateLog()
        collectedLog['sruRecordUpdate'] = collectedLog['update-scope']['sruRecordUpdate']
        del collectedLog['update-scope']
        self.top.do.writeLog(collectedLog)
        self.assertEquals([], self.observer.calledMethodNames())


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
