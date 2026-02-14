## begin license ##
#
# "Gustos-Meresco" is a set of Gustos components for Meresco based projects.
#
# Copyright (C) 2014 Maastricht University Library http://www.maastrichtuniversity.nl/web/Library/home.htm
# Copyright (C) 2014, 2021 SURF https://www.surf.nl
# Copyright (C) 2014-2015, 2021, 2026 Seecr (Seek You Too B.V.) https://seecr.nl
# Copyright (C) 2015, 2021 Stichting Kennisnet https://www.kennisnet.nl
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

from meresco.core import Observable
from gustos_meresco.utils import IntervalCheck

class _TimedLogWriter(Observable):
    """The TimedLogWriter will send a gustos after the interval has passed.

    writeLog(...) is called by the meresco.components.log.LogCollector.
    At every call TimedLogWriter will inform its observers by calling analyseLog().
    This can be used for gustos reporters who are counting all calls.
    If the interval has passed it will call fillReport(...) to the observers to add
    their part to the report.

    (LogCollector(),
        (TimedLogWriter(),
            (SomeCountingLogger(),),
            (SomeOtherReportLogger(),),
            (gustosClient,),
        ),
        ... # the actual tree that does the work
    )
    """
    def __init__(self, interval=1.0, **kwargs):
        super(_TimedLogWriter, self).__init__(**kwargs)
        self._interval = IntervalCheck(None)
        if interval is not None:
            self.setInterval(interval)

    def writeLog(self, collectedLog):
        groups = {}
        now, shouldReport = self._interval.check()

        self.do.analyseLog(collectedLog=collectedLog)

        if not shouldReport:
            return

        self.do.fillReport(groups=groups, collectedLog=collectedLog)

        if groups:
            self.call.report(values=groups) # call, because it returns packet data
            self._interval.done(now)

class GustosLogWriter(_TimedLogWriter):
    def __init__(self, **kwargs):
        if 'interval' in kwargs:
            raise TypeError("interval cannot be set for GustosLogWriter")
        super(GustosLogWriter, self).__init__(interval=None, **kwargs)

class GustosTimedLogWriter(_TimedLogWriter):
    def __init__(self, interval, **kwargs):
        if interval <= 0.0:
            raise TypeError("Interval should be > 0.0, or use the GustosLogWriter.")
        super(GustosTimedLogWriter, self).__init__(interval=interval, **kwargs)

    def setInterval(self, interval):
        if interval <= 0.0:
            raise ValueError('Expected interval to be > 0.0')
        self._interval = IntervalCheck(interval)

