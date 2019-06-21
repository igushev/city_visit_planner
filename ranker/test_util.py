import unittest
from data import city_visit
from data import point


class MockVisitLocation(city_visit.VisitLocationInterface):
  pass 


class MockDayVisitParameters(city_visit.DayVisitParametersInterface):
  pass


class MockPointType(point.PointTypeInterface):
  pass


class MockAgeGroup(point.AgeGroupInterface):
  pass


class MockCityVisitParameters(city_visit.CityVisitParametersInterface):
  pass


class RankAdjusterTestUtils(unittest.TestCase):
  
  def assertScorePointsEqual(
      self, score_points_expected, score_points_actual, places=None):
    for ((score_expected, point_expected),
         (score_actual, point_actual)) in zip(score_points_expected,
                                              score_points_actual):
      self.assertAlmostEqual(score_expected, score_actual, places=places)
      self.assertEqual(point_expected, point_actual)
