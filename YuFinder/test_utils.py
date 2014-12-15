import os

import Yusi
from Yusi.YuFinder import read_csv
from Yusi.YuFinder.city_visit import MoveType, MoveDescription
from Yusi.YuFinder.point import CoordinatesInterface


class MockCoordinates(CoordinatesInterface):
  def __init__(self, name):
    assert isinstance(name, str)
    self.name = name

  def __eq__(self, other):
    return self.__dict__ == other.__dict__

  def __str__(self):
    return self.name


# NOTE(igushev): Here we mock Coordinates with simple str and in this
# dictionary just define move_description between two given points.
# MockMoveCalculator relies instead of some sort of calculation of this
# dictionary.
MOVE_HOURS = {frozenset({'Hotel', 'Ferry Biulding'}): 1.,
              frozenset({'Hotel', 'Pier 39'}): 3.,
              frozenset({'Hotel', 'Golden Gate Bridge'}): 6.,
              frozenset({'Hotel', 'Union Square'}): 1.,
              frozenset({'Hotel', 'Twin Peaks'}): 3.,
              frozenset({'Hotel', 'Restaurant'}): 1.,
              frozenset({'Ferry Biulding', 'Pier 39'}): 1.,
              frozenset({'Ferry Biulding', 'Golden Gate Bridge'}): 8.,
              frozenset({'Ferry Biulding', 'Union Square'}): 2.,
              frozenset({'Ferry Biulding', 'Twin Peaks'}): 5.,
              frozenset({'Ferry Biulding', 'Restaurant'}): 2.,
              frozenset({'Pier 39', 'Golden Gate Bridge'}): 5.,
              frozenset({'Pier 39', 'Union Square'}): 2.,
              frozenset({'Pier 39', 'Twin Peaks'}): 5.,
              frozenset({'Pier 39', 'Restaurant'}): 4.,
              frozenset({'Golden Gate Bridge', 'Union Square'}): 5.,
              frozenset({'Golden Gate Bridge', 'Twin Peaks'}): 5.,
              frozenset({'Golden Gate Bridge', 'Restaurant'}): 6.,
              frozenset({'Twin Peaks', 'Union Square'}): 3.,
              frozenset({'Twin Peaks', 'Restaurant'}): 2.,
              frozenset({'Union Square', 'Restaurant'}): 1.}


class MockMoveCalculator(object):
  def CalculateMoveDescription(self, coordinates_from, coordinates_to):
    coordinates_between = (
      frozenset({coordinates_from.name, coordinates_to.name}))
    if not coordinates_between in MOVE_HOURS:
      raise AssertionError(
          'MOVE_HOURS is not defined between coordinates: %s and %s' % (
              coordinates_from, coordinates_to))
    return MoveDescription(MOVE_HOURS[coordinates_between], MoveType.walking)


# TODO(igushev): Change points to points_dict everywhere in code and
# for other dicts (?).
def MockPoints():
  points = read_csv.ReadCSVToDict(
      os.path.join(Yusi.GetYusiDir(), 'YuFinder', 'test_sf_1.csv'))
  for point in points.values():
    point.coordinates_starts = MockCoordinates(point.name)
    point.coordinates_ends = MockCoordinates(point.name)
  return points
