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

class startUp:
	def __init__(self):
		print(hyperlocale.getLocalisedString("starting"))
		conf.restricted = 0
		self.splashArea = splash()
		update_ui()
		self.checkEnviroment()
	def checkEnviroment(self):
		#add reporting of minor revisions //theemahn
		axUser.log("!!Starting Hypermatix64 %s!!"%axConf.version['number'])
		cur_user = getpass.getuser()
		if cur_user != 'root':
			self.splashArea.window.hide()
			alert("<b>Hypermatix64 must be run as root!</b>\nPlease try again.", sys.exit)
		conf.uName = getDistName()
		self.splashArea.prog.set_text("Checking %s version..."%conf.uName)
		self.splashArea.prog.set_fraction(0.2)
		update_ui()
		global uVersion
		conf.uVersion = getDistVersion()
		getDesktop()
		self.splashArea.prog.set_text("Found %s..."%conf.uVersion)
		update_ui()
		if axConf.distro['version'] != conf.uVersion or axConf.distro['name'] != conf.uName:
			self.splashArea.window.hide()
			alert("This version of Automatix is for %s %s only"%(axConf.distro['name'],axConf.distro['version']),sys.exit)
		#check enviroment for synaptic ect...
		self.splashArea.prog.set_text("Checking environment...")
		self.splashArea.prog.set_fraction(0.4)
		update_ui()
		conflicts = checkConflicts();
		#locker = exclusive_lock();
		#report conflicts if any
		if conflicts:
			self.splashArea.window.hide()
			alert(conflicts[1],sys.exit)
		self.splashArea.prog.set_text("Checking for Internet Connection...")
		self.splashArea.prog.set_fraction(0.5)
		update_ui()
		#check for an internerd connection...
		if checkConnection() == False:
			self.splashArea.window.destroy()
			alert("<b>Internet Disruption</b>\nPlease check that you are connected to the internet.\nIf you are connected and getting this message please try again later.",sys.exit)
		self.splashArea.prog.set_text("Checking Repositories List...")
		self.splashArea.prog.set_fraction(0.6)
		update_ui()
		##update splash...
		self.splashArea.prog.set_text("Retrieving Keys...")
		self.splashArea.prog.set_fraction(0.555)
		update_ui()
		#get keys...
		conf.update_my_repos = 0;
		saved_frac = self.splashArea.prog.get_fraction()
		int = len(axConf.keys)/100.00
		count = 0
		#for key in axConf.keys:
		#	count += 1
		#	self.splashArea.prog.set_text("Retrieving Keys, This May Take a Moment...")
		#	if getKey(key['id'],key['address']):
		#		pass
		#	else:
		#		self.splashArea.window.destroy()
			#	alert("Sorry Automatix can not continue because some keys could not be downloaded, please try again later.",sys.exit)	
		#	self.splashArea.prog.set_text("Retrieving Keys (%s), Please Wait..."%count)
		#	self.splashArea.prog.set_fraction(count*int)
		#	update_ui()
		self.splashArea.prog.set_fraction(int)			
		##update splash...
		self.splashArea.prog.set_text("Setting Up Repositories...")
		self.splashArea.prog.set_fraction(0.7)
		update_ui()	
		repoUpdate = setupRepos()
		##update splash...
		self.splashArea.prog.set_text("Updating Repositories...")
		self.splashArea.prog.set_fraction(0.8)
		update_ui()
		if repoUpdate or conf.update_my_repos == 1:
				self.splashArea.window.hide()
				axUser.update_apt()
				self.splashArea.window.show()
				update_ui()
				conf.update_my_repos = 0;
		self.splashArea.prog.set_text("Building Scripts List...")
		self.splashArea.prog.set_fraction(0.9)
		update_ui()
		buildScripts()
		self.splashArea.prog.set_fraction(1)
		update_ui()
		self.splashArea.window.hide()
		update_ui()
