## begin license ##
#
# "Gustos-Meresco" is a set of Gustos components for Meresco based projects.
#
# Copyright (C) 2014 Seecr (Seek You Too B.V.) http://seecr.nl
# Copyright (C) 2014 Stichting Kennisnet http://www.kennisnet.nl
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
from gustos.meresco import GustosQueryCountLogWriter, GustosQueryLogWriter
from decimal import Decimal
from gustos.common.units import TIME, COUNT, MEMORY
from time import sleep

class GustosQueryLogWriterTest(SeecrTestCase):
    def setUp(self):
        SeecrTestCase.setUp(self)
        self.timeObserver = CallTrace('gustosclient time')
        self.countObserver = CallTrace('gustosclient count')
        self.top = be((Observable(),
            (GustosQueryLogWriter(gustosGroup='gustosGroup', scopeNames=('query-scope', 'sub-scope'), interval=None),
                (self.timeObserver,)
            ),
            (GustosQueryCountLogWriter(gustosGroup='gustosGroup', scopeNames=('query-scope', 'sub-scope'), interval=0.1),
                (self.countObserver,)
            )
        ))

    def testIndexSruQuery(self):
        def fillReport(gustosReport):
            gustosReport['additional'] = 'reported'
        self.countObserver.methods['fillReport'] = fillReport
        logItems = exampleSruLogItems()
        self.top.do.writeLog(collectedLog=logItems)
        self.assertEquals(['report'], self.timeObserver.calledMethodNames())
        self.assertEquals(['analyseLog', 'fillReport', 'report'], self.countObserver.calledMethodNames())
        self.maxDiff = None
        self.assertEquals({
            'gustosGroup': {
                'ResponseTime': {
                    'index': { TIME: 0.1 },
                    'queryTime': { TIME: 1.0 },
                    'sru': { TIME: 1.3 },
                },
                'Query clauses': {
                    'boolean clauses': {
                        COUNT: 2
                    }
                },
                'Query length': {
                    'query length': {
                        COUNT: 205
                    },
                },
                'Query result size': {
                    'size': {
                        MEMORY: 1889
                    }
                },
            }
        }, self.timeObserver.calledMethods[0].kwargs['values'])
        analyseLogMethod, fillReportMethod, reportMethod = self.countObserver.calledMethods
        self.assertEquals({
            'gustosGroup': {
                'Queries count': {
                    'Queries': {
                        COUNT: 1
                    },
                },
                'additional': 'reported'
            },
        }, reportMethod.kwargs['values'])
        self.assertEquals(reportMethod.kwargs['values']['gustosGroup'], fillReportMethod.kwargs['gustosReport'])
        self.assertEquals(set(['collectedLog', 'scopeNames']), set(analyseLogMethod.kwargs.keys()))
        self.assertEquals(('query-scope', 'sub-scope'), analyseLogMethod.kwargs['scopeNames'])

    def testEmptyQuery(self):
        collectedLog = exampleSruEmptyLogItems()
        self.top.do.writeLog(collectedLog)
        self.assertEquals(['analyseLog', 'fillReport', 'report'], self.countObserver.calledMethodNames())
        gustosReport = self.countObserver.calledMethods[-1].kwargs['values']
        self.assertEquals({
                    'Queries': {
                        COUNT: 0
                    },
                }, gustosReport['gustosGroup']['Queries count'])

    def testDoNotLogIfScopeNotPresent(self):
        collectedLog = exampleSruEmptyLogItems()
        del collectedLog['query-scope']['sub-scope']
        self.top.do.writeLog(collectedLog)
        self.assertEquals([], self.timeObserver.calledMethodNames())
        self.assertEquals([], self.countObserver.calledMethodNames())

    def testReportAfterInterval(self):
        def lastQueriesCount():
            return self.countObserver.calledMethods[-1].kwargs['values']['gustosGroup']['Queries count']['Queries'][COUNT]
        def lastIndexTime():
            return self.timeObserver.calledMethods[-1].kwargs['values']['gustosGroup']['ResponseTime']['index'][TIME]
        def logItems(indexTime):
            result = exampleSruLogItems()
            result['query-scope']['sub-scope']['sru']['indexTime'] = [Decimal(indexTime)]
            return result
        self.top.do.writeLog(collectedLog=logItems(indexTime='0.010'))
        self.assertEquals(['report'], self.timeObserver.calledMethodNames())
        self.assertEquals(['analyseLog', 'fillReport', 'report'], self.countObserver.calledMethodNames())
        self.assertAlmostEqual(0.010, lastIndexTime())
        self.assertEquals(1, lastQueriesCount())
        self.top.do.writeLog(collectedLog=logItems(indexTime='0.020'))
        self.assertEquals(['analyseLog', 'fillReport', 'report', 'analyseLog'], self.countObserver.calledMethodNames())
        self.assertEquals(['report', 'report'], self.timeObserver.calledMethodNames())
        sleep(0.11)
        self.top.do.writeLog(collectedLog=logItems(indexTime='0.040'))
        self.assertEquals(['analyseLog', 'fillReport', 'report', 'analyseLog', 'analyseLog', 'fillReport', 'report'], self.countObserver.calledMethodNames())
        self.assertEquals(['report', 'report', 'report'], self.timeObserver.calledMethodNames())
        self.assertAlmostEqual(0.040, lastIndexTime())
        self.assertEquals(3, lastQueriesCount())


def exampleSruLogItems():
    return {
        'httpRequest': {
            'timestamp': [1396596372.708574],
            'Headers': [{}],
            'Client': [('127.0.0.1', 57075)],
            'arguments': [{
                'query': ['meta.upload.id exact "NICL:oai:mdms.kenict.org:oai:nicl.nl:k163645"'],
                'operation': ['searchRetrieve'],
                'version': ['1.2'],
                'recordPacking': ['xml'],
                'recordSchema': ['smbAggregatedData']
            }],
            'RequestURI': ['/edurep/sruns?query=meta.upload.id+exact+%22NICL%3Aoai%3Amdms.kenict.org%3Aoai%3Anicl.nl%3Ak163645%22&operation=searchRetrieve&version=1.2&recordPacking=xml&recordSchema=smbAggregatedData'],
            'query': ['query=meta.upload.id+exact+%22NICL%3Aoai%3Amdms.kenict.org%3Aoai%3Anicl.nl%3Ak163645%22&operation=searchRetrieve&version=1.2&recordPacking=xml&recordSchema=smbAggregatedData'],
            'path': ['/edurep/sruns'],
            'Method': ['GET'],
            'HTTPVersion': ['1.0']
        },
        'query-scope': {
            'sub-scope': {
                'cqlClauses': [2],
                'sru': {
                    'indexTime': [Decimal('0.100')],
                    'handlingTime': [Decimal('1.300')],
                    'numberOfRecords': [1],
                    'queryTime': [Decimal('1.000')],
                    'arguments': [{
                        'recordSchema': 'smbAggregatedData',
                        'version': '1.2',
                        'recordPacking': 'xml',
                        'maximumRecords': 10,
                        'startRecord': 1,
                        'query': 'meta.upload.id exact "NICL:oai:mdms.kenict.org:oai:nicl.nl:k163645"',
                        'operation': 'searchRetrieve'
                    }]
                }
            }
        },
        'httpResponse': {
            'duration': [0.004216909408569336],
            'httpStatus': ['200'],
            'size': [1889]
        }
    }

def exampleSruEmptyLogItems():
    return {
        'httpRequest': {
            'timestamp': [1396596372.708574],
            'Headers': [{}],
            'Client': [('127.0.0.1', 57075)],
            'arguments': [{}],
            'RequestURI': ['/edurep/sruns'],
            'query': [''],
            'path': ['/edurep/sruns'],
            'Method': ['GET'],
            'HTTPVersion': ['1.0']
        },
        'query-scope': {
            'sub-scope': {
            }
        },
        'httpResponse': {
            'duration': [0.004216909408569336],
            'httpStatus': ['200'],
            'size': [1889]
        }
    }

def exampleSruRecordUpdateAdd():
    return {
        'responseHttpStatus': ['200'],
        'RequestURI': ['/edurep/update'],
        'Headers': [{
            'Content-Length': '5496',
            'Content-Type': 'text/xml; charset="utf-8"'
        }],
        'Client': [('127.0.0.1', 33167)],
        'arguments': [{}],
        'timestamp': [1395843906.2992],
        'duration': [0.012806892395019531],
        'query': [''],
        'path': ['/edurep/update'],
        'sruRecordUpdateAdd': ['EdurepDev:cq2_failed_11112'],
        'Method': ['POST'],
        'responseSize': [306],
        'HTTPVersion': ['1.0']
    }