## begin license ##
#
# "Gustos-Meresco" is a set of Gustos components for Meresco based projects.
#
# Copyright (C) 2014 Seecr (Seek You Too B.V.) http://seecr.nl
# Copyright (C) 2014 Stichting Bibliotheek.nl (BNL) http://www.bibliotheek.nl
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
from meresco.components.log import LogCollector, collectLogForScope
from gustos.meresco import GustosLogWriter, CountReport

class CountReportTest(SeecrTestCase):
    def testCountOne(self):
        self.report = CallTrace(returnValues={'report': None}, onlySpecifiedMethods=True)
        self.top = be((Observable(),
            (LogCollector(),
                (GustosLogWriter(),
                    (CountReport(gustosGroup='gustosGroup', scopeNames=(), curveName='calls'),),
                    (CountReport(gustosGroup='gustosGroup', scopeNames=(), curveName='collectTimes', keys=('collectResponse', 'some')),),
                    (self.report,),
                ),
                (CollectMeALog(),)
            )
        ))
        self.top.do.callMe(times=3)
        self.assertEquals(['report'], self.report.calledMethodNames())
        countReport = self.report.calledMethods[0].kwargs['values']['gustosGroup']['Counts']
        self.assertEquals({'collectTimes': {'count': 3}, 'calls': {'count': 1}}, countReport)

class CollectMeALog(object):
    def callMe(self, times=1):
        for i in range(times):
            collectLogForScope(collectResponse={'some':'value'})