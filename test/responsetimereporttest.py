## begin license ##
#
# "Gustos-Meresco" is a set of Gustos components for Meresco based projects.
#
# Copyright (C) 2014-2015 Seecr (Seek You Too B.V.) http://seecr.nl
# Copyright (C) 2014 Stichting Bibliotheek.nl (BNL) http://www.bibliotheek.nl
# Copyright (C) 2015 Stichting Kennisnet http://www.kennisnet.nl
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
from gustos.meresco import GustosLogWriter, ResponseTimeReport
from decimal import Decimal

class ResponseTimeReportTest(SeecrTestCase):
    def testCountOne(self):
        self.report = CallTrace(returnValues={'report': {"packet":"data"}}, onlySpecifiedMethods=True)
        self.top = be((Observable(),
            (LogCollector(),
                (GustosLogWriter(),
                    (ResponseTimeReport(gustosGroup='gustosGroup', scopeNames=(), curveName='http'),),
                    (ResponseTimeReport(gustosGroup='gustosGroup', scopeNames=(), curveName='other', keys=('otherResponse', 'duration')),),
                    (self.report,),
                ),
                (CollectMeALog(),)
            )
        ))
        self.top.do.callMe(times=3)
        self.assertEquals(['report'], self.report.calledMethodNames())
        theReport = self.report.calledMethods[0].kwargs['values']['gustosGroup']['ResponseTime']
        self.assertEquals({'other': {'time': 0.3}, 'http': {'time': 0.0}}, theReport)

class CollectMeALog(object):
    def callMe(self, times=1):
        for i in range(times):
            collectLogForScope(httpResponse={'duration':Decimal(0.4 * i)})
        collectLogForScope(otherResponse={'duration':Decimal(0.3)})
