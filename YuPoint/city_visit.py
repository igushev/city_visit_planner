import datetime
import hashlib
import itertools

import Yusi
from Yusi.YuPoint.point import Point, CoordinatesInterface, PointTypeInterface,\
  AgeGroupInterface
from Yusi.YuUtils.hash_utils import HashKey


class StartEndDatetimeInterface(object):
  """Start and end time interface."""

  def Fit(self, time):
    """Check if time fits to incorporated time range."""
    raise NotImplemented()


class StartEndDatetime(StartEndDatetimeInterface):
  """Start and end time implementation."""

  def __init__(self, start, end):
    assert isinstance(start, datetime.datetime)
    assert isinstance(end, datetime.datetime)
    self.start = start
    self.end = end

  def Fit(self, time):
    if self.start < time and time <= self.end:
      return True
    return False

  def DatelessHashKey(self):
    m = hashlib.md5()
    m.update(HashKey(self.start.time()))
    m.update(HashKey(self.end.time()))
    return m.hexdigest()    
  
  def __eq__(self, other):
    return self.__dict__ == other.__dict__

  def __str__(self):
    return 'from %s to %s' % (self.start.time(), self.end.time())


class DayVisitParametersInterface(object):
  """Set of users parameter for a particular day interface."""
  pass


class DayVisitParameters(DayVisitParametersInterface):
  """Set of users parameter for a particular day implementation."""

  def __init__(self, start_datetime, end_datetime,
               lunch_start_datetime, lunch_hours,
               start_coordinates, end_coordinates=None):
    assert isinstance(start_datetime, datetime.datetime)
    assert isinstance(end_datetime, datetime.datetime)
    assert isinstance(lunch_start_datetime, datetime.datetime)
    assert isinstance(lunch_hours, float)
    assert isinstance(start_coordinates, CoordinatesInterface)
    if end_coordinates is not None:
      assert isinstance(end_coordinates, CoordinatesInterface)

    self.start_datetime = start_datetime
    self.end_datetime = end_datetime
    self.lunch_start_datetime = lunch_start_datetime
    self.lunch_hours = lunch_hours
    self.start_coordinates = start_coordinates
    self.end_coordinates = end_coordinates or start_coordinates

  def DatelessHashKey(self):
    m = hashlib.md5()
    m.update(HashKey(self.start_datetime.time()))
    m.update(HashKey(self.end_datetime.time()))
    m.update(HashKey(self.lunch_start_datetime.time()))
    m.update(HashKey(self.lunch_hours))
    m.update(HashKey(self.start_coordinates))
    m.update(HashKey(self.end_coordinates))
    return m.hexdigest()    

  def __eq__(self, other):
    return self.__dict__ == other.__dict__


class CityVisitParametersInterface(object):
  """Set of users parameter for city visit interface."""
  pass


class CityVisitParameters(CityVisitParametersInterface):
  """Set of users parameter for city visit implementation."""

  def __init__(self, day_visit_parameterss, point_type, age_group):
    for day_visit_parameters in day_visit_parameterss:
      assert isinstance(day_visit_parameters, DayVisitParametersInterface)
    assert isinstance(point_type, PointTypeInterface)  # Must not be None
    assert isinstance(age_group, AgeGroupInterface)  # Must not be None

    self.day_visit_parameterss = day_visit_parameterss
    self.point_type = point_type
    self.age_group = age_group

  def __eq__(self, other):
    return self.__dict__ == other.__dict__


class ActionInterface(object):
  """Abstract interface for an action (visit a point, etc.) of a user."""
  
  def __init__(self, start_end_datetime):
    assert isinstance(start_end_datetime, StartEndDatetimeInterface)
    self.start_end_datetime = start_end_datetime

  def DatelessHashKey(self):
    m = hashlib.md5()
    m.update(self.start_end_datetime.DatelessHashKey())
    return m.hexdigest()

  def __eq__(self, other):
    return self.__dict__ == other.__dict__

  def __str__(self):
    raise NotImplemented()


class PointVisit(ActionInterface):
  """Visiting a point by a user."""

  def __init__(self, start_end_datetime, point):
    assert isinstance(point, Point)
    assert ((start_end_datetime.end - start_end_datetime.start) ==
            datetime.timedelta(hours=point.duration))

    self.point = point
    super(PointVisit, self).__init__(start_end_datetime)

  def DatelessHashKey(self):
    m = hashlib.md5()
    m.update(super(PointVisit, self).DatelessHashKey())
    m.update(HashKey(self.point))
    return m.hexdigest()    

  def __str__(self):
    return 'Visiting point "%s" %s' % (self.point.name, self.start_end_datetime)


# TODO(igushev): Make it Enum.
class MoveType(object):
  walking = 1
  driving = 2
  ptt = 3
  

class MoveDescription(object):
  """Moving description."""
  
  def __init__(self, from_coordinates, to_coordinates, move_hours, move_type):
    assert isinstance(from_coordinates, CoordinatesInterface)
    assert isinstance(to_coordinates, CoordinatesInterface)
    assert isinstance(move_hours, float)
    assert isinstance(move_type, int)

    self.from_coordinates = from_coordinates
    self.to_coordinates = to_coordinates
    self.move_hours = move_hours
    self.move_type = move_type


class MoveBetween(ActionInterface):
  """Moving between points by a user."""

  def __init__(self, start_end_datetime, move_description):
    assert isinstance(move_description, MoveDescription)
    assert ((start_end_datetime.end - start_end_datetime.start) ==
            datetime.timedelta(hours=move_description.move_hours))

    self.move_description = move_description
    super(MoveBetween, self).__init__(start_end_datetime)

  def DatelessHashKey(self):
    m = hashlib.md5()
    m.update(super(MoveBetween, self).DatelessHashKey())
    m.update(HashKey(self.move_description))
    return m.hexdigest()    

  def __str__(self):
    if self.move_description.move_type == MoveType.walking:
      move_type_str = "Walking"
    elif self.move_description.move_type == MoveType.driving:
      move_type_str = "Driving"
    elif self.move_description.move_type == MoveType.ptt:
      move_type_str = "Using PTT"
    else:
      raise NotImplemented(
          'Unknown MoveType: %s' % self.move_description.move_type)
    return '%s from %s to %s %s' % (
        move_type_str, self.move_description.from_coordinates,
        self.move_description.to_coordinates, self.start_end_datetime)


class Lunch(ActionInterface):
  """Having lunch during the day."""

  def __init__(self, start_end_datetime, lunch_hours):
    assert isinstance(lunch_hours, float)
    assert ((start_end_datetime.end - start_end_datetime.start) ==
            datetime.timedelta(hours=lunch_hours))

    self.lunch_hours = lunch_hours
    super(Lunch, self).__init__(start_end_datetime)

  def DatelessHashKey(self):
    m = hashlib.md5()
    m.update(super(Lunch, self).DatelessHashKey())
    m.update(HashKey(self.lunch_hours))
    return m.hexdigest()    

  def __str__(self):
    return 'Having lunch %s' % self.start_end_datetime


class DayVisitInterface(object):
  """Set of visiting points and moving between points in particular day
  interface."""

  def GetPoints(self):
    """Get points for incorporated day in order of visiting."""
    raise NotImplemented()


class DayVisit(DayVisitInterface):
  """Set of visiting points and moving between points in particular day
  implementation."""

  def __init__(self, start_datetime, actions, cost):
    assert isinstance(start_datetime, datetime.datetime)
    have_lunch = False
    must_move = True
    self.price = 0
    for action in actions:
      if isinstance(action, Lunch):
        have_lunch = True
        continue
      if must_move:
        assert isinstance(action, MoveBetween), (
            'Wrong order of actions: no MoveBetween.')
      else:
        assert isinstance(action, PointVisit), (
            'Wrong order of actions: no PointVisit.')
        self.price += action.point.price
      must_move = not must_move    
    assert len(actions) % 2 == (0 if have_lunch else 1), (
        'Wrong number of actions.')
    assert isinstance(cost, float)
    assert start_datetime == actions[0].start_end_datetime.start

    self.start_datetime = start_datetime
    self.actions = actions
    self.cost = cost

  def DatelessHashKey(self):
    m = hashlib.md5()
    m.update(HashKey(self.start_datetime.time()))
    for action in self.actions:
      m.update(action.DatelessHashKey())
    m.update(HashKey(self.cost))
    return m.hexdigest()

  def GetPoints(self):
    return [action.point for action in self.actions
            if isinstance(action, PointVisit)]

  def __eq__(self, other):
    return self.__dict__ == other.__dict__

  def __str__(self):
    return '\n'.join(['Date: %s' % self.start_datetime.date(),
                      '\n'.join(['%s' % action for action in self.actions]),
                      'Cost: %.2f' % self.cost,
                      'Price: %.2f' % self.price])
      

class CityVisitInterface(object):
  """Set of day visiting interface."""
  pass


class CityVisit(CityVisitInterface):
  """Set of day visiting implementation."""

  def __init__(self, day_visits, cost):
    self.price = 0
    for day_visit in day_visits:
      isinstance(day_visit, DayVisit)
      self.price += day_visit.price
    assert isinstance(cost, float)

    self.day_visits = day_visits
    self.cost = cost

  def GetPoints(self):
    return list(itertools.chain.from_iterable(
        day_visit.GetPoints() for day_visit in self.day_visits))

  def __eq__(self, other):
    return self.__dict__ == other.__dict__

  def __str__(self):
    return '\n'.join(['%s' % day_visit for day_visit in self.day_visits] +
                     ['Total cost: %.2f' % self.cost,
                      'Total price: %.2f' % self.price])
    
