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
from time import time

class IntervalCheck(object):
    def __init__(self, interval):
        self._interval = interval
        self._timeLastReportSent = 0
        self.check = self._check
        self.done = self._done
        if self._interval is None:
            self.check = lambda: (0, True)
            self.done = lambda now: None

    def _check(self):
        now = time()
        return now, now - self._timeLastReportSent > self._interval

    def _done(self, aTime):
        self._timeLastReportSent = aTime