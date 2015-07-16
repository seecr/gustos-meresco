## begin license ##
#
# "Gustos-Meresco" is a set of Gustos components for Meresco based projects.
#
# Copyright (C) 2014-2015 Seecr (Seek You Too B.V.) http://seecr.nl
# Copyright (C) 2014 Stichting Bibliotheek.nl (BNL) http://www.bibliotheek.nl
# Copyright (C) 2015 Koninklijke Bibliotheek (KB) http://www.kb.nl
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

from gustos.common.units import TIME
from gustos.meresco.utils import IntervalCheck

from meresco.core import Observable

class ResponseTime(Observable):

    def __init__(self, type, interval=None, **kwargs):
        Observable.__init__(self, **kwargs)
        self._type = type
        self._interval = IntervalCheck(interval)

    def handleQueryTimes(self, **kwargs):
        now, shouldReport = self._interval.check()
        if shouldReport:
            responseTimeData = dict((key, {TIME: float(value)}) for key, value in kwargs.items())
            self.do.report(values={"%s" % self._type: {
                    "ResponseTime": responseTimeData,
                }})
            self._interval.done(now)

