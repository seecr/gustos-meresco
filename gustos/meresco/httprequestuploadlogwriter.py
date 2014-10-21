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

from meresco.core import Observable
from meresco.components.log.utils import getFirst, getScoped, scopePresent
from gustos.common.units import MEMORY, TIME
from gustos.meresco.utils import IntervalCheck

class HttpRequestUploadLogWriter(Observable):
    def __init__(self, gustosGroup, scopeNames, interval=None, **kwargs):
        Observable.__init__(self, **kwargs)
        if type(scopeNames) is not tuple:
            raise ValueError('Expected tuple')
        self._gustosGroup = gustosGroup
        self._scopeNames = scopeNames
        self.setInterval(interval)

    def setInterval(self, interval):
        self._interval = IntervalCheck(interval)

    def writeLog(self, collectedLog):
        if not scopePresent(collectedLog, self._scopeNames):
            return
        gustosReport = {}

        now, shouldReport = self._interval.check()
        if not shouldReport:
            return

        httpRequest = getScoped(collectedLog, scopeNames=self._scopeNames, key='httpRequest')
        bodySize = getFirst(httpRequest, 'bodySize')
        if bodySize:
            gustosReport['Upload size'] = {'size': {MEMORY: bodySize}}
        httpResponse = getScoped(collectedLog, scopeNames=self._scopeNames, key='httpResponse')
        duration = getFirst(httpResponse, 'duration')
        if duration:
            gustosReport['Upload duration'] = {'duration': {TIME: duration}}
        if gustosReport:
            self.do.report(values={self._gustosGroup: gustosReport})
        self._interval.done(now)