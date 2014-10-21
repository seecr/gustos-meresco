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
from gustos.meresco import AgentCountReport, TimedLogWriter
from gustos.meresco.agentcountreport import extractUserAgentString

from meresco.components.log import LogCollector, HandleRequestLog, LogCollectorScope

from weightless.core import be, Observable, compose, tostring

GOOGLE_BOT = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"

class AgentCountReportTest(SeecrTestCase):

    def testExtractUsefulAgentStringPart(self):
        self.assertEquals("Googlebot/2.1", extractUserAgentString(GOOGLE_BOT))
        self.assertEquals("Intel Mac OS X 10_10_0", extractUserAgentString("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.27 Safari/537.36"))

        self.assertEquals(None, extractUserAgentString(''))
        self.assertEquals(None, extractUserAgentString(None))
        self.assertEquals(None, extractUserAgentString('something (between) brackets'))
        self.assertEquals(None, extractUserAgentString('something (between;) brackets'))

    def testAnalyseLog(self):
        observer = CallTrace()
        def handleRequest(**kwargs):
            yield "We did it!"
        handleRequestMock = CallTrace(methods={'handleRequest': handleRequest})
        dna = be(
            (Observable(),
                (LogCollector(),
                    (TimedLogWriter(interval=None),
                        (AgentCountReport(gustosGroup="Gustos Group", scopeNames=('mock', )), ),
                        (observer, )
                    ),
                    (LogCollectorScope("mock"),
                        (HandleRequestLog(),
                            (handleRequestMock, )
                        )
                    )
                )
             )
        )

        result = list(compose(dna.all.handleRequest(Headers={'User-Agent': GOOGLE_BOT})))
        self.assertEquals("We did it!", result[0])

        valuesKwarg = observer.calledMethods[-1].kwargs['values']
        self.assertEquals({'Gustos Group': {'User agents': {'Googlebot/2.1': {'count': 1}}}}, valuesKwarg)




