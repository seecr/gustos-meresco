## begin license ##
#
# "Gustos-Meresco" is a set of Gustos components for Meresco based projects.
#
# Copyright (C) 2014 Maastricht University Library http://www.maastrichtuniversity.nl/web/Library/home.htm
# Copyright (C) 2014, 2021 SURF https://www.surf.nl
# Copyright (C) 2014, 2021 Seecr (Seek You Too B.V.) https://seecr.nl
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

from gustos.common.units import COUNT
from gustos.meresco.report import Report

class CountReport(Report):
    def __init__(self, curveName='total', subgroupName='Counts', keys=None, **kwargs):
        super(CountReport, self).__init__(**kwargs)
        self._curveName = curveName
        self._subgroupName = subgroupName
        if keys is None:
            keys = None, None
        self._scopeKey, self._countKey = keys
        self._counts = 0

    def analyseLog(self, collectedLog):
        if self._scopeKey is None:
            self._counts += 1
        else:
            self._counts += len(self._getScoped(collectedLog, key=self._scopeKey).get(self._countKey, []))

    def fillReport(self, groups, collectedLog):
        self.subgroupReport(groups, self._subgroupName)[self._curveName] = {COUNT: self._counts }
