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
from meresco.components.log.utils import getFirst
from gustos.common.units import COUNT
from gustos.meresco.report import Report

class SruQueryCountReport(Report):
    def __init__(self, **kwargs):
        super(SruQueryCountReport, self).__init__(**kwargs)
        self._counts ={
            'queries': 0,
        }

    def analyseLog(self, collectedLog):
        sru = self._getScoped(collectedLog, key='sru')
        sruArguments = getFirst(sru, 'arguments', {})
        if sruArguments:
            self._counts['queries'] += 1

    def fillReport(self, groups, collectedLog):
        self.subgroupReport(groups, 'Queries count')['Queries'] = {COUNT: self._counts['queries'] }
