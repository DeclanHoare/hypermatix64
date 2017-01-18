from resin_config import *
from resin_ui import *
from distro_helpers import *
from extra_functions import *
from terminal import *
#from warnings import warn
#warnings.filterwarnings("ignore", "apt API not stable yet", FutureWarning)
#import apt
#import apt_pkg
def ask_question(in_question,window=None):
	q = question(in_question,window)
	while q.wait:
		update_ui()
		time.sleep(.1)
	return (q.input,q)
def ask_info_question(info,in_question,window=None,okay=False):
	q = info_box(info,in_question,window)
	if okay == True:
		q.no_button.hide()
		q.yes_button.set_label("ok")
	while q.wait:
		update_ui()
		time.sleep(.1)
	return (q.input,q)
def keep_debs (window):
	## Cleanup class needs to be added ///TheeMahn
	alert("<b>This feature has not yet been implemented.</b>",None,self.main_window.window)
def exit_routine(window):
	"""quest = ask_question("<b>Are you sure you would like to exit Ultimatix?</b>")
	if quest[0]:
		sys.exit()
	else:
		quest[1].window.hide()
		return True
	"""
	#unlock_apt()
	sys.exit()
def no_destroy(widget,event):
	exit_routine(widget)
	return True
class apt_update:
	def __init__(self):
		## add code to ask the user to add repos ///TheeMahn
		#aa = unlock_apt()
		if "AUTOMATIX" != "AUTOMATIX BLEEDER":
			repo_check = ask_info_question(axConf.version['repos'].strip(),"Do you wish to modify your sources.list?")
			if repo_check[0]:
				repo_check[1].window.hide()
				conf.restricted = 1
			else:
				repo_check[1].window.hide()
				alert("Some scripts simply will not work, without the repositories enabled.")
				conf.restricted = 0
			conf.restricted = 0
		#self.splashArea = splash()
		update_ui()
		#time.sleep(.5)
		#self.checkEnviroment();
		## End addition
		#repo_check = ask_info_question(axConf.version['legal'].strip(),"Do you agree?")
		#quest = ask_question("<b>Ultamatix & Mediaubuntu Repositories are not in your list, many apps / games will not install without them.  Would you like to add them?</b>")
		#tempunlock = unlock_apt()
		try:
			if self.term:
				pass
			else:
				self.term = quick_terminal()
		except:
			self.term = quick_terminal()
		try:
			conf.trayIcon.set_window(self.term.terminal.window)
			conf.trayIcon.set_label("Updating Apt")
		except:
			pass
		update_ui()		
		self.term.terminal.window.show()
		call = "#!/bin/bash\necho 'Updating your sources list please wait...'\nsleep 1\napt-get update\n"
		script = axUser.conf_folder+"/update.autoscript"
		open(script,'w').write(call)
		os.chmod(script,0777)
		self.term.connect_pipe(script)		
		os.unlink(script)
		time.sleep(1)
		self.term.terminal.window.hide()
		axUser.log("Updated APT")
class repo_add:
	def __init__(self):
		## add code to ask the user to add repos ///TheeMahn
		if "AUTOMATIX" != "AUTOMATIX BLEEDER":
			repo_check = ask_info_question(axConf.version['repos'].strip(),"Do you wish to modify your sources.list?")
			if repo_check[0]:
				repo_check[1].window.hide()
				conf.restricted = 1
			else:
				repo_check[1].window.hide()
				alert("Some scripts simply will not work, without the repositories enabled.")
				conf.restricted = 0
			conf.restricted = 0
		#self.splashArea = splash()
		update_ui()
		#time.sleep(.5)
		#self.checkEnviroment();
		## End addition
		#repo_check = ask_info_question(axConf.version['legal'].strip(),"Do you agree?")
		#quest = ask_question("<b>Ultamatix & Mediaubuntu Repositories are not in your list, many apps / games will not install without them.  Would you like to add them?</b>")
		#tempunlock = unlock_apt()
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
#def run_synaptic(self, id, action, lock):
#    try:
#        apt_pkg.PkgSystemUnLock()
#    except SystemError:
#        pass
#    cmd = ["/usr/sbin/synaptic", "--hide-main-window",  "--non-interactive",
#           "--plug-progress-into", "%s" % (id) ]
#    if action == INSTALL:
#      cmd.append("--set-selections")
#      cmd.append("--progress-str")
#      cmd.append("%s" % _("Please wait, this can take some time."))
#      cmd.append("--finish-str")
#      cmd.append("%s" %  _("Update is complete"))
#      proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
#      f = proc.stdin
#      for s in self.packages:
#        f.write("%s\tinstall\n" % s)
#      f.close()
#      proc.wait()
#    elif action == UPDATE:
#      cmd.append("--update-at-startup")
#      subprocess.call(cmd)
#    else:
#      print "run_synaptic() called with unknown action"
#      sys.exit(1)
#
    # use this once gksudo does propper reporting
    #if os.geteuid() != 0:
    #  if os.system("gksudo  /bin/true") != 0:
    #    return
    #  cmd = "sudo " + cmd;
#    lock.release()
