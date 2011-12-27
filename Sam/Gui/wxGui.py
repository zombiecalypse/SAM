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
		<div style="bottom: 0; position: absolute;">By <ul>{authors}</ul></div>
		</body>
	</html>
	"""
	def __init__(self, parent):
		wx.Dialog.__init__(self,parent, wx.NewId(), "About SAM")
		info = wx.html.HtmlWindow(self)
		authors_string = "\n".join('<li>{}</li>'.format(author) for author in authors())
		info.SetPage(self.aboutText.format(
			version = version,
			authors = authors_string
			))
		button = wx.Button(self, wx.ID_OK, _("Ok"))
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
		self.initLanguages()
		self._makeMenu()
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self._makeControlls(), 0, wx.EXPAND | wx.ALL)
		sizer.Add(self._makeFeedback(), 1, wx.EXPAND)
	def initLanguages(self):
		self.languages = [dict(name = 'English', file=''), 
							dict(name = 'Deutsch', file='translation_de')]
		mylocale = wx.Locale()
		mylocale.AddCatalogLookupPathPrefix('.')
		for language in self.languages:
			mylocale.AddCatalog(language['file'])
		self._ = wx.GetTranslation
		#For testing:
		print wx.GetTranslation('file')
	def _makeMenu(self):
		menuBar = wx.MenuBar()
		with addMenu(menuBar, _("File")) as filemenu:
			quit = filemenu.Append(wx.ID_EXIT, _("Quit"))
			self.Bind(wx.EVT_MENU, self.OnQuit, quit)
		with addMenu(menuBar, _("Settings")) as settingsmenu:
			with addMenu(settingsmenu, _("Languages")) as languagemenu:
				for language in self.languages:
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
		self.mission_player = None
		self.parent = parent
		allSizer = wx.BoxSizer(wx.VERTICAL)
		topSizer = wx.BoxSizer(wx.HORIZONTAL)
		bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
		min, max = difficulty_range()
		slider = LabeledSlider(self, _('Difficulty'), self.TranslateDifficulty, minValue = min, maxValue = max)
		topSizer.Add(slider, 1, wx.EXPAND | wx.ALL, border=5)
		topSizer.Add(self.MakeButtons(), 0, wx.CENTER | wx.ALL | wx.ALIGN_RIGHT, border=5)
		
		missionLog = wx.TextCtrl(self, style=wx.TE_MULTILINE)
		bottomSizer.Add(missionLog, 1, wx.EXPAND | wx.ALL, border=5)
		
		allSizer.Add(topSizer, 0, wx.EXPAND | wx.ALIGN_TOP)
		allSizer.Add(wx.StaticLine(self), 1, wx.EXPAND | wx.ALIGN_TOP)
		allSizer.Add(bottomSizer, 1, wx.EXPAND)
		self.SetSizer(allSizer)
	def MakeButtons(self):
		self.run_button = wx.Button(self, wx.ID_ANY, _('Run'))
		self.cancel_button = wx.Button(self, wx.ID_ANY, _('Cancel Mission'))
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
