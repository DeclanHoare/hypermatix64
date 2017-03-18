# Copyright 2006-2008 (?) Automatix Team
# Copyright 2010 (?) TheeMahn
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
# startup.py - splash screen

import xml_functions
import resin_config, resin_ui
import distro_helpers, extra_functions
import resin_controllers, hyperlocale
import tray, interface, getpass
import conf, sys

class startUp:
	def __init__(self):
		print(hyperlocale.getLocalisedString("starting"))
		conf.restricted = 0
		self.splashArea = resin_ui.splash()
		extra_functions.update_ui()
		self.checkEnviroment()
	def checkEnviroment(self):
		resin_config.log(hyperlocale.getLocalisedString("logStarting").format(conf.version))
		cur_user = getpass.getuser()
		if cur_user != "root":
			self.splashArea.window.hide()
			resin_ui.alert(hyperlocale.getLocalisedString("notRunningAsRootError"), sys.exit)
		conf.uName = distro_helpers.getDistName()
		self.splashArea.prog.set_text(hyperlocale.getLocalisedString("checkVersion").format(conf.uName))
		self.splashArea.prog.set_fraction(0.2)
		extra_functions.update_ui()
		conf.uVersion = distro_helpers.getDistVersion()
		distro_helpers.getDesktop()
		self.splashArea.prog.set_text(hyperlocale.getLocalisedString("foundVersion").format(conf.uVersion))
		extra_functions.update_ui()
		if conf.uName not in conf.supported_linux_dists:
			self.splashArea.window.hide()
			resin_ui.alert(hyperlocale.getLocalisedString("incorrectSystemError").format(conf.uName), sys.exit)
		#check enviroment for synaptic ect...
		self.splashArea.prog.set_text(hyperlocale.getLocalisedString("checkEnvironment"))
		self.splashArea.prog.set_fraction(0.4)
		extra_functions.update_ui()
		conflicts = distro_helpers.checkConflicts()
		#locker = exclusive_lock();
		#report conflicts if any
		if conflicts:
			self.splashArea.window.hide()
			resin_ui.alert(conflicts[1], sys.exit)
		self.splashArea.prog.set_text(hyperlocale.getLocalisedString("checkConnection"))
		self.splashArea.prog.set_fraction(0.5)
		extra_functions.update_ui()
		#check for an internerd connection...
		if not distro_helpers.checkConnection():
			self.splashArea.window.destroy()
			resin_ui.alert(hyperlocale.getLocalisedString("notConnectedError"), sys.exit)
		#FIXME
		#self.splashArea.prog.set_text("Setting Up Repositories...")
		#self.splashArea.prog.set_fraction(0.7)
		#extra_functions.update_ui()	
		#repoUpdate = setupRepos()
		###update splash...
		#self.splashArea.prog.set_text("Updating Repositories...")
		#self.splashArea.prog.set_fraction(0.8)
		#extra_functions.update_ui()
		#if repoUpdate or conf.update_my_repos == 1:
				#self.splashArea.window.hide()
				#axUser.update_apt()
				#self.splashArea.window.show()
				#update_ui()
				#conf.update_my_repos = 0;
		self.splashArea.prog.set_text("Building Scripts List...")
		self.splashArea.prog.set_fraction(0.9)
		extra_functions.update_ui()
		extra_functions.buildScripts()
		self.splashArea.prog.set_fraction(1)
		extra_functions.update_ui()
		self.splashArea.window.hide()
		extra_functions.update_ui()
