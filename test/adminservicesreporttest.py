## begin license ##
#
# "Gustos-Meresco" is a set of Gustos components for Meresco based projects.
#
# Copyright (C) 2013-2015, 2021 Seecr (Seek You Too B.V.) https://seecr.nl
# Copyright (C) 2013-2014 Stichting Bibliotheek.nl (BNL) http://www.bibliotheek.nl
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

from seecr.test import SeecrTestCase, CallTrace
from seecr.test.io import stdout_replaced

from weightless.core import be, consume
from meresco.core import Observable

from gustos.meresco.adminservicesreport import AdminServicesReport


class AdminServicesReportTest(SeecrTestCase):
    def setUp(self):
        SeecrTestCase.setUp(self)

        self.client = CallTrace('Client')
        self.report = AdminServicesReport()
        self.dna = be((Observable(),
            (self.report,
                (self.client,),
            )
        ))

    def testShouldReportToClientOnHandle(self):
        self.client.returnValues['listServices'] = {
            'joe-joe-aiyedee': {
                'ipAddress': "127.0.0.1",
                'fqdn': "name.example.org",
                'number': 42,
                'lastseen': 1234567890.123456,
                'active': True,
                'type': "typeName",
                'port': 4321,
                'data': {'errors': 1, 'warnings': 1}},
            'other': {
                'ipAddress': "127.0.0.2",
                'fqdn': "other.example.org",
                'number': 2,
                'lastseen': 1.1,
                'active': False,  # False active
                'type': "typeName",
                'port': 4321},
        }

        with stdout_replaced() as out:
            consume(self.dna.all.handle())
            self.assertEqual('''\
AdminServicesReport: Error Services:
    type: typeName, identifier: joe-joe-aiyedee
AdminServicesReport: Inactive Services:
    type: typeName, identifier: other
''', out.getvalue())

        self.assertEqual(['listServices', 'report'], self.client.calledMethodNames())
        self.assertEqual({'Admin Information':
            {'Services':
                {'active':
                    {'count': 1},
                 'inactive':
                    {'count': 1}
                 }
            ,'Errors':
                {'errors': {'count': 1},
                'warnings': {'count': 1}
                }
            }
         }, self.client.calledMethods[-1].kwargs['values'])

    @stdout_replaced
    def testShouldRememberState(self):
        self.client.returnValues['listServices'] = {
            'server': {
                'ipAddress': "127.0.0.1",
                'fqdn': "name.example.org",
                'number': 42,
                'lastseen': 1234567890.123456,
                'active': True,
                'type': "typeName",
                'port': 4321,
                'data': {'errors': 1, 'warnings': 1}
            }
        }
        consume(self.dna.all.handle())
        self.assertEqual({'Admin Information':
            {'Services':
                {'active': {'count': 1}, 'inactive': {'count': 0}}
            ,'Errors':
                {'errors': {'count': 1}, 'warnings': {'count': 1}}
            }
         }, self.client.calledMethods[-1].kwargs['values'])

        consume(self.dna.all.handle())
        self.assertEqual({'Admin Information':
            {'Services':
                {'active': {'count': 2}, 'inactive': {'count': 0}}
            ,'Errors':
                {'errors': {'count': 2}, 'warnings': {'count': 2}}
            }
         }, self.client.calledMethods[-1].kwargs['values'])

        self.client.returnValues['listServices'] = {
            'server': {
                'ipAddress': "127.0.0.1",
                'fqdn': "name.example.org",
                'number': 42,
                'lastseen': 1234567890.123456,
                'active': True,
                'type': "typeName",
                'port': 4321,
                'data': {'errors': 0, 'warnings': 0}
            }
        }

        consume(self.dna.all.handle())
        self.assertEqual({'Admin Information':
            {'Services':
                {'active': {'count': 3}, 'inactive': {'count': 0}}
            ,'Errors':
                {'errors': {'count': 2}, 'warnings': {'count': 2}}
            }
         }, self.client.calledMethods[-1].kwargs['values'])
