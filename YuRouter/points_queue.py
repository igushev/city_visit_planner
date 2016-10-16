class PointsQueueInterface(object):
  """Abstract class which maintains points queue for pushing."""

  def HasPoints(self):
    """If queue has more points."""
    raise NotImplemented()
  
  def GetPushPoints(self, day_visit_parameterss):
    """Returns list of points to push by given day_visit_parameterss."""
    raise NotImplemented()

  def AddBackToQueue(self, points_left):
    """Add given points_left back to queue to return later."""
    raise NotImplemented()

  def GetPointsLeft(self):
    """Returns points which still left in the queue."""
    raise NotImplemented()


class PointsQueueGeneratorInterface(object):
  """Abstract which returns new instance of PointsQueueInterface."""

  def Generate(self, points):
    """Returns new instance of PointsQueueInterface."""
    raise NotImplemented()


class OneByOnePointsQueue(PointsQueueInterface):
  
  def __init__(self, points):
    self._points = points
  
  def HasPoints(self):
    return bool(self._points)

  def GetPushPoints(self, day_visit_parameterss):
    return [self._points.pop(0)]
  
  def AddBackToQueue(self, points_left):
    self._points = points_left + self._points

  def GetPointsLeft(self):
    return self._points


class OneByOnePointsQueueGenerator(PointsQueueGeneratorInterface):
  
  def Generate(self, points):
    return OneByOnePointsQueue(points)
