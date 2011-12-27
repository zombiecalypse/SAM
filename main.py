#!/usr/bin/python

# Filename: main.py
# Author:   Aaron Karper
# Created:  2011-11-29
#
import sys
sys.path.append('./Python-Logger')
from Sam import MissionGenerator
from Sam import version
import wx

class SpaceAlertMissionGeneratorApp(wx.App):
	def __init__(self, **kargs):
		wx.App.__init__(self, **kargs)
		self.mainframe = MissionGenerator()
		self.mainframe.Show(True)
	def OnInit(self):
		return True
if __name__=="__main__":
	app = SpaceAlertMissionGeneratorApp()
	app.MainLoop()

