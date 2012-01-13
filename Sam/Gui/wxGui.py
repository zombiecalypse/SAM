#!/usr/bin/python

# Filename: wxGui.py
# Author:   Aaron Karper
# Created:  2011-10-06
# Description:
#          A wxGui for the Mission Generator 

from threading import Thread
import wx, wx.html
from .gui_helpers import *
from ..helpers import languages
from wx import GetTranslation as _

class AboutDialog(wx.AboutDialogInfo):
	def __init__(self, parent):
		super(AboutDialog, self).__init__()
		description = """Space Alert Mission-generator, in short SAM, is an 
		application for generating missions for the highly addictive board game
		space alert."""

		licence = """SAM is free software; you can redistribute 
		it and/or modify it under the terms of the GNU General Public License v3 """

		#self.SetIcon(wx.Icon('hunter.png', wx.BITMAP_TYPE_PNG))
		authors='''Aaron Karper, Stefan Moser'''
		self.SetName('Space Alert Mission-generator')
		self.SetVersion(version)
		self.SetDescription(description)
		self.SetWebSite('http://www.github.com/zombiecalypse/SAM')
		self.SetLicence(licence)
		self.AddDeveloper(authors)
		self.AddDocWriter(authors)
		self.AddArtist(authors)
		self.AddTranslator(authors)

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
		self.SetMinSize((400, 400))
		self.initLanguages()
		self._makeMenu()
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self._makeControlls(), 0, wx.EXPAND | wx.ALIGN_TOP)
		sizer.Add(wx.StaticLine(self), 0, wx.EXPAND | wx.ALIGN_TOP)
		sizer.Add(self._makeFeedback(), 1, wx.EXPAND)
		self.SetSizer(sizer)
		self.Bind(wx.EVT_CLOSE, self.OnClose)
	def OnClose(self, event):
		#TODO: make mission player
		self.mission_player = None
		if not self.mission_player is None:
			dial = wx.MessageDialog(None, _('Are really that scared?!?'), _('Abort mission?'),
				wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
			ret = dial.ShowModal()
			if ret == wx.ID_YES:
				self.Destroy()
			else:
				event.Veto()
		else: 
			self.Destroy()
	def initLanguages(self):
		mylocale = wx.Locale()
		mylocale.AddCatalogLookupPathPrefix('./Sam/Media/strings')
		for language in languages.getAllLanguages():
			mylocale.AddCatalog(language['file'])
		#For testing:
		print(wx.GetTranslation('File'))
	def _makeMenu(self):
		menuBar = wx.MenuBar()
		with addMenu(menuBar, _("File")) as filemenu:
			quit = filemenu.Append(wx.ID_EXIT, _("Quit"))
			self.Bind(wx.EVT_MENU, self.OnQuit, quit)
		with addMenu(menuBar, _("Settings")) as settingsmenu:
			with addMenu(settingsmenu, _("Languages")) as languagemenu:
				for language in languages.getAllLanguages():
					langEntry = languagemenu.Append(wx.ID_ANY, language['name'], kind=wx.ITEM_CHECK)
					def setToLanguage(l, languagemenu, langEntry):
						return lambda evt: self.SetLanguage(l, languagemenu, langEntry)
					self.Bind(wx.EVT_MENU, setToLanguage(language, languagemenu, langEntry), langEntry)
		with addMenu(menuBar, _("Help")) as helpmenu:
			about = helpmenu.Append(wx.ID_ABOUT, _("About"))
			self.Bind(wx.EVT_MENU, self.OnAbout, about)
		self.SetMenuBar(menuBar)
	def TranslateDifficulty(self, val):
		try: 
			return self.difficulties[val]
		except IndexError:
			return val
	def SetLanguage(self, language, languagemenu, selectedEntry):
		for entry in languagemenu.GetMenuItems():
			languagemenu.Check(entry.GetId(), False)
		languagemenu.Check(selectedEntry.GetId(), True)
		print(language)
	def OnAbout(self, evt):
		wx.AboutBox(AboutDialog(self))
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
		right = wx.BoxSizer(wx.VERTICAL)
		left = wx.BoxSizer(wx.VERTICAL)
		label = wx.StaticText(self, label=_('Mission Log'))
		missionLog = wx.TextCtrl(self, style=wx.TE_MULTILINE)
		left.Add(label, 0, wx.TOP | wx.LEFT, border=5)
		left.Add(missionLog, 1, wx.EXPAND | wx.ALL, border=5)
		description = wx.StaticText(self, label=_('Stuff happens'))
		right.Add(description, 1, wx.CENTER | wx.EXPAND)
		sizer.Add(left, 1, wx.EXPAND)
		sizer.Add(right, 1, wx.EXPAND)
		return sizer
	
class ControllPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
		self.mission_player = None
		self.parent = parent
		sizer = wx.BoxSizer(wx.HORIZONTAL)		
		min, max = difficulty_range()
		slider = LabeledSlider(self, _('Difficulty'), lambda x: _(self.TranslateDifficulty(x)), minValue = min, maxValue = max)
		sizer.Add(slider, 1, wx.EXPAND | wx.ALL, border=5)
		sizer.Add(self.MakeButtons(), 0, wx.CENTER | wx.ALL | wx.ALIGN_RIGHT, border=5)
		self.SetSizer(sizer)
	def MakeButtons(self):
		self.run_button = wx.Button(self, wx.ID_ANY, _('Run'))
		self.cancel_button = wx.Button(self, wx.ID_STOP, _('Cancel Mission'))
		self.cancel_button.Disable()
		self.Bind(wx.EVT_BUTTON, self.OnRun, self.run_button)
		self.Bind(wx.EVT_BUTTON, self.OnCancel, self.cancel_button)
		button_sizer = wx.BoxSizer(wx.HORIZONTAL)
		button_sizer.Add(self.run_button, wx.ALIGN_RIGHT)
		button_sizer.Add(self.cancel_button, wx.ALIGN_RIGHT)
		return button_sizer
	def TranslateDifficulty(self, value):
		return _(self.parent.TranslateDifficulty(value))
	def OnRun(self, evt):
		if self.mission_player is None:
			self.cancel_button.Enable()
			self.run_button.SetLabel(_('Pause'))
			mission_player = Mission.generate(self.slider.GetValue())
			mission_player.subscribe(parent.OnMissionPlayer)
			mission_player.start()
		elif not self.mission_player.done:
			self.mission_player.pause()
			self.run_button.SetLabel(_('Resume'))
		else:
			self.mission_player.resume()
			self.run_button.SetLabel(_('Pause'))
	def OnCancel(self, evt):
		return self.parent.OnCancel(evt)
