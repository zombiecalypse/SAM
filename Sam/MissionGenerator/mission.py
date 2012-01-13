#!/usr/bin/python

# Filename: mission.py
# Author:   Aaron Karper
# Created:  2011-12-02
# Description:
#           The mission statement and functions that generate them.

from ..helpers import accessor
from .encounter import Event
import random as _random

class Mission(object):

	encounters = accessor('encounters', immutable = True)

	def __init__(self, encounters = list()):
		self._encounters = encounters

	def encountersAt(self, time):
		return set(enc for enc in self.encounters if time == enc.time)
	def encountersUntil(self, time):
		return set(enc for enc in self.encounters if time <= enc.time)

	@property
	def difficulty(self):
		base_value = sum(encounter.inherentDanger for encounter in self.encounters)
		relational_value = sum(encounter.relativeDanger(self.encounters) for encounter in self.encounters)
		return base_value + relational_value
	
	@classmethod
	def random(cls):
		return Mission().mutate()

	def mutate(self, random = _random):
		f = random.choice((
			lambda rand : self._removeEncounter(rand), 
			lambda rand : self._addEncounter(rand)))
		return f(random)

	def _removeEncounter(self, random):
		encounter = random.choice(self.encounters) if self.encounters else None
		return Mission([enc for enc in self.encounters if enc != encounter])

	def _addEncounter(self, random):
		encounter = Event.generateRandom(random)
		return Mission(self.encounters + [encounter])
