# Copyright 2006-2008 (?) Automatix Team
# Copyright 2010 (?) TheeMahn
# Copyright 2016, 2017 Declan Hoare
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
# main_interface.py

import copy
import resin_config
import resin_ui
import distro_helpers
import extra_functions
import resin_controllers
import threading
import gtk, gobject
import conf
import traceback

class main_ui:
	def __init__(self):
		self.build_interface()
		self.term = False
	def build_interface(self):
		self.saved_cat = ['0','0']
		self.current_cat = None
		self.saved_page = None
		self.type_state = 0
		self.menu_options = []
		self.main_window = resin_ui.main_interface()
		usage = resin_config.get_usage_log()
		self.main_window.menu_restore.connect("activate",self.restore_sources)
		self.main_window.menu_about.connect("activate",self.main_window.show_about)
		self.main_window.menu_licence.connect("activate",self.licence_info)
		self.main_window.menu_credits.connect("activate",self.credits_info)
		self.main_window.menu_errors_and_information.connect("activate",self.show_errorbox)
		self.main_window.window.connect("destroy", resin_controllers.exit_routine)
		self.main_window.window.connect("delete-event", resin_controllers.no_destroy)
		self.main_window.menu_quit.connect("activate", resin_controllers.exit_routine)
		self.main_window.window.set_icon_from_file(resin_config.images['windowIcon'])
		extra_functions.set_title(self.main_window.window)
		self.main_window.about.window.hide()

		self.generate_menu_columns()
		self.generate_catalog_columns()		
		self.main_window.start_button.connect("clicked",self.start_exec)
		self.main_window.toggle_apps.connect("clicked",self.do_toggle_apps)
		self.main_window.catalog_tree.connect("cursor-changed",self.catalog_change)
		self.main_window.catalog_tree_page2.connect("cursor-changed",self.catalog_change)
		self.switch_handler = self.main_window.notebook.connect("switch-page",self.switch_type_page)
		conf.need_generate = 1
		self.generate_menus()
		self.check_notebook()
		extra_functions.update_ui()
		self.error_box = resin_ui.error_report()
		self.textviewer = resin_ui.textviewer()
		"""self.main.window.menu_keep_debs.connect("activate",self.keep_debs)##added"""
		self.main_window.menu_view_help.connect("activate",self.view_help)
		self.main_window.menu_view_activity_log1.connect("activate",self.show_activity)
		self.main_window.menu_view_sources.connect("activate",self.show_sources)
		self.main_window.menu_view_changelog.connect("activate",self.show_changelog)
		self.app_switch = 0;
		self.write_info_html('<h1>Welcome to <a href="http://home.exetel.com.au/declanhoare/hypermatix64">Hypermatix64</a>.</h1><p>Choose a category from the left-hand side to see what you can install. Check the box for each item you want to install, then click Start to install them.</p><p>To uninstall an item, click the Uninstall tab, check the box for each item you want to uninstall, then click Start to uninstall them.</p>')
	def do_toggle_apps(self,signal):
		if (self.app_switch == 0):
			conf.desktop += [conf.other_desktop]
			self.app_switch = 1;
			self.main_window.toggle_icon.set_from_file(conf.toggle_icons[1])
			self.main_window.toggle_apps.set_label("Select all");
		else:
			conf.desktop = conf.desktop[0:-1];
			self.main_window.toggle_icon.set_from_file(conf.toggle_icons[0])
			self.main_window.toggle_apps.set_label("Deselect all");
			self.app_switch = 0;
		buildScripts()
		self.generate_menus()
		self.check_notebook()
		self.set_menu(self.menu_options[0])
		try:
			self.set_menu(self.current_catagory)
		except:
			traceback.print_exc()
		extra_functions.update_ui()
		#self.main_window.window.show_all()
	def show_errorbox(self,signal):
		self.error_box.window.show()
	def show_activity(self,signal):
		self.textviewer.set_text(resin_config.get_activity())
		self.textviewer.window.show_all()
		#added via theemahn
	def view_help(self,signal):
		self.textviewer.set_text(open('/usr/share/ultamatix/README','r').read())
		self.textviewer.window.show_all()
	def show_changelog(self,signal):
		self.textviewer.set_text(resin_config.get_changelog())
		self.textviewer.window.show_all()
	def show_sources(self,signal):
		self.textviewer.set_text(open('/etc/apt/sources.list','r').read())
		self.textviewer.window.show_all()
	def licence_info(self,widget):
		qu = ask_info_question(resin_config.version['licence'].strip(),"",None,True)
		qu[1].window.hide()
	def credits_info(self,widget):
		qu = ask_info_question(resin_config.version['credits'].strip(),"",None,True)
		qu[1].window.hide()
	def write_info_html(self,info):
		self.main_window.info_html.load_html_string("<html><head></head><body>%s</body></html>"%info,"about:blank")
	def restore_sources(self,item):
		quest = ask_question("Would you like to remove Ultimate Edition repositiories from your source list?")
		if quest[0]:
			resin_config.restore_sources()
			quest[1].window.hide()
			self.main_window.window.hide()
			resin_config.update_apt()
			conf.trayIcon.destroy()
			alert("<b>Your sources have been updated.</b> \nUltamatix will now exit",sys.exit)
		else:
			quest[1].window.hide()		
	def generate_menus(self):
		if conf.need_generate:
			extra_functions.buildScripts()
			conf.need_generate = 0
		self.generate_catalog_model()
		self.main_window.catalog_tree.set_model(self.catalog_model)
		self.main_window.catalog_tree_page2.set_model(self.catalog_model)
		if not self.current_cat:
			self.set_menu(self.menu_options[0])
	def check_notebook(self):
		if len(resin_config.get_installed()) == 0:
			self.main_window.notebook.set_current_page(0)
			if self.saved_page == None:
				self.saved_page = self.main_window.notebook.get_nth_page(1)
			self.main_window.notebook.remove_page(1)
			extra_functions.update_ui()
		else:
			if self.saved_page != None:
				self.main_window.notebook.append_page(self.saved_page,gtk.Label("Uninstall"))
				self.saved_page = None
				self.main_window.notebook.set_current_page(0)
				return True
			self.main_window.page2_label.set_text("Uninstall")
			self.uni_mode = 1
			extra_functions.update_ui()
	def catalog_change(self,tree):
		model = tree.get_model()
		row = tree.get_cursor()[0][0]
		self.current_cat = row
		row = model.get_iter_from_string("%s"%row)
		catagory = model.get(row,0)[0]
		self.current_catagory = catagory;
		self.set_menu(catagory)
	def	switch_type_page(self,button,page,number):
		prestate = self.type_state
		tmp = self.current_cat
		if self.type_state == 0 and resin_config.get_installed() != []:
			self.type_state = 1
			tree = self.main_window.catalog_tree_page2
		else:
			self.type_state = 0
			tree = self.main_window.catalog_tree
		if self.main_window.notebook.get_current_page() == 1:
			self.type_state = 0
			tree = self.main_window.catalog_tree
		self.generate_menus()
		tree.set_cursor(self.saved_cat[self.type_state] )
		self.saved_cat[prestate] = tmp
		extra_functions.update_ui()
	def cancel_term(self,button):
		self.stop = True
		alert2 = deepcopy(alert)
		note = alert2("<b>Cancelling...</b>\nPlease wait one moment while Hypermatix64 finishes the current script.",None,self.term.terminal.window)
		del alert2
		try:
			self.term.thread.run = 1
		except:
			traceback.print_exc()
	def keep_debs(self,item):
		alert("<b>This feature has not yet been implemented.</b>",None,self.main_window.window)	# attempt in -7
	def start_exec(self,button):
		#check for conflicts before running installs...
		conflicts = checkConflicts();
		#report conflicts if any...
		#Unlock apt - will cease to exist in -7
		
		if conflicts:
			alert("<b>Hypermatix64 cannot continue because %s is running.</b> \nPlease shut down %s and try again."%(conflicts[0],conflicts[0]))
			return False
		self.stop = False
		if len(conf.selected_scripts) == 0:
			alert("<b>No scripts have been selected</b>",None,self.main_window.window)
			return False
		##############################################################################
		#create a terminal window to run in...
		try:
			if not self.term:
				self.term = activity_terminal()
				self.term.terminal.cancel.connect("clicked",self.cancel_term)
		except:
				alert("<b>EXCEPTION: </b>" + traceback.format_exc())
				return False
				#self.term = activity_terminal()
				#self.term.terminal.cancel.connect("clicked",self.cancel_term)
		#conf.trayIcon.set_window(self.term.terminal.window)
		#create some pipes to read and write to...
		resin_config.create_pipes()
		#hide the main window...
		self.main_window.window.hide()
		
		#show the terminal window...
		self.term.terminal.window.show()
		pre = self.term.terminal.label.get_label()
		c = 1.0000000
		#clear deselectors...
		conf.deselector = []
		deselect = []
		#gather selected...
		selected = conf.selected_scripts
		uninstall = []
		install = []
		#divide up selected scripts...
		for sc in selected:
			if sc in resin_config.get_installed():
				uninstall += [sc]
			else:
				install += [sc]
			s_data = get_script(sc)
			if s_data.depends:
				if not s_data.depends in resin_config.get_installed():
					if not s_data.depends in install:
						install = [s_data.depends] + install # put dependencies first
				if s_data.depends in uninstall:
					uninstall.remove(s_data.depends) # don't uninstall something you need
		selected = uninstall + install
		#okay now we run them...
		#lock apt
		#exclusive = apt_unlock(), depriciates in -7
		try:
				apt_pkg.pkgsystem_unlock()
		except apt_pkg.Error:
			traceback.print_exc() # Silent exception handling is the spawn of Satan.
		except Exception as Argument:
				alert("<b>EXCEPTION: </b>" + traceback.format_exc())
				return False
		for sc in selected:
			if sc not in conf.deselector:
				#get the information on the script
				s_data = get_script(sc)
				#set what script is being run in conf
				conf.current_executing = sc
				#setup watch man...
				watchman = watch_pipe()
				watchman.function = alert
				watchman.window = self.main_window.window
				watchman.start()
				#create percent done info for info area...
				curr = c/len(conf.selected_scripts)
				self.term.terminal.progress.set_fraction(curr)
				c+=1
				#okay now determine what exec script should be run (install or uninstall)
				if sc in uninstall and sc not in conf.dep_uninstalled:
					state = "Uninstalling "
					if s_data.uninstall:
						exe = s_data.uninstall
					else:
						exe = "echo 'Does not have an uninstall routine'\nAX_warning 'Does not have an uninstall routine, please remove manually'\n "
				elif sc in install and sc not in conf.dep_installed:
					state = "Installing "
					exe = s_data.exe
				extra_functions.update_ui()
				self.term.terminal.progress.set_text(state+s_data.title)
				#conf.trayIcon.set_label(state+s_data.title)
				#now we put it all together and send it to bash...
				send = "#!/bin/bash\n%s\n%s\necho 'Finished'\nsleep 1\n"%(resin_config.masterInit,exe)
				auto = resin_config.conf_folder+"/ax.autoscript"
				open(resin_config.conf_folder+"/ax.autoscript","w").write(send)
				os.chmod(auto,777)
				self.term.connect_pipe(auto)
				#finished now we cancel the watchman
				watchman.watch = False
				open(resin_config.ax_in,"w").write("die")
				#and delete the script we made
				os.unlink(auto)
				del watchman
				#log the output of that script
				resin_config.log("!!SCRIPT OUTPUT START!!\n%s\n!!SCRIPT OUTPUT END!!"%self.term.logged)	
				#determine if the install failed...
				fail = 0
				for fi in conf.failed:
					if fi == sc:
						fail=1
						break
				#do stuff if we didn't fail
				if fail != 1:
					deselect += [sc]
					curscript = get_script(sc)			
					if sc in uninstall:
						resin_config.remove_installed(sc)
						if curscript.post_info:
							conf.script_errors += [[2,curscript.id,curscript.post_info]]
					else:
						resin_config.add_installed(sc)
						if curscript.pre_info:
							conf.script_errors += [[2,curscript.id,curscript.pre_info]]
						#I think this part is deprecated...
						"""
						if curscript.depends:
							depends = []
							if "," in curscript.depends:
								tmp = curscript.depends.split(",")
								for t in tmp:
									depends += [t.strip()]
							else:
								depends += [curscript.depends.strip()]
							for d in depends:
								if d not in resin_config.get_installed():
									resin_config.add_installed(d)
								dep = get_script(d)
								if dep.pre_info:
									conf.script_errors += [[2,dep.id,dep.pre_info]]
						"""
				if conf.dep_installed:
					for d in conf.dep_installed:
						if d not in resin_config.get_installed():
							resin_config.add_installed(d)
						dep = get_script(d)
						if dep.pre_info:
							conf.script_errors += [[2,dep.id,dep.pre_info]]
					conf.dep_installed=[]
				if conf.dep_uninstalled:
					for d in conf.dep_uninstalled:
						if d in resin_config.get_installed():
							resin_config.remove_installed(d)
						dep = get_script(d)
						if dep.post_info:
							conf.script_errors += [[2,dep.id,dep.pre_info]]
					conf.dep_uninstalled=[]	
				if self.stop == True:
					break
			else:
				deselect += [sc]
		for d in deselect:
			k = 0
			for select in conf.selected_scripts:
				if d == select:
					del conf.selected_scripts[k]
				k+=1
		conf.need_generate = 1
		if resin_config.get_installed() == []:
			self.type_state = 0
		for failedScript in conf.failed:
			alert("<b>" + failedScript + " encountered a fatal error:</b> " + conf.failmessages[failedScript])
		conf.failed = []
		self.generate_menus()
		self.check_notebook()
		self.term.terminal.window.hide()
		self.set_menu(self.menu_options[0])
		self.main_window.window.show()
		conf.trayIcon.set_window(self.main_window.window)
		conf.trayIcon.set_label("Ultamatix")
		extra_functions.update_ui()
		# now do some error roeporting
		if conf.script_errors:
			print "ERRORS OR WARNINGS WHERE REPORTED"
			resin_config.log("ERRORS OR WARNINGS WHERE REPORTED")
			print "-"*50
			print "-"*50
			for e in conf.script_errors:
				print "%s - %s"%(e[0],e[2])
				print "-"*35
				es = get_script(e[1])
				sc_name = es.title
				errors = ('WARNING','FATAL','INFO')
				resin_config.log("%s - %s - %s"%(errors[int(e[0])],sc_name,e[2].strip()))
			self.error_box.generate_model(conf.script_errors)
			self.error_box.window.show()
		conf.script_errors = []
		resin_config.delete_pipes()
		#self.activity_log.set_text(resin_config.get_activity())
	def generate_catalog_model(self):
		self.catalog_model = gtk.ListStore(
					gobject.TYPE_STRING,gobject.TYPE_INT,gtk.gdk.Pixbuf,gobject.TYPE_STRING				
					);
		for list in conf.script_list:
			icon= gtk.gdk.pixbuf_new_from_file(list.icon.format(resin_config.locations["image"]))
			if self.type_state == 0:
				check = list.scripts
			else:
				check = list.scripts_uninstall
			if len(check) > 0:
				self.menu_options += [list.type]
				new = self.catalog_model.append()
				self.catalog_model.set(new,
						0,list.type,
						1,12,
						2,icon,
						3,"<b>%s</b>"%list.type
						)
	def generate_catalog_columns(self):
		tree = self.main_window.catalog_tree
		column = gtk.TreeViewColumn(None, gtk.CellRendererPixbuf(),
									pixbuf=2)
		tree.append_column(column)
		column = gtk.TreeViewColumn(None, gtk.CellRendererText(),markup=3)
		tree.append_column(column)
		tree = self.main_window.catalog_tree_page2
		column = gtk.TreeViewColumn(None, gtk.CellRendererPixbuf(),
									pixbuf=2)
		tree.append_column(column)
		column = gtk.TreeViewColumn(None, gtk.CellRendererText(),markup=3)
		tree.append_column(column)
	def generate_menu_columns(self):
		tree = self.main_window.menu_tree
		model = tree.get_model()
		renderer = gtk.CellRendererToggle()
		renderer.connect('toggled', self.fixed_toggled)
		column = gtk.TreeViewColumn(None, renderer, active=0)
		tree.append_column(column)
		cellrend = gtk.CellRendererText()
		column = gtk.TreeViewColumn(None,cellrend ,markup=1,foreground=4)
		tree.append_column(column)
		tree = self.main_window.menu_tree_page2
		model = tree.get_model()
		renderer = gtk.CellRendererToggle()
		renderer.connect('toggled', self.fixed_toggled)
		column = gtk.TreeViewColumn(None, renderer, active=0)
		tree.append_column(column)
		column = gtk.TreeViewColumn(None, gtk.CellRendererText(),markup=1,foreground=4)
		tree.append_column(column)
	def set_menu(self,catagory):
		for list in conf.script_list:
			if list.type == catagory:
				self.main_window.status_bar.push(214324,"(%s installed / %s available)"%(len(list.scripts_uninstall),len(list.scripts)+len(list.scripts_uninstall)))
				new_model = list.generate_model(self.type_state)
				self.main_window.menu_tree.set_model(new_model)
				self.main_window.menu_tree_page2.set_model(new_model)
				self.main_window.menu_tree.connect("cursor-changed",self.updateScriptInfo)
				self.main_window.menu_tree_page2.connect("cursor-changed",self.updateScriptInfo)
				self.write_info_html("<h1>%s</h1>%s"%(catagory,list.info));
	def updateScriptInfo(self,tree):
		model = tree.get_model()
		row = tree.get_cursor()[0][0]
		row = model.get_iter_from_string("%s"%row)
		script = model.get(row,3)[0]
		script = extra_functions.get_script(script)
		if (script.info):
			info = script.info
		else:
			info = script.description
		if (script.version):
			ver = "<h3><i>Version: %s</i></h3>"%script.version
		else:
			ver = ""
		self.write_info_html("<h2>%s</h2>%s<p>%s</p>"%(script.title,ver,info))
	def fixed_toggled(self, cell, path):
		models = [self.main_window.menu_tree.get_model(), self.main_window.menu_tree_page2.get_model()]
		model = models[self.main_window.notebook.get_current_page()]
		it = model.get_iter(path)
		if conf.restricted == 0:
			script = get_script(model.get_value(it,3))
			if script.restricted == "True":
				return False
		# get toggled iter
		iter = model.get_iter((int(path),))
		fixed = model.get_value(iter, 0)
		# do something with the value
		fixed = not fixed
		# set new value
		model.set(iter, 0, fixed)
		if model.get_value(it,0):
			conf.selected_scripts += [model.get_value(it,3)]
		else:
			c = 0 
			for ss in conf.selected_scripts:
				if ss == model.get_value(it,3):
					del conf.selected_scripts[c]
					break
				c+=1
class watch_pipe( threading.Thread ):
	def new_winder(self,question):
		gladeUI = conf.gladeUI #get glade interface
		gladeUI.signal_autoconnect(self)
		self.window = gladeUI.get_widget("watch_question")
		label = gladeUI.get_widget("question_label")
		label.set_markup(question)
		yes = gladeUI.get_widget("q_yes")
		no = gladeUI.get_widget("q_no")
		self.window.connect("delete-event",self.no_delete)
		yes.connect("clicked",self.button_no_clicked)
		no.connect("clicked",self.button_yes_clicked)
		set_title(self.window,"Question")
		self.window.set_icon_from_file(resin_config.images["windowIcon"])
		self.window.show_all()
	def no_delete(self,window,event):
		return True
	def button_yes_clicked(self,button):
		self.window.hide()
		self.quest_answer = 0
		self.answer = False
	def button_no_clicked(self,button):
		self.window.hide()
		self.quest_answer = 1
		self.answer = False
	def run( self ):
		self.alert = alert
		self.watch = True
		while self.watch == True:
			check = open(resin_config.ax_in,"r")
			check = check.read()
			if "QUESTION::" in check:
				check = check[len("QUESTION::"):len(check)]
				self.new_winder("<b>%s</b>"%check)
				self.answer = True
				while self.answer:
					extra_functions.update_ui()
				test = self.quest_answer
				open(resin_config.ax_out,"w").write("%s"%test)
			if "ALERT::" in check:
				check = check[len("ALERT::"):len(check)]
				alert("<b>%s</b>"%check)
				open(resin_config.ax_out,"w").write("Finished")
			if "WARNING::" in check:
				print "%s reported the warning: %s"%(conf.current_executing,check[len("WARNING::"):len(check)])
				conf.script_errors += [[0,conf.current_executing,check[len("WARNING::"):len(check)]]]
				open(resin_config.ax_out,"w").write("received \n")
			if "INFORMATION::" in check:
				print "%s reported the info: %s"%(conf.current_executing,check[len("INFORMATION::"):len(check)])
				conf.script_errors += [[2,conf.current_executing,check[len("INFORMATION::"):len(check)]]]
				open(resin_config.ax_out,"w").write("received \n")
			if "FATAL::" in check:
				print "%s encountered a fatal error: %s"%(conf.current_executing,check[len("FATAL::"):len(check)])
				conf.failed += [conf.current_executing]
				conf.failmessages[conf.current_executing] = check[len("FATAL::"):len(check)]
				conf.script_errors += [[1,conf.current_executing,check[len("FATAL::"):len(check)]]]
				open(resin_config.ax_out,"w").write("received \n")
			#this part still needs work...	
			if "ADDREPO::" in check:
				repo = check[len("ADDREPO::"):len(check)]
				if ("\n" in repo):
					r = repo.split("\n")
					repo = r[0]
				current = repo_proc("/etc/apt/sources.list")
				if repo.strip() not in open("/etc/apt/sources.list").read():
					current.add_repo(repo.strip())
				open(resin_config.ax_out,"w").write("received \n")							
			if "INSTALLED::" in check:
				info = check[len("INSTALLED::"):len(check)].strip()
				print "%s reported the install of script: %s"%(conf.current_executing,check[len("INSTALLED::"):len(check)])
				if "," in info:
					info = info.split(",")
					conf.dep_installed += info
					conf.deselector += info
					for i in info:
						resin_config.add_installed(info)
				else:
					conf.dep_installed += [info]
					conf.deselector += [info]
					resin_config.add_installed(info)
				open(resin_config.ax_out,"w").write("received \n")
			if "REMOVE::" in check:
				info = check[len("REMOVE::"):len(check)].strip()
				print "%s reported the uninstall of script: %s"%(conf.current_executing,check[len("REMOVE::"):len(check)])
				if "," in info:
					info = info.split(",")
					conf.dep_uninstalled += info
					conf.deselector = info
					for i in info:
						resin_config.remove_installed(i)
				else:
					conf.dep_uninstalled += [info]
					conf.deselector += [info]
					resin_config.remove_installed(info)
				open(resin_config.ax_out,"w").write("received \n")
			if "DROPDOWN::" in check:
				print check
				title = check[len("DROPDOWN::"):check.find("OPTIONS::")]
				options = check[check.find("OPTIONS::")+len("OPTIONS::"):]
				options = options.split(",")
				drop = dropdown_window()
				drop.set_options(options)
				drop.label.set_markup("<b>%s</b>"%title)
				drop.window.show_all()
				while drop.up:
					extra_functions.update_ui()
				drop.window.hide()
				if (drop.leaf):
					active = drop.menu.get_active()
					val = drop.model[active][0]
					open(resin_config.ax_out,"w").write(val)
				else:
					open(resin_config.ax_out,"w").write("AX:FALSE")
#def unlock_apt():
#        """unlock here to make sure that lock/unlock are always run pair-wise (and don't explode on errors)"""
#        try:
#            apt_pkg.PkgSystemUnLock()
#        except SystemError:
#            print "WARNING: trying to unlock a not-locked PkgSystem"
#            pass
