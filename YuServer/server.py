from Yusi.YuUtils import json_utils
from Yusi.YuServer.city_visit_finder_task import CityVisitFinderTaskWorkerGenerator
from Yusi.YuUtils.task_utils import TaskManager
from Yusi.YuPoint.city_visit import CityVisitParameters


STATUS_OK = 200
STATUS_BAD_REQUEST = 400
STATUS_ERROR = 500


@json_utils.JSONDecorator()
class Status(object):

  def __init__(self, message):
    self.message = message


class Server(object):
  
  def __init__(self, database_connection, city_visit_finder,
               idle_seconds_terminate):
    self.database_connection = database_connection
    self.city_visit_finder = city_visit_finder
    city_visit_finder_task_worker_generator = (
        CityVisitFinderTaskWorkerGenerator(self.city_visit_finder))
    self.task_manager = (
        TaskManager(city_visit_finder_task_worker_generator,
                    idle_seconds_terminate))

  def Start(self, city_visit_parameters_simple):
    city_visit_parameters = (
        CityVisitParameters.FromSimple(city_visit_parameters_simple))


  def Ping(self):
    status = Status('Yusi Server')
    status_simple = status.ToSimple()
    return status_simple, STATUS_OK
