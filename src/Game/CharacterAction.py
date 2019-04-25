# encoding : UTF-8


class CharacterAction:
	def __init__(self, action):
		self.action = action
	
	def __str__(self): return self.action
	
	def __cmp__(self, other):
		return str.cmp(self.action, other.action)
	
	# Necessary when __cmp__ or __eq__ is defined
	# in order to make this class usable as a
	# dictionary key:
	def __hash__(self):
		return hash(self.action)


# Static fields; an enumeration of instances:
CharacterAction.idling = CharacterAction("idling")
CharacterAction.running = CharacterAction("running")
CharacterAction.jumping = CharacterAction("jumping")
CharacterAction.throwing = CharacterAction("throwing")
