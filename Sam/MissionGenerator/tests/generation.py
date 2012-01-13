#!/usr/bin/python

# Filename: generation.py
# Author:   Aaron Karper
# Created:  2012-01-11
# Description:
#           

import unittest
from ..generation import MissionGenerator

class MissionGeneratorTest(unittest.TestCase):
	def setUp(self):
		self.seeds = range(1,100)
	
	def test_simple_missions(self):
		for seed in self.seeds:
			mission = MissionGenerator(difficulty = 40, seed = seed).generate()
			self.assertAlmostEqual(40, mission.difficulty, delta = 10)

	def test_medium_missions(self):
		for seed in self.seeds:
			mission = MissionGenerator(60, seed = seed).generate()
			self.assertAlmostEqual(60, mission.difficulty, delta = 10)

	def test_hard_missions(self):
		for seed in self.seeds:
			mission = MissionGenerator(100, seed = seed).generate()
			self.assertAlmostEqual(100, mission.difficulty, delta = 10)
