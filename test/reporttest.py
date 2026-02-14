## begin license ##
#
# "Gustos-Meresco" is a set of Gustos components for Meresco based projects.
#
# Copyright (C) 2014, 2021, 2026 Seecr (Seek You Too B.V.) https://seecr.nl
# Copyright (C) 2014 Stichting Bibliotheek.nl (BNL) http://www.bibliotheek.nl
# Copyright (C) 2021 Data Archiving and Network Services https://dans.knaw.nl
# Copyright (C) 2021 SURF https://www.surf.nl
# Copyright (C) 2021 Stichting Kennisnet https://www.kennisnet.nl
# Copyright (C) 2021 The Netherlands Institute for Sound and Vision https://beeldengeluid.nl
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

from gustos_meresco import ResponseTimeReport
from seecr.test import SeecrTestCase
from gustos_meresco.report import Report

class ReportTest(SeecrTestCase):

    def testResponseTimeReport(self):
        self.report = ResponseTimeReport(
                gustosGroup='gustosGroup',
                scopeNames=('scope',),
            )
        collectedLog = {
                'httpResponse': {
                    'duration': [0.3],
                },
                'scope': {
                    'something': ['value']
                }
            }
        groups = {}
        self.report.fillReport(groups=groups, collectedLog=collectedLog)
        self.assertEqual({
                'gustosGroup': {
                    'ResponseTime': {
                        'total': {
                            'time': 0.3
                        }
                    }
                }
            }, groups)

    def testResponseTimeReportOtherKeys(self):
        self.report = ResponseTimeReport(
                gustosGroup='gustosGroup',
                subgroupName='Triplestore',
                curveName='index',
                scopeNames=('scope',),
                keys=('triplestoreResponse', 'indexTime')
            )
        collectedLog = {
                'triplestoreResponse': {
                    'indexTime': [0.3],
                },
                'scope': {
                    'something': ['value']
                }
            }
        groups = {}
        self.report.fillReport(groups=groups, collectedLog=collectedLog)
        self.assertEqual({
                'gustosGroup': {
                    'Triplestore': {
                        'index': {
                            'time': 0.3
                        }
                    }
                }
            }, groups)

    def testMultipleResponseTimeReports(self):
        indexReport = ResponseTimeReport(
                gustosGroup='gustosGroup',
                subgroupName='Triplestore',
                curveName='index',
                scopeNames=('scope',),
                keys=('triplestoreResponse', 'indexTime')
            )
        queryReport = ResponseTimeReport(
                gustosGroup='gustosGroup',
                subgroupName='Triplestore',
                curveName='queryTime',
                scopeNames=('scope',),
                keys=('triplestoreResponse', 'queryTime')
            )
        collectedLog = {
                'triplestoreResponse': {
                    'indexTime': [0.3],
                    'queryTime': [0.8],
                },
                'scope': {
                    'something': ['value']
                }
            }
        groups = {}
        indexReport.fillReport(groups=groups, collectedLog=collectedLog)
        queryReport.fillReport(groups=groups, collectedLog=collectedLog)
        self.assertEqual({
                'gustosGroup': {
                    'Triplestore': {
                        'index': {
                            'time': 0.3
                        },
                        'queryTime': {
                            'time': 0.8
                        }
                    }
                }
            }, groups)

    def testSubclassAutomaticallyChecksScope(self):
        analyseLogCalls = []
        fillReportLogCalls = []
        class MyReport(Report):
            def analyseLog(inner, collectedLog):
                analyseLogCalls.append(collectedLog)
            def fillReport(inner, groups, collectedLog):
                fillReportLogCalls.append((groups, collectedLog))

        report = MyReport(gustosGroup='gustosGroup', scopeNames=('scope',))

        collectedLogWithScope = {'response':{'size': [3]}, 'scope': {}}
        collectedLogNoScope = {'response':{'size': [3]}}

        report.analyseLog(collectedLog=collectedLogWithScope)
        report.analyseLog(collectedLog=collectedLogNoScope)
        self.assertEqual([collectedLogWithScope], analyseLogCalls)
        groups = {}
        report.fillReport(groups=groups, collectedLog=collectedLogWithScope)
        report.fillReport(groups=groups, collectedLog=collectedLogNoScope)
        self.assertEqual([(groups, collectedLogWithScope)], fillReportLogCalls)


