from extra_functions import *
from resin_config import *
import sys,os,time,user
import gtk, gtk.glade
from gtk import gdk
import gobject
import pango 
import threading
import time
from copy import *
import vte
import webkit
import tray
class main_interface:
	def __init__(self):
		self.about=AX_About()
		gladeUI = conf.gladeUI
		gladeUI.signal_autoconnect(self)
		self.window = gladeUI.get_widget("main_interface")
		self.catalog_tree = gladeUI.get_widget("catalog_tree")
		self.menu_tree = gladeUI.get_widget("menu_tree")
		self.catalog_tree_page2 = gladeUI.get_widget("catalog_tree_page2")
		self.menu_tree_page2 = gladeUI.get_widget("menu_tree_page2")
		self.status_bar = gladeUI.get_widget("statusbar1")
		self.menu_quit = gladeUI.get_widget("quit1")
		self.menu_about = gladeUI.get_widget("about_automatix2")
		self.menu_licence = gladeUI.get_widget("licence_info")
		self.menu_credits = gladeUI.get_widget("menu_credits")
		self.menu_restore = gladeUI.get_widget("restore_sources")
		self.menu_keep_debs = gladeUI.get_widget("keep_debs")
		self.menu_view_help = gladeUI.get_widget("view_help")
		self.menu_view_activity_log1 = gladeUI.get_widget("view_activity_log1")
		self.menu_view_sources = gladeUI.get_widget("sources")
		self.menu_view_changelog = gladeUI.get_widget("change_log")
		self.menu_errors_and_information = gladeUI.get_widget("errors_and_information1")
		self.start_button = gladeUI.get_widget("start_scripts")
		self.notebook = gladeUI.get_widget("notebook1")
		self.page2_label = gladeUI.get_widget("page2_label")
		#do some stuff to the toolbar...
		self.toolbar = gladeUI.get_widget("toolbar1")
		self.toggle_apps =  gladeUI.get_widget("toggle-apps")
		self.toggle_icon = gtk.Image()
		self.toggle_icon.set_from_file(conf.toggle_icons[0])
		self.toggle_apps.set_icon_widget(self.toggle_icon);
		self.toggle_apps.set_label("Deselect all")
		self.show_apps =  gladeUI.get_widget("showButton")
		self.view_menu =  gladeUI.get_widget("view1_menu")
		self.show_apps.connect("clicked",lambda signal:self.show_apps.get_menu().popup());
		self.showIcon = gtk.Image()
		self.showIcon.set_from_file("/usr/share/ultamatix/pixmaps/view_icon.png")
		self.show_apps.set_icon_widget(self.showIcon);
		self.show_apps.set_menu(self.view_menu);
		self.info_holder =  gladeUI.get_widget("infoholder")
		self.info_html = webkit.WebView()
		self.info_html.load_html_string("<html><head></head><body></body></html>", "about:blank")
		self.info_holder.add(self.info_html)
		conf.trayIcon = self.makeTrayIcon(self.window)
		update_ui();
		self.window.set_role("MAIN_WINDOW")
		self.window.show_all()
	def makeTrayIcon(self,who):
			self.icony = tray.TrayIcon(who)
			#self.icony.myTip.set_tip(self.icony.icon, "Ultamatix")
			return self.icony
	def link_clicked(self,doc,url):
		if conf.strict_desktop != "KDE":
			os.system("su %s $(gconftool-2 -g /desktop/gnome/applications/browser/exec) %s &"%(axUser.username,url))
		else:
			os.system("su %s konqueror %s &"%(axUser.username,url))
	def show_about(self,item):
		self.about.window.show()
class textviewer:
	def __init__(self):
		gladeUI = conf.gladeUI
		gladeUI.signal_autoconnect(self)
		self.window = gladeUI.get_widget("textview")
		self.window.connect("delete-event",self.window.hide_on_delete)
		self.textview = gladeUI.get_widget("text_text")
		self.textbuffer = gtk.TextBuffer()
		self.textview.set_buffer(self.textbuffer)
		self.window.set_icon_from_file(axConf.images["windowIcon"])
		self.window.set_title(axConf.version['name'])
	def set_text(self,text):
		self.textbuffer.set_text(text)
		self.textbuffer.place_cursor(self.textbuffer.get_end_iter())
		update_ui()
	def hide():
		self.window.hide()
class term_status_window:
	def __init__(self):
		gladeUI = conf.gladeUI #get glade interface
		gladeUI.signal_autoconnect(self)
		self.window = gladeUI.get_widget("term_status")
		self.terminal = gladeUI.get_widget("ts_terminal")
		self.label = gladeUI.get_widget("ts_label")
		self.cancel = gladeUI.get_widget("term_cancel")
		self.vbox = gladeUI.get_widget("term_holder")
		self.prog_holder = gladeUI.get_widget("term_prog_holder")
		self.progress = gtk.ProgressBar()
		self.progress.set_size_request(-1,24)
		self.prog_holder.set_size_request(-1,24)
		self.prog_holder.pack_start(self.progress)
		self.progress.pulse()
		update_ui()
		self.progress.set_text("Initializing script")
		self.vte_terminal = vte.Terminal()
		self.vte_terminal.set_encoding("UTF-8")
		self.vte_terminal.set_font_from_string ('monospace')
		self.vte_terminal.set_color_dim(gtk.gdk.color_parse("white"))
		self.vte_terminal.set_color_foreground(gtk.gdk.color_parse("white"))
		self.vte_terminal.set_color_background(gtk.gdk.color_parse("black"))
		self.vte_terminal.set_cursor_blinks(True)
		self.vbox.pack_end(self.vte_terminal)
		self.vbox.show_all()
		update_ui()
		self.label.set_text("<span size='x-large'><b>Setting Up and Running Scripts</b></span>\n\nPlease Wait")
		self.label.set_use_markup(True)
		self.window.connect("delete-event",no_delete)
		self.window.set_icon_from_file(axConf.images["windowIcon"])
		self.window.set_title(axConf.version['name'])
		self.vte_terminal.grab_focus()
class AX_About:
	def __init__(self):
		gladeUI = conf.gladeUI #get glade interface
		gladeUI.signal_autoconnect(self)
		logo = gtk.gdk.pixbuf_new_from_file(axConf.images['aboutSplash'])
		self.window = gladeUI.get_widget('AX_about')
		self.window.set_modal(True)
		self.label = gladeUI.get_widget('about_label')
		self.logo_area = gladeUI.get_widget('AX_image')
		self.logo_area.set_from_pixbuf(logo)
		self.okay = gladeUI.get_widget('AX_about_ok_button')
		self.okay.connect("clicked",self.hide)
		self.window.set_icon_from_file(axConf.images['windowIcon'])
		set_title(self.window,"About")
		self.window.connect("delete-event",no_delete)
		self.label.set_text("<span size='x-large'><b>%s %s</b></span>\n%s"%(axConf.version['name'],axConf.version['number'],axConf.version['about']))
		self.label.set_use_markup(True)
	def hide(self,button):
		self.window.hide()
class splash:
	def __init__(self):
		gladeUI = conf.gladeUI #get glade interface
		gladeUI.signal_autoconnect(self)
		logo = gtk.gdk.pixbuf_new_from_file(axConf.images['splash'])
		image = gtk.Image()
		image.set_from_pixbuf(logo)
		vbox = gladeUI.get_widget('image_holder')
		vbox.pack_end(image)
		self.prog = gtk.ProgressBar()
		self.prog.set_fraction(0)
		self.prog.set_size_request(-1, 1)
		self.prog.set_text("starting up...")
		vbox2 = gladeUI.get_widget('prog_holder')
		vbox2.pack_end(self.prog)
		self.window = gladeUI.get_widget('splash')
		self.window.show_all()
class alert(object):
	def __init__(self,message=None,handler=None,window=None,width=None,height=None):
		self.handler = handler
		gladeUI = conf.gladeUI
		gladeUI.signal_autoconnect(self)
		self.window = gladeUI.get_widget('alert')
		if width and height:
			self.window.resize(width,height)
		label = gladeUI.get_widget('alert_label')
		label.set_text(message)
		label.set_use_markup(True)
		set_title(self.window,"Alert!")
		self.window.connect("delete-event",no_delete)
		self.window.set_modal(True)
		self.window.show()
		if window:
			self.window.set_transient_for(window)
		self.up = 1
		if self.handler == None:
			self.handler = self.window.hide
		while self.up:
			time.sleep(.1)
			update_ui()
	def on_die_button_clicked(self,signal):
		self.up = 0
		return self.handler()
class question:
	def __init__(self,question,window):
		self.wait = 1
		self.input = None
		gladeUI = conf.gladeUI
		gladeUI.signal_autoconnect(self)
		self.window = gladeUI.get_widget("watch_question")
		label = gladeUI.get_widget("question_label")
		label.set_markup(question)
		label.set_line_wrap(1)
		yes = gladeUI.get_widget("q_yes")
		no = gladeUI.get_widget("q_no")
		self.window.connect("delete-event",no_delete)
		yes.connect("clicked",self.button_yes_clicked)
		no.connect("clicked",self.button_no_clicked)
		set_title(self.window,"Question")
		self.window.set_modal(True)
		self.window.set_transient_for(window)
		self.window.set_icon_from_file(axConf.images["windowIcon"])
		self.window.show_all()
	def button_no_clicked(self,button):
		self.wait = 0
		self.input = 0
	def button_yes_clicked(self,button):
		self.wait = 0
		self.input = 1
class quick_terminal_window:
	def __init__(self):
		gladeUI = conf.gladeUI
		gladeUI.signal_autoconnect(self)
		self.window = gladeUI.get_widget('quick_terminal')
		self.vbox = gladeUI.get_widget('quick_term_vbox')
		self.vte_terminal = vte.Terminal()
		self.vte_terminal.set_encoding("UTF-8")
		self.vte_terminal.set_font_from_string ('monospace')
		self.vte_terminal.set_color_dim(gtk.gdk.color_parse("white"))
		self.vte_terminal.set_color_foreground(gtk.gdk.color_parse("white"))
		self.vte_terminal.set_color_background(gtk.gdk.color_parse("black"))
		self.vte_terminal.set_cursor_blinks(True)
		self.vbox.pack_end(self.vte_terminal)
		self.vbox.show_all()
		update_ui()
		set_title(self.window,"Updating your sources list")
		self.window.set_icon_from_file(axConf.images["windowIcon"])
		self.window.connect("delete-event",no_delete)
		self.window.show()
		update_ui()
class info_box:
	def __init__(self,info,question,window):
		self.wait = 1
		self.input = None
		gladeUI = conf.gladeUI
		gladeUI.signal_autoconnect(self)
		self.window = gladeUI.get_widget("info_box")
		label = gladeUI.get_widget("info_label")
		label.set_markup(question)
		label.set_line_wrap(1)
		#self.document = webkit.DOMDocument()
		#self.document.clear()
		#self.document.open_stream('text/html')
		view = webkit.WebView()
		view.load_html_string("<html><head></head><body>%s</body></html>"%info, "about:blank")
		#self.document.close_stream()
		scroll = gladeUI.get_widget("info_scroll")
		if scroll.get_child():
			scroll.get_child().destroy()
		scroll.add(view)
		yes = gladeUI.get_widget("info_yes")
		no = gladeUI.get_widget("info_no")
		self.window.connect("delete-event",no_delete)
		self.yes_button = yes
		self.no_button = no
		yes.connect("clicked",self.button_yes_clicked)
		no.connect("clicked",self.button_no_clicked)
		set_title(self.window,"Information")
		self.window.set_modal(True)
		self.window.set_transient_for(window)
		self.window.set_icon_from_file(axConf.images["windowIcon"])
		self.window.show_all()
	def button_no_clicked(self,button):
		self.wait = 0
		self.input = 0
	def button_yes_clicked(self,button):
		self.wait = 0
		self.input = 1
class error_report:
	def __init__(self):
		gladeUI = conf.gladeUI
		gladeUI.signal_autoconnect(self)
		self.window = gladeUI.get_widget("error_report") 
		self.tree = gladeUI.get_widget("error_tree")
		self.close = gladeUI.get_widget("error_close")
		self.label = gladeUI.get_widget("error_label")
		self.close.connect("clicked",self.on_close)
		self.window.connect("delete-event",self.window.hide_on_delete)
		self.window.set_icon_from_file(axConf.images["windowIcon"])
		set_title(self.window,"Error and Information Report")
		tree = self.tree
		cell = gtk.CellRendererPixbuf()
		cell.set_property("width",56)
		column = gtk.TreeViewColumn(None, cell,
									pixbuf=0)
		tree.append_column(column)
		cell = gtk.CellRendererText()
		cell.set_property("wrap-width",500)
		column = gtk.TreeViewColumn(None,cell,markup=1)
		column.set_fixed_width(400)
		column.set_max_width(400)
		column.set_clickable(False)
		tree.append_column(column)
		self.label.set_markup("<span size='x-large'><b>Errors and information...</b></span>\nSee below for more details")
		self.tree.connect("cursor-changed",self.unselect)
	def unselect(self,tree):
		sel = tree.get_selection()
		sel.unselect_all()
	def on_close(self,window):	
		self.window.hide()
	def generate_model(self,array):
		self.error_model = gtk.ListStore(
					gtk.gdk.Pixbuf,gobject.TYPE_STRING,	
					);
		for error in array:
			script = get_script(error[1])
			if error[0] == 2:
				icon= gtk.gdk.pixbuf_new_from_file(axConf.images['infoIcon'])
				type = "INFORMATION"
				report = "<span foreground='blue'><b>%s: %s</b>\n %s</span>"%(type,script.title,error[2])
			if error[0] == 1:
				icon= gtk.gdk.pixbuf_new_from_file(axConf.images['warningIcon'])
				type = "FATAL ERROR"
				report = "<span foreground='red'><b>%s: %s</b>\n %s</span>"%(type,script.title,error[2])
			if error[0] == 0:
				icon= gtk.gdk.pixbuf_new_from_file(axConf.images['fatalIcon'])
				type = "WARNING"
				report = "<span foreground='black'><b>%s: %s</b>\n %s</span>"%(type,script.title,error[2])
			new = self.error_model.append()
			self.error_model.set(new,
					0,icon,
					1,report
					)
		self.tree.set_model(self.error_model)
		selection = self.tree.get_selection()
		selection.unselect_all()
class dropdown_window:
	def __init__(self):
		gladeUI = conf.gladeUI
		gladeUI.signal_autoconnect(self)
		self.window = gladeUI.get_widget("dropdown") 
		self.label = gladeUI.get_widget("drop_label") 
		self.menu = gladeUI.get_widget("dropcombo") 
		self.okay = gladeUI.get_widget("drop_ok")
		self.cancel = gladeUI.get_widget("drop_cancel")
		self.okay.connect("clicked",self.okay_clicked)
		self.cancel.connect("clicked",self.cancel_clicked)
		self.window.connect("delete-event",no_delete)
		self.window.set_modal(True)
		set_title(self.window,"")
		self.leaf = 0
		self.up = 1
		cell = gtk.CellRendererText()
		self.menu.clear()
  		self.menu.pack_start(cell, True)
  		self.menu.add_attribute(cell, 'text', 0)
	def okay_clicked(self,signal):
		print "OKAY CLICKED"
		self.leaf = 1
		self.up = 0
	def cancel_clicked(self,signal):
		print "CANCEL CLICKED"
		self.leaf = 0
		self.up = 0
	def set_options(self,inar):
		try:
			if self.model:
				del self.model
		except:
			pass
		self.model = gtk.ListStore(
					gobject.TYPE_STRING
					)
		for a in inar:
			if a:
				new = self.model.append()
				self.model.set(new,0,a)
		def checkIter(model,path,iter):
			test = model.get(iter,0)[0]
			if not test.strip():
				model.remove(iter)
		self.model.foreach(checkIter)
		self.menu.set_model(None)
		self.menu.set_model(self.model)
		self.menu.set_active_iter(self.model.get_iter_first())
