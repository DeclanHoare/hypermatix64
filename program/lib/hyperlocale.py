# This file is part of Hypermatix64.
#
# Hypermatix64 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hypermatix64 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hypermatix64.  If not, see <http://www.gnu.org/licenses/>.
#
# hyperlocale.py - functions for localising strings

import locale, os, xml.etree.ElementTree
import conf

systemLanguage = locale.getdefaultlocale()[0]
theoreticalDataDirectory = os.path.join(conf.home, "lang", systemLanguage)
if os.path.isdir(theoreticalDataDirectory):
	dataDirectory = theoreticalDataDirectory
else:
	theoreticalDataDirectory = os.path.join(conf.home, "lang", systemLanguage.split("_")[0])
	if os.path.isdir(theoreticalDataDirectory):
		dataDirectory = theoreticalDataDirectory
	else:
		dataDirectory = os.path.join(conf.home, "lang", "en")
localisationFileLocation = os.path.join(dataDirectory, "strings.xml")
localisationTree = xml.etree.ElementTree.parse(localisationFileLocation)
localisationRoot = localisationTree.getroot()

def getLocalisedString(stringName):
  return localisationRoot.find(stringName).text
