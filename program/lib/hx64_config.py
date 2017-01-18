# Copyright 2006-2008 (?) Automatix Team
# Copyright 2008-2010 (?) TheeMahn
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
# hx64_config.py - class "conf"

import sys, os, gtk.glade
import __main__

class conf:
	def __init__(self):
		self.uVersion = ""
		self.gladeUI = gtk.glade.XML(os.path.join(__main__.LOCATION, "resin_glade.glade"))
		self.catalog = []
		self.script_list = []
		self.selected_scripts = []
		self.need_generate = 0
		self.failed = []
		self.script_errors = []
		self.changed_sources = 0
		self.dep_installed = []
		self.dep_uninstalled = []
		self.deselector = []
