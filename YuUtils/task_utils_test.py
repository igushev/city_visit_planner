import time
import unittest
from Yusi.YuUtils.task_utils import TaskWorkerGeneratorInterface, TaskManager,\
  TaskWorkerInterface


def Sqr(num):
  return num*num


class SqrTaskWorker(TaskWorkerInterface):
  
  def __init__(self, worker_conn):
    self.worker_conn = worker_conn
  
  def Start(self, num_list, sleep):
    for i, num in enumerate(num_list):
      time.sleep(sleep)
      self.worker_conn.send((Sqr(num), i == len(num_list)-1))

    
class SqrTaskWorkerGenerator(TaskWorkerGeneratorInterface):

  def Generate(self, worker_conn):
    return SqrTaskWorker(worker_conn)


class TaskUtilsTest(unittest.TestCase):
  
  def testGeneral(self):
    sqr_task_worker_general = SqrTaskWorkerGenerator() 
    task_manager = TaskManager(sqr_task_worker_general, 1.0)
    
    input_1 = range(0, 11, 2)
    results_1 = [Sqr(num) for num in input_1]
    input_2 = range(1, 8, 2)
    results_2 = [Sqr(num) for num in input_2]
    task_id_1 = task_manager.Start(input_1, 0.2)
    task_id_2 = task_manager.Start(input_2, 0.2)

    time.sleep(0.5)
    read_list_1_1 = list(task_manager.Read(task_id_1))
    read_list_2_1 = list(task_manager.Read(task_id_2))
    self.assertTrue(1 <= len(read_list_1_1) <= 3)
    self.assertEqual(results_1[:len(read_list_1_1)], read_list_1_1)
    self.assertTrue(1 <= len(read_list_2_1) <= 3)
    self.assertEqual(results_2[:len(read_list_2_1)], read_list_2_1)
    results_1 = results_1[len(read_list_1_1):]
    results_2 = results_2[len(read_list_2_1):]
    
    time.sleep(0.5)
    read_list_1_2 = list(task_manager.Read(task_id_1))
    read_list_2_2 = list(task_manager.Read(task_id_2))
    self.assertTrue(1 <= len(read_list_1_2) <= 3)
    self.assertEqual(results_1[:len(read_list_1_2)], read_list_1_2)
    self.assertTrue(1 <= len(read_list_2_2) <= 3)
    self.assertEqual(results_2, read_list_2_2)
    results_1 = results_1[len(read_list_1_2):]
    results_2 = []

    time.sleep(0.5)
    read_list_1_3 = list(task_manager.Read(task_id_1))
    self.assertRaisesRegexp(
        AssertionError, 'No task with id %s' % task_id_2,
        list, task_manager.Read(task_id_2))
    self.assertTrue(1 <= len(read_list_1_3) <= 3)
    self.assertEqual(results_1, read_list_1_3)
    results_1 = []
    
    time.sleep(0.5)
    self.assertRaisesRegexp(
        AssertionError, 'No task with id %s' % task_id_1,
        list, task_manager.Read(task_id_1))
    self.assertRaisesRegexp(
        AssertionError, 'No task with id %s' % task_id_2,
        list, task_manager.Read(task_id_2))

  def testCleanUp(self):
    sqr_task_worker_general = SqrTaskWorkerGenerator() 
    task_manager = TaskManager(sqr_task_worker_general, 0.5)
    
    input_1 = range(0, 3, 2)
    input_2 = range(1, 4, 2)
    task_id_1 = task_manager.Start(input_1, 0.2)
    task_id_2 = task_manager.Start(input_2, 0.2)

    time.sleep(1.5)
    self.assertRaisesRegexp(
        AssertionError, 'No task with id %s' % task_id_1,
        list, task_manager.Read(task_id_1))
    self.assertRaisesRegexp(
        AssertionError, 'No task with id %s' % task_id_2,
        list, task_manager.Read(task_id_2))


if __name__ == '__main__':
    unittest.main()
