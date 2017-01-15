#!/usr/bin/env python
# Copyright 2006-2008 (?) Automatix Team
# Copyright 2010 (?) TheeMahn
# Copyright 2016 Declan Hoare
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
# ultamatix.py - entry point
import sys
if len(sys.argv) < 2:
	print "You can't run Hypermatix64 like this. Try '/usr/bin/hypermatix64' instead."
	sys.exit()
sys.path += ["/usr/lib/ultamatix"]
from resin_config import *
sys.path += [axConf.locations['modules']]
ultamatix_version = "Hypermatix64: 1.9.0"
resin_version = "Resin version: 3.2.4"

if '-d' in sys.argv or '--debug' in sys.argv:
	print "Hypermatix64 is running in debug mode. All errors, no matter how small, will be displayed."
	print ultamatix_version
	print resin_version
if '-v' in sys.argv or '--version' in sys.argv:
	print ultamatix_version
	print resin_version
	sys.exit()
if '-e' in sys.argv or '--dumplog' in sys.argv:
	try:
		dump = open("%s/.ultamatix/activity.log"%axUser.home).readlines()
	except:
		print "No activity log was found"
		sys.exit()
	for d in dump:
		print d,
	sys.exit()
if '-h' in sys.argv  or '--help' in sys.argv:
	print """
	Hypermatix64 1.9.0
	-v	--version		dump version info
	-e	--dumplog		dump activity log
	-h	--help			this help message
	-d      --debug		pushes python into debug mode
	"""
	sys.exit()

from startup import *

#        mixer.music.play(-1)
start = startUp()
from main_interface import *
main = main_ui()
gtk.main()
