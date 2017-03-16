#!/usr/bin/env python2
# Copyright 2017 Declan Hoare
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
# hypermatix64.py - handles initialisation:
# - gets root access (and python debug mode if needed)
# - detects language
# - parses arguments

import sys, os, argparse, distutils.spawn

sys.path.append("lib")
mypath = os.path.realpath(os.path.abspath(__file__))
location = os.path.dirname(mypath)

import conf

conf.home = location

import hyperlocale

# FIXME - There should be a more specific way to get the DE than just
# using an environment variable to determine if we're on KDE or not.
if "KDE_FULL_SESSION" in os.environ:
	conf.onkde = True

if "--relaunch" in sys.argv:
	sys.argv.pop(sys.argv.index("--relaunch")) # hide from argparse
	relaunched = True
else:
	relaunched = False
	welcome = hyperlocale.getLocalisedString("welcome")
	print(welcome)
	for count in welcome:
		sys.stdout.write("=")
	# btw, this page doesn't actually exist on my site yet - I will make
	# it and remove this comment once HX64 is usable
	print("\nhttp://home.exetel.com.au/declanhoare/hypermatix64")

parser = argparse.ArgumentParser(description=hyperlocale.getLocalisedString("productDescription"))

parser.add_argument("-d", "--debug", dest="debug", action="store_const", const=True, default=False, help=hyperlocale.getLocalisedString("debugHelp"))
parser.add_argument("-v", "--version", dest="version", action="store_const", const=True, default=False, help=hyperlocale.getLocalisedString("versionHelp"))
parser.add_argument("-e", "--dumplog", dest="dumplog", action="store_const", const=True, default=False, help=hyperlocale.getLocalisedString("dumplogHelp"))

conf.args = parser.parse_args()

relaunch = False
usesudo = False

if os.getuid() != 0:
	relaunch = True
	usesudo = True

if conf.args.version or conf.args.dumplog:
	relaunch = False
	usesudo = False

if conf.args.debug and not relaunched:
	print(hyperlocale.getLocalisedString("debugMode"))
	relaunch = True

if relaunch:
	command = sys.executable
	arguments = [command]
	if conf.args.debug:
		arguments.append("-d")
	arguments.append(mypath)
	if conf.args.debug:
		arguments.append("--debug")
	arguments.append("--relaunch")
	if usesudo:
		cmdstring = " ".join(arguments)
		if conf.onkde:
			command = distutils.spawn.find_executable("kdesudo")
			arguments = [command, "-c", cmdstring, "-d", "-n", "--comment", hyperlocale.getLocalisedString("enterPassword")]
		else:
			command = distutils.spawn.find_executable("gksudo")
			arguments = [command, "--message", hyperlocale.getLocalisedString("enterPassword"), cmdstring]
	os.execv(command, arguments)

import interface
