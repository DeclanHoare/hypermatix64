import sys,os,time,user
import gtk, gtk.glade
from gtk import gdk
import gobject
import pango 
from resin_config import *
from extra_functions import *
from resin_ui import *
import threading
import time
from copy import *
import vte
import webkit
class termPipe( threading.Thread ):
	def run( self ):
		self.running = 1		
		pid = self.terminal.fork_command(self.script)
		run = 1
		while run:
			try:
				if os.popen("ps -eo %p"+"|grep ^[[:space:]]*%s$"%pid).read() == "":
					run = 0
					break
				else:
					time.sleep(.111111)
			except:
				run = 0
				print "broken pipe!"
				break
		self.running = 0
class termPipe2( threading.Thread ):
	def run( self ):
		self.running = 1		
		pid = self.terminal.fork_command(self.script)
		run = 1
		while run:
			try:
				if os.popen("ps -eo %p"+"|grep ^[[:space:]]*%s$"%pid).read() == "":
					run = 0
					break
				else:
					time.sleep(2)
			except:
				run = 0
				print "broken pipe!"
				break
		self.running = 0
class activity_terminal:
	def __init__(self):
		self.terminal = term_status_window()
	def connect_pipe(self,command):
		self.logged = ''
		self.r = 0
		self.terminal.vte_terminal.grab_focus()
		self.terminal.vte_terminal.connect("cursor-moved",self.log_output)
		self.thread = termPipe()
		self.thread.script = command
		self.thread.terminal = self.terminal.vte_terminal
		self.thread.start()
		self.thread.running = 1
		self.pipe_open = 1
		pre = self.terminal.label.get_label()
		eli = ""
		while self.thread.running:
			if (len(eli) >= 3):
				eli = ""
			else:
				eli+="."
			self.terminal.label.set_markup(pre+eli)
			time.sleep(.1)
			update_ui()
		self.terminal.label.set_markup(pre)
		self.pipe_open = 0
	def log_output(self,term):
		column,row = self.terminal.vte_terminal.get_cursor_position()
		if self.r != row:
			off = row-self.r
			text = self.terminal.vte_terminal.get_text_range(row-off,0,row-1,-1,self.capture_text)
			self.r=row
			text = text.strip()
			if "\n" not in text or text[-1] != "\n":
				text += "\n"
			self.logged += text
	def capture_text(self,text,text2,text3,text4):
		return True
class quick_terminal:
	def __init__(self):
		self.terminal = quick_terminal_window()
	def connect_pipe(self,command):
		self.terminal.vte_terminal.grab_focus()
		self.thread = termPipe2()
		self.thread.script = command
		self.thread.terminal = self.terminal.vte_terminal
		self.thread.start()
		self.thread.running = 1
		self.pipe_open = 1
		while self.thread.running:
			update_ui()
		self.pipe_open = 0
