# NOTE(igushev): Source http://www.movable-type.co.uk/scripts/latlong.html
# (Bearing)
import math

from data import point
from data import city_visit


R = 3959  # Earth radius in miles.


def CalculateDistance(coordinates_from, coordinates_to):
  """Calculates distance in km/miles."""
  assert isinstance(coordinates_from, point.CoordinatesInterface)
  assert isinstance(coordinates_to, point.CoordinatesInterface)
    
  lat_1 = math.radians(coordinates_from.latitude)
  lat_2 = math.radians(coordinates_to.latitude)
  delta_lat = math.radians(coordinates_to.latitude - coordinates_from.latitude)
  long_1 = math.radians(coordinates_from.longitude)
  long_2 = math.radians(coordinates_to.longitude)
  delta_long = math.radians(
      coordinates_to.longitude - coordinates_from.longitude)

  a = (math.sin(delta_lat/2) * math.sin(delta_lat/2) +
       math.cos(lat_1) * math.cos(lat_2) *
       math.sin(delta_long/2) * math.sin(delta_long/2))
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
  d = R * c
  return d


def CalculateCityDistance(coordinates_from, coordinates_to):
    d = CalculateDistance(coordinates_from, coordinates_to)
    return d * math.sqrt(2)  # Because most cities have grid streets.


class MoveCalculatorInterface(object):
  """Abstract class which calculates move_description."""
  
  def CalculateMoveDescription(self, coordinates_from, coordinates_to):
    """Calculate time and type to move from one coordinates to another."""
    raise NotImplemented()


class SimpleMoveCalculator(MoveCalculatorInterface):
  """Calculates move_description considering pause before moving."""
  
  def __init__(self, speed, move_type, pause=0.):
    assert isinstance(speed, float)
    assert isinstance(move_type, int)
    assert isinstance(pause, float)
    
    self._speed = speed
    self._move_type = move_type
    self._pause = pause

  def CalculateMoveDescription(self, coordinates_from, coordinates_to):
    assert isinstance(coordinates_from, point.CoordinatesInterface)
    assert isinstance(coordinates_to, point.CoordinatesInterface)
    
    d = CalculateCityDistance(coordinates_from, coordinates_to)
    return city_visit.MoveDescription(coordinates_from, coordinates_to,
                                      (d / self._speed) + self._pause, self._move_type)


class MultiMoveCalculator(MoveCalculatorInterface):
  """Calculates move_description differently depending on distance."""

  def __init__(self, distances_splits, move_calculators):
    for move_calculator in move_calculators:
      assert isinstance(move_calculator, MoveCalculatorInterface)
    for distances_split in distances_splits:
      assert isinstance(distances_split, float)
    assert sorted(distances_splits) == distances_splits, (
        'Distances splits must be in sorted order.')
    assert len(move_calculators) == len(distances_splits) + 1, (
        'Number of MoveCalculatorInterface should exactly one more than'
        ' distances splits.')
    
    self._distances_splits = distances_splits
    self._move_calculators = move_calculators

  def CalculateMoveDescription(self, coordinates_from, coordinates_to):
    assert isinstance(coordinates_from, point.CoordinatesInterface)
    assert isinstance(coordinates_to, point.CoordinatesInterface)

    d = CalculateCityDistance(coordinates_from, coordinates_to)
    
    for i, distances_split in enumerate(self._distances_splits):
      if d < distances_split:
        move_calculator = self._move_calculators[i]
        break
    else:
      move_calculator = self._move_calculators[-1]
  
    return move_calculator.CalculateMoveDescription(
        coordinates_from, coordinates_to)
