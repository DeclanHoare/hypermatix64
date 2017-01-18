#!/usr/bin/env python2
# Copyright 2006-2008 (?) Automatix Team
# Copyright 2010 (?) TheeMahn
# Copyright 2016, 2017 Declan Hoare
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
# interface.py - starts interface

import sys, argparse
from resin_config import *
import hyperlocale

localisationFile = hyperlocale.getAndParseLocalisationFile()
ultamatix_version_num = "1.9.0"
resin_version_num = "3.2.5"
ultamatix_version = hyperlocale.getLocalisedString(localisationFile, "productName") + ": " + ultamatix_version_num
resin_version = hyperlocale.getLocalisedString(localisationFile, "resinVersionText") + resin_version_num
if len(sys.argv) < 2:
	print hyperlocale.getLocalisedString(localisationFile, "incorrectExecutableErrorMessage")
	sys.exit()

parser = argparse.ArgumentParser(description=hyperlocale.getLocalisedString(localisationFile, "productName") + " " + ultamatix_version_num)

parser.add_argument("-d", "--debug", dest="debugMode", action="store_const", const=True, default=False, help=hyperlocale.getLocalisedString(localisationFile, "debugModeHelpText"))
parser.add_argument("-v", "--version", dest="displayVersion", action="store_const", const=True, default=False, help=hyperlocale.getLocalisedString(localisationFile, "versionHelpText"))
parser.add_argument("-e", "--dumplog", dest="displayLog", action="store_const", const=True, default=False, help=hyperlocale.getLocalisedString(localisationFile, "dumpLogHelpText"))

args=parser.parse_args()

if args.displayVersion:
	print ultamatix_version
	print resin_version
	sys.exit()
if args.debugMode:
	print "Hypermatix64 is running in debug mode. All errors, no matter how small, will be displayed."
	print ultamatix_version
	print resin_version
if args.displayLog:
	try:
		dump = open("/etc/hypermatix64/activity.log").readlines()
	except:
		print hyperlocale.getLocalisedString(localisationFile, "noActivityLogErrorMessage")
		sys.exit()
	for d in dump:
		print d,
	sys.exit()

from startup import *
start = startUp()
from main_interface import *
main = main_ui()
gtk.main()
