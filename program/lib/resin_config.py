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
# resin_config.py - configuration information

# !!FIXME FIXME FIXME!!
# This file contains a LOT of APT-specific code.
# This should all be cut out of this file and moved to an APT module
# so that we can more easily work with distros which do not use APT.

import sys, os, time, user, platform
import gtk, gtk.glade, gobject, pango
import hyperlocale
import conf, xml_functions
import distro_helpers

def log(statement):
	date = time.strftime('[%d/%m/%Y - %H:%M.%S]')
	open_log = open(log_file,"a")
	open_log.write("{0} - {1}\n".format(date,statement))
	open_log.close()
	return True

def create_log():
	global log_file
	log_file =  "/var/log/hypermatix64_activity.log"
	try:
		os.stat(log_file)
	except:
		open(log_file,'w').write("")
		log(hyperlocale.getLocalisedString("logStarted"))

def sim_log(string):
	open_log = open(log_file,"a")
	open_log.write(string)
	open_log.close()
	return True

def set_source_mode(mode):
	if mode:
		open(source_change_file,"w").write("1")
	else:
		open(source_change_file,"w").write("0")

def get_source_mode():
	try:
		os.stat(source_change_file)
	except:
		return 0
	if open(source_change_file,"r").read().strip() == "1":
		return 1
	else:
		return 0

def create_conf_folder():
	try:
		os.stat(conf_folder)
	except:
		try:
			os.mkdir(conf_folder)
		except:
			message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
			message.set_markup(hyperlocale.getLocalisedString("cannotCreateConfError"))
			message.set_title(hyperlocale.getLocalisedString("productName"))
			message.run()
			sys.exit(1)
		os.chmod(conf_folder,0755)

def create_installed_log():
	global install_log
	install_log = conf_folder + "/installed"
	try:
		os.stat(install_log)
	except:
		open(install_log,"w").write("")

def create_usage_log():
	global usage_log
	usage_log = conf_folder + "/user"
	try:
		os.stat(usage_log)
	except:
		open(usage_log,"w").write("0\n")

def set_first_use():
	usage = get_usage_log()
	usage[0] = "1"
	tmp = open(usage_log,"w")
	tmp.write("\n".join(usage))
	tmp.close()

def get_usage_log():
	tmp = open(usage_log,"r").readlines()
	tmp2 = []
	for t in tmp:
		tmp2.append(t.strip("\n"))
	return tmp2

def get_installed():
	tmp = open(install_log,"r").readlines()
	tmp2 = []
	for t in tmp:
		if t.strip("\n") != "":
			tmp2.append(t.strip("\n"))
	return tmp2

def add_installed(id):
	tmp = open(install_log,"a")
	tmp.write(id + "\n")
	tmp.close()
	return True

def remove_installed(id):
	installed = get_installed()
	c=0
	installed.remove(id)
	tmp = open(install_log,"w")
	tmp.write("\n".join(installed) + "\n")
	tmp.close()
	return True

def get_activity(self):
	return open(self.log_file).read()

conf_folder = "/etc/hypermatix64"
source_change_file = conf_folder + "/sc"

create_conf_folder()
create_usage_log()
create_installed_log()
create_log()

gladeUI = gtk.glade.XML(os.path.join(conf.home, "resin_glade.glade"))
dist = distro_helpers.getDistName()
print(hyperlocale.getLocalisedString("distro") + dist)
dom = xml_functions.DOMX()
dom.load(os.path.join(conf.home, "conf_data.xml"))
locations = dom.return_dict_with_xpath('/*/locations/*')
images = dom.return_dict_with_xpath('/*/images/*')
for key in images.keys():
	self.images[key] = self.locations['image']+"/"+self.images[key]
dom = resin.DOMX()
dom.load(locations['clientData']+"/version.xml")
distro = dom.return_dict_with_xpath('/*/distro/*')
version = dom.return_dict_with_xpath('/*/version/*')
key_dom = resin.DOMX()
key_dom.load(locations['clientData']+"/key_data.xml")
keys = key_dom.xBuild()
apt_sources = locations['sources']+"/sources.list"
catagorys = resin.DOMX()
catagorys.load(locations['clientData']+"/category_data.xml")
catagory = catagorys.xBuild()
master = open(locations["clientData"]+"/init_master").read()+"\n"
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
def get_changelog(self):
	# FIXME! The changelog is going to end up somewhere more sane,
	# and we should get its path using conf_data.xml anyway.
	return open("/usr/share/hypermatix64/changelog",'r').read()
