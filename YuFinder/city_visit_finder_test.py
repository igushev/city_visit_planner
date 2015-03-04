import unittest
from Yusi.YuFinder.city_visit_finder import CityVisitFinder
from Yusi.YuFinder.database_connection import DatabaseConnectionInterface
from Yusi.YuRanker.points_ranker import PointsRankerInterface
from Yusi.YuRouter.city_visit_router import CityVisitRouterInterface
from Yusi.YuPoint.city_visit import DayVisitParametersInterface,\
  CityVisitParameters
from Yusi.YuPoint.point import PointTypeInterface, AgeGroupInterface


class MockDayVisitParameters(DayVisitParametersInterface):
  pass


class MockPointType(PointTypeInterface):
  pass


class MockAgeGroup(AgeGroupInterface):
  pass


class MockPoints(object):
  pass


class MockCityVisit(object):
  pass


class MockDatabaseConnection(DatabaseConnectionInterface):

  def __init__(self, test_obj, city_visit_parameters_expected, points_input):
    self.test_obj = test_obj
    self.city_visit_parameters_expected = city_visit_parameters_expected
    self.points_input = points_input

  def GetPoints(self, city_visit_parameters):
    self.test_obj.assertTrue(
        city_visit_parameters is self.city_visit_parameters_expected)
    return self.points_input


class MockPointsRanker(PointsRankerInterface):

  def __init__(self, test_obj, points_input_expected,
               city_visit_parameters_expected, points_ranked):
    self.test_obj = test_obj
    self.points_input_expected = points_input_expected
    self.city_visit_parameters_expected = city_visit_parameters_expected
    self.points_ranked = points_ranked

  def RankPoints(self, points, city_visit_parameters):
    self.test_obj.assertTrue(points is self.points_input_expected)
    self.test_obj.assertTrue(
        city_visit_parameters is self.city_visit_parameters_expected)
    return self.points_ranked


class MockCityVisitRouter(CityVisitRouterInterface):
  
  def __init__(self, test_obj, points_ranked_expected,
               day_visit_parameterss_expected, city_visit):
    self.test_obj = test_obj
    self.points_ranked_expected = points_ranked_expected
    self.day_visit_parameterss_expected = day_visit_parameterss_expected
    self.city_visit = city_visit

  def RouteCityVisit(self, points, day_visit_parameterss):
    self.test_obj.assertTrue(points is self.points_ranked_expected)
    self.test_obj.assertTrue(
        day_visit_parameterss is self.day_visit_parameterss_expected)
    return self.city_visit


class CityVisitFinderTest(unittest.TestCase):
  
  def testGeneral(self):
    day_visit_parameterss=[MockDayVisitParameters()]
    
    city_visit_parameters = CityVisitParameters(
        day_visit_parameterss=day_visit_parameterss,
        point_type=MockPointType(),
        age_group=MockAgeGroup())

    points_input = MockPoints()
    points_ranked = MockPoints()
    city_visit = MockCityVisit()

    database_connection = MockDatabaseConnection(
        self, city_visit_parameters, points_input)
    points_ranker = MockPointsRanker(
        self, points_input, city_visit_parameters, points_ranked)
    city_visit_router = MockCityVisitRouter(
        self, points_ranked, day_visit_parameterss, city_visit)

    city_visit_finder = CityVisitFinder(
        database_connection=database_connection,
        points_ranker=points_ranker,
        city_visit_router=city_visit_router)
    
    city_visit_finder.FindDayVisit(city_visit_parameters)
                     

if __name__ == '__main__':
    unittest.main()
