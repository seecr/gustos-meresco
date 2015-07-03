## begin license ##
#
# "Gustos-Meresco" is a set of Gustos components for Meresco based projects.
#
# Copyright (C) 2014-2015 Seecr (Seek You Too B.V.) http://seecr.nl
# Copyright (C) 2014-2015 Stichting Bibliotheek.nl (BNL) http://www.bibliotheek.nl
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
from weightless.core import be, consume
from meresco.core import Observable
from meresco.xml.utils import createElement, createSubElement
from gustos.meresco.gustosoairecordcount import GustosOaiRecordCount
from gustos.common.units import COUNT
from time import sleep

class GustosOaiRecordCountTest(SeecrTestCase):

    def testAll(self):
        client = CallTrace('gustosclient', returnValues=dict(report={'packet':'data'}))
        handler = CallTrace('handler', emptyGeneratorMethods=['handle'])
        top = be((Observable(),
            (GustosOaiRecordCount(type='Summary', interval=0.1),
                (client,)
            ),
            (handler,)
        ))

        consume(top.all.handle(lxmlNode=oaiResult(adds=1, deletes=1)))
        self.assertEquals(['report'], client.calledMethodNames())
        consume(top.all.handle(lxmlNode=oaiResult(adds=2, deletes=2)))
        sleep(0.11)
        consume(top.all.handle(lxmlNode=oaiResult(adds=4, deletes=4)))
        consume(top.all.handle(lxmlNode=oaiResult(adds=8, deletes=8)))

        self.assertEquals(['handle', 'handle', 'handle', 'handle'], handler.calledMethodNames())
        self.assertEquals(['report', 'report'], client.calledMethodNames())
        self.assertEquals({
            'Summary': {
                'Updated records': {
                    'adds': {
                        COUNT: 1
                    },
                    'deletes': {
                        COUNT: 1
                    }
                }
            }
        }, client.calledMethods[0].kwargs['values'])
        self.assertEquals({
            'Summary': {
                'Updated records': {
                    'adds': {
                        COUNT: 7
                    },
                    'deletes': {
                        COUNT: 7
                    }
                }
            }
        }, client.calledMethods[1].kwargs['values'])

def oaiResult(adds, deletes):
    oaipmhNode = createElement('oai:OAI-PMH')
    listRecords = createSubElement(oaipmhNode, 'oai:ListRecords')
    for i in xrange(adds + deletes):
        record = createSubElement(listRecords, 'oai:record')
        attrib = {'status': 'deleted'} if i >= adds else {}
        createSubElement(record, 'oai:header', attrib=attrib)
    return oaipmhNode
