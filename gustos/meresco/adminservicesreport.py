## begin license ##
#
# "Gustos-Meresco" is a set of Gustos components for Meresco based projects.
#
# Copyright (C) 2013-2015, 2021 Seecr (Seek You Too B.V.) https://seecr.nl
# Copyright (C) 2013-2014 Stichting Bibliotheek.nl (BNL) http://www.bibliotheek.nl
# Copyright (C) 2015 Koninklijke Bibliotheek (KB) http://www.kb.nl
# Copyright (C) 2021 Data Archiving and Network Services https://dans.knaw.nl
# Copyright (C) 2021 SURF https://www.surf.nl
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

import sys

from gustos.common.units import COUNT
from meresco.core import Observable

class AdminServicesReport(Observable):
    def __init__(self):
        Observable.__init__(self)
        self._counts = {
            'active': 0,
            'inactive': 0,
            'errors': 0,
            'warnings': 0
        }

    def handle(self):
        services = self.call.listServices(activeOnly=False)

        def getServices(type):
            return [
                (identifier, service)
                for identifier, service
                in services.items()
                if service['active']
                if service.get('data', {}).get(type)
            ]
        errors = getServices('errors')
        errorsCount = sum(service['data']['errors'] for _, service in errors)
        warnings = getServices('warnings')
        warningsCount = sum(service['data']['warnings'] for _, service in warnings)
        if errors:
            print(('%s: Error Services:' % self.__class__.__name__))
            for _type, identifier in sorted(map(_typeAndIdentifier, errors)):
                print(('    type: %s, identifier: %s' %  (_type, identifier)))
            sys.stdout.flush()

        activeCount = len([
            identifier
            for identifier, service
            in services.items()
            if service['active']
        ])
        inactiveCount = len(services) - activeCount
        inactiveForLogging = [
            (identifier, service)
            for identifier, service
            in services.items()
            if not service['active']
        ]
        if inactiveCount:
            print('%s: Inactive Services:' % self.__class__.__name__)
            for _type, identifier in sorted(map(_typeAndIdentifier, inactiveForLogging)):
                print('    type: %s, identifier: %s' %  (_type, identifier))
            sys.stdout.flush()

        self._counts['active'] += activeCount
        self._counts['inactive'] += inactiveCount
        self._counts['errors'] += errorsCount
        self._counts['warnings'] += warningsCount

        self.call.report(values={
            "Admin Information": {
                "Services": {
                    "active": {
                        COUNT: self._counts['active']
                    },
                    "inactive": {
                        COUNT: self._counts['inactive']
                    }
                },
                "Errors": {
                    "errors": {
                        COUNT: self._counts['errors']
                    },
                    "warnings": {
                        COUNT: self._counts['warnings']
                    }
                }
            }
        })
        return
        yield


def _typeAndIdentifier(o):
    return o[1]['type'], o[0]
