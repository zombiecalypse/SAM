#!/usr/bin/python

# Filename: generation.py
# Author:   Aaron Karper
# Created:  2012-01-13
# Description:
#           
from random import Random
from ..helpers import accessor
from .mission import Mission

class MissionGenerator(object):
	difficulty = accessor('difficulty', type = float)
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
			if 0.9 < self._fitness(solution) < 1.1 or i > self.MAX_ITERATIONS:
				return solution

	def _fitness(self, solution):
		return solution.difficulty/self.difficulty

	def _generateIteratively(self):
		sample = self._generateSample()
		while True:
			yield sample
			sample = self._mutate(sample)

	@staticmethod
	def _generateSample():
		return Mission.random()

	def _mutate(self, sample):
		return sample.mutate(self._random)
