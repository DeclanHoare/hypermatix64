import sys,os,time,user
import threading
import apt, apt_pkg
from xml_functions import *
from resin_config import *
from extra_functions import *
#import warnings
#warnings.filterwarnings("ignore", "apt API not stable yet", FutureWarning)
def getDesktop():
	if '--kde_desktop' in sys.argv:
		conf.desktop = ["any","KDE"]
		conf.strict_desktop = "KDE"
		conf.toggle_icons = ["/usr/share/ultamatix/pixmaps/gapps.png","/usr/share/ultamatix/pixmaps/gapps_active.png"];
		conf.other_desktop = "gnome"
	else:
		conf.desktop = ["any","gnome"]
		conf.strict_desktop = "gnome"
		conf.toggle_icons = ["/usr/share/ultamatix/pixmaps/kapps.png","/usr/share/ultamatix/pixmaps/kapps_active.png"];
		conf.other_desktop = "KDE"
def getDistName():
	#find the version of ubuntu the user is running...
	versions = (('Ubuntu','Ubuntu'),('Mepis','Mepis'),('Debian','Debian'))
	for v in versions:
		if testOutput('lsb_release -i | grep "%s"'%v[0]):
			return v[1]
	return None
def getDistVersion():
	#find the version of ubuntu the user is running...
	versions = (('8.04','hardy'),('7.10','gutsy'),('8.10','intrepid'),('9.04','jaunty'),('4.0r0','4.0r0'),(2.2,'jaguar'),('9.10',"karmic"),('16.10',"yakkety"))
	for v in versions:
		if testOutput('lsb_release -r | grep "%s"'%v[0]):
			return v[1]
	return None
def checkConflicts():
	"""determine if any conflicting programs are running..."""
	if(testOutput('ps -U root -u root u | grep "synaptic" | grep -v grep')):
		return ("Synaptic","<b>Synaptic is running</b>\nPlease close Synaptic and restart Ultamatix. ")
	if(testOutput('ps -U root -u root u | grep "update-manager" | grep -v grep')):
		return ("Update-Manager","<b>Ubuntu Update Manager is running</b>\nPlease close Ubuntu Update Manager and restart Ultamatix. ")
	if(testOutput('ps -U root -u root u | grep "apt-get" | grep -v grep')):
		return ("Apt","<b>Apt-get is running</b>\nPlease close Apt-get and restart Ultamatix. ")
	if(testOutput('ps -U root -u root u | grep "adept" | grep -v grep')):
		return ("Adept","<b>Adept is running</b>\nPlease close Adept and restart Ultamatix. ")
	if(testOutput('ps -U root -u root u | grep "ultamatix.py" | grep "/usr/bin/python" | grep -v grep | grep -v %s'%os.getpid())):
		return ("another Ultamatix session","<b>Ultamatix is already running</b>\nOnly one Ultamatix session may be run at any time. ")
	""" get the APT lock //major bug in automatix, will not exist in ultamatix
        try_acquire_lock"""	
	#x = exclusive_lock()
	return None
#def exclusive_lock():
#	try:
#		apt_pkg.PkgSystemLock()
#       	except SystemError:
#		return ("Unable to get Exclusive Lock","<b>A package manager is running</b>\nPlease close and restart Ultamatix. ")
#	else:
#		return None 
#def unlock_apt():
#        """unlock here to make sure that lock/unlock are always run pair-wise (and don't explode on errors)"""
#        try:
#            apt_pkg.PkgSystemUnLock()
#        except SystemError:
#            print "WARNING: trying to unlock a not-locked PkgSystem"
#            pass
def checkConnection():
	check = os.popen3("ping getautomatix.com -c 1 -w 1");
	if "unknown host" in check[2].read():
		if os.system("cd %s;wget http://www.getautomatix.com/files/example"%axUser.conf_folder):
			pass
		else:
			os.system("cd %s;rm ./example"%axUser.conf_folder)				
			return True
	else:
		return True
	return False	
def setupRepos():
			#change repos...Prompt end user first, perhaps add option user selectable //theemahn
			axUser.backup_sources()
			call = "cp /etc/apt/sources.list /etc/apt/sources.list_backup_`date +%Y%m%d%H%M`\nchmod 644 /etc/apt/sources.list_backup_`date +%Y%m%d%H%M`\n"
			os.system(call)
			update = 0
			current = repo_proc("/etc/apt/sources.list")
			current_list = current.get_current_repo()
			ax_version = repo_proc(axConf.apt_sources).get_current_repo()
			local = current.find_local()
			if local:
				local +="."
			else:
				local = ""
			for a in ax_version:
				loc = a[0].replace("%%LOCAL%%",local)
				non = a[0].replace("%%LOCAL%%","")
				f_dir = []
				f = 0
				for cur in current_list:
					if loc == cur[0] or non == cur[0]:
						f_dir += cur[1]
						f = 1
				if f:
					post = []
					for dire in a[1]:
						if dire not in f_dir:
							post += [dire]
					if post:
						if non != None and None not in post:
							add = non+" "+" ".join(post)
							print "ADD: %s"%add
							current.add_repo(add)
							update = 1
				else:
						if non != None:
							add = non+" "+" ".join(a[1])
							current.add_repo(add)
							update = 1
			axUser.set_source_mode(1)
			##run apt-get update...
			if update:
				return True
			else:
				return False
def getKey(key,address):
	new_key = address[address.rfind('/')+1:len(address)]
	if testOutput('apt-key list | grep "%s"'%key) == False:
		conf.update_my_repos = 1;
		key_directory = axUser.conf_folder+"/keys"
		try:
			os.mkdir(key_directory)
		except:
			print "could not create keys directory"
		if os.system('cd %s \n wget --tries=2 --timeout=45 %s'%(key_directory,address))==0:
			os.system("""cd %s \ngpg --import %s\n
			gpg --export --armor %s | apt-key add -"""%(key_directory,new_key,key))
			axUser.log("Updated keys with %s"%key)
			os.system("rm %s -R"%key_directory)
			return True
		else:
			return False
	else:		
		return True




