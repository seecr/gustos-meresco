# -*- coding: utf-8 -*-
## begin license ##
#
# "Gustos-Meresco" is a set of Gustos components for Meresco based projects.
#
# Copyright (C) 2014 Maastricht University Library http://www.maastrichtuniversity.nl/web/Library/home.htm
# Copyright (C) 2014, 2021 SURF https://www.surf.nl
# Copyright (C) 2014-2015, 2021 Seecr (Seek You Too B.V.) https://seecr.nl
# Copyright (C) 2014-2015 Stichting Bibliotheek.nl (BNL) http://www.bibliotheek.nl
# Copyright (C) 2015, 2021 Stichting Kennisnet https://www.kennisnet.nl
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

from os import getuid
assert getuid() != 0, "Do not run tests as 'root'"

from seecrdeps import includeParentAndDeps       #DO_NOT_DISTRIBUTE
includeParentAndDeps(__file__)                   #DO_NOT_DISTRIBUTE

import unittest
from warnings import simplefilter,filterwarnings
filterwarnings('ignore', message=r".*has no __module__ attribute.*", category=DeprecationWarning)

from adminservicesreporttest import AdminServicesReportTest
from srurecordupdatereporttest import SruRecordUpdateReportTest
from clauselogtest import ClauseLogTest
from gustoslogwriterintegrationtest import GustosLogWriterIntegrationTest
from gustostimedlogwritertest import GustosTimedLogWriterTest
from agentcountreporttest import AgentCountReportTest
from responsetimereporttest import ResponseTimeReportTest
from uploadsizereporttest import UploadSizeReportTest
from reporttest import ReportTest
from countreporttest import CountReportTest
from gustoscontinuouslogwriterintegrationtest import GustosContinuousLogWriterIntegrationTest
from gustosoairecordcounttest import GustosOaiRecordCountTest
from querycounttest import QueryCountTest
from responsetimetest import ResponseTimeTest
from updatablegustosclienttest import UpdatableGustosClientTest


if __name__ == '__main__':
    unittest.main()
