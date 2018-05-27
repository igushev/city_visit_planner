import datetime
import hashlib
import itertools

import Yusi
from Yusi.base_util import data_util
from Yusi.base_util import json_util
from Yusi.YuPoint import point as point_


class StartEndDatetimeInterface(data_util.AbstractObject):
  """Start and end time interface."""

  def Fit(self, time):
    """Check if time fits to incorporated time range."""
    raise NotImplemented()


@json_util.JSONDecorator(
    {'start': json_util.JSONDateTime(),
     'end': json_util.JSONDateTime()})
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
    m.update(data_util.HashKey(self.start.time()).encode('utf-8'))
    m.update(data_util.HashKey(self.end.time()).encode('utf-8'))
    return m.hexdigest()    

  def __str__(self):
    return 'from %s to %s' % (self.start.time(), self.end.time())


class DayVisitParametersInterface(data_util.AbstractObject):
  """Set of users parameter for a particular day interface."""
  pass


@json_util.JSONDecorator(
    {'start_datetime': json_util.JSONDateTime(),
     'end_datetime': json_util.JSONDateTime(),
     'lunch_start_datetime': json_util.JSONDateTime(),
     'start_coordinates': json_util.JSONObject(point_.Coordinates),
     'end_coordinates': json_util.JSONObject(point_.Coordinates)})
class DayVisitParameters(DayVisitParametersInterface):
  """Set of users parameter for a particular day implementation."""

  def __init__(self, start_datetime, end_datetime,
               lunch_start_datetime, lunch_hours,
               start_coordinates, end_coordinates=None):
    assert isinstance(start_datetime, datetime.datetime)
    assert isinstance(end_datetime, datetime.datetime)
    assert isinstance(lunch_start_datetime, datetime.datetime)
    assert isinstance(lunch_hours, float)
    assert isinstance(start_coordinates, point_.CoordinatesInterface)
    if end_coordinates is not None:
      assert isinstance(end_coordinates, point_.CoordinatesInterface)

    self.start_datetime = start_datetime
    self.end_datetime = end_datetime
    self.lunch_start_datetime = lunch_start_datetime
    self.lunch_hours = lunch_hours
    self.start_coordinates = start_coordinates
    self.end_coordinates = end_coordinates or start_coordinates

  def DatelessHashKey(self):
    m = hashlib.md5()
    m.update(data_util.HashKey(self.start_datetime.time()).encode('utf-8'))
    m.update(data_util.HashKey(self.end_datetime.time()).encode('utf-8'))
    m.update(data_util.HashKey(self.lunch_start_datetime.time()).encode('utf-8'))
    m.update(data_util.HashKey(self.lunch_hours).encode('utf-8'))
    m.update(data_util.HashKey(self.start_coordinates).encode('utf-8'))
    m.update(data_util.HashKey(self.end_coordinates).encode('utf-8'))
    return m.hexdigest()    


class VisitLocationInterface(data_util.AbstractObject):
  """Set of users parameter for visit location interface."""
  pass


@json_util.JSONDecorator()
class VisitLocation(VisitLocationInterface):
  """Set of users parameter for visit location implementation."""
  
  def __init__(self, city_name):
    self.city_name = city_name


class CityVisitParametersInterface(data_util.AbstractObject):
  """Set of users parameter for city visit interface."""
  pass


@json_util.JSONDecorator(
    {'visit_location': json_util.JSONObject(VisitLocation),
     'day_visit_parameterss':
     json_util.JSONList(json_util.JSONObject(DayVisitParameters)),
     'point_type': json_util.JSONObject(point_.PointType),
     'age_group': json_util.JSONObject(point_.AgeGroup)})
class CityVisitParameters(CityVisitParametersInterface):
  """Set of users parameter for city visit implementation."""

  def __init__(self, visit_location, day_visit_parameterss,
               point_type, age_group):
    assert isinstance(visit_location, VisitLocationInterface)
    for day_visit_parameters in day_visit_parameterss:
      assert isinstance(day_visit_parameters, DayVisitParametersInterface)
    assert isinstance(point_type, point_.PointTypeInterface)  # Must not be None
    assert isinstance(age_group, point_.AgeGroupInterface)  # Must not be None

    self.visit_location = visit_location
    self.day_visit_parameterss = day_visit_parameterss
    self.point_type = point_type
    self.age_group = age_group


@json_util.JSONDecorator(
    {'start_end_datetime': json_util.JSONObject(StartEndDatetime)},
    inherited=True)
class ActionInterface(data_util.AbstractObject):
  """Abstract interface for an action (visit a point, etc.) of a user."""
  
  def __init__(self, start_end_datetime):
    assert isinstance(start_end_datetime, StartEndDatetimeInterface)
    self.start_end_datetime = start_end_datetime

  def DatelessHashKey(self):
    m = hashlib.md5()
    m.update(self.start_end_datetime.DatelessHashKey().encode('utf-8'))
    return m.hexdigest()

  def __str__(self):
    raise NotImplemented()


@json_util.JSONDecorator({
    'point': json_util.JSONObject(point_.Point)})
class PointVisit(ActionInterface):
  """Visiting a point by a user."""

  def __init__(self, start_end_datetime, point):
    assert isinstance(point, point_.Point)
    assert ((start_end_datetime.end - start_end_datetime.start) ==
            datetime.timedelta(hours=point.duration))

    self.point = point
    super(PointVisit, self).__init__(start_end_datetime)

  def DatelessHashKey(self):
    m = hashlib.md5()
    m.update(super(PointVisit, self).DatelessHashKey().encode('utf-8'))
    m.update(data_util.HashKey(self.point).encode('utf-8'))
    return m.hexdigest()    

  def __str__(self):
    return 'Visiting point "%s" %s' % (self.point.name, self.start_end_datetime)


# TODO(igushev): Make it Enum.
class MoveType(object):
  walking = 1
  driving = 2
  ptt = 3
  

@json_util.JSONDecorator(
    {'from_coordinates': json_util.JSONObject(point_.Coordinates),
     'to_coordinates': json_util.JSONObject(point_.Coordinates),
     'move_type': json_util.JSONInt()})
class MoveDescription(data_util.AbstractObject):
  """Moving description."""
  
  def __init__(self, from_coordinates, to_coordinates, move_hours, move_type):
    assert isinstance(from_coordinates, point_.CoordinatesInterface)
    assert isinstance(to_coordinates, point_.CoordinatesInterface)
    assert isinstance(move_hours, float)
    assert isinstance(move_type, int)

    self.from_coordinates = from_coordinates
    self.to_coordinates = to_coordinates
    self.move_hours = move_hours
    self.move_type = move_type


@json_util.JSONDecorator({
    'move_description': json_util.JSONObject(MoveDescription)})
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
    m.update(super(MoveBetween, self).DatelessHashKey().encode('utf-8'))
    m.update(data_util.HashKey(self.move_description).encode('utf-8'))
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


@json_util.JSONDecorator()
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
    m.update(super(Lunch, self).DatelessHashKey().encode('utf-8'))
    m.update(data_util.HashKey(self.lunch_hours).encode('utf-8'))
    return m.hexdigest()    

  def __str__(self):
    return 'Having lunch %s' % self.start_end_datetime


class DayVisitInterface(data_util.AbstractObject):
  """Set of visiting points and moving between points in particular day
  interface."""

  def GetPoints(self):
    """Get points for incorporated day in order of visiting."""
    raise NotImplemented()


@json_util.JSONDecorator(
    {'start_datetime': json_util.JSONDateTime(),
     'actions': json_util.JSONList(json_util.JSONObject(ActionInterface))})
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
    m.update(data_util.HashKey(self.start_datetime.time()).encode('utf-8'))
    for action in self.actions:
      m.update(action.DatelessHashKey().encode('utf-8'))
    m.update(data_util.HashKey(self.cost).encode('utf-8'))
    return m.hexdigest()

  def GetPoints(self):
    return [action.point for action in self.actions
            if isinstance(action, PointVisit)]

  def __str__(self):
    return '\n'.join(['Date: %s' % self.start_datetime.date(),
                      '\n'.join(['%s' % action for action in self.actions]),
                      'Cost: %.2f' % self.cost,
                      'Price: %.2f' % self.price])


class CityVisitSummaryInterface(data_util.AbstractObject):
  """Set of summary information about CityVisit."""
  pass


@json_util.JSONDecorator()
class CityVisitSummary(CityVisitSummaryInterface):
  
  def __init__(self, cost, price):
    self.cost = cost
    self.price = price

  def __str__(self):
    return '\n'.join(['Total cost: %.2f' % self.cost,
                      'Total price: %.2f' % self.price])


class CityVisitInterface(data_util.AbstractObject):
  """Set of day visiting interface."""
  pass


@json_util.JSONDecorator(
    {'day_visits': json_util.JSONList(json_util.JSONObject(DayVisit)),
     'city_visit_summary': json_util.JSONObject(CityVisitSummary)})
class CityVisit(CityVisitInterface):
  """Set of day visiting implementation."""

  def __init__(self, day_visits, city_visit_summary):
    for day_visit in day_visits:
      assert isinstance(day_visit, DayVisitInterface)
    assert isinstance(city_visit_summary, CityVisitSummaryInterface)
    self.day_visits = day_visits
    self.city_visit_summary = city_visit_summary

  def GetPoints(self):
    return list(itertools.chain.from_iterable(
        day_visit.GetPoints() for day_visit in self.day_visits))

  def __str__(self):
    return '\n'.join(['%s' % day_visit for day_visit in self.day_visits] +
                     ['%s' % self.city_visit_summary])
    
