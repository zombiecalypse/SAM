#!/usr/bin/python

# Filename: wxGui.py
# Author:   Aaron Karper
# Created:  2011-10-06
# Description:
#          A wxGui for the Mission Generator 

from threading import Thread
import wx, wx.html
from gui_helpers import *

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
	def __init__(self):
		wx.Frame.__init__(self, None, wx.NewId(), "SAM")
		self.languages = [dict(name = 'English'), dict(name = 'German')]
		self._makeMenu()
		self._makeControlls()
		self._makeFeedback()
	def _makeMenu(self):
		menuBar = wx.MenuBar()
		with addMenu(menuBar, "&File") as filemenu:
			quit = filemenu.Append(-1, "&Quit")
			self.Bind(wx.EVT_MENU, self.OnQuit, quit)
		with addMenu(menuBar, "&Settings") as settingsmenu:
			with addMenu(settingsmenu, "&Languages") as languagemenu:
				for language in self.languages:
					lang = languagemenu.Append(-1, language['name'])
					self.Bind(wx.EVT_MENU, lambda evt: self.SetLanguage(language), lang)
		with addMenu(menuBar, "&Help") as helpmenu:
			about = helpmenu.Append(-1, "About")
			self.Bind(wx.EVT_MENU, self.OnAbout, about)
		self.SetMenuBar(menuBar)
	def SetLanguage(self, language):
		print language
	def OnAbout(self, evt):
		about = AboutDialog(self)
		about.ShowModal()
		about.Destroy()
	def OnQuit(self, evt):
		self.Destroy()
	def _makeControlls(self):
		pass
	def _makeFeedback(self):
		pass