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
from gustos.common.units import COUNT
from gustos.meresco.utils import IntervalCheck

class SruRecordUpdateCountLogWriter(Observable):
    def __init__(self, gustosGroup, scopeNames, interval=1.0, **kwargs):
        Observable.__init__(self, **kwargs)
        if type(scopeNames) is not tuple:
            raise ValueError('Expected tuple')
        self._gustosGroup = gustosGroup
        self._scopeNames = scopeNames
        self._counts = {
            'sruAdd': 0,
            'sruDelete': 0,
        }
        self.setInterval(interval)

    def setInterval(self, interval):
        self._interval = IntervalCheck(interval)

    def writeLog(self, collectedLog):
        if not scopePresent(collectedLog, self._scopeNames):
            return
        gustosReport = {}

        sruRecordUpdate = getScoped(collectedLog, scopeNames=self._scopeNames, key='sruRecordUpdate')
        addIdentifier = getFirst(sruRecordUpdate, 'add')
        deleteIdentifier = getFirst(sruRecordUpdate, 'delete')
        if addIdentifier is None and deleteIdentifier is None:
            return
        self._counts['sruAdd'] += (0 if addIdentifier is None else 1)
        self._counts['sruDelete'] += (0 if deleteIdentifier is None else 1)
        now, shouldReport = self._interval.check()
        if not shouldReport:
            return
        gustosReport['Upload count'] = {
                'Add': { COUNT: self._counts['sruAdd'] },
                'Delete': { COUNT: self._counts['sruDelete']},
                'Uploads': { COUNT: self._counts['sruAdd'] + self._counts['sruDelete'] },
            }
        self.do.report(values={self._gustosGroup: gustosReport})
        self._interval.done(now)
