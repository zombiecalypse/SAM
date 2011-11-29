#!/usr/bin/python

# Filename: wxGui.py
# Author:   Aaron Karper
# Created:  2011-10-06
# Description:
#          A wxGui for the Mission Generator 

from threading import Thread
import wx, wx.html
from helpers import *

class AboutDialog(wx.Dialog):
	aboutText = """
	<html>
		<body>
		<h1>SAM {version}</h1>
		<h2>Space Alert Missions</h2>
		<div style="bottom: 0">By <b>{author}</b></div>
	"""
	def __init__(self, parent):
		wx.Dialog.__init__(self,parent, wx.NewId(), "About SAM")
		info = wx.html.HtmlWindow(self)
		info.SetPage(self.aboutText.format(
			version = version,
			author = author
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
		self._makeMenu()
	def _makeMenu(self):
		menuBar = wx.MenuBar()
		filemenu = wx.Menu()
		menuBar.Append(filemenu, "&File")
		helpmenu = wx.Menu()
		about = helpmenu.Append(-1, "About")
		self.Bind(wx.EVT_MENU, self.OnAbout, about)
		menuBar.Append(helpmenu, "&Help")
		self.SetMenuBar(menuBar)
	def OnAbout(self, evt):
		about = AboutDialog(self)
		about.ShowModal()
		about.Destroy()
