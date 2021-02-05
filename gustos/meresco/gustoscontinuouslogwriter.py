## begin license ##
#
# "Gustos-Meresco" is a set of Gustos components for Meresco based projects.
#
# Copyright (C) 2014 Maastricht University Library http://www.maastrichtuniversity.nl/web/Library/home.htm
# Copyright (C) 2014, 2021 SURF https://www.surf.nl
# Copyright (C) 2014, 2021 Seecr (Seek You Too B.V.) https://seecr.nl
# Copyright (C) 2021 Data Archiving and Network Services https://dans.knaw.nl
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

from meresco.core import Observable
from gustos.meresco.utils import IntervalCheck

class GustosContinuousLogWriter(Observable):
    def __init__(self, reactor, interval=1.0, **kwargs):
        super(GustosContinuousLogWriter, self).__init__(**kwargs)
        self._reactor = reactor
        self._interval = interval
        self._values = {}
        self._reactor.addTimer(self._interval, self.report)

    def writeLog(self, collectedLog):
        self.do.analyseLog(collectedLog=collectedLog)
        self.do.fillReport(groups=self._values, collectedLog=collectedLog)

    def report(self):
        if len(self._values) > 0:
            self.do.report(values=self._values)
        self._reactor.addTimer(self._interval, self.report)
