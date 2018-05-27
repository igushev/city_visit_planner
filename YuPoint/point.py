import copy
import datetime

from base_util import data_util
from base_util import json_util


class CoordinatesInterface(data_util.AbstractObject):
  """Coordinates on Earth interface."""

  def Copy(self):
    return copy.deepcopy(self)


@json_util.JSONDecorator()
class Coordinates(CoordinatesInterface):
  """Coordinates on Earth using latitude and longitude."""  

  def __init__(self, latitude, longitude):
    assert isinstance(latitude, float)
    assert isinstance(longitude, float)
    self.latitude = latitude
    self.longitude = longitude

  def __str__(self):
    return '%.4f:%.4f' % (self.latitude, self.longitude)


class OperatingHoursInterface(data_util.AbstractObject):
  """Operating hours of a Point interface."""
  pass


@json_util.JSONDecorator({
    'opens': json_util.JSONDateTime(),
    'closes': json_util.JSONDateTime()})
class OperatingHours(OperatingHoursInterface):
  """Operating hours of a Point straightforward implementation. Doesn't know
  about days of week, seasons, etc."""

  def __init__(self, opens, closes):
    assert isinstance(opens, datetime.time)
    assert isinstance(closes, datetime.time)
    self.opens = opens
    self.closes = closes

  def __str__(self):
    return '%s - %s' % (self.opens, self.closes)


class PointTypeInterface(data_util.AbstractObject):
  """Type of a point interface."""
  pass


@json_util.JSONDecorator({
    'city_tours': json_util.JSONInt(),
    'landmarks': json_util.JSONInt(),
    'nature': json_util.JSONInt(),
    'museums': json_util.JSONInt(),
    'shopping': json_util.JSONInt(),
    'dining': json_util.JSONInt()})
class PointType(PointTypeInterface):
  """Type of a point implementation using assigned value to each type."""

  def __init__(self, city_tours, landmarks, nature, museums, shopping, dining):
    if city_tours is not None:
      assert isinstance(city_tours, int)
    if landmarks is not None:
      assert isinstance(landmarks, int)
    if nature is not None:
      assert isinstance(nature, int)
    if museums is not None:
      assert isinstance(museums, int)
    if shopping is not None:
      assert isinstance(shopping, int)
    if dining is not None:
      assert isinstance(dining, int)

    self.city_tours = city_tours or 0
    self.landmarks = landmarks or 0
    self.nature = nature or 0
    self.museums = museums or 0
    self.shopping = shopping or 0
    self.dining = dining or 0

  def GetNamesPointTypes(self):
    return {'City Tours': self.city_tours,
            'Landmarks': self.landmarks,
            'Nature': self.nature,
            'Museums': self.museums,
            'Shopping': self.shopping,
            'Dining': self.dining}

  def __str__(self):
    names_point_types = [
        (name, point_type)
        for name, point_type in sorted(self.GetNamesPointTypes().items())
        if point_type > 0]
    names_point_types = sorted(
        names_point_types, key = lambda name_point_type: name_point_type[1],
        reverse=True)
    if names_point_types:
      return ', '.join(
          ['%s (%d)' % (name, point_type)
           for name, point_type in names_point_types])
    else:
      return 'No point type'


class AgeGroupInterface(data_util.AbstractObject):
  """Age groups most suitable for a Point interface."""
  pass


@json_util.JSONDecorator({
    'senior': json_util.JSONInt(),
    'adult': json_util.JSONInt(),
    'junior': json_util.JSONInt(),
    'child': json_util.JSONInt(),
    'toddlers': json_util.JSONInt()})
class AgeGroup(AgeGroupInterface):
  """Age groups most suitable for a Point implementation using assigned value to
  each age group."""

  def __init__(self, senior, adult, junior, child, toddlers):
    if senior is not None:
      assert isinstance(senior, int)
    if adult is not None:
      assert isinstance(adult, int)
    if junior is not None:
      assert isinstance(junior, int)
    if child is not None:
      assert isinstance(child, int)
    if toddlers is not None:
      assert isinstance(toddlers, int)
      
    self.senior = senior or 0
    self.adult = adult or 0
    self.junior = junior or 0
    self.child = child or 0
    self.toddlers = toddlers or 0

  def GetNamesAgeGroups(self):
    return {'Senior': self.senior,
            'Adult': self.adult,
            'Junior': self.junior,
            'Child': self.child,
            'Toddlers': self.toddlers}

  def __str__(self):
    names_age_groups = [
        (name, age_group)
        for name, age_group in sorted(self.GetNamesAgeGroups().items())
        if age_group > 0]
    names_age_groups = sorted(
        names_age_groups, key = lambda name_age_group: name_age_group[1],
        reverse=True)
    if names_age_groups:
      return ', '.join(
          ['%s (%d)' % (name, age_group)
           for name, age_group in names_age_groups])
    else:
      return 'No age group'


class PointInterface(data_util.AbstractObject):
  """Sightseeing, Attraction or Point Of Interest interface."""
  pass


@json_util.JSONDecorator({
    'coordinates_starts': json_util.JSONObject(Coordinates),
    'coordinates_ends': json_util.JSONObject(Coordinates),
    'operating_hours': json_util.JSONObject(OperatingHours),
    'popularity': json_util.JSONInt(),
    'point_type': json_util.JSONObject(PointType),
    'age_group': json_util.JSONObject(AgeGroup),
    'parking': json_util.JSONInt(),
    'eating': json_util.JSONInt()})
class Point(PointInterface):
  """Sightseeing, Attraction or Point Of Interest common implementation."""

  def __init__(self, name, coordinates_starts, coordinates_ends,
               operating_hours, duration, popularity, point_type,
               age_group, price, parking, eating):
    assert isinstance(name, str)  # Must not be None
    # Must not be None
    assert isinstance(coordinates_starts, CoordinatesInterface)
    if coordinates_ends is not None:
      assert isinstance(coordinates_ends, CoordinatesInterface)
    if operating_hours is not None:
      assert isinstance(operating_hours, OperatingHoursInterface)
    assert isinstance(duration, float)   # Must not be None
    assert isinstance(popularity, int)   # Must not be None
    assert isinstance(point_type, PointTypeInterface)  # Must not be None
    assert isinstance(age_group, AgeGroupInterface)  # Must not be None
    if price is not None:
      assert isinstance(price, float)
    if parking is not None:
      assert isinstance(parking, int)
    if eating is not None:
      assert isinstance(eating, int)

    self.name = name
    self.coordinates_starts = coordinates_starts
    self.coordinates_ends = (
      coordinates_ends if coordinates_ends is not None else coordinates_starts)
    self.operating_hours = operating_hours  # None means 24/7.
    self.duration = duration
    self.popularity = popularity
    self.point_type = point_type
    self.age_group = age_group
    self.price = price or 0.
    self.parking = parking or 0
    self.eating = eating or 0

  def __str__(self):
    s = str()
    s += 'Name: "%s"\n' % self.name
    s += 'Coordinates Starts: %s\n' % self.coordinates_starts
    s += 'Coordinates Ends: %s\n' % self.coordinates_ends
    s += 'Operating Hours: %s\n' % (
        self.operating_hours if self.operating_hours is not None else '24/7') 
    s += 'Duration: %.2f\n' % self.duration
    s += 'Popularity: %d\n' % self.popularity
    s += 'Point type: %s\n' % self.point_type
    s += 'Age group: %s\n' % self.age_group
    s += 'Price: %.2f\n' % self.price
    s += 'Parking: %d\n' % self.parking
    s += 'Eating: %d\n' % self.eating
    return s
