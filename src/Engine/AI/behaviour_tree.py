# encoding : UTF-8

# see http://magicscrollsofcode.blogspot.com/2010/12/behavior-trees-by-example-ai-in-android.html


class TaskController:
	def __init__(self, task):
		self.__done = None
		self.__success = None
		self.__started = None
		self.__task = None
		
		self.set_task(task)
		self.__initialize()
		
	def set_task(self, task):
		self.__task = task
		
	def __initialize(self):
		self.__done = False
		self.__success = True
		self.__started = False
		
	def safe_start(self):
		self.__started = True
		self.__task.start()
		
	def safe_end(self):
		self.__done = False
		self.__started = False
		self.__task.end()
		
	def finish_with_success(self):
		self.__success = True
		self.__done = True
		# print(self.__task, "finished with success")
		
	def finish_with_failure(self):
		self.__success = False
		self.__done = True
		# print(self.__task, "finished with failure")
		
	def succeeded(self):
		return self.__success
	
	def failed(self):
		return not self.__success
	
	def finished(self):
		return self.__done
	
	def started(self):
		return self.__started
	
	def reset(self):
		self.__done = False


class ParentTaskController(TaskController):
	def __init__(self, task):
		TaskController.__init__(self, task)
		
		self.subtasks = []
		self.cur_task = None
		
	def add(self, task):
		self.subtasks += [task]
		
	def reset(self):
		TaskController.reset(self)
		self.set_first_ready_task()

	def set_first_ready_task(self):
		for task in self.subtasks:
			if task.check_conditions():
				self.cur_task = task
				if task is None:
					print("current task has a null action")
				break
		else:
			self.cur_task = None
		
		
class Task:
	def __init__(self, ai_entity):
		self.ai_entity = ai_entity
		
	def check_conditions(self):
		assert -1, "to implement"
		return True
	
	def start(self):
		assert -1, "to implement"
	
	def end(self):
		assert -1, "to implement"
	
	def do_action(self):
		assert -1, "to implement"
		
	def get_control(self):
		assert -1, "to implement"


class LeafTask(Task):
	def __init__(self, ai_entity):
		Task.__init__(self, ai_entity)
		self._control = None
		
		self.create_controller()
		
	def create_controller(self):
		self._control = TaskController(self)
		
	def get_control(self):
		return self._control
	

class ParentTask(Task):
	def __init__(self, ai_entity):
		Task.__init__(self, ai_entity)
		self.control = None
		self.create_controller()
		
	def create_controller(self):
		self.control = ParentTaskController(self)
		
	def get_control(self):
		return self.control
	
	def check_conditions(self):
		# print("checking conditions")
		return len(self.control.subtasks) > 0
	
	def child_succeeded(self):
		assert -1, "to implement"
		
	def child_failed(self):
		assert -1, "to implement"
		
	def do_action(self):
		# print("doing action")
		
		if self.control.finished():
			return
		if self.control.cur_task is None:
			return
		if not self.control.cur_task.get_control().started():
			self.control.cur_task.get_control().safe_start()
		elif self.control.cur_task.get_control().finished():
			self.control.cur_task.get_control().safe_end()
			if self.control.cur_task.get_control().succeeded():
				self.child_succeeded()
			else:
				self.child_failed()
		else:
			self.control.cur_task.do_action()
			
	def end(self):
		# print("ending")
		pass
		
	def start(self):
		# print("starting")
		self.control.set_first_ready_task()


class Sequence(ParentTask):
	def child_failed(self):
		self.control.finish_with_failure()
		
	def child_succeeded(self):
		cur_pos = self.control.subtasks.index(self.control.cur_task)
		
		if cur_pos == len(self.control.subtasks) - 1:
			self.control.finish_with_success()
		else:
			self.control.cur_task = self.control.subtasks[cur_pos + 1]
			if not self.control.cur_task.check_conditions():
				self.control.finish_with_failure()


class Selector(ParentTask):
	def choose_new_task(self):
		task = None
		found = False
		cur_pos = self.control.subtasks.index(self.control.cur_task)
		
		while not found:
			if cur_pos == len(self.control.subtasks) - 1:
				task = None
				break
			cur_pos += 1
			
			task = self.control.subtasks[cur_pos]
			if task.check_conditions():
				found = True
		return task
	
	def child_failed(self):
		self.control.cur_task = self.choose_new_task()
		if self.control.cur_task is None:
			self.control.finish_with_failure()
	
	def child_succeeded(self):
		self.control.finish_with_success()


class TaskDecorator(Task):
	def __init__(self, ai_entity, task):
		Task.__init__(self, ai_entity)
		self.task = None

		self.__init_task(task)
		
	def __init_task(self, task):
		self.task = task
		self.task.get_control().set_task(self)
		
	def check_conditions(self):
		return self.task.check_conditions()
	
	def end(self):
		self.task.end()
	
	def get_control(self):
		return self.task.get_control()
	
	def start(self):
		self.task.start()


class ResetDecorator(TaskDecorator):
	def do_action(self):
		self.task.do_action()
		if self.task.get_control().finished():
			self.task.get_control().reset()


class RegulatorDecorator(TaskDecorator):
	pass


class DummyTask1(LeafTask):
	def check_conditions(self):
		return True

	def start(self):
		# print(self, "start")
		pass

	def end(self):
		# print(self, "end")
		pass

	def do_action(self):
		print("do action 1 !")
		self.get_control().finish_with_success()


class DummyTask2(LeafTask):
	def check_conditions(self):
		return True

	def start(self):
		# print(self, "start")
		pass

	def end(self):
		# print(self, "end")
		pass

	def do_action(self):
		print("do action 2 !")
		self.get_control().finish_with_success()


if __name__ == "__main__":
	# dummy create behaviour tree
	ai_entity = None
	
	dummy_task_1 = DummyTask1(ai_entity)
	dummy_task_2 = DummyTask2(ai_entity)
	
	planner = Sequence(ai_entity)
	planner.get_control().add(dummy_task_1)
	planner.get_control().add(dummy_task_2)
	planner = ResetDecorator(ai_entity, planner)
	
	planner.start()
	for _ in range(10):
		planner.do_action()
		