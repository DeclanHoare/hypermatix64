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
# resin_config.py - classes "AX_user", "AX_conf", and "HX_locale"

# !!FIXME FIXME FIXME!!
# This file contains a LOT of APT-specific code.
# This should all be cut out of this file and moved to an APT module
# so that we can more easily work with distros which do not use APT.

import sys, os, time, user, platform
import gtk, gtk.glade, gobject, pango
import locale, xml.etree.ElementTree
import hx64_config, xml_functions

# User/system related configuration.
class AX_user:
	def __init__(self):
		self.username = sys.argv[1]
		self.home = sys.argv[2]
		self.uid = int(sys.argv[3])
		self.conf_folder = "/etc/hypermatix64"
		self.source_change_file = self.conf_folder+"/sc"
		self.create_conf_folder()
		self.create_usage_log()
		self.create_installed_log()
		self.create_log()
		self.ax_in = self.conf_folder + "/ax_in"
		self.ax_out = self.conf_folder + "/ax_out"
		self.delete_pipes()
	def create_log(self):
		self.log_file = self.conf_folder + "/activity.log"
		try:
			os.stat(self.log_file)
		except:
			open(self.log_file,'w').write("")
			os.chown(self.log_file,self.uid,-1)
			self.log("Log started.")
	def log(self,statement):
		date = time.strftime('[%m/%d/%Y - %H:%M.%S]')
		self.open_log = open(self.log_file,"a")
		self.open_log.write("%s - %s\n"%(date,statement))
		self.open_log.close()
		return True
	def sim_log(self,string):
		self.open_log = open(self.log_file,"a")
		self.open_log.write(string)
		self.open_log.close()
		return True
	def set_source_mode(self,mode):
		if mode:
			open(self.source_change_file,"w").write("1")
			os.chown(self.source_change_file,self.uid,-1)
		else:
			open(self.source_change_file,"w").write("0")
			os.chown(self.source_change_file,self.uid,-1)
	def get_source_mode(self):
		try:
			os.stat(self.source_change_file)
		except:
			return 0
		if open(self.source_change_file,"r").read().strip() == "1":
			return 1
		else:
			return 0
	def backup_sources(self):
		file = self.conf_folder + "/sources_backup.list"
		call = "cp /etc/apt/sources.list %s"%file
		os.system(call)
		os.chown(file,self.uid,-1)
	def restore_sources(self):
		source = "/etc/apt/sources.list"
		tmp = open(source,'r').read()
		if "#ULTAMATIX REPOS START" not in tmp:
			return 0
		final = tmp[0:tmp.find("#ULTAMATIX REPOS START")].strip()+tmp[tmp.find("#ULTAMATIX REPOS END")+len("#ULTAMATIX REPOS END"):len(tmp)].strip()
		open(source,"w").write(final)
	def update_apt(self):
		#will be unecessary, when I am done - TheeMahn
		##run apt-get update...
		import resin_controllers
		#tempunlock = unlock_apt()
		update = resin_controllers.apt_update()
		#relock = exclusive_lock() also will be replaced as soon as I get the rest under control
	def create_pipes(self):
		try:
			os.mkfifo(self.ax_in)
			os.mkfifo(self.ax_out)
		except:
			pass
	def delete_pipes(self):
		try:
			os.unlink(self.ax_in)
			os.unlink(self.ax_out)
		except:
			pass
	def create_conf_folder(self):
		try:
			os.stat(self.conf_folder)
		except:
			try:
				os.mkdir(self.conf_folder)
			except:
				print "Cannot create your configuration folder please check the permissions of your home directory"
				sys.exit()
			os.chown(self.conf_folder,self.uid,-1)
			os.chmod(self.conf_folder,0755)
	def create_installed_log(self):
		self.install_log = self.conf_folder+"/installed"
		try:
			os.stat(self.install_log)
		except:
			open(self.install_log,"w").write("")
			os.chown(self.install_log,self.uid,-1)
	def create_usage_log(self):
		self.usage_log = self.conf_folder+"/user"
		try:
			os.stat(self.usage_log)
		except:
			open(self.usage_log,"w").write("0\n")
			os.chown(self.usage_log,self.uid,-1)
	def set_first_use(self):
		usage = self.get_usage_log()
		usage[0] = "1"
		tmp = open(self.usage_log,"w")
		tmp.write("\n".join(usage))
		tmp.close()
	def get_usage_log(self):
		tmp = open(self.usage_log,"r").readlines()
		tmp2 = []
		for t in tmp:
			tmp2 += [t.strip("\n")]
		return tmp2	
	def get_installed(self):
		tmp = open(self.install_log,"r").readlines()
		tmp2 = []
		for t in tmp:
			if t.strip("\n") != "":
				tmp2 += [t.strip("\n")]
		return tmp2
	def add_installed(self,id):
		tmp = open(self.install_log,"a")
		tmp.write(id+"\n")
		tmp.close()
		return True
	def remove_installed(self,id):
		installed = self.get_installed()
		c=0
		for i in installed:			
			if i == id:
				del installed[c]
				break
			else:
				c+=1
		tmp = open(self.install_log,"w")
		tmp.write("\n".join(installed)+"\n")
		tmp.close()
		return True
	def get_activity(self):
		return open("%s/activity.log"%self.conf_folder,'r').read()
	def get_changelog(self):
		# FIXME! The changelog is going to end up somewhere more sane,
		# and we should get its path using conf_data.xml anyway.
		return open("/usr/share/hypermatix64/changelog",'r').read()

# Distro and path configuration.
class AX_conf:
	def __init__(self):
		import xml_functions as resin
		dist = (os.popen('lsb_release -c | cut -f 2').read())
		print "Distro detected: "+dist
		dom = resin.DOMX()
		dom.load(conf.config_path)
		self.locations = dom.return_dict_with_xpath('/*/locations/*')
		self.images = dom.return_dict_with_xpath('/*/images/*')
		for key in self.images.keys():
			self.images[key] = self.locations['image']+"/"+self.images[key]
		dom = resin.DOMX()
		dom.load(self.locations['clientData']+"/version.xml")
		self.distro = dom.return_dict_with_xpath('/*/distro/*')
		self.version = dom.return_dict_with_xpath('/*/version/*')
		key_dom = resin.DOMX()
		key_dom.load(self.locations['clientData']+"/key_data.xml")
		self.keys = key_dom.xBuild()
		self.apt_sources = self.locations['sources']+"/sources.list"
		catagorys = resin.DOMX()
		catagorys.load(self.locations['clientData']+"/category_data.xml")
		self.catagory = catagorys.xBuild()
		master = open(self.locations["clientData"]+"/init_master").read()+"\n"
		client = ""
		file_li = os.popen("find %s"%self.locations['clientData']+'scripts/'+dist,"r").readlines()
		print "Scripting location:"+self.locations['clientData']+'scripts/'+dist
		for f in file_li:
			f = f.strip()
			print "File: "+f
			check = f[f.rfind(".")+1:len(f)]
			if  check == 'autoscript':
				con = open(f,"r").read()
				client += con+"\n"
		pre = "AXUSER=%s\nAXHOME=%s\nAXPIPEIN=%s\nAXPIPEOUT=%s\n"%(axUser.username,axUser.home,axUser.ax_in,axUser.ax_out)
		self.masterInit = pre+master+client



axUser = AX_user()
axConf = AX_conf()	

