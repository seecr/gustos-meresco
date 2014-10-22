## begin license ##
#
# "Gustos-Meresco" is a set of Gustos components for Meresco based projects.
#
# Copyright (C) 2014 Maastricht University Library http://www.maastrichtuniversity.nl/web/Library/home.htm
# Copyright (C) 2014 SURF http://www.surf.nl
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

from seecr.test import SeecrTestCase
from gustos.meresco import SruRecordUpdateCountReport
from gustos.common.units import COUNT

class SruRecordUpdateReportTest(SeecrTestCase):
    maxDiff = None
    def setUp(self):
        SeecrTestCase.setUp(self)
        self.report = SruRecordUpdateCountReport(gustosGroup='gustosGroup', scopeNames=('update-scope',))

    def testUpdate(self):
        collectedLog = exampleUpdateLog()
        self.report.analyseLog(collectedLog=collectedLog)
        groups = {}
        self.report.fillReport(groups=groups, collectedLog=collectedLog)

        self.assertEquals({
            'gustosGroup': {
                'Upload count': {
                    'Uploads': { COUNT: 1 },
                    'Add': { COUNT: 1 },
                    'Delete': { COUNT: 0},
                    'Invalid': { COUNT: 0},
                },
            }
        }, groups)

    def testDoNotLogIfNotEnabled(self):
        collectedLog = exampleUpdateLog()
        collectedLog['sruRecordUpdate'] = collectedLog['update-scope']['sruRecordUpdate']
        del collectedLog['update-scope']
        self.report.analyseLog(collectedLog=collectedLog)
        groups = {}
        self.report.fillReport(groups=groups, collectedLog=collectedLog)
        self.assertEquals({}, groups)

    def testReportInterval(self):
        collectedLog = exampleUpdateLog()
        self.report.analyseLog(collectedLog=collectedLog)
        groups = {}
        self.report.fillReport(groups=groups, collectedLog=collectedLog)
        self.assertEquals(1, groups['gustosGroup']['Upload count']['Uploads'][COUNT])
        self.report.analyseLog(collectedLog=collectedLog)
        self.report.analyseLog(collectedLog=collectedLog)
        groups = {}
        self.report.fillReport(groups=groups, collectedLog=collectedLog)
        self.assertEquals(3, groups['gustosGroup']['Upload count']['Uploads'][COUNT])

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
