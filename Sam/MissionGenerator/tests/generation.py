#!/usr/bin/python

# Filename: generation.py
# Author:   Aaron Karper
# Created:  2012-01-11
# Description:
#           

import unittest
from ..generation import MissionGenerator

class MissionGenerator(unittest.TestCase):
	def setUp(self):
		self.seeds = range(1,100)
	
	def generate_simple_mission(self, seed):
		mission = MissionGenerator(40, seed = seed).generate()
		self.assertAlmostEqual(40, mission.difficulty(), places = -1)

	def generate_medium_mission(self, seed):
		mission = MissionGenerator(60, seed = seed).generate()
		self.assertAlmostEqual(60, mission.difficulty(), places = -1)

	def generate_hard_mission(self, seed):
		mission = MissionGenerator(100, seed = seed).generate()
		self.assertAlmostEqual(100, mission.difficulty(), places = -1)

	def test_simple_missions(self):
		for seed in self.seeds:
			self.generate_simple_mission(seed)

	def test_medium_missions(self):
		for seed in self.seeds:
			self.generate_medium_mission(seed)

	def test_hard_missions(self):
		for seed in self.seeds:
			self.generate_hard_mission(seed)
