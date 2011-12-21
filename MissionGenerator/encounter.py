class Encounter(object):
	@property
	def inherentDanger(self):
		return self.seriousnessDanger + self.positionalDanger + self.constantDanger
	@property
	def constantDanger(self):
		return 10
class SeriousEncounter(Encounter):
	@property
	def seriousnessDanger(self):
		return 5
class NormalEncounter(Encounter):
	@property
	def seriousnessDanger(self):
		return 0
class InternalEncounter(Encounter):
	@property
	def positionalDanger(self):
		return 5
class ExternalEncounter(Encounter):
	@property
	def positionalDanger(self):
		return 0

