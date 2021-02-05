## begin license ##
#
# "Gustos-Meresco" is a set of Gustos components for Meresco based projects.
#
# Copyright (C) 2014 Maastricht University Library http://www.maastrichtuniversity.nl/web/Library/home.htm
# Copyright (C) 2014, 2021 SURF https://www.surf.nl
# Copyright (C) 2014, 2021 Seecr (Seek You Too B.V.) https://seecr.nl
# Copyright (C) 2014, 2021 Stichting Kennisnet https://www.kennisnet.nl
# Copyright (C) 2021 Data Archiving and Network Services https://dans.knaw.nl
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

from weightless.core import be, compose
from meresco.core import Observable
from meresco.components.log import LogCollector, collectLog

from seecr.test import SeecrTestCase, CallTrace
from meresco.testsupport.stoppablereactor import StoppableReactor

from gustos.meresco import GustosContinuousLogWriter

class GustosContinuousLogWriterIntegrationTest(SeecrTestCase):
    maxDiff = None

    def testOne(self):
        def fillReport(groups, collectedLog):
            if not 'count' in groups:
                groups['count'] = 0
            groups['count'] += collectedLog['count'][0]
        reports = []
        def report(values):
            reports.append(values.copy())

        observer = CallTrace(methods={'fillReport': fillReport, 'report': report})
        reactor = StoppableReactor()

        class SomethingCounter(object):
            def something(this):
                collectLog(dict(count=1))

        def reactorShutdown():
            reactor.stop()

        reactor.addTimer(2.5, reactorShutdown)

        dna = be(
            (Observable(),
                (LogCollector(),
                    (GustosContinuousLogWriter(reactor=reactor, interval=1.0),
                        (observer, )
                    ),
                    (SomethingCounter(), )
                )
            )
        )

        def job():
            dna.do.something()
            reactor.addTimer(0.5, job)
        job()
        reactor.loop()
        self.assertEqual([
            'analyseLog', 'fillReport', 'analyseLog', 'fillReport', 'report',
            'analyseLog', 'fillReport', 'analyseLog', 'fillReport', 'report',
            'analyseLog', 'fillReport'], [m.name for m in observer.calledMethods])
        self.assertEqual([{'count': 2}, {'count': 4}], reports)

