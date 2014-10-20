## begin license ##
#
# "Gustos-Meresco" is a set of Gustos components for Meresco based projects.
#
# Copyright (C) 2014 Seecr (Seek You Too B.V.) http://seecr.nl
# Copyright (C) 2014 Stichting Kennisnet http://www.kennisnet.nl
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

from seecr.test import SeecrTestCase, CallTrace
from gustos.meresco import ClauseLog
from weightless.core import be, retval
from collections import defaultdict
from meresco.core import Observable
from cqlparser import parseString

class ClauseLogTest(SeecrTestCase):

    def count(self, query):
        __callstack_var_logCollector__ = defaultdict(list)
        def executeQuery(**kwargs):
            raise StopIteration('result')
            yield
        observer = CallTrace(methods={'executeQuery': executeQuery})
        log = be((Observable(),
            (ClauseLog(),
                (observer,)
            )
        ))
        result = retval(log.any.executeQuery(key='value', cqlAbstractSyntaxTree=parseString(query)))
        self.assertEquals('result', result)

        return __callstack_var_logCollector__

    def testSimpleCount(self):
        self.assertEquals({'cqlClauses': [1]}, self.count('query'))
        self.assertEquals({'cqlClauses': [2]}, self.count('query AND query'))
        self.assertEquals({'cqlClauses': [6]}, self.count('query AND (query NOT query) OR (query OR (query AND query))'))

