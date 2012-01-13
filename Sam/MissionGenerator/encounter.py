from ..helpers import *
from functools import reduce
from itertools import imap, chain
class Event(object):
	E_COM_BREAKDOWN_TIME = 5
	ENCOUNTER_RANGE = (1,8)
	@classmethod
	def generateRandom(cls, random):
		return random.choice((
			cls.generateRandomEncounter, 
			cls.generateRandomIncomingData,
			cls.generateRandomTransaction,
			cls.generateRandomCommunicationBreakdown))(random)
	
	@classmethod
	def generateRandomEncounter(cls, random):
		return Encounter.generateRandom(random)

	@classmethod
	def generateRandomIncomingData(cls, random):
		return IncomingData.generate(random.randint(*cls.ENCOUNTER_RANGE))

	@classmethod
	def generateRandomTransaction(cls, random):
		return Transaction.generate(random.randint(*cls.ENCOUNTER_RANGE))

	@classmethod
	def generateRandomCommunicationBreakdown(cls, random):
		return CommunicationBreakdown.generate(random.randint(*cls.ENCOUNTER_RANGE), random.expovariate(cls.E_COM_BREAKDOWN_TIME))

	@classmethod
	def generateEncounter(cls, *args, **kargs):
		return Encounter.generate(*args,**kargs)

	@classmethod
	def generateIncomingData(cls, *args, **kargs):
		return IncomingData.generate(*args, **kargs)

	@classmethod
	def generateTransaction(cls, *args, **kargs):
		return Transaction.generate(*args, **kargs)

	@classmethod
	def generateCommunicationBreakdown(cls, *args, **kargs):
		return CommunicationBreakdown.generate(*args, **kargs)

	def __init__(self, time):
		self._time = time

	@property
	def inherentDanger(self):
		raise NotImplementedError("%s has no defined inherentDanger" % self.__class__.__name__)

	time = accessor('time', immutable = True, doc = 'The appearance of the Encounter')

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
		weighted_before = imap(self.before_kern, before)
		weighted_after  = imap(self.after_kern, after)
		return sum(chain(weighted_before, weighted_after))

	def before_kern(self, _):
		return 0

	def after_kern(self, e):
		return 2**((self.time - e.time))*e.inherentDanger
class Encounter(Event):
	SERIOUS, NON_SERIOUS = 10, 0
	INTERNAL, EXTERNAL = 5, 0

	@classmethod
	def generate(cls, time, serious = False, internal = False):
		return cls(time, 
				cls.SERIOUS if serious else cls.NON_SERIOUS,
				cls.INTERNAL if internal else cls.EXTERNAL)
	
	@classmethod
	def generateRandom(cls, random):
		return cls(
				random.randint(cls.ENCOUNTER_RANGE[0], cls.ENCOUNTER_RANGE[1]),
				random.choice((cls.SERIOUS, cls.NON_SERIOUS)),
				random.choice((cls.INTERNAL, cls.EXTERNAL)))

	def __init__(self, time, seriousness, positional):
		Event.__init__(self, time)
		self._seriousnessDanger = seriousness
		self._positionalDanger = positional
	
	seriousnessDanger = accessor('seriousnessDanger', immutable = True, doc = 'The danger imposed from being serious or normal')
	positionalDanger = accessor('positionalDanger', immutable = True, doc = 'The danger imposed from being external or internal')

	@property
	def inherentDanger(self):
		return self.seriousnessDanger + self.positionalDanger + self.constantDanger

	@property
	def constantDanger(self):
		"Each encounter is at least this difficult"
		return 10


class CommunicationBreakdown(Event):
	@classmethod
	def generate(cls, time,  length):
		return CommunicationBreakdown(time, length)

	def __init__(self, time, length):
		Event.__init__(self, time)
		self._length = length
	@property
	def inherentDanger(self):
		return self.length
	length = accessor('length', immutable = True, doc = 'Length in which players are not allowed to talk')

class Transaction(Event):
	@classmethod
	def generate(cls, time):
		return Transaction(time)
	@property
	def inherentDanger(self):
		return -3

class IncomingData(Event):
	@classmethod
	def generate(cls, time):
		return IncomingData(time)
	@property
	def inherentDanger(self):
		return -3
