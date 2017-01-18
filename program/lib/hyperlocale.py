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
# hyperlocale.py - class "HX64Locale" for localising strings

import locale, os, xml.etree.ElementTree
import __main__

class HX64Locale:
	def __init__(self):
		systemLanguage = locale.getdefaultlocale()[0]
		theoreticalDataDirectory = os.path.join(__main__.LOCATION, "lang", systemLanguage)
		if os.path.isdir(theoreticalDataDirectory):
			self.dataDirectory = theoreticalDataDirectory
		else:
			theoreticalDataDirectory = os.path.join(__main__.LOCATION, "lang", systemLanguage.split("_")[0])
			if os.path.isdir(theoreticalDataDirectory):
				self.dataDirectory = theoreticalDataDirectory
			else:
				self.dataDirectory = os.path.join(__main__.LOCATION, "lang", "en")
		localisationFileLocation = os.path.join(self.dataDirectory, "strings.xml")
		localisationTree = xml.etree.ElementTree.parse(localisationFileLocation)
		self.localisationRoot = localisationTree.getroot()
	def getLocalisedString(self, stringName):
	  return self.localisationRoot.find(stringName).text
