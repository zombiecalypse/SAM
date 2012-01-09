#!/usr/bin/python

# Filename: mission.py
# Author:   Aaron Karper
# Created:  2011-12-02
# Description:
#           The mission statement and functions that generate them.

from ..helpers import accessor

class Mission(object):

	terror_red = accessor('terror_red')
	terror_white = accessor('terror_white')
	terror_blue = accessor('terror_blue')
	terror_internal = accessor('terror_internal')
	ship = accessor('ship')

	@property
	def terror(self):
		return dict(
				red = self.terror_red,
				white = self.terror_white,
				blue = self.terror_blue,
				internal = self.terror_internal)
	def __init__(self):
		self.terror_red = TerrorRow(self)
		self.terror_blue = TerrorRow(self)
		self.terror_white = TerrorRow(self)
		self.terror_internal = TerrorRow(self)

	def addEncounter(self, time, encounter):
		self.encounters.add((time, encounter))
	def encountersAt(self, time):
		return set(enc for t,enc in self.encounters if time == t)
	def encountersUntil(self, time):
		return set(enc for t,enc in self.encounters if time <= t)

