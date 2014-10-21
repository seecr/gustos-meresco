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
from gustos.meresco.report import Report
from collections import defaultdict
from meresco.components.log.utils import getFirst
from gustos.common.units import COUNT

import re
userAgentRe = re.compile("\S+ \((?P<usefull>[^)]*)\)\S*")
def extractUserAgentString(userAgentString):
    match = userAgentRe.match(userAgentString if userAgentString else '')
    if not match:
        return None
    usefull = match.groupdict()['usefull']
    if not ';' in usefull:
        return None
    secondPart = usefull.split(';')[1].strip()
    return secondPart if len(secondPart) > 0 else None

class AgentCountReport(Report):
    def __init__(self, **kwargs):
        super(AgentCountReport, self).__init__(**kwargs)
        self._counts = defaultdict(int)

    def analyseLog(self, collectedLog):
        httpRequest = self._getScoped(collectedLog, key='httpRequest')
        headers = getFirst(httpRequest, 'Headers', {})
        userAgent = extractUserAgentString(headers.get('User-Agent', None))
        self._counts[userAgent] += 1

    def fillReport(self, groups, collectedLog):
        queriesCount = groups.setdefault(self._gustosGroup, {}).setdefault('User agents', {})
        for userAgent, count in self._counts.items():
            queriesCount[userAgent] = {COUNT: count }
