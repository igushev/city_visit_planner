from Yusi.YuUtils import json_utils


STATUS_OK = 200
STATUS_BAD_REQUEST = 400
STATUS_ERROR = 500


@json_utils.JSONDecorator()
class Status(object):

  def __init__(self, message):
    self.message = message


class Server(object):
  
  def __init__(self, database_connection, city_visit_finder):
    self.database_connection = database_connection
    self.city_visit_finder = city_visit_finder

  def Ping(self):
    status = Status('Yusi Server')
    status_simple = status.ToSimple()
    return status_simple, STATUS_OK
