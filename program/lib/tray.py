# FIXME: this doesn't actually create a tray icon anymore,
# meaning it needs to either be fixed or removed entirely.
# The tray icon is pretty much pointless in Ultamatix
# anyway, meaning the latter may be a good idea.
import gtk, pango
import sys
import traceback
class TrayIcon(object):
	__icon = False
	__mapped = False
	__tips = ''
	__menu = None
	def __init__(self, window):
		self.icon = gtk.StatusIcon()
		self.icon.set_from_file("/usr/share/ultamatix/pixmaps/ultimate_icon.png")
		self.icon.set_tooltip('') 
		self.windowevent = self.icon.connect('button-press-event', self.__button, window)
		self.icon.connect('activate', self.__show_window)
		#window.connect('delete-event', self.__window_delete)
		#self.myTip = gtk.Tooltips()
		print "TRAY ICON CREATED"
		self.icon.set_visible(True)
	def set_window(self,window):
		self.icon.disconnect(self.windowevent)
		self.windowevent = self.icon.connect('button-press-event', self.__button, window)
	def set_label(self,text):
		self.icon.set_tooltip(self.icon, text)

	def __window_delete(self, window, event):
		if self.enabled:
			self.__hide_window(window)
			return True
	def __show_window(self, window):
		try: window.move(*window.__position)
		except AttributeError: traceback.print_exc()
		window.show()
	def __hide_window(self, window):
		window.__position = window.get_position()
		window.hide()
	def __enabled(self):
		return (self.__icon  and self.__mapped and
				self.__icon.get_property('visible'))
		enabled = property(__enabled)
	def __button(self, icon, event, window):
		if event.button == 1:
			if window.get_property('visible'): self.__hide_window(window)
			else: self.__show_window(window)
	def destroy(self):
		if self.__icon: self.__icon.destroy()
		if self.__menu: self.__menu.destroy()

