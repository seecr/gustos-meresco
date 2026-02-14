## begin license ##
#
# "Gustos-Meresco" is a set of Gustos components for Meresco based projects.
#
# Copyright (C) 2014 Maastricht University Library http://www.maastrichtuniversity.nl/web/Library/home.htm
# Copyright (C) 2014, 2021 SURF https://www.surf.nl
# Copyright (C) 2014, 2021, 2024, 2026 Seecr (Seek You Too B.V.) https://seecr.nl
# Copyright (C) 2014 Stichting Bibliotheek.nl (BNL) http://www.bibliotheek.nl
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

from gustos_meresco.report import Report
from meresco.components.log.utils import getFirst
from gustos_common.units import TIME

class ResponseTimeReport(Report):
    def __init__(self, curveName='total', subgroupName='ResponseTime', keys=None, selection="first", **kwargs):
        super(ResponseTimeReport, self).__init__(**kwargs)
        self._curveName = curveName
        self._subgroupName = subgroupName
        self._valueSelection = selections[selection]
        if keys is None:
            keys = 'httpResponse', 'duration'
        self._scopeKey, self._responseTimeKey = keys

    def fillReport(self, groups, collectedLog):
        responseTimes = map(floatOrNone, self._getScoped(collectedLog, key=self._scopeKey).get(self._responseTimeKey, []))
        responseTime = self._valueSelection(responseTimes)
        if responseTime is not None:
            self.subgroupReport(groups, self._subgroupName)[self._curveName] = {TIME: responseTime}

floatOrNone = lambda f: f if f is None else float(f)

def first(iterable, default=None):
    for i in iterable:
        return i
    return default

def sumOrNone(iterable):
    items = [i for i in iterable if i is not None]
    if not items:
        return None
    return sum(items)

selections = {
    "first": first,
    "sum": sumOrNone,
}
