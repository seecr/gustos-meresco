# -*- encoding: utf-8 -*-
## begin license ##
#
# "Gustos-Meresco" is a set of Gustos components for Meresco based projects.
#
# Copyright (C) 2014-2015, 2021, 2026 Seecr (Seek You Too B.V.) https://seecr.nl
# Copyright (C) 2014 Stichting Bibliotheek.nl (BNL) http://www.bibliotheek.nl
# Copyright (C) 2015, 2021 Stichting Kennisnet https://www.kennisnet.nl
# Copyright (C) 2021 Data Archiving and Network Services https://dans.knaw.nl
# Copyright (C) 2021 SURF https://www.surf.nl
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

from seecr.test import SeecrTestCase, CallTrace

from gustos_meresco import QueryCount

from decimal import Decimal
from time import sleep
from gustos_common.units import COUNT
from weightless.core import be
from meresco.core import Observable

class QueryCountTest(SeecrTestCase):
    def setUp(self):
        SeecrTestCase.setUp(self)
        self.observer = CallTrace('gustos for count')
        self.top = be((Observable(),
            (QueryCount(type="TYPE", interval=0.1),
                (self.observer,)
            )
        ))

    def testReportQueryCount(self):
        self.top.do.handleQueryTimes(index=Decimal("1.000"), sru=Decimal("1.500"), queryTime=Decimal("2.000"))
        self.assertEqual(['report'], self.observer.calledMethodNames())

        self.assertEqual({
            'TYPE': {
                'QueryCount': {
                    'Queries': {COUNT: 1}
                }
            }
        }, self.observer.calledMethods[0].kwargs['values'])

    def testReportAfterInterval(self):
        def countFromLastMethod():
            return self.observer.calledMethods[-1].kwargs['values']['TYPE']['QueryCount']['Queries'][COUNT]
        msg = lambda nr: dict(index=Decimal("%s.000" % nr), sru=Decimal("1.500"), queryTime=Decimal("2.000"))
        self.top.do.handleQueryTimes(**msg(1))
        self.assertEqual(1, countFromLastMethod())
        self.assertEqual(['report'] * 1, self.observer.calledMethodNames())
        self.top.do.handleQueryTimes(**msg(2))
        self.top.do.handleQueryTimes(**msg(3))
        self.top.do.handleQueryTimes(**msg(4))
        self.top.do.handleQueryTimes(**msg(5))
        self.assertEqual(['report'] * 1, self.observer.calledMethodNames())
        sleep(0.1)
        self.top.do.handleQueryTimes(**msg(6))
        self.assertEqual(['report'] * 2, self.observer.calledMethodNames())
        self.assertEqual(6, countFromLastMethod())
        self.top.do.handleQueryTimes(**msg(7))
        self.top.do.handleQueryTimes(**msg(8))
        self.top.do.handleQueryTimes(**msg(9))
        self.top.do.handleQueryTimes(**msg(10))
        self.assertEqual(['report'] * 2, self.observer.calledMethodNames())
        sleep(0.1)
        self.top.do.handleQueryTimes(**msg(11))
        self.assertEqual(['report'] * 3, self.observer.calledMethodNames())
        self.assertEqual(11, countFromLastMethod())

