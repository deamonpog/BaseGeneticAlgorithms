from random import randrange
from random import random

class RandomNumberGenerator:
	@staticmethod
	def GetRandomIntValue(in_InclusiveMin, in_ExclusiveMax):
	    return randrange(in_InclusiveMin, in_ExclusiveMax)

	@staticmethod
	def GetRandomProbabilityValue():
	    return random()
