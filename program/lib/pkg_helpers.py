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
# pkg_helpers.py - contains identically-behaving classes for each
#                  package manager supported by Hypermatix64

# needs_for(packagename) - what this package depends on that is NOT
#                          installed
# depends_for(packagename) - what depends on this package that IS
#                            installed
# is_installed(packagename) - is package installed?

class HX64Pacman:
	def __init__(self):
		import pacman
	def needs_for(self, packagename):
		import pacman
		dependlist = pacman.needs_for(packagename)
		dependlist.reverse()
		dependlist.remove(packagename)
		return dependlist
	def depends_for(self, packagename):
		dependlist = pacman.depends_for(packagename)
		dependlist.reverse()
		dependlist.remove(packagename)
		return dependlist
