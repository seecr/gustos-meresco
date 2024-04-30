## begin license ##
#
# "Gustos-Meresco" is a set of Gustos components for Meresco based projects.
#
# Copyright (C) 2014, 2021 Seecr (Seek You Too B.V.) https://seecr.nl
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

from distutils.core import setup

version = '$Version: 0$'[9:-1].strip()

from os import walk
packages = []
for path, dirs, files in walk('gustos'):
    if '__init__.py' in files and path != 'gustos':
        packagename = path.replace('/', '.')
        packages.append(packagename)

setup(
    name='gustos-meresco',
    packages=[
            'gustos'        #DO_NOT_DISTRIBUTE
        ] + packages,
    version=version,
    url='http://gustos.seecr.nl',
    author='Seecr',
    author_email='development@seecr.nl',
    maintainer='Seecr',
    maintainer_email='development@seecr.nl',
    description='Gustos components for Meresco based projects',
    long_description='A set of Gustos components for Meresco based projects',
    license='GPL',
    platforms='all',
)
