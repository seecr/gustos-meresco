## begin license ##
#
# "Gustos-Meresco" is a set of Gustos components for Meresco based projects.
#
# Copyright (C) 2014 Maastricht University Library http://www.maastrichtuniversity.nl/web/Library/home.htm
# Copyright (C) 2014 SURF http://www.surf.nl
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
from gustos.meresco.utils import IntervalCheck

class TimedLogWriter(Observable):
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
        super(TimedLogWriter, self).__init__(**kwargs)
        self.setInterval(interval)

    def setInterval(self, interval):
        self._interval = IntervalCheck(interval)

    def writeLog(self, collectedLog):
        groups = {}
        now, shouldReport = self._interval.check()

        self.do.analyseLog(collectedLog=collectedLog)

        if not shouldReport:
            return

        self.do.fillReport(groups=groups, collectedLog=collectedLog)

        if groups:
            self.do.report(values=groups)
            self._interval.done(now)
