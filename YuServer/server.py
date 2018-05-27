from base_util import json_util
from YuUtils import task_util

from YuPoint import city_visit
from YuServer import city_visit_finder_task


STATUS_OK = 200
STATUS_BAD_REQUEST = 400
STATUS_ERROR = 500


@json_util.JSONDecorator()
class Status(object):

  def __init__(self, message):
    self.message = message


class Server(object):
  
  def __init__(self, database_connection, city_visit_finder,
               idle_seconds_terminate):
    self.database_connection = database_connection
    self.city_visit_finder = city_visit_finder
    city_visit_finder_task_worker_generator = (
        city_visit_finder_task.CityVisitFinderTaskWorkerGenerator(self.city_visit_finder))
    self.task_manager = task_util.TaskManager(city_visit_finder_task_worker_generator, idle_seconds_terminate)

  def Start(self, city_visit_parameters_simple):
    city_visit_parameters = city_visit.CityVisitParameters.FromSimple(city_visit_parameters_simple)


  def Ping(self):
    status = Status('Yusi Server')
    status_simple = status.ToSimple()
    return status_simple, STATUS_OK
