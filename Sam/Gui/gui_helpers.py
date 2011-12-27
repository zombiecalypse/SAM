#!/usr/bin/python

# Filename: helpers.py
# Author:   Aaron Karper
# Created:  2011-11-29
import PyLogger
import wx
from contextlib import contextmanager
from ..helpers import version
_ = lambda x:x
__THEADS__ = set()

def difficulty_range():
	return (0,10)

def authors():
	return (
			"Aaron Karper &lt;maergil@gmail.com&gt;",
		"Stefan Moser &lt;smmuzi@gmail.com&gt;")

_sam_logger = PyLogger.LoggerParent()
debug = _sam_logger(PyLogger.Debug)
log = _sam_logger(PyLogger.Log)
warn = _sam_logger(PyLogger.Warn)
error = _sam_logger(PyLogger.Error)
fatal = _sam_logger(PyLogger.Fatal)


def doAsync(f,callback = _, args = tuple()):
	"Calls the function (*not* a method, closure it via lambda) `f :: argsType -> returnType` and then calls the `callback :: returnType, exception -> ignored`"
	def call(back, arg):
		try:
			val = f(*arg)
			callback(val,None)
		except Exception as e:
			try:
				error(e.message())
				callback(None,e)
			except:
				error("Callback failed")
	def callback_(thread, x):
		callback(x)
		__THREADS__.remove(thread)
	t = Thread(call, args=(callback_,args))
	__THREADS__.add(t)
	t.start()

class LabeledSlider(wx.Panel):
	def __init__(self, parent, title, translation, *args, **kargs):
		wx.Panel.__init__(self,parent)
		self.slider = wx.Slider(self, *args, **kargs)
		sizer = wx.BoxSizer(wx.VERTICAL)
		self.translation = translation
		sizer.Add(wx.StaticText(self, label = title), flag = wx.EXPAND | wx.HORIZONTAL)
		sizer.Add(self.slider, flag = wx.EXPAND| wx.HORIZONTAL)
		self.label = wx.StaticText(self, label = '')
		sizer.Add(self.label, flag = wx.EXPAND| wx.HORIZONTAL)
		self.Bind(wx.EVT_SLIDER, self.OnSlide, self.slider)
		self.SetSizer(sizer)
		self.label.SetLabel(str(self.translation(self.GetValue())))
	def GetValue(self):
		return self.slider.GetValue()
	def OnSlide(self, evt):
		self.label.SetLabel(str(self.translation(self.GetValue())))

@contextmanager
def addMenu(bar, name):
	"Creates a submenu in the `bar` with the given name."
	menu = wx.Menu()
	yield menu
	if isinstance(bar, wx.MenuBar):
		bar.Append(menu, name)
	elif isinstance(bar, wx.Menu):
		bar.AppendSubMenu(menu, name)
