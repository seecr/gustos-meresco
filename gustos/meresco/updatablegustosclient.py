## begin license ##
#
# "Gustos-Meresco" is a set of Gustos components for Meresco based projects.
#
# Copyright (C) 2013-2015 Seecr (Seek You Too B.V.) http://seecr.nl
# Copyright (C) 2013-2014 Stichting Bibliotheek.nl (BNL) http://www.bibliotheek.nl
# Copyright (C) 2015 Koninklijke Bibliotheek (KB) http://www.kb.nl
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

from gustos.client import Client

from meresco.core import Observable

class UpdatableGustosClient(Observable):

    def __init__(self, identifier, name=None):
        Observable.__init__(self, name=name)
        self._identifier = identifier
        self._client = None

    def updateConfig(self, config, **kwargs):
        if not 'gustos' in config:
            if self._client is not None:
                self._client.stop()
            self._client = None
            return

        if self._client is None:
            self._client = Client(
                id=self._identifier,
                gustosHost=config['gustos']['host'],
                gustosPort=config['gustos']['port'],
                threaded=False)
        else:
            self._client.updateSender(
                host=config['gustos']['host'],
                port=config['gustos']['port'])

        return
        yield

    def report(self, values):
        if not self._client:
            return
        self._client.report(values=values)
