#!/usr/bin/python

# Filename: generation.py
# Author:   Aaron Karper
# Created:  2012-01-13
# Description:
#           
from random import Random
from ..helpers import accessor

class MissionGenerator(object):
	difficulty = accessor('difficulty', float)
	MAX_ITERATIONS = 1000
	def __init__(self, 
			difficulty = 50, 
			use_internal = True, 
			use_communication_breakdown = True, 
			use_serious_threats = True,
			seed = None):
		self._random = Random(seed)
		self.difficulty = difficulty
		self.use = dict(
				internal = use_internal,
				communication_breakdown = use_communication_breakdown,
				serious_threats = use_serious_threats)
	def generate(self):
		for i,solution in enumerate(self._generateIteratively()):
			if 0.9 < solution.difficulty()/self.difficulty < 1.1 or i > self.MAX_ITERATIONS:
				return solution
