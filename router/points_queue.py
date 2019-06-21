import datetime


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


class AllPointsQueue(PointsQueueInterface):
  
  def __init__(self, points, cut_off_multiplier):
    self._points = points
    self._cut_off_multiplier = cut_off_multiplier
  
  def HasPoints(self):
    return bool(self._points)

  def GetPushPoints(self, day_visit_parameterss):
    total_timedelta = datetime.timedelta()
    for day_visit_parameters in day_visit_parameterss:
      total_timedelta += (
          day_visit_parameters.end_datetime -
          day_visit_parameters.start_datetime -
          datetime.timedelta(hours=day_visit_parameters.lunch_hours))
    total_hours = total_timedelta.total_seconds() / 60. / 60.
    cut_off_hours = total_hours * self._cut_off_multiplier
    
    points_hours = 0.
    for cut_off_i in range(len(self._points)):
      points_hours += self._points[cut_off_i].duration
      if points_hours >= cut_off_hours:
        break
    
    push_points = self._points[:cut_off_i+1]
    self._points = self._points[cut_off_i+1:]
    return push_points
  
  def AddBackToQueue(self, points_left):
    self._points = points_left + self._points

  def GetPointsLeft(self):
    return self._points


class AllPointsQueueGenerator(PointsQueueGeneratorInterface):

  def __init__(self, cut_off_multiplier):
    self._cut_off_multiplier = cut_off_multiplier

  def Generate(self, points):
    return AllPointsQueue(points, self._cut_off_multiplier)
