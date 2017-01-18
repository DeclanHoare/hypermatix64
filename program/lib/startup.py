import xml_functions as xml
from resin_config import *
from resin_ui import *
from distro_helpers import *
from extra_functions import *
from resin_controllers import *
import tray
class startUp:
	def __init__(self):
		print "Starting"		
		conflicts = checkConflicts();
		#report conflicts if any & set exclusive lock on all package managers //theemahn
		if conflicts:
			alert(conflicts[1],sys.exit)
		conf.restricted = 0
		self.splashArea = splash()
		update_ui()
		#time.sleep(.5)
		self.checkEnviroment();
	def checkEnviroment(self):
		#add reporting of minor revisions //theemahn
		axUser.log("!!Starting Hypermatix64 %s!!"%axConf.version['number'])
		cur_user = os.popen("echo $USER").read()
		if cur_user != 'root\n':
			self.splashArea.window.hide()
			alert("<b>Hypermatix64 must be run as root!</b>\nPlease try again.",sys.exit);
		conf.uName = getDistName()
		self.splashArea.prog.set_text("Checking %s version..."%conf.uName)
		self.splashArea.prog.set_fraction(0.2)
		update_ui()
		#get distro version...
		time.sleep(.5);
		global uVersion
		conf.uVersion = getDistVersion()
		getDesktop()
		self.splashArea.prog.set_text("Found %s..."%conf.uVersion)
		update_ui()
		time.sleep(.5);
		#if axConf.distro['version'] != conf.uVersion or axConf.distro['name'] != conf.uName:
		#	self.splashArea.window.hide()
		#	alert("This version of Automatix is for %s %s only"%(axConf.distro['name'],axConf.distro['version']),sys.exit)
		#check enviroment for synaptic ect...
		self.splashArea.prog.set_text("Checking environment...")
		self.splashArea.prog.set_fraction(0.4)
		update_ui()
		time.sleep(.1);
		conflicts = checkConflicts();
		#locker = exclusive_lock();
		#report conflicts if any
		if conflicts:
			self.splashArea.window.hide()
			alert(conflicts[1],sys.exit)
		#self.splashArea.prog.set_text("Checking for Internet Connection...")
		self.splashArea.prog.set_fraction(0.5)
		update_ui()
		#check for an internerd connection...
		#if checkConnection() == False:
		#	self.splashArea.window.destroy()
		#	alert("<b>Internet Disruption</b>\nPlease check that you are connected to the internet.\nIf you are connected and getting this message please try again later.",sys.exit)
		self.splashArea.prog.set_text("Checking Repositories List...")
		self.splashArea.prog.set_fraction(0.6)
		update_ui()
		time.sleep(.5)
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
		time.sleep(.1)
		self.splashArea.prog.set_fraction(1)
		update_ui()
		time.sleep(.1)
		self.splashArea.window.hide()
		update_ui()
