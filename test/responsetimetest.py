# -*- encoding: utf-8 -*-
## begin license ##
#
# "Gustos-Meresco" is a set of Gustos components for Meresco based projects.
#
# Copyright (C) 2014-2015 Seecr (Seek You Too B.V.) http://seecr.nl
# Copyright (C) 2014 Stichting Bibliotheek.nl (BNL) http://www.bibliotheek.nl
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

from seecr.test import SeecrTestCase, CallTrace

from gustos.meresco import ResponseTime

from decimal import Decimal
from time import sleep
from gustos.common.units import TIME, COUNT
from weightless.core import be
from meresco.core import Observable

class ResponseTimeTest(SeecrTestCase):
    def setUp(self):
        SeecrTestCase.setUp(self)
        self.observer = CallTrace('gustos for time')
        self.top = be((Observable(),
            (ResponseTime(type="TYPE"),
                (self.observer,)
            ),
        ))

    def testReportResponseTime(self):
        self.top.do.handleQueryTimes(index=Decimal("1.000"), sru=Decimal("1.500"), queryTime=Decimal("2.000"))
        self.assertEquals(['report'], self.observer.calledMethodNames())

        self.assertEquals({
            'TYPE': {
                'ResponseTime': {
                    'index': {TIME: 1.0},
                    'queryTime': {TIME: 2.0},
                    'sru': {TIME: 1.5}
                },
            }
        }, self.observer.calledMethods[0].kwargs['values'])


    def testReportAfterInterval(self):
        msg = lambda nr: dict(index=Decimal("%s.000" % nr), sru=Decimal("1.500"), queryTime=Decimal("2.000"))
        self.top.do.handleQueryTimes(**msg(1))
        self.assertAlmostEqual(1.0, self.indexTimeFromLastMethod())
        self.assertEquals(['report'] * 1, self.observer.calledMethodNames())
        self.top.do.handleQueryTimes(**msg(2))
        self.top.do.handleQueryTimes(**msg(3))
        self.top.do.handleQueryTimes(**msg(4))
        self.top.do.handleQueryTimes(**msg(5))
        self.assertEquals(['report'] * 5, self.observer.calledMethodNames())
        sleep(0.1)
        self.top.do.handleQueryTimes(**msg(6))
        self.assertEquals(['report'] * 6, self.observer.calledMethodNames())
        self.assertAlmostEqual(6.0, self.indexTimeFromLastMethod())
        self.top.do.handleQueryTimes(**msg(7))
        self.top.do.handleQueryTimes(**msg(8))
        self.top.do.handleQueryTimes(**msg(9))
        self.top.do.handleQueryTimes(**msg(10))
        self.assertEquals(['report'] * 10, self.observer.calledMethodNames())
        sleep(0.1)
        self.top.do.handleQueryTimes(**msg(11))
        self.assertEquals(['report'] * 11, self.observer.calledMethodNames())
        self.assertAlmostEqual(11.0, self.indexTimeFromLastMethod())

    def testIntervalledReportAfterInterval(self):
        self.top = be((Observable(),
            (ResponseTime(type="TYPE", interval=0.1),
                (self.observer,)
            ),
        ))
        msg = lambda nr: dict(index=Decimal("%s.000" % nr), sru=Decimal("1.500"), queryTime=Decimal("2.000"))
        self.top.do.handleQueryTimes(**msg(1))
        self.assertAlmostEqual(1.0, self.indexTimeFromLastMethod())
        self.assertEquals(['report'] * 1, self.observer.calledMethodNames())
        self.top.do.handleQueryTimes(**msg(2))
        self.top.do.handleQueryTimes(**msg(3))
        self.top.do.handleQueryTimes(**msg(4))
        self.top.do.handleQueryTimes(**msg(5))
        self.assertEquals(['report'] * 1, self.observer.calledMethodNames())
        sleep(0.1)
        self.top.do.handleQueryTimes(**msg(6))
        self.assertEquals(['report'] * 2, self.observer.calledMethodNames())
        self.assertAlmostEqual(6.0, self.indexTimeFromLastMethod())
        self.top.do.handleQueryTimes(**msg(7))
        self.top.do.handleQueryTimes(**msg(8))
        self.top.do.handleQueryTimes(**msg(9))
        self.top.do.handleQueryTimes(**msg(10))
        self.assertEquals(['report'] * 2, self.observer.calledMethodNames())
        sleep(0.1)
        self.top.do.handleQueryTimes(**msg(11))
        self.assertEquals(['report'] * 3, self.observer.calledMethodNames())
        self.assertAlmostEqual(11.0, self.indexTimeFromLastMethod())

    def indexTimeFromLastMethod(self):
        return self.observer.calledMethods[-1].kwargs['values']['TYPE']['ResponseTime']['index'][TIME]
