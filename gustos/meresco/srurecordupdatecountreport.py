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

from meresco.components.log.utils import getFirst, getScoped
from gustos.common.units import COUNT
from gustos.meresco.report import Report

class SruRecordUpdateCountReport(Report):
    def __init__(self, **kwargs):
        super(SruRecordUpdateCountReport, self).__init__(**kwargs)
        self._counts = {
            'sruAdd': 0,
            'sruDelete': 0,
            'sruInvalid': 0,
        }

    def analyseLog(self, collectedLog):
        sruRecordUpdate = getScoped(collectedLog, scopeNames=self._scopeNames, key='sruRecordUpdate')
        addIdentifier = getFirst(sruRecordUpdate, 'add')
        deleteIdentifier = getFirst(sruRecordUpdate, 'delete')
        invalidIdentifier = getFirst(sruRecordUpdate, 'invalid')
        if addIdentifier is None and deleteIdentifier is None:
            return
        self._counts['sruAdd'] += (0 if addIdentifier is None else 1)
        self._counts['sruDelete'] += (0 if deleteIdentifier is None else 1)
        self._counts['sruInvalid'] += (0 if invalidIdentifier is None else 1)

    def fillReport(self, groups, collectedLog):
        groupReport = self.groupReport(groups)
        groupReport['Upload count'] = {
                'Add': { COUNT: self._counts['sruAdd'] },
                'Delete': { COUNT: self._counts['sruDelete']},
                'Uploads': { COUNT: self._counts['sruAdd'] + self._counts['sruDelete'] },
                'Invalid': { COUNT: self._counts['sruInvalid']},
            }
