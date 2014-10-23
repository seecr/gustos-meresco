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

from seecr.test import SeecrTestCase, CallTrace

from gustos.meresco import GustosTimedLogWriter
from weightless.core import be
from meresco.core import Observable
from time import sleep

class GustosTimedLogWriterTest(SeecrTestCase):
    def setUp(self):
        super(GustosTimedLogWriterTest, self).setUp()
        self.observer = CallTrace()
        self.top = be((Observable(),
            (GustosTimedLogWriter(interval=0.1),
                (self.observer,)
            )
        ))

    def testWriteLog(self):
        collectedLog = {'collected':'log'}
        def fillReport(groups, collectedLog):
            groups['fill me'] = 'up'
        self.observer.methods['fillReport'] = fillReport
        self.top.do.writeLog(collectedLog=collectedLog)
        self.assertEquals(['analyseLog', 'fillReport', 'report'], self.observer.calledMethodNames())

    def testWriteEmptyLog(self):
        collectedLog = {'collected':'log'}
        self.top.do.writeLog(collectedLog=collectedLog)
        self.assertEquals(['analyseLog', 'fillReport'], self.observer.calledMethodNames())

    def testTimedWriting(self):
        collectedLog = {'collected':'log'}
        def fillReport(groups, collectedLog):
            groups['fill me'] = 'up'
        self.observer.methods['fillReport'] = fillReport
        self.top.do.writeLog(collectedLog=collectedLog)
        self.assertEquals(['analyseLog', 'fillReport', 'report'], self.observer.calledMethodNames())
        self.top.do.writeLog(collectedLog=collectedLog)
        self.top.do.writeLog(collectedLog=collectedLog)
        self.assertEquals(['analyseLog', 'fillReport', 'report', 'analyseLog', 'analyseLog'], self.observer.calledMethodNames())
        sleep(0.11)
        self.top.do.writeLog(collectedLog=collectedLog)
        self.assertEquals(['analyseLog', 'fillReport', 'report', 'analyseLog', 'analyseLog', 'analyseLog', 'fillReport', 'report'], self.observer.calledMethodNames())
