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
import hyperlocale
import conf

ultamatix_version_num = "1.9.0"
ultamatix_version = hyperlocale.getLocalisedString("productName") + ": " + ultamatix_version_num

if conf.args.version:
	print(ultamatix_version)
	sys.exit(0)
if conf.args.debug:
	print(hyperlocale.getLocalisedString("runningInDebugMode"))
	print(ultamatix_version)
if conf.args.dumplog:
	try:
		dump = open("/var/log/hypermatix64_activity.log").readlines()
	except:
		print(hyperlocale.getLocalisedString("noActivityLogError"))
		sys.exit(1)
	for d in dump:
		print(d)
	sys.exit(0)

import startup
start = startup.startUp()
import main_interface
main = main_interface.main_ui()

