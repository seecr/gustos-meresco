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

from .report import Report
from meresco.components.log.utils import getFirst
from urllib.parse import urlencode
from gustos.common.units import COUNT, TIME

class SruResponseTimesReport(Report):
    def fillReport(self, groups, collectedLog):
        gustosReport = self.groupReport(groups)
        sru = self._getScoped(collectedLog, key='sru')
        sruArguments = getFirst(sru, 'arguments', {})
        queryLength = len(urlencode(sruArguments))
        if queryLength:
            gustosReport['Query length'] = {'query length': {COUNT: queryLength}}

        responseTimeData = {}
        for key, gustosKey in RESPONSE_TIMEKEYS:
            value = getFirst(sru, key, None)
            if value is not None:
                responseTimeData[gustosKey] = {TIME: float(value)}
        if responseTimeData:
            gustosReport['ResponseTime'] = responseTimeData

RESPONSE_TIMEKEYS = [
    ('handlingTime', 'sru'),
    ('indexTime', 'index'),
    ('queryTime', 'queryTime'),
]