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
		self._children = None
		self._parent = None
		
	# TODO: property for parent and children
	def set_parent(self, parent):
		self._parent = parent
	
	def set_children(self, children):
		self._children = iter(children)
	
	def run(self, task):
		return TreeNodeState.TO_IMPLEMENT
		

# COMPOSITE
class Composite(TreeNode):
	def __init__(self):
		TreeNode.__init__(self)

	def run(self, task):
		return TreeNodeState.TO_IMPLEMENT
		

class Sequence(Composite):
	def __init__(self):
		Composite.__init__(self)
		
		self.current_running_child = None
	
	def set_children(self, children):
		Composite.set_children(self, iter(children))
		# TODO: attribute relative to execution (like self.current_running_child) to remove
		#  --> must work with several tasks
		self.current_running_child = next(self._children)
	
	def run(self, task):
		# TODO: put this method in an attribute, self.run_method = run
		task.current_node = self

		ret = self.current_running_child.run(task)
		
		if ret == TreeNodeState.FAILURE:
			return ret
		elif ret == TreeNodeState.SUCCESS:
			self.current_running_child = next(self._children)
			if self.current_running_child == StopIteration:
				return TreeNodeState.SUCCESS
		elif ret == TreeNodeState.RUNNING:
			return TreeNodeState.RUNNING
		else:
			raise ValueError(ret)


# LEAF
class Leaf(TreeNode):
	def __init__(self):
		TreeNode.__init__(self)
	
	
class DummyLeaf(Leaf):
	def run(self, task):
		task.current_node = self
		print("dummy leaf {} run".format(id(self)))
		return TreeNodeState.SUCCESS

	
# Task
class Task:
	def __init__(self, node):
		self.current_node = node
		
	def run(self):
		print("current node :", self.current_node)
		self.current_node.run(task=self)
		print("")


class Context:
	# TODO: use that in a list in Task ?
	# TODO: remove a Context object from this list if node has been run and returning value != RUNNING ?
	def __init__(self, node, result):
		self.node = node
		self.result = result  # value in TreeNodeState


if __name__ == "__main__":
	seq = Sequence()
	leaves = [DummyLeaf() for _ in range(5)]
	seq.set_children(leaves)
	for leaf in leaves:
		leaf.set_parent(seq)
		
	task = Task(seq)
	
	for _ in range(4):
		task.run()
		