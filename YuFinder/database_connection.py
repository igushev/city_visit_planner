class DatabaseConnectionInterface(object):
  """Abstract class for DatabaseConnection."""
  
  def GetPoints(self, city_visit_parameters):
    """For given city_visit_parameters return initial set of points."""
    raise NotImplemented()
