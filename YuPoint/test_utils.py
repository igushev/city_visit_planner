import os

import Yusi
from Yusi.YuPoint.point import CoordinatesInterface
from Yusi.YuPoint.read_csv import ReadCSVToDict


class MockCoordinates(CoordinatesInterface):
  def __init__(self, name):
    assert isinstance(name, str)
    self.name = name

  def __eq__(self, other):
    return self.__dict__ == other.__dict__

  def __str__(self):
    return self.name


def MockPoints():
  points = ReadCSVToDict(
      os.path.join(Yusi.GetYusiDir(), 'YuPoint', 'test_sf_1.csv'))
  for point in points.values():
    point.coordinates_starts = MockCoordinates(point.name)
    point.coordinates_ends = MockCoordinates(point.name)
  return points
