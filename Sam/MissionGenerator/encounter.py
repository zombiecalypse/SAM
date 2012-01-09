from ..helpers import *
class Encounter(object):
	SERIOUS, NON_SERIOUS = 10, 0
	INTERNAL, EXTERNAL = 5, 0

	BEFORE_KERN, AFTER_KERN = ([], [2**k for k in range(1,9)])
	@classmethod
	def generate(cls, time, serious = False, internal = False):
		return cls(time, 
				cls.SERIOUS if serious else cls.NON_SERIOUS,
				cls.INTERNAL if internal else cls.EXTERNAL)

	def __init__(self, time, seriousness, positional):
		self._time = time
		self._seriousnessDanger = seriousness
		self._positionalDanger = positional
	
	time = accessor('time', immutable = True, doc = 'The appearance of the Encounter')
	seriousnessDanger = accessor('seriousnessDanger', immutable = True, doc = 'The danger imposed from being serious or normal')
	positionalDanger = accessor('positionalDanger', immutable = True, doc = 'The danger imposed from being external or internal')

	@property
	def inherentDanger(self):
		return self.seriousnessDanger + self.positionalDanger + self.constantDanger

	@property
	def constantDanger(self):
		"Each encounter is at least this difficult"
		return 10

	def relativeDanger(self, other_encounters):
		"""The danger of this encounter imposed from the relation to other
		encounters.

		The following properties hold:
			* if x != a: a.relativeDanger(l) < a.relativeDanger(l+[x])

		other_encounters :: [Encounter]
		"""
		other_encounters = filter(lambda x: x != self, other_encounters)
		before = filter(lambda x: x.time < self.time, other_encounters)
		after  = filter(lambda x: x.time >=  self.time, other_encounters)
		before_danger_map = [0] * reduce(max, [e.time for e in before], 0)
		after_danger_map = [0] * reduce(max, [e.time for e in after], 0)
		for e in before:
			before_danger_map[e.time-self.time - 1] = e.inherentDanger
		for e in after:
			after_danger_map[self.time-e.time] = e.inherentDanger
		weighted_before = zip(self.BEFORE_KERN, before_danger_map)
		weighted_after  = zip(self.AFTER_KERN, after_danger_map)
		return sum(w*x for w,x in (weighted_before+weighted_after))

