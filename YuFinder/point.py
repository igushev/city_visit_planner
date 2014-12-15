import datetime


class CoordinatesInterface(object):
  pass


class Coordinates(CoordinatesInterface):
  """Coordinates on Earth of anything."""

  def __init__(self, latitude, longitude):
    assert isinstance(latitude, float)
    assert isinstance(longitude, float)
    self.latitude = latitude
    self.longitude = longitude

  def __eq__(self, other):
    return self.__dict__ == other.__dict__

  def __str__(self):
    return '%.4f:%.4f' % (self.latitude, self.longitude)


class OperatingHours(object):
  """Operating hours of a Point."""

  def __init__(self, opens, closes):
    assert isinstance(opens, datetime.time)
    assert isinstance(closes, datetime.time)
    self.opens = opens
    self.closes = closes

  def __eq__(self, other):
    if other is None:
      return False
    return self.__dict__ == other.__dict__

  def __str__(self):
    return '%s - %s' % (self.opens, self.closes)


class Point(object):
  """Sightseeing, Attraction or Point Of Interest."""

  def __init__(self, name, coordinates_starts, coordinates_ends, operating_hours, duration):
    assert isinstance(name, str)
    assert isinstance(coordinates_starts, CoordinatesInterface)
    if coordinates_ends:
      assert isinstance(coordinates_ends, CoordinatesInterface)
    if operating_hours:
      assert isinstance(operating_hours, OperatingHours)
    assert isinstance(duration, float)
    
    self.name = name
    self.coordinates_starts = coordinates_starts
    self.coordinates_ends = (
      coordinates_ends if coordinates_ends is not None else coordinates_starts)
    self.operating_hours = operating_hours  # None means 24/7.
    self.duration = duration

  def __eq__(self, other):
    return self.__dict__ == other.__dict__

  def __str__(self):
    s = str()
    s += 'Name "%s"\n' % self.name
    s += 'Coordinates Starts %s\n' % self.coordinates_starts
    s += 'Coordinates Ends %s\n' % self.coordinates_ends
    s += 'Operating Hours %s\n' % self.operating_hours
    s += 'Duration %.2f\n' % self.duration
    return s
