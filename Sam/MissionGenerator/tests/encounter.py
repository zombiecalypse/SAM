#!/usr/bin/python

# Filename: encounter.py
# Author:   Aaron Karper
# Created:  2011-12-28
# Description:
#           

import unittest
from ..encounter import Encounter

class RelativeDangerAxioms(unittest.TestCase):
	def setUp(self):
		self.far_encounter = Encounter.generate(1, serious = True, internal = False)
		self.close_encounter = Encounter.generate(2, serious = True, internal = False)
		self.list       = [Encounter.generate(i, serious = False, internal = True) for i in range(3,9)]
	def test_increasing(self):
		self.assertLess(
				self.far_encounter.relativeDanger(self.list),
				self.far_encounter.relativeDanger(self.list+[self.close_encounter]), 
				'relative Danger does not increase if faced with more encounters')
	def test_distance_decreases(self):
		relative_danger_far  = self.far_encounter.relativeDanger(self.list)
		relative_danger_near = self.close_encounter.relativeDanger(self.list)
		self.assertLess(
				relative_danger_far,
				relative_danger_near,
				'relative danger does not increase if the encounters are closer together (near: {near} vs far: {far})'.format(near = relative_danger_near, far = relative_danger_far))
	def test_identical_for_same_event(self):
		self.assertEqual(
				self.far_encounter.relativeDanger(self.list),
				self.far_encounter.relativeDanger(self.list+[self.far_encounter]))

if __name__=="__main__":
	unittest.main()
