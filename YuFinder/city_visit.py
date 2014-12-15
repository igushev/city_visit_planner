import datetime
import hashlib

import Yusi
from Yusi.YuFinder.point import Point, CoordinatesInterface


class StartEndDatetime(object):
  """Start and end time."""

  def __init__(self, start, end):
    assert isinstance(start, datetime.datetime)
    assert isinstance(end, datetime.datetime)
    self.start = start
    self.end = end

  def Fit(self, time):
    if self.start < time and time <= self.end:
      return True
    return False
  
  def __eq__(self, other):
    return self.__dict__ == other.__dict__

  def __str__(self):
    return 'from %s to %s' % (self.start.time(), self.end.time())  # FIXME


# TODO(igushev): Create more complicated structure for lunch.
class DayVisitParameters(object):
  """Set of users parameter for a particular day"""

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

  def HashKey(self):
    m = hashlib.md5()
    m.update(str(self.start_datetime).encode('utf-8'))
    m.update(str(self.end_datetime).encode('utf-8'))
    m.update(str(self.lunch_start_datetime).encode('utf-8'))
    m.update(str(self.lunch_hours).encode('utf-8'))
    m.update(str(self.start_coordinates).encode('utf-8'))
    m.update(str(self.end_coordinates).encode('utf-8'))
    return m.hexdigest()    

  
class PointVisit(object):
  """Visiting a point by a user."""

  def __init__(self, point, start_end_datetime):
    assert isinstance(point, Point)
    assert isinstance(start_end_datetime, StartEndDatetime)
    assert ((start_end_datetime.end - start_end_datetime.start) ==
            datetime.timedelta(hours=point.duration))

    self.point = point
    self.start_end_datetime = start_end_datetime

  def __eq__(self, other):
    return self.__dict__ == other.__dict__

  def __str__(self):
    return 'Visiting point "%s" %s' % (self.point.name, self.start_end_datetime)


# TODO(igushev): Make it Enum.
class MoveType(object):
  walking = 1
  driving = 2
  

class MoveDescription(object):
  """Moving description."""
  
  def __init__(self, move_hours, move_type):
    assert isinstance(move_hours, float)
    assert isinstance(move_type, int)
    self.move_hours = move_hours
    self.move_type = move_type


class MoveBetween(object):
  """Moving between points by a user."""

  def __init__(self, from_coordinates, to_coordinates,
               start_end_datetime, move_description):
    assert isinstance(from_coordinates, CoordinatesInterface)
    assert isinstance(to_coordinates, CoordinatesInterface)
    assert isinstance(start_end_datetime, StartEndDatetime)
    assert isinstance(move_description, MoveDescription)
    assert ((start_end_datetime.end - start_end_datetime.start) ==
            datetime.timedelta(hours=move_description.move_hours))

    self.from_coordinates = from_coordinates
    self.to_coordinates = to_coordinates
    self.start_end_datetime = start_end_datetime
    self.move_description = move_description

  def __eq__(self, other):
    return self.__dict__ == other.__dict__

  def __str__(self):
    if self.move_description.move_type == MoveType.walking:
      move_type_str = "Walking"
    elif self.move_description.move_type == MoveType.driving:
      move_type_str = "Driving"
    else:
      raise NotImplemented('Unknown MoveType: %s' % self.move_description.move_type)
    return '%s from %s to %s %s' % (
        move_type_str, self.from_coordinates, self.to_coordinates,
        self.start_end_datetime)


class Lunch(object):
  """Having lunch during the day."""

  def __init__(self, start_end_datetime):
    assert start_end_datetime
    self.start_end_datetime = start_end_datetime

  def __eq__(self, other):
    return self.__dict__ == other.__dict__

  def __str__(self):
    return 'Having lunch %s' % self.start_end_datetime


class DayVisit(object):
  """Set of visiting points and moving between points by a user in a day."""

  def __init__(self, start_datetime, actions, cost):
    assert isinstance(start_datetime, datetime.datetime)
    have_lunch = False
    must_move = True
    for i, action in enumerate(actions):
      if isinstance(action, Lunch):
        have_lunch = True
        continue
      if must_move:
        assert isinstance(action, MoveBetween), (
            'Wrong order of actions: no MoveBetween.')
      else:
        assert isinstance(action, PointVisit), (
            'Wrong order of actions: no PointVisit.')
      must_move = not must_move    
    assert len(actions) % 2 == (0 if have_lunch else 1), (
        'Wrong number of actions.')
    assert isinstance(cost, float)
    assert start_datetime == actions[0].start_end_datetime.start

    self.start_datetime = start_datetime
    self.actions = actions
    self.cost = cost

  def HashKey(self):
    # self.start_datetime doesn't matter.
    m = hashlib.md5()
    for action in self.actions:
      m.update(str(action).encode('utf-8'))
    m.update(str(self.cost).encode('utf-8'))
    return m.hexdigest()

  def GetPoints(self):
    return [action.point for action in self.actions
            if isinstance(action, PointVisit)]

  def __eq__(self, other):
    return self.__dict__ == other.__dict__

  def __str__(self):
    s = 'Date: %s\n' % self.start_datetime.date()  # FIXME
    s += 'Cost: %.2f\n' % self.cost
    s += '\n'.join(['%s' % action for action in self.actions])
    return s
      

class CityVisit(object):
  """Set of day visiting by a user ."""

  def __init__(self, day_visits):
    self.cost = 0
    for day_visit in day_visits:
      isinstance(day_visit, DayVisit)
      self.cost += day_visit.cost
    self.day_visits = day_visits

  def __eq__(self, other):
    return self.__dict__ == other.__dict__

  def __str__(self):
    return '\n'.join(['%s' % day_visit for day_visit in self.day_visits] +
                     ['Total cost: %.2f' % self.cost])
    
