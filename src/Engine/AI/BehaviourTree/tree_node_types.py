# encoding : UTF-8

from enum import Enum

"""
see https://www.gamasutra.com/blogs/ChrisSimpson/20140717/221339/Behavior_trees_for_AI_How_they_work.php

				_______ Composite _______
			   /            |            \
			  /             |             \
			Leaf        Decorator        Leaf
						    |
						    |
						  Leaf
"""

class TreeNodeState(Enum):
	FAILURE = -1
	SUCCESS = 0
	RUNNING = 1
	TO_IMPLEMENT = 2
	

class TreeNode:
	def __init__(self):
		self.children = None
		self.parent = None
		
		self.initialized = False
		
	def init(self):
		self.initialized = True
	
	def run(self):
		return TreeNodeState.TO_IMPLEMENT
		

# COMPOSITE
class Composite(TreeNode):
	def __init__(self, parent, children):
		TreeNode.__init__(self)
		self.parent = parent
		self.children = iter(children)
	
	def init(self):
		self.initialized = True

	def run(self):
		if not self.initialized:
			self.init()
		return TreeNodeState.TO_IMPLEMENT
		

class Sequence(Composite):
	def __init__(self, parent, children):
		Composite.__init__(self, parent, children)
		
		self.current_running_child = None
	
	def init(self):
		self.current_running_child = next(self.children)
		self.initialized = True
	
	def run(self):
		if not self.initialized:
			self.init()
		ret = self.current_running_child.run()
		
		if ret == TreeNodeState.FAILURE:
			return ret
		elif ret == TreeNodeState.SUCCESS:
			self.current_running_child = next(self.children)
			if self.current_running_child == StopIteration:
				return TreeNodeState.SUCCESS
		elif ret == TreeNodeState.RUNNING:
			return TreeNodeState.RUNNING
		else:
			raise ValueError(ret)


# LEAF
class Leaf(TreeNode):
	def __init__(self, parent):
		TreeNode.__init__(self)
		self.parent = parent
	
	
class DummyLeaf(Leaf):
	def run(self):
		print("dummy leaf run")
		return TreeNodeState.RUNNING

	
if __name__ == "__main__":
	seq = Sequence(None, [DummyLeaf(None) for _ in range(5)])
	seq.run()  # run 1 step
