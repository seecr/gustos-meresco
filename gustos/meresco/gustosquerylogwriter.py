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
from gustos.common.units import TIME, COUNT, MEMORY
from meresco.components.log.utils import getFirst, getScoped, scopePresent
from gustos.meresco.utils import IntervalCheck
from urllib import urlencode

class GustosQueryLogWriter(Observable):
    def __init__(self, gustosGroup, scopeNames, interval=None, **kwargs):
        Observable.__init__(self, **kwargs)
        if type(scopeNames) is not tuple:
            raise ValueError('Expected tuple')
        self._gustosGroup = gustosGroup
        self._scopeNames = scopeNames
        self._interval = IntervalCheck(interval)

    def writeLog(self, collectedLog):
        if not scopePresent(collectedLog, self._scopeNames):
            return
        gustosReport = {}

        now, shouldReport = self._interval.check()
        if not shouldReport:
            return

        sru = getScoped(collectedLog, scopeNames=self._scopeNames, key='sru')
        sruArguments = getFirst(sru, 'arguments', {})
        queryLength = len(urlencode(sruArguments))
        if queryLength:
            gustosReport['Query length'] = {'query length': {COUNT: queryLength}}

        responseTimeData = {}
        for key, gustosKey in RESPONSE_TIMEKEYS:
            value = getFirst(sru, key, None)
            if value is not None:
                responseTimeData[gustosKey] = {TIME: float(value)}
        if responseTimeData:
            gustosReport['ResponseTime'] = responseTimeData

        clauses = getScoped(collectedLog, scopeNames=self._scopeNames, key='cqlClauses', default=[None])[0]
        if not clauses is None:
            gustosReport['Query clauses'] = {'boolean clauses': {COUNT: clauses}}

        responseSize = getFirst(getScoped(collectedLog, scopeNames=self._scopeNames, key='httpResponse'), 'size', 0)
        if responseSize:
            gustosReport['Query result size'] = {'size': {MEMORY: responseSize}}

        if gustosReport:
            self.do.report(values={self._gustosGroup: gustosReport})
            self._interval.done(now)


RESPONSE_TIMEKEYS = [
    ('handlingTime', 'sru'),
    ('indexTime', 'index'),
    ('queryTime', 'queryTime'),
]
