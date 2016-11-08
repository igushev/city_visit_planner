class DatabaseConnectionInterface(object):
  """Abstract class for DatabaseConnection."""
  
  def GetPoints(self, visit_location):
    """For given visit_location return initial set of points."""
    raise NotImplemented()

  def GetPoint(self, visit_location, point_name):
    """For given visit_location and Point name return a point."""
    raise NotImplemented()
