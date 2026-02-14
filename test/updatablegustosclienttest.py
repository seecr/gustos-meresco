## begin license ##
#
# "Gustos-Meresco" is a set of Gustos components for Meresco based projects.
#
# Copyright (C) 2014-2015, 2021, 2026 Seecr (Seek You Too B.V.) https://seecr.nl
# Copyright (C) 2014 Stichting Bibliotheek.nl (BNL) http://www.bibliotheek.nl
# Copyright (C) 2015 Koninklijke Bibliotheek (KB) http://www.kb.nl
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

from seecr.test import SeecrTestCase
from gustos_meresco import UpdatableGustosClient
from seecr.test.portnumbergenerator import PortNumberGenerator
from seecr.test.udplistenandlog import UdpListenAndLog
from gustos_common.units import COUNT
from weightless.core import consume
from time import sleep
from simplejson import loads

class UpdatableGustosClientTest(SeecrTestCase):
    def setUp(self):
        SeecrTestCase.setUp(self)
        self.client = UpdatableGustosClient(identifier='identifier')
        self.port = PortNumberGenerator.next()
        self.listen = UdpListenAndLog(self.port)

    def tearDown(self):
        self.listen.stop()
        SeecrTestCase.tearDown(self)

    def testNothing(self):
        self.client.report(values=DATA)
        self.assertEqual([], self.listen.log())

    def testUpdateOnce(self):
        consume(self.client.updateConfig(config={'gustos':{'host':'localhost', 'port':self.port}}, services='ignored'))
        self.client.report(values=DATA)
        sleep(0.1)
        log = self.listen.log()
        self.assertEqual(1, len(log))
        self.assertEqual(DATA, loads(log[0])['data'])

DATA = {
    'Group': {
        'subgroup': {
            'series': {
                COUNT: 8
            }
        }
    }
}