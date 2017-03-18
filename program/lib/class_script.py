import resin_config, operator, gtk, gobject, conf
class script:
	def __init__(self):
		self.id = ""
		self.title = ""
		self.description = ""
		self.exe = ""
	def __cmp__(self, other):
		return cmp(self.title, other.title)
	def __str__(self):
		return str(self.title)
class script_list:
	def __init__(self):
		self.type = ""
		self.icon = ""
		self.scripts = []
		self.scripts_uninstall = []
	def seperate_scripts(self):
		tmp = []
		for script in self.scripts:
			if script.id not in resin_config.get_installed():
				tmp += [script]
			else:
				self.scripts_uninstall += [script]
		self.scripts = tmp
		self.scripts.sort(key=operator.attrgetter('title'))
		self.scripts_uninstall.sort(key=operator.attrgetter('title'))
	def generate_model(self,state):
		if state == 0:
			selected = self.scripts
			note = ""			
		else:
			selected = self.scripts_uninstall
			note = "<i>(Installed Check to uninstall)</i>"
		self.model = gtk.ListStore(
					gobject.TYPE_BOOLEAN,
					gobject.TYPE_STRING,
					gobject.TYPE_BOOLEAN,
					gobject.TYPE_STRING,
					gobject.TYPE_STRING
					);
		selected.sort()
		for script in selected:
			note = "";
			if script.restricted == "True":
				if conf.restricted:
					rest_color = None
				else:
					rest_color = "grey"
					note+="<i> (Restricted) </i>"
			else:
				if (script.not_strict):
					rest_color = "blue"
					note+="<i> (%s) </i>"%script.desktop
				else:
					rest_color = None
			if script.id in conf.selected_scripts:
				check = True
			else:
				check = False
			desc = "<b>%s</b>\n%s %s"%(script.title,script.description,note)
			new = self.model.append()
			self.model.set(new,
					0,check,
					1,desc,
					2,1,
					3,script.id,
					4,rest_color
					)
		return self.model
