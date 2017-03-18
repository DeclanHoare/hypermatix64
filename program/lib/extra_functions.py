import threading
import xml_functions
import resin_config
import class_script
import gtk, os
import conf
import hyperlocale

class repo_proc:
	def __init__(self,repo_file=None):
		self.repo_file = repo_file	
	def get_current_repo(self):
		out = []
		repo_file =self.repo_file
		repo = open(repo_file,'r').readlines()
		for r in repo:
			r = r[0:r.find("#")]
			if r.strip() !="":
				tmp = r.strip().split(" ")
				new = []
				for t in tmp:
					t = t.strip()
					if t != "":
						new += [t]
				if None not in new:
					if new[1][-1] == "/":
						new[1] = new[1][0:len(new[1])-1]
					#print new[1]
					out += [[" ".join(new[0:3]),new[3:len(new)]]]
		return out
	def add_repo(self,repo):
		"""Needs fixed///TheeMahn"""
		self.add_stamp()
		ore = open(self.repo_file,"r").read()
		ore = ore.split("#ULTAMATIX REPOS START")
		ore[0] += "#ULTAMATIX REPOS START\n\n%s"%repo.strip()
		open(self.repo_file,"w").write("".join(ore))
	def add_stamp(self):
		if "#ULTAMATIX REPOS START" not in open(self.repo_file,"r").read() or "#ULTAMATIX REPOS END" not in open(self.repo_file,"r").read():
			open(self.repo_file,"a").write("\n#ULTAMATIX REPOS START\n#ULTAMATIX REPOS END\n")
	def find_local(self):
		rep = self.get_current_repo()
		for r in rep:
			r = r[0]
			if ("archive.ubuntu.com") in r:
				tmp = r[0:r.find("archive.ubuntu.com")]
				tmp = tmp[tmp.rfind("/")+1:-1]
				if tmp.strip() != "":
					return tmp.strip()
		for r in rep:
			r = r[0]
			if ("debian.org") in r:
				tmp = r[0:r.find("debian.org")]
				tmp = tmp[tmp.rfind("/")+1:-1]
				if (tmp[0:3] == "ftp"):
					tmp = tmp[tmp.rfind("ftp.")+4:]
					if tmp.strip() != "":
						return tmp.strip()
class runScript ( threading.Thread ):
	running = 1
	def run ( self ):
		self.write = ""
		self.running = 1
		self.call = os.popen4(self.script)
		out = self.call[1].read(128)
		while out:
			self.terminal(out)
			out = self.call[1].read(1)
		self.running = 0
#do exact comparison of two source files...
def compare_sources():
	#actually forget this lets just return false...
	return False
	current = repo_proc("/etc/apt/sources.list")
	ax_version = repo_proc(axConf.apt_sources).get_current_repo()
	current_list = current.get_current_repo()
	local = current.find_local()
	if local:
		local +="."
	else:
		local = ""
	for a in ax_version:
		loc = a.replace("%%LOCAL%%",local)
		non = a.replace("%%LOCAL%%","")
		if loc not in current_list and non not in current_list :
			return  False
	return True
#gtk window support
def no_delete(window,event):
	return True
#set the title of a GTK window according to a set standard
def set_title(window,addition=False):
	if addition:
		window.set_title("{0}: {1}".format(hyperlocale.getLocalisedString("productName"), addition))
	else:
		window.set_title(hyperlocale.getLocalisedString("productName"))
#create a pipe and see if anything is returned...
def testOutput(sys_call):
	if(os.popen(sys_call).read()):
		return True
	else:
		return False
#update the main gtk loop...
def update_ui():
	if gtk.events_pending():
		while gtk.events_pending():
					gtk.main_iteration(False)
#get list of XML files...
def get_script_xml_files():
# Possibly extensible.
# Currently just returns script_data.xml in a list, but maybe it will
# need to return a distro-specific file for repositories in the future.
	return [os.path.join(resin_config.locations["clientData"], "script_data.xml")]
#start building scripts
def buildScripts():
	conf.script_list = []
	for script in get_script_xml_files():
		build = buildScript(script)
	cleanup_installed()
#return a list of all available scripts (id only)
def get_all_scripts():
	out = []
	for list in conf.script_list:
		for script in list.scripts:
			out+=[script.id]
		for script in list.scripts_uninstall:
			out+=[script.id]
	return out
#return a script object according to its id.
def get_script(id):
	out = []
	for list in conf.script_list:
		for script in list.scripts:
			out+=[script]
		for script in list.scripts_uninstall:
			out+=[script]
	for o in out:
		if o.id == id:
			return o
	return False
#determined if installed AX scripts are still supported by the AX team
def cleanup_installed():
	installed = resin_config.get_installed()
	all = get_all_scripts()
	for i in installed:
		if i not in all:
			axUser.remove_installed(i)
#parse the script info	
def buildScript(search_script):
		xml = xml_functions.DOMX()
		xml.load(search_script)
		conf.script_data = xml.xBuild()
		for scr in conf.script_data:
			if scr['type'] not in conf.catalog:
				conf.catalog += [scr['type']]
		conf.catalog.sort()
		conf.catalog.reverse()
		for cat_type in conf.catalog:
			conf_data = None
			new_list=None
			c = 0
			for prev in conf.script_list:
				if prev.type == cat_type:
					new_list = prev
					sw = 1
					break_end = c
					break
				c+=1
			if not new_list:
				sw = 0	
				new_list = class_script.script_list()
				new_list.type = cat_type
				new_list.scripts = []
				for cat in resin_config.catagory:
					if cat['name'].lower() == new_list.type.lower():
						conf_data = cat
						break
				if conf_data:
					if conf_data['icon'] != "None" and conf_data['icon'] != None:
							new_list.icon = conf_data['icon']
					else:
						new_list.icon = resin_config.locations['image']+'/window.png'
					if conf_data['summary'] != "None" and conf_data['summary'] != None:
							new_list.summary = conf_data['summary']
					else:
						new_list.summary = ""
					if 'info' in conf_data.keys():
							new_list.info = conf_data['info']
					else:
						new_list.info = ""
				else:
					new_list.icon = resin_config.locations['image']+'/window.png'
					new_list.summary = ""		
			for script_dict in conf.script_data: 
				new = class_script.script()
				try:
					final = []
					desktop = script_dict['desktop']
					if "," in desktop:
						desktop = desktop.split(",")
						for d in desktop:
							final += [d.strip()]
					else:
						final = [desktop.strip()]
					desktop = final
				except:
					desktop = ['any']
				desk_sw = 0
				for d in desktop:
					if d in conf.desktop:
						desk_sw = 1
						if d != 'any' and d != conf.strict_desktop:
							not_strict = 1
						else:
							not_strict = 0
						break
				if script_dict['type'] == new_list.type and desk_sw == 1:
					new = class_script.script()
					new.id = script_dict['id']
					new.title = script_dict['title']
					new.description = script_dict['description']
					new.exe = script_dict['exec'].strip()
					try:
						new.uninstall = script_dict['uninstall'].strip()
					except:
					 	new.uninstall = None
					try:
						new.info = script_dict['info']
					except:
					 	new.info = None
					try:
						new.version = script_dict['version']
					except:
					 	new.version = None
					try:
						new.pre_info = script_dict['preinfo']
					except:
					 	new.pre_info = None
					try:
						new.post_info = script_dict['postinfo']
					except:
					 	new.post_info = None
					try:
						new.restricted = script_dict['restricted']
					except:
					 	new.restricted = None
					try:
						new.depends = script_dict['depends']
					except:
					 	new.depends = None
					if not_strict:
						new.not_strict = 1
						new.desktop =desktop[0];
					else:
						new.not_strict = 0
						new.desktop = "";
					new_list.scripts[0:0]= [new]
					new =""
			if sw == 0:
				new_list.seperate_scripts()
				conf.script_list[0:0] = [new_list]
			else:
				new_list.seperate_scripts()
				conf.script_list[break_end] = new_list
