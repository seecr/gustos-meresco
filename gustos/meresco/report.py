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
from meresco.components.log.utils import scopePresent, getScoped

class Report(object):
    def __init__(self, gustosGroup, scopeNames):
        if type(scopeNames) is not tuple:
            raise ValueError('Expected tuple')
        self._gustosGroup = gustosGroup
        self._scopeNames = scopeNames

        self._wrapMethod('analyseLog')
        self._wrapMethod('fillReport')

    def _getScoped(self, collectedLog, *args, **kwargs):
        return getScoped(collectedLog, scopeNames=self._scopeNames, *args, **kwargs)

    def _wrapMethod(self, methodName):
        method = getattr(self, methodName, None)
        if method is None:
            return
        def wrap(collectedLog, **kwargs):
            if scopePresent(collectedLog, self._scopeNames):
                return method(collectedLog=collectedLog, **kwargs)
        setattr(self, methodName, wrap)
