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

from meresco.core import Observable
from gustos.common.units import COUNT
from meresco.components.log.utils import getFirst, getScoped, scopePresent
from time import time
from gustos.meresco.utils import IntervalCheck

class GustosQueryCountLogWriter(Observable):
    _time = time
    def __init__(self, gustosGroup, scopeNames, interval=1.0, **kwargs):
        Observable.__init__(self, **kwargs)
        if type(scopeNames) is not tuple:
            raise ValueError('Expected tuple')
        self._gustosGroup = gustosGroup
        self._scopeNames = scopeNames
        self._interval = IntervalCheck(interval)
        self._counts ={
            'queries': 0,
        }

    def writeLog(self, collectedLog):
        if not scopePresent(collectedLog, self._scopeNames):
            return
        gustosReport = {}
        now, shouldReport = self._interval.check()

        self.do.analyseLog(collectedLog=collectedLog, scopeNames=self._scopeNames)

        sru = getScoped(collectedLog, scopeNames=self._scopeNames, key='sru')
        sruArguments = getFirst(sru, 'arguments', {})
        if sruArguments:
            self._counts['queries'] += 1

        if not shouldReport:
            return

        gustosReport['Queries count'] = {
                'Queries': {COUNT: self._counts['queries'] },
            }
        self.do.fillReport(gustosReport=gustosReport)

        if gustosReport:
            self.do.report(values={self._gustosGroup: gustosReport})
            self._interval.done(now)


LOADBALANCER_IPS = set([
    '145.97.39.67',
    '145.97.39.68',
])
