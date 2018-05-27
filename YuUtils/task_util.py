from collections import namedtuple
from datetime import datetime 
import multiprocessing
import threading
import uuid

from YuUtils import misc_util


TaskWorkerContext = namedtuple(
    'TaskWorkerContext', 'process manager_conn last_read')


class TaskWorkerInterface(object):
  """Abstract class which executes a task.""" 

  def Start(self):
    raise NotImplemented()


class TaskWorkerGeneratorInterface(object):
  """Abstract class which generates TaskWorkerInterface objects.""" 

  def Generate(self, worker_conn):
    raise NotImplemented()


class TaskManager(object):
  
  def __init__(self, task_worker_generator, idle_seconds_terminate):
    self.task_worker_generator = task_worker_generator
    self.idle_seconds_terminate = idle_seconds_terminate
    self.worker_process_dict = {}
    self.timer = threading.Timer(self.idle_seconds_terminate, misc_util.WeakBoundMethod(self, TaskManager._CleanUp))
    self.timer.start()
    self.lock = threading.Lock()
  
  def __del__(self):
    self.timer.cancel()
    self._CleanUp(start_over=False)
  
  @misc_util.Synchronized()
  def Start(self, *args, **kwargs):
    manager_conn, worker_conn = multiprocessing.Pipe(duplex=False)
    task_worker = self.task_worker_generator.Generate(worker_conn)
    task_id = uuid.uuid1()
    worker_process = multiprocessing.Process(target=task_worker.Start, args=args, kwargs=kwargs)
    worker_process.start()
    self.worker_process_dict[task_id] = (
        TaskWorkerContext(worker_process, manager_conn, datetime.now()))
    return task_id

  @misc_util.Synchronized()
  def Read(self, task_id):
    worker_context = self.worker_process_dict.get(task_id)
    if not worker_context:
      raise AssertionError(
          'No task with id %s. It might have been completed or expired.' %
          task_id)
    while worker_context.manager_conn.poll():
      res, done = worker_context.manager_conn.recv()
      yield res
      if done:
        worker_context.process.join()
        del self.worker_process_dict[task_id]
        return
    self.worker_process_dict[task_id] = (
        TaskWorkerContext(worker_context.process, worker_context.manager_conn,
                          datetime.now()))

  @misc_util.Synchronized()
  def _CleanUp(self, start_over=True):
    task_id_list = list(self.worker_process_dict.keys()) 
    for task_id in task_id_list:
      worker_context = self.worker_process_dict[task_id]
      if ((datetime.now() - worker_context.last_read).total_seconds() >
          self.idle_seconds_terminate):
        worker_context.process.terminate()
        del self.worker_process_dict[task_id]
    if start_over:
      self.timer = threading.Timer(self.idle_seconds_terminate, misc_util.WeakBoundMethod(self, TaskManager._CleanUp))
      self.timer.start()
