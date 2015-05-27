## begin license ##
#
# "Gustos-Meresco" is a set of Gustos components for Meresco based projects.
#
# Copyright (C) 2014-2015 Seecr (Seek You Too B.V.) http://seecr.nl
# Copyright (C) 2014-2015 Stichting Bibliotheek.nl (BNL) http://www.bibliotheek.nl
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

from meresco.xml import xpath
from gustos.common.units import COUNT
from meresco.core import Observable
from time import time

class OaiRecordCount(Observable):
    _time = time

    def __init__(self, type, interval=1.0, **kwargs):
        Observable.__init__(self, **kwargs)
        self._interval = interval
        self._lastReportTime = 0
        self._type = type
        self._addCount = 0
        self._deleteCount = 0

    def handle(self, lxmlNode):
        recordCount = len(xpath(lxmlNode, "/oai:OAI-PMH/oai:ListRecords/oai:record"))
        deleteCount = len(xpath(lxmlNode, "/oai:OAI-PMH/oai:ListRecords/oai:record/oai:header[@status='deleted']"))
        self._addCount += recordCount - deleteCount
        self._deleteCount += deleteCount

        now = self._time()
        if now - self._lastReportTime > self._interval:
            self.do.report(values={
                "%s" % self._type: {
                    "Updated records": {
                        "adds": {
                            COUNT: self._addCount
                        },
                        "deletes": {
                            COUNT: self._deleteCount
                        }
                    }
                }
            })
            self._lastReportTime = now
        return
        yield
