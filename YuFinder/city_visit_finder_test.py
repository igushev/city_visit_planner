import unittest
from Yusi.YuFinder.city_visit_finder import CityVisitFinder
from Yusi.YuRanker.points_ranker import PointsRankerInterface
from Yusi.YuRouter.city_visit_router import CityVisitRouterInterface
from Yusi.YuPoint.city_visit import DayVisitParametersInterface,\
  CityVisitParameters, CityVisitInterface
from Yusi.YuPoint.point import PointTypeInterface, AgeGroupInterface,\
  PointInterface
from Yusi.YuRanker.test_utils import MockVisitLocation
from Yusi.YuPoint.database_connection import DatabaseConnectionInterface


class MockDayVisitParameters(DayVisitParametersInterface):
  pass


class MockPointType(PointTypeInterface):
  pass


class MockAgeGroup(AgeGroupInterface):
  pass


class MockPoint(PointInterface):
  pass


class MockCityVisit(CityVisitInterface):
  pass


class MockDatabaseConnection(DatabaseConnectionInterface):

  def __init__(self, test_obj, visit_location_expected, points_input):
    self.test_obj = test_obj
    self.visit_location_expected = visit_location_expected
    self.points_input = points_input

  def GetPoints(self, visit_location):
    self.test_obj.assertTrue(visit_location is self.visit_location_expected)
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
               day_visit_parameterss_expected, city_visit, points_left):
    self.test_obj = test_obj
    self.points_ranked_expected = points_ranked_expected
    self.day_visit_parameterss_expected = day_visit_parameterss_expected
    self.city_visit = city_visit
    self.points_left = points_left

  def RouteCityVisit(self, points, day_visit_parameterss):
    self.test_obj.assertTrue(points is self.points_ranked_expected)
    self.test_obj.assertTrue(
        day_visit_parameterss is self.day_visit_parameterss_expected)
    return self.city_visit, self.points_left


class CityVisitFinderTest(unittest.TestCase):
  
  def testGeneral(self):
    visit_location = MockVisitLocation()
    day_visit_parameterss=[MockDayVisitParameters()]
    
    city_visit_parameters = CityVisitParameters(
        visit_location=visit_location,
        day_visit_parameterss=day_visit_parameterss,
        point_type=MockPointType(),
        age_group=MockAgeGroup())

    points_input = [MockPoint(), MockPoint()]
    points_ranked = [MockPoint(), MockPoint()]
    points_left = [MockPoint(), MockPoint()]
    city_visit = MockCityVisit()

    database_connection = MockDatabaseConnection(
        self, visit_location, points_input)
    points_ranker = MockPointsRanker(
        self, points_input, city_visit_parameters, points_ranked)
    city_visit_router = MockCityVisitRouter(
        self, points_ranked, day_visit_parameterss, city_visit, points_left)

    city_visit_finder = CityVisitFinder(
        database_connection=database_connection,
        points_ranker=points_ranker,
        city_visit_router=city_visit_router)
    
    city_visit_actual = (
        city_visit_finder.FindCityVisit(city_visit_parameters))
    
    self.assertTrue(city_visit_actual is city_visit)
                     

if __name__ == '__main__':
    unittest.main()
