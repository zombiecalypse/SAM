#!/usr/bin/python

# Filename: wxGui.py
# Author:   Aaron Karper
# Created:  2011-10-06
# Description:
#          A wxGui for the Mission Generator 

from threading import Thread
import wx, wx.html
from .gui_helpers import *
from .gui_helpers import _

class AboutDialog(wx.Dialog):
	aboutText = """
	<html>
		<body>
		<h1>SAM {version}</h1>
		<h2>Space Alert Missions</h2>
		<div style="bottom: 0; position: absolute;">By <ul><b>{authors}</b></ul></div>
	"""
	def __init__(self, parent):
		wx.Dialog.__init__(self,parent, wx.NewId(), "About SAM")
		info = wx.html.HtmlWindow(self)
		authors_string = "\n".join('<li>{}</li>'.format(author) for author in authors())
		info.SetPage(self.aboutText.format(
			version = version,
			authors = authors_string
			))
		button = wx.Button(self, wx.ID_OK, "Ok")
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(info, 1, wx.EXPAND | wx.ALL, 5)
		sizer.Add(button, 0, wx.ALIGN_CENTER | wx.ALL)
		self.SetSizer(sizer)
		self.Layout()

class MissionGenerator(wx.Frame):
	difficulties = [
					'toddler',
					'kiddie',
					'cadett',
					'freshmen',
					'officer',
					'captain',
					'veteran',
					'survivor',
					'actionhero',
					'suicidal']
	def __init__(self):
		wx.Frame.__init__(self, None, wx.NewId(), "SAM")
		self.languages = [dict(name = 'English'), dict(name = 'Deutsch')]
		self._makeMenu()
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self._makeControlls(), 0, wx.EXPAND | wx.ALL)
		sizer.Add(self._makeFeedback(), 1, wx.EXPAND)
	def _makeMenu(self):
		menuBar = wx.MenuBar()
		with addMenu(menuBar, _("File")) as filemenu:
			quit = filemenu.Append(wx.ID_EXIT, _("Quit"))
			self.Bind(wx.EVT_MENU, self.OnQuit, quit)
		with addMenu(menuBar, _("Settings")) as settingsmenu:
			with addMenu(settingsmenu, _("Languages")) as languagemenu:
				for language in self.languages:
					lang = languagemenu.Append(wx.ID_ANY, language['name'])
					def setToLanguage(l):
						return lambda evt: self.SetLanguage(l)
					self.Bind(wx.EVT_MENU, setToLanguage(language) , lang)
		with addMenu(menuBar, _("Help")) as helpmenu:
			about = helpmenu.Append(wx.ID_ABOUT, _("About"))
			self.Bind(wx.EVT_MENU, self.OnAbout, about)
		self.SetMenuBar(menuBar)
	def TranslateDifficulty(self, val):
		try: 
			return self.difficulties[val]
		except IndexError:
			return val
	def SetLanguage(self, language):
		print language
	def OnAbout(self, evt):
		about = AboutDialog(self)
		about.ShowModal()
		about.Close()
	def OnQuit(self, evt):
		self.Close()
	def _makeControlls(self):
		return ControllPanel(self)
	def OnRun(self, evt):
		pass
	def OnCancel(self, evt):
		pass
	def _makeFeedback(self):
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		return sizer
class ControllPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
		self.parent = parent
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		min, max = difficulty_range()
		slider = LabeledSlider(self, 'Difficulty', self.TranslateDifficulty, minValue = min, maxValue = max)
		run_button = wx.Button(self, wx.ID_ANY, 'Run')
		cancel_button = wx.Button(self, wx.ID_ANY, 'Cancel Mission')
		button_sizer = wx.BoxSizer(wx.HORIZONTAL)
		button_sizer.Add(run_button)
		button_sizer.Add(cancel_button)
		sizer.Add(slider,1, flag = wx.EXPAND | wx.ALL)
		sizer.Add(button_sizer,1)
		self.SetSizer(sizer)
		self.Bind(wx.EVT_BUTTON, self.OnRun, run_button)
		self.Bind(wx.EVT_BUTTON, self.OnCancel, cancel_button)
	def TranslateDifficulty(self, value):
		return self.parent.TranslateDifficulty(value)
	def OnRun(self, evt):
		return self.parent.OnRun(evt)
	def OnCancel(self, evt):
		return self.parent.OnCancel(evt)
