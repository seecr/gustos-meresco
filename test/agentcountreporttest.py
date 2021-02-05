## begin license ##
#
# "Gustos-Meresco" is a set of Gustos components for Meresco based projects.
#
# Copyright (C) 2014 Maastricht University Library http://www.maastrichtuniversity.nl/web/Library/home.htm
# Copyright (C) 2014, 2021 SURF https://www.surf.nl
# Copyright (C) 2014, 2021 Seecr (Seek You Too B.V.) https://seecr.nl
# Copyright (C) 2014, 2021 Stichting Kennisnet https://www.kennisnet.nl
# Copyright (C) 2021 Data Archiving and Network Services https://dans.knaw.nl
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

from seecr.test import SeecrTestCase, CallTrace
from gustos.meresco import AgentCountReport, GustosLogWriter
from gustos.meresco.agentcountreport import extractUserAgentString

from meresco.components.log import LogCollector, HandleRequestLog, LogCollectorScope

from weightless.core import be, Observable, compose

GOOGLE_BOT = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"

class AgentCountReportTest(SeecrTestCase):

    def testExtractUsefulAgentStringPart(self):
        self.assertEqual("Googlebot/2.1", extractUserAgentString(GOOGLE_BOT))
        self.assertEqual("Macintosh", extractUserAgentString("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.27 Safari/537.36"))
        self.assertEqual('Windows NT 6.1', extractUserAgentString("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130331 Firefox/21.0"))
        self.assertEqual("bingbot/2.0", extractUserAgentString("Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"))
        self.assertEqual("MJ12bot/v1.4.5", extractUserAgentString("Mozilla/5.0 (compatible; MJ12bot/v1.4.5; http://www.majestic12.co.uk/bot.php?+)"))
        self.assertEqual("x86_64-redhat-linux-gnu", extractUserAgentString("curl/7.19.7 (x86_64-redhat-linux-gnu) libcurl/7.19.7 NSS/3.15.3 zlib/1.2.3 libidn/1.18 libssh2/1.4.2"))

        self.assertEqual(None, extractUserAgentString(''))
        self.assertEqual(None, extractUserAgentString(None))
        self.assertEqual("between", extractUserAgentString('something (between) brackets'))
        self.assertEqual("between", extractUserAgentString('something (between;) brackets'))

    def testAnalyseLog(self):
        observer = CallTrace()
        def handleRequest(**kwargs):
            yield "We did it!"
        handleRequestMock = CallTrace(methods={'handleRequest': handleRequest})
        dna = be(
            (Observable(),
                (LogCollector(),
                    (GustosLogWriter(),
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
        self.assertEqual("We did it!", result[0])

        valuesKwarg = observer.calledMethods[-1].kwargs['values']
        self.assertEqual({'Gustos Group': {'User agents': {'Googlebot/2.1': {'count': 1}}}}, valuesKwarg)




