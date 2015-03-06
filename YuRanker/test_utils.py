import unittest
from Yusi.YuPoint.city_visit import DayVisitParametersInterface,\
  CityVisitParametersInterface
from Yusi.YuPoint.point import PointTypeInterface, AgeGroupInterface


class MockDayVisitParameters(DayVisitParametersInterface):
  pass


class MockPointType(PointTypeInterface):
  pass


class MockAgeGroup(AgeGroupInterface):
  pass


class MockCityVisitParameters(CityVisitParametersInterface):
  pass


class RankAdjusterTestUtils(unittest.TestCase):
  
  def assertScorePointsEqual(
      self, score_points_expected, score_points_actual, places=None):
    for ((score_expected, point_expected),
         (score_actual, point_actual)) in zip(score_points_expected,
                                              score_points_actual):
      self.assertAlmostEqual(score_expected, score_actual, places=places)
      self.assertEqual(point_expected, point_actual)
